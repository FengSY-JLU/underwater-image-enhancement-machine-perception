#!/usr/bin/env python3
"""Cross-table structural checks; never equate distinct estimands.

Avoids comparing E3 sign groups to E6 sign groups, and avoids comparing
E2 dataset-global mIoU with its separately source-paired contrasts.
"""
from __future__ import annotations
import csv
from pathlib import Path
from collections import Counter

DATA=Path(__file__).resolve().parents[1]/'data'

def load(name):
    with (DATA/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def require(test,msg):
    if not test: raise AssertionError(msg)
    print('PASS:',msg)

def main():
    # E1: 10 configurations x 3 frozen observers.
    a=load('e1_frozen_observer_summary.csv')
    require(len(a)==30 and len(set((r['method'],r['observer']) for r in a))==30,
            'E1 unique method-observer pairs')
    require(len({r['method'] for r in a})==10 and
            all(n==3 for n in Counter(r['method'] for r in a).values()),
            'E1 10 configurations each with three observers')
    # E2: grid structure; no subtraction across different estimands.
    x=load('e2_train_test_domain_matrix.csv')
    expected={'RAW','HSRUIE','DTI-UIE'}
    obs={r['observer'] for r in x}
    require(len(obs)==2 and all({(r['train_domain'],r['test_domain']) for r in x if r['observer']==o}==
            {(t,s) for t in expected for s in expected} for o in obs),
            'E2 per-observer complete train/test 3x3 grids')
    contrasts=load('e2_domain_contrasts.csv')
    require(len(contrasts)==12 and all(n==3 for n in Counter(r['observer_domain'] for r in contrasts).values()) and
            all({r['contrast'] for r in contrasts if r['observer_domain']==g}=={'RE-RR','EE-RE','EE-RR'}
                for g in {r['observer_domain'] for r in contrasts}),
            'E2 twelve distinct source-paired contrasts in four groups')
    # E3/E6 are separate reference protocols; each table is checked internally only.
    for name,keys in [
        ('e3_observer_sign_patterns.csv',['all_observers_benefit_count','mixed_sign_count','all_observers_harmed_count']),
        ('e6_joint_observer_harm.csv',['all_three_benefit_count','mixed_sign_count','all_three_harm_count']),
    ]:
        z=load(name)
        require(len(z)==10 and len({r['method'] for r in z})==10 and
                all(sum(int(r[k]) for k in keys)==110 for r in z),
                name+' ten distinct configurations and separate 110-source accounting')
    # E4: the two Mask R-CNN endpoints must remain distinct but dependent.
    f=load('e4_source_level_f1_summary.csv')
    counts=load('e4_holm39_sign_tests.csv')
    endpoints={'Faster R-CNN Box','Mask R-CNN Box','Mask R-CNN Mask'}
    require(len(f)==39 and len({r['domain'] for r in f})==13 and
            all({r['endpoint'] for r in f if r['domain']==d}==endpoints for d in {r['domain'] for r in f}),
            'E4 13 domain variants x 3 endpoints (2 model architectures)')
    require(len(counts)==39 and len({(r['domain'],r['endpoint']) for r in counts})==39 and
            len({r['domain'] for r in counts})==13 and
            all(sum(int(r[k]) for k in ('pos','neg','zero'))==3370 for r in counts),
            'E4 distinct sign tests and complete source accounting')
    # E5: metric x observer x method combinations; TACL n=109 only.
    c=load('e5_visual_task_correlations.csv')
    require(len(c)==60 and len({(r['method'],r['metric'],r['observer']) for r in c})==60 and
            {r['metric'] for r in c}=={'UCIQE','UIQM'} and
            all(int(r['n_sources'])==(109 if r['method'].startswith('TACL G-') else 110) for r in c),
            'E5 60 paired test rows, 109-source TACL exception')
    q=load('e5_visual_task_sign_quadrants.csv')
    sign_cols=('visual_positive_task_positive','visual_positive_task_negative',
               'visual_negative_task_positive','visual_negative_task_negative')
    require(len(q)==60 and len({(r['method'],r['metric'],r['observer']) for r in q})==60 and
            all(sum(int(r[k]) for k in sign_cols)==int(r['n_sources']) for r in q),
            'E5 60 visual/task sign quadrant tables sum to their denominators')
    risk=load('e6_observer_risk_profiles.csv')
    require(len(risk)==30 and len({(r['method'],r['observer']) for r in risk})==30,
            'E6 30 observer-level risk profiles')
    print('All protocol-aware structural checks passed.')

if __name__=='__main__': main()
