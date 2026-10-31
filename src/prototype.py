"""高光谱像素分割 — deterministic numerical prototype."""
import argparse,json
from pathlib import Path
import numpy as np

def finite(a,ndim=None):
 a=np.asarray(a,dtype=float)
 if not np.isfinite(a).all() or not a.size or (ndim is not None and a.ndim!=ndim): raise ValueError('Invalid shape, empty or nonfinite input')
 return a
def process(cube,endmembers):
 cube=finite(cube,3);endmembers=finite(endmembers,2)
 if cube.shape[-1]!=endmembers.shape[1] or len(endmembers)<2:raise ValueError('Endmember bands mismatch')
 flat=cube.reshape(-1,cube.shape[-1]);norm=np.linalg.norm(flat,axis=1);enorm=np.linalg.norm(endmembers,axis=1)
 if np.any(norm==0) or np.any(enorm==0):raise ValueError('Zero spectrum')
 angles=np.arccos(np.clip((flat/norm[:,None])@(endmembers/enorm[:,None]).T,-1,1))
 return np.argmin(angles,axis=1).reshape(cube.shape[:2])

def demo():
 rng=np.random.default_rng(42);y,x=np.mgrid[:80,:120];mask=((x-60)**2/900+(y-40)**2/400)<1
 bands=np.linspace(0,1,24);ends=np.stack([.2+bands*.7,.9-bands*.5]);cube=ends[mask.astype(int)]+rng.normal(0,.025,(80,120,24))
 result=process(cube,ends);iou=float(np.sum((result==1)&mask)/np.sum((result==1)|mask));assert iou>.98
 return None,{'Segmentation':result,'Ground truth':mask},{'synthetic_foreground_IoU':iou,'pixels':9600}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('artifacts'));args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 x,series,metrics=demo()
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 if x is None:
  fig,axes=plt.subplots(1,len(series),figsize=(14,4),layout='constrained');axes=np.atleast_1d(axes)
  for ax,(label,values) in zip(axes,series.items()):ax.imshow(values,cmap='viridis');ax.set_title(label);ax.set_axis_off()
 else:
  fig,ax=plt.subplots(figsize=(11,5),layout='constrained')
  for label,values in series.items():ax.plot(x,values,label=label)
  ax.legend();ax.grid(alpha=.2)
 fig.suptitle('Synthetic prototype validation — not field measurements')
 fig.savefig(args.output/'result.png',dpi=140);plt.close(fig)
 np.savez_compressed(args.output/'results.npz',**{str(i):v for i,v in enumerate(series.values())})
 (args.output/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
