"""Reproducible, editable SVG/PDF schematic of overlapping UIE research emphases."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from pathlib import Path

root=Path(__file__).resolve().parent
fig_dir=root/'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
fig,ax=plt.subplots(figsize=(10.0,6.0),dpi=190)
fig.patch.set_facecolor('white'); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
navy='#20344C'; muted='#52677C'; grey='#8EA1B2'
colors=['#2D6792','#0E888B','#A07143','#66539A']
pale=['#F0F6FB','#EBF7F5','#FCF6EF','#F4F1F9']
ax.text(.34,5.64,'HOW THE RESEARCH QUESTION HAS SHIFTED',fontsize=16.6,color=navy,weight='bold',va='center')
ax.text(9.66,5.64,'overlapping emphases',fontsize=11.0,color=muted,style='italic',ha='right',va='center')

rows=[
 ('Appearance-first','How can degraded underwater images be improved?',
  'Evidence focus: image fidelity, appearance, UCIQE / UIQM'),
 ('Task-informed','Can recognition information guide enhancement?',
  'Evidence focus: semantic priors, task losses, joint training'),
 ('Intervention effect','Does an enhanced input help a particular observer?',
  'Evidence focus: matched RAW--enhanced task-response changes'),
 ('Conditional utility','When, for whom, and at what risk is it beneficial?',
  'Evidence: task, observer, protocol, geometry, information and risk'),
]
ys=[4.50,3.40,2.30,1.20]
for i,((lab,q,ev),y) in enumerate(zip(rows,ys)):
 c=colors[i]
 r=FancyBboxPatch((1.08,y-.42),8.58,.89,boxstyle='round,pad=.02,rounding_size=.12',
                  edgecolor=c,facecolor=pale[i],linewidth=1.25)
 ax.add_patch(r)
 ax.add_patch(Circle((.58,y+.02),.23,facecolor=c,edgecolor='white',linewidth=1.3,zorder=5))
 ax.text(.58,y+.02,str(i+1),ha='center',va='center',color='white',fontsize=12.6,weight='bold',zorder=6)
 # Labels are visually separated from questions, unlike existing five-strand landscape.
 ax.text(1.34,y+.22,lab,fontsize=13.1,weight='bold',color=c,va='center')
 ax.text(4.05,y+.19,q,fontsize=13.1,color=navy,weight='medium',va='center')
 ax.text(4.05,y-.19,ev,fontsize=11.6,color=muted,va='center')
 if i<3:
  ax.add_patch(FancyArrowPatch((.58,y-.30),(.58,ys[i+1]+.29),
                 arrowstyle='-|>',mutation_scale=13,lw=1.45,color=grey))

ax.plot([.35,9.67],[.56,.56],color='#D7E0E8',lw=.9)
ax.text(.4,.28,'The emphases overlap and coexist; the sequence organizes research questions, not a rigid timeline.',
        color=muted,fontsize=11.4,ha='left',va='center')
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
name='fig02a_question_evolution'
fig.savefig(fig_dir/(name+'.pdf'),bbox_inches='tight',pad_inches=.11,facecolor='white')
fig.savefig(fig_dir/(name+'.svg'),bbox_inches='tight',pad_inches=.11,facecolor='white')
fig.savefig(root/(name+'.png'),bbox_inches='tight',pad_inches=.11,dpi=160,facecolor='white')
plt.close(fig)
print('figure ready')
