#!/usr/bin/env python3
"""Cross-platform verification of the published SHA256SUMS list.

Checks the current working files. On Windows a Git checkout may use CRLF for
text files, whereas the repository records canonical LF bytes. Such a case is
reported as CRLF-normalized rather than silently counted as a byte-for-byte match.
Use --strict to require identical on-disk bytes.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--strict',action='store_true',help='require identical bytes; do not permit CRLF normalization')
    args=ap.parse_args()
    records=[]
    for line in (ROOT/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        parts=line.split('  ',1)
        if len(parts)!=2 or len(parts[0])!=64:
            raise SystemExit('FAIL invalid checksum record: '+line)
        records.append((parts[0].lower(),parts[1]))
    exact=normalized=0
    failures=[]
    for digest,filename in records:
        p=ROOT/filename
        if p.is_absolute() or '..' in Path(filename).parts or not p.is_file():
            failures.append(filename+' (not found/unsafe path)'); continue
        content=p.read_bytes()
        if sha(content)==digest:
            exact+=1
        elif not args.strict and b'\r\n' in content and sha(content.replace(b'\r\n',b'\n'))==digest:
            normalized+=1
        else:
            failures.append(filename+' (digest mismatch)')
    if failures:
        for x in failures: print('FAIL:',x)
        raise SystemExit(1)
    print(f'PASS: {len(records)} checksum entries ({exact} exact bytes, {normalized} CRLF-normalized)')
    if normalized:
        print('NOTE: canonical LF hashes validated after normalizing checkout CRLF. Use --strict for raw on-disk bytes.')

if __name__=='__main__':
    main()
