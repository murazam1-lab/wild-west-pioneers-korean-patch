import os
import pathlib,sys,json,collections,time
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'))
import UnityPy
D=(pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data')
AA=D/'StreamingAssets/aa/StandaloneWindows64'
files=sys.argv[1:]
out={}
for f in files:
    t=time.time()
    p=D/f if (D/f).exists() else AA/f
    extra=[str(AA/'c528ee817af37ad2f5b2f64797639c8f_monoscripts_3978cf45d9d912d9ad29ab4af9161121.bundle')] if p.suffix=='.bundle' else []
    env=UnityPy.load(str(p),*extra)
    cache={};cnt=collections.Counter();types=collections.Counter()
    for o in env.objects:
        types[o.type.name]+=1
        if o.type.name!='MonoBehaviour':continue
        try:
            h=o.parse_monobehaviour_head();pp=h.m_Script;k=(o.assets_file.name,pp.m_FileID,pp.m_PathID)
            if k not in cache:
                try:s=pp.deref_parse_as_object();cache[k]=f'{s.m_AssemblyName}:{s.m_Namespace}.{s.m_ClassName}'
                except Exception as e:cache[k]='?'+type(e).__name__
            cnt[cache[k]]+=1
        except Exception as e:cnt['!head '+type(e).__name__]+=1
    interesting={k:v for k,v in cnt.items() if any(s in k.lower() for s in ['text','local','font','uidocument','visualtree','panelsettings','label','tooltip','dropdown','input','?','!'])}
    out[f]={'types':dict(types),'mb':dict(cnt)}
    print(f,'%.0fs'%(time.time()-t),'objs',sum(types.values()),'MB',sum(cnt.values()),json.dumps(interesting,ensure_ascii=False),flush=True)
    del env
pathlib.Path(sys.argv[0]).with_name('census_'+str(abs(hash(tuple(files)))%10000)+'.json').write_text(json.dumps(out,indent=1),encoding='utf8')
