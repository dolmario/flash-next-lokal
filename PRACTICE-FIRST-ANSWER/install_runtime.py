from pathlib import Path
import argparse,hashlib,json,subprocess,urllib.request,zipfile
KIT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main(output):
    root=Path(output).resolve();root.mkdir(parents=True,exist_ok=False);manifest=json.loads((KIT/'RUNTIME.json').read_text('utf-8'));archive=root/'runtime-download.zip';runtime=root/'runtime'
    with urllib.request.urlopen(manifest['url'],timeout=120)as response,archive.open('wb')as out:
        while block:=response.read(4*1024*1024):out.write(block)
    if sha(archive)!=manifest['archive_sha256']:raise RuntimeError('Runtime archive checksum mismatch; original download preserved')
    with zipfile.ZipFile(archive)as z:
        if z.testzip()is not None:raise RuntimeError('Runtime ZIP CRC failed')
        for info in z.infolist():
            if not(runtime/info.filename).resolve().is_relative_to(runtime):raise RuntimeError('Unexpected archive path')
        z.extractall(runtime)
    for row in manifest['members']:
        file=runtime/row['path']
        if file.stat().st_size!=row['bytes']or sha(file)!=row['sha256']:raise RuntimeError('Runtime member mismatch: '+row['path'])
    result=subprocess.run([str(runtime/'llama-server.exe'),'--version'],cwd=runtime,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=30)
    if result.returncode:raise RuntimeError('Runtime version command failed')
    (root/'INSTALL.json').write_text(json.dumps(dict(archive_sha256=sha(archive),all_runtime_member_hashes_verified=True,runtime=str(runtime),version_output=result.stdout+result.stderr,system_settings_changed=False),indent=2)+'\n','utf-8')
    print(result.stdout+result.stderr);print('Runtime ready:',runtime)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Download, check and extract the pinned official Windows runtime into a new folder.');parser.add_argument('--output',required=True);main(parser.parse_args().output)
