from pathlib import Path
import argparse, concurrent.futures, ctypes, hashlib, json, os, socket, subprocess, time, urllib.request

KIT=Path(__file__).resolve().parent
class Memory(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong),('total_physical',ctypes.c_ulonglong),('available_physical',ctypes.c_ulonglong),('total_page',ctypes.c_ulonglong),('available_page',ctypes.c_ulonglong),('total_virtual',ctypes.c_ulonglong),('available_virtual',ctypes.c_ulonglong),('available_extended',ctypes.c_ulonglong)]
def available():
    data=Memory();data.length=ctypes.sizeof(data)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(data)):raise OSError('Cannot read Windows memory')
    return data.available_physical/2**30
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as f:
        while block:=f.read(16*1024*1024):h.update(block)
    return h.hexdigest()
def read(path):return json.loads(Path(path).read_text('utf-8'))
def save(path,data):Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
def url_json(url,data=None):
    request=urllib.request.Request(url,None if data is None else json.dumps(data).encode(),{}if data is None else{'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=180 if data else 5)as response:return json.load(response)
def stop(process):
    # Popen keeps the handle of the exact child we launched. No PID lookup or foreign stop.
    if process.poll()is not None:return
    process.terminate()
    try:process.wait(10)
    except subprocess.TimeoutExpired:process.kill();process.wait(10)

def main(args):
    if os.name!='nt':raise RuntimeError('This tested profile is for Windows')
    runtime=Path(args.runtime).resolve();models=Path(args.models).resolve();output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=False)
    record=dict(status='checking',runtime=str(runtime),models=str(models),output=str(output),port=args.port,whole_human_listening=False);save(output/'RUN.json',record)
    for row in read(KIT/'RUNTIME.json')['members']:
        file=(runtime/row['path']).resolve()
        if not file.is_relative_to(runtime)or not file.is_file()or file.stat().st_size!=row['bytes']or sha(file)!=row['sha256']:raise RuntimeError('Runtime mismatch: '+row['path'])
    for row in read(KIT/'MODELS.json')['files']:
        file=models/row['filename']
        if not file.is_file()or file.stat().st_size!=row['bytes']or sha(file)!=row['sha256']:raise RuntimeError('Model mismatch: '+row['filename'])
        print('Model SHA256 passed:',file.name,flush=True)
    record['all_runtime_and_model_hashes_verified']=True;save(output/'RUN.json',record)
    if args.check_only:record['status']='checked';save(output/'RUN.json',record);return
    for port in(8079,8081,8090,8082,8188,8189,8191,args.port):
        with socket.socket()as s:
            if s.connect_ex(('127.0.0.1',port))==0:raise RuntimeError(f'Local model port {port} is occupied; finish that work first')
    if available()<12:raise RuntimeError('Less than12GiB available Windows RAM before starting')
    profile=read(KIT/'PROFILE.json');server=runtime/'llama-server.exe';model=models/read(KIT/'MODELS.json')['files'][0]['filename']
    command=[str(server),'-m',str(model),'--host','127.0.0.1','--port',str(args.port)]+profile['arguments']
    env=os.environ.copy()
    for key in list(env):
        if key.startswith('LLAMA_ARG_'):del env[key]
    process=None;minimum=available();low_since=None
    def guard():
        nonlocal minimum,low_since
        free=available();minimum=min(minimum,free)
        data=Memory();data.length=ctypes.sizeof(data)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(data)):raise OSError('Cannot read commit reserve')
        commit_free=data.available_page/2**30
        critical=free<.004 or(free<.25 and commit_free<2)
        low_since=(low_since or time.monotonic())if critical else None
        save(output/'RAM.json',dict(available_gib=free,minimum_gib=minimum,available_commit_gib=commit_free,physical_emergency_gib=.004,combined_low_physical_gib=.25,combined_low_commit_gib=2,critical_seconds=5))
        if low_since is not None and time.monotonic()-low_since>=5:
            if process is not None:stop(process)
            raise RuntimeError('Windows physical/commit reserve stayed critically low for5seconds')
        if process is not None and process.poll()is not None:raise RuntimeError('Owned server exited; inspect SERVER.log')
    try:
        with(output/'SERVER.log').open('w',encoding='utf-8')as log:process=subprocess.Popen(command,cwd=runtime,env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        record.update(status='loading',owned_pid=process.pid,command=command);save(output/'RUN.json',record);start=time.monotonic();deadline=start+600;base=f'http://127.0.0.1:{args.port}'
        while time.monotonic()<deadline:
            guard()
            try:
                if url_json(base+'/health').get('status')=='ok':break
            except (OSError,ValueError):pass
            time.sleep(.5)
        else:raise RuntimeError('Server loading deadline')
        record.update(status='ready',load_seconds=time.monotonic()-start,props=url_json(base+'/props'));save(output/'RUN.json',record);print('Open',base,flush=True)
        if args.test_and_exit:
            payload=read(KIT/'EXAMPLE-REQUEST.json');start=time.monotonic()
            with concurrent.futures.ThreadPoolExecutor(max_workers=1)as executor:
                future=executor.submit(url_json,base+'/v1/chat/completions',payload)
                while not future.done():guard();time.sleep(.5)
                reply=future.result()
            answer=reply['choices'][0]['message']['content']
            if not answer.strip():raise RuntimeError('The source example returned an empty answer')
            save(output/'REQUEST.json',payload);save(output/'RESPONSE.json',reply);record.update(api_seconds=time.monotonic()-start,api_answer=answer,actual_inference_completed=True)
            print(answer,flush=True)
        else:
            print('Press Ctrl+C here when finished to stop this exact server.',flush=True)
            while True:guard();time.sleep(1)
        record['status']='completed'
    except KeyboardInterrupt:record['status']='stopped_by_user'
    except BaseException as exc:record.update(status='failed',error=str(exc));raise
    finally:
        if process is not None:stop(process);record['owned_process_stopped']=True
        record['minimum_available_ram_gib']=minimum;save(output/'RUN.json',record)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Start the recorded Windows AMD/Vulkan Flash Next profile. Existing runtime and models stay read-only.')
    parser.add_argument('--runtime',required=True);parser.add_argument('--models',required=True);parser.add_argument('--output',required=True);parser.add_argument('--port',type=int,default=18194);parser.add_argument('--check-only',action='store_true');parser.add_argument('--test-and-exit',action='store_true');main(parser.parse_args())
