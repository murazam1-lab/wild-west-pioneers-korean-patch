import os
import pathlib,sys,json,collections,re
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'))
import UnityPy,numpy as np
D=(pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data');AA=D/'StreamingAssets/aa/StandaloneWindows64'
MONO=str(AA/'c528ee817af37ad2f5b2f64797639c8f_monoscripts_3978cf45d9d912d9ad29ab4af9161121.bundle')
S=pathlib.Path(sys.argv[0]).parent
r=json.load(open(S/'texts.json',encoding='utf8'))
loc={(x['cab'],x['go']) for x in r if x.get('cls')=='I2.Loc.Localize'}
cand=collections.defaultdict(set)
for x in r:
    if 'text' in x and (x['cab'],x['go']) not in loc and re.search('[A-Za-z]{2,}',re.sub(r'<[^>]+>','',x['text'] or '')):
        cand[x['file']].add(x['pid'])
out={}
for f,pids in cand.items():
    p=D/f if (D/f).exists() else AA/f
    env=UnityPy.load(str(p),*([MONO] if p.suffix=='.bundle' else []))
    P=np.array(sorted(pids),dtype=np.int64);cache={}
    refs=collections.defaultdict(list)
    for o in env.objects:
        if o.type.name!='MonoBehaviour':continue
        raw=o.get_raw_data()
        for off in range(4):
            b=raw[off:];n=len(b)//4
            if n<3:continue
            a=np.frombuffer(b[:n*4],'<i4').astype(np.int64)
            z=np.nonzero(a[:-2]==0)[0]
            if not len(z):continue
            pid=(a[z+1]&0xffffffff)|(a[z+2]<<32)
            hit=np.isin(pid,P)
            for i in z[hit]:
                t=int(pid[np.nonzero(z==i)[0][0]])
                if t==o.path_id:continue
                k=o.path_id
                if k not in cache:
                    try:
                        s=o.parse_monobehaviour_head().m_Script.deref_parse_as_object();cache[k]=s.m_ClassName
                    except Exception:cache[k]='?'
                refs[t].append(cache[k])
    out[f]={str(k):sorted(set(v)) for k,v in refs.items()}
    print(f,len(pids),'referenced',len(refs),flush=True)
json.dump(out,open(S/'refs.json','w',encoding='utf8'),indent=0)
