#!/usr/bin/env python3
"""Download, validate and extract one experiment without Git LFS or credentials."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


def download(url, target, expected):
    h=hashlib.sha256();size=0
    with urllib.request.urlopen(url,timeout=120) as response, target.open('wb') as out:
        while chunk:=response.read(1024*1024):
            size+=len(chunk);h.update(chunk);out.write(chunk)
    if size!=expected['bytes'] or h.hexdigest()!=expected['sha256']:
        raise ValueError(f'Download checksum/size mismatch: {target.name}')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('experiment')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    manifest_path=root/'experiments'/args.experiment/'archive.json'
    if manifest_path.parent.parent != root/'experiments':
        raise ValueError('Invalid experiment name')
    meta=json.loads(manifest_path.read_text())
    assert meta['experiment']==args.experiment
    args.output.mkdir(parents=True,exist_ok=True)
    destination=args.output/args.experiment
    if destination.exists():raise FileExistsError(f'Will not overwrite {destination}')
    with tempfile.TemporaryDirectory(prefix='.download-',dir=args.output) as tmp:
        work=Path(tmp);archive=work/meta['archive']['name'];full=hashlib.sha256();size=0
        with archive.open('wb') as out:
            for part in meta['parts']:
                print('Downloading',part['name'],flush=True)
                path=work/part['name'];download(part['url'],path,part)
                with path.open('rb') as f:
                    while chunk:=f.read(1024*1024):out.write(chunk);full.update(chunk);size+=len(chunk)
                path.unlink()
        if size!=meta['archive']['bytes'] or full.hexdigest()!=meta['archive']['sha256']:
            raise ValueError('Reconstructed archive mismatch')
        extraction=work/'extracted';extraction.mkdir()
        with subprocess.Popen(['zstd','-q','-dc',str(archive)],stdout=subprocess.PIPE) as proc:
            with tarfile.open(fileobj=proc.stdout,mode='r|') as tar:
                seen=set()
                for member in tar:
                    relative=Path(member.name)
                    if (not member.isfile() or relative.is_absolute() or '..' in relative.parts
                        or relative.parts[0]!=args.experiment or member.name in seen):
                        raise ValueError(f'Unsafe/duplicate member: {member.name}')
                    seen.add(member.name)
                    target=extraction/relative;target.parent.mkdir(parents=True,exist_ok=True)
                    with tar.extractfile(member) as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)
            if proc.wait()!=0:raise RuntimeError('zstd decompression failed')
        (extraction/args.experiment).rename(destination)
    print('Extracted verified archive to',destination)


if __name__=='__main__':main()
