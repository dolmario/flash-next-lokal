from pathlib import Path
import argparse,hashlib,json,urllib.request
KIT=Path(__file__).resolve().parent
def sha(path):
    h=hashlib.sha256()
    with path.open('rb')as f:
        while block:=f.read(16*1024*1024):h.update(block)
    return h.hexdigest()
def main(folder):
    root=Path(folder).resolve();root.mkdir(parents=True,exist_ok=True);manifest=json.loads((KIT/'MODELS.json').read_text('utf-8'))
    for row in manifest['files']:
        target=root/row['filename'];partial=target.with_suffix(target.suffix+'.part')
        if target.exists():
            if target.stat().st_size==row['bytes']and sha(target)==row['sha256']:print('Already verified:',target.name,flush=True);continue
            raise RuntimeError('Existing unverified file preserved: '+str(target))
        offset=partial.stat().st_size if partial.exists() else 0
        if offset>row['bytes']:raise RuntimeError('Oversized partial download preserved')
        if offset<row['bytes']:
            request=urllib.request.Request(row['url'],headers={'Range':f'bytes={offset}-'}if offset else{})
            with urllib.request.urlopen(request,timeout=120)as response:
                if offset and response.status!=206:raise RuntimeError('Server did not resume the partial file; existing data preserved')
                with partial.open('ab'if offset else'wb')as out:
                    while block:=response.read(4*1024*1024):out.write(block)
        if partial.stat().st_size!=row['bytes']or sha(partial)!=row['sha256']:raise RuntimeError('Model checksum mismatch; partial file preserved')
        partial.rename(target);print('Verified:',target.name,flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Download the pinned three GGUF parts; existing files must match and interrupted downloads are resumed.');parser.add_argument('--output',required=True);main(parser.parse_args().output)
