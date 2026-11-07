#!/usr/bin/env python3
"""Run all offline checks available from released aggregate results.

Does NOT rerun enhancement, perception inference, bootstrap resampling,
or reproduce source-level analyses without source records.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
    'validate_release_tables.py',
    'validate_claims.py',
    'validate_e4_holm39.py',
    'validate_protocol_contracts.py',
    'check_repository_hashes.py',
]

def main()->None:
    for item in SCRIPTS:
        print('\n=== '+item+' ===',flush=True)
        subprocess.run([sys.executable,str(ROOT/'scripts'/item)],cwd=ROOT,check=True)
    print('\nPASS: all aggregate-data review checks completed',flush=True)

if __name__=='__main__':
    main()
