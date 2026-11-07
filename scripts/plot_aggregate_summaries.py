#!/usr/bin/env python3
"""Create NEW diagnostic plots from released aggregate summaries.

These are NOT bit-for-bit reconstructions of any figure in the manuscript.
No source-level scores, unreported numbers, or images are created.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def load(name):
    with (DATA/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,default=ROOT/'generated'/'aggregate_plots')
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    # E1 mean source-level mIoU change, no inference from confidence intervals.
    e1=load('e1_frozen_observer_summary.csv')
    methods=list(dict.fromkeys(r['method'] for r in e1))
    observers=list(dict.fromkeys(r['observer'] for r in e1))
    x=np.arange(len(methods))
    fig,ax=plt.subplots(figsize=(12,5))
    for j,obs in enumerate(observers):
        vals=[float(next(r['mean_delta_miou_pp'] for r in e1 if r['method']==m and r['observer']==obs)) for m in methods]
        ax.bar(x+(j-1)*0.26,vals,width=0.25,label=obs)
    ax.axhline(0,lw=0.8,color='black')
    ax.set_xticks(x,methods,rotation=55,ha='right')
    ax.set_ylabel('Mean source-level mIoU change (percentage points)')
    ax.set_title('E1: frozen-observer aggregate means (not new inference)')
    ax.legend(fontsize=8);fig.tight_layout()
    fig.savefig(args.output_dir/'E1_frozen_means.png',dpi=180);plt.close(fig)

    # E2 dataset-global mIoU; separate from source-paired E2 contrast table.
    e2=load('e2_train_test_domain_matrix.csv')
    domains=['RAW','HSRUIE','DTI-UIE']
    obs=list(dict.fromkeys(r['observer'] for r in e2))
    for o in obs:
        d={(r['train_domain'],r['test_domain']):float(r['miou_percent']) for r in e2 if r['observer']==o}
        mat=np.array([[d[t,s] for s in domains] for t in domains])
        fig,ax=plt.subplots(figsize=(5.6,4.4))
        im=ax.imshow(mat,cmap='viridis',vmin=0,vmax=100)
        ax.set_xticks(range(3),domains);ax.set_yticks(range(3),domains)
        ax.set_xlabel('Test domain');ax.set_ylabel('Train domain')
        for i in range(3):
            for j in range(3): ax.text(j,i,f'{mat[i,j]:.2f}',ha='center',va='center',color=('white' if mat[i,j]<50 else 'black'))
        ax.set_title('E2 dataset-global mIoU: '+o)
        fig.colorbar(im,ax=ax,label='mIoU (%)',shrink=0.85)
        fig.tight_layout();fig.savefig(args.output_dir/('E2_'+o.replace('-','_')+'.png'),dpi=180);plt.close(fig)

    # E3 historical original-RAW sign categories, without merging E6 references.
    e3=load('e3_observer_sign_patterns.csv')
    mm=[r['method'] for r in e3];pos=np.array([int(r['all_observers_benefit_count']) for r in e3]);mixed=np.array([int(r['mixed_sign_count']) for r in e3]);neg=np.array([int(r['all_observers_harmed_count']) for r in e3])
    fig,ax=plt.subplots(figsize=(11,5))
    xx=np.arange(len(mm));ax.bar(xx,pos,label='All benefit');ax.bar(xx,mixed,bottom=pos,label='Mixed');ax.bar(xx,neg,bottom=pos+mixed,label='All harm')
    ax.set_xticks(xx,mm,rotation=55,ha='right');ax.set_ylabel('Sources (out of 110)')
    ax.set_ylim(0,112);ax.set_title('E3: three-observer signs, historical original-RAW protocol')
    ax.legend(ncol=3);fig.tight_layout();fig.savefig(args.output_dir/'E3_observer_sign_patterns.png',dpi=180);plt.close(fig)

    # E4 source-level fixed-threshold F1, not COCO AP.
    e4=load('e4_source_level_f1_summary.csv')
    dom=list(dict.fromkeys(r['domain'] for r in e4));eps=list(dict.fromkeys(r['endpoint'] for r in e4))
    fig,ax=plt.subplots(figsize=(15,5.5));xx=np.arange(len(dom))
    for j,ep in enumerate(eps):
        v=[float(next(r['mean_delta_f1_pp'] for r in e4 if r['domain']==d and r['endpoint']==ep)) for d in dom]
        ax.bar(xx+(j-1)*0.26,v,width=0.25,label=ep)
    ax.axhline(0,lw=0.8,color='black');ax.set_xticks(xx,dom,rotation=65,ha='right')
    ax.set_ylabel('Mean source-level fixed-threshold F1 change (pp)')
    ax.set_title('E4: 13 variants x 3 dependent endpoints (2 trained models)');ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(args.output_dir/'E4_fixed_F1_means.png',dpi=180);plt.close(fig)

    # E5 only number of BH-significant tests, no implied source scatter.
    e5=load('e5_visual_task_correlations.csv');metrics=['UCIQE','UIQM'];tests=['pearson_bh_q','spearman_bh_q']
    fig,ax=plt.subplots(figsize=(5.6,4.4));xx=np.arange(2)
    for j,key in enumerate(tests):
        y=[sum(float(r[key])<0.05 for r in e5 if r['metric']==m) for m in metrics]
        ax.bar(xx+(j-0.5)*0.34,y,width=0.32,label=('Pearson' if j==0 else 'Spearman'))
    ax.set_xticks(xx,metrics);ax.set_ylabel('BH-significant correlations (q < .05)')
    ax.set_title('E5: released 120-test BH family');ax.legend()
    fig.tight_layout();fig.savefig(args.output_dir/'E5_BH_counts.png',dpi=180);plt.close(fig)

    # E6, separate from E3 due to different references for some methods.
    e6=load('e6_joint_observer_harm.csv')
    fig,ax=plt.subplots(figsize=(11,4.8))
    ax.bar(range(len(e6)),[float(r['any_observer_harm_percent']) for r in e6])
    ax.set_xticks(range(len(e6)),[r['method'] for r in e6],rotation=55,ha='right')
    ax.set_ylim(0,105);ax.set_ylabel('Any-observer harm rate (%)')
    ax.set_title('E6: source-matched harm rates under E6 reference protocol')
    fig.tight_layout();fig.savefig(args.output_dir/'E6_any_observer_harm.png',dpi=180);plt.close(fig)

    print('PASS: 7 descriptive plots generated under',args.output_dir)
    print('NOTE: these plots visualize aggregate tables; they do not reproduce the original source-level analyses.')

if __name__=='__main__':main()
