import os
import pathlib,sys,json,collections,time,traceback
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'))
import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
GAME=pathlib.Path(os.environ['WWP_GAME'])
D=GAME/'WWP_Data';AA=D/'StreamingAssets/aa/StandaloneWindows64'
MONO=str(AA/'c528ee817af37ad2f5b2f64797639c8f_monoscripts_3978cf45d9d912d9ad29ab4af9161121.bundle')
S=pathlib.Path(sys.argv[0]).parent
t0=time.time();g=TypeTreeGenerator('6000.1.17f1');g.load_local_game(str(GAME));print('gen',time.time()-t0,flush=True)
WANT={'TMPro.TextMeshProUGUI':'Unity.TextMeshPro','TMPro.TextMeshPro':'Unity.TextMeshPro','I2.Loc.Localize':'I2Loc','UnityEngine.UI.Text':'UnityEngine.UI','TMPro.TMP_InputField':'Unity.TextMeshPro','TMPro.TMP_Dropdown':'Unity.TextMeshPro','AztecEngine.Code.Modules.UI.TMP_DropdownExtended':'UI'}
NODES={}
def nodes(asm,cls):
    k=(asm,cls)
    if k not in NODES:
        ns=g.get_nodes(asm,cls);NODES[k]=TypeTreeNode.from_list([TypeTreeNode(x.m_Level,x.m_Type,x.m_Name,0,0,m_MetaFlag=x.m_MetaFlag) for x in ns])
    return NODES[k]
res=[]
TR={}
def gopath(byid,cab,go,depth=0):
    try:
        gobj=byid[(cab,go)];gt=gobj.read_typetree();name=gt['m_Name']
        if depth>12:return name
        comp=gt['m_Component'][0]['component']['m_PathID']
        tt=byid[(cab,comp)].read_typetree();fa=tt.get('m_Father',{}).get('m_PathID',0)
        if not fa:return name
        ft=byid[(cab,fa)].read_typetree();fgo=ft['m_GameObject']['m_PathID']
        return gopath(byid,cab,fgo,depth+1)+'/'+name
    except Exception as e:
        return '?'+type(e).__name__
for f in sys.argv[1:]:
    p=D/f if (D/f).exists() else AA/f
    env=UnityPy.load(str(p),*([MONO] if p.suffix=='.bundle' else []))
    cache={};gos={};n=0
    objs=[o for o in env.objects]
    byid={(o.assets_file.name,o.path_id):o for o in objs}
    for o in objs:
        if o.type.name!='MonoBehaviour':continue
        try:
            h=o.parse_monobehaviour_head();pp=h.m_Script;k=(o.assets_file.name,pp.m_FileID,pp.m_PathID)
            if k not in cache:
                try:s=pp.deref_parse_as_object();cache[k]=(s.m_AssemblyName,(s.m_Namespace+'.' if s.m_Namespace else '')+s.m_ClassName)
                except Exception:cache[k]=None
            c=cache[k]
            if not c or c[1] not in WANT:continue
            try:tree=o.read_typetree()
            except Exception:tree=o.read_typetree(nodes=nodes(c[0],c[1]))
            go=tree['m_GameObject']['m_PathID']
            if go not in gos:gos[go]=gopath(byid,o.assets_file.name,go)
            r={'file':f,'cab':o.assets_file.name,'pid':o.path_id,'cls':c[1],'go':go,'goname':gos[go]}
            if c[1].startswith('TMPro.TextMeshPro'):r.update(text=tree['m_text'],font=tree['m_fontAsset']['m_PathID'],fontfile=tree['m_fontAsset']['m_FileID'])
            elif c[1]=='UnityEngine.UI.Text':r.update(text=tree['m_Text'],font=tree['m_FontData']['m_Font']['m_PathID'])
            elif c[1]=='I2.Loc.Localize':r.update(term=tree.get('mTerm'),term2=tree.get('mTermSecondary'),target=str(tree.get('mTarget')),enabled=tree.get('m_Enabled'))
            else:r.update(keys=[k for k in tree if 'ext' in k or 'laceholder' in k or 'ption' in k][:10])
            res.append(r);n+=1
        except Exception as e:
            res.append({'file':f,'pid':o.path_id,'err':repr(e)[:200]})
    print(f,'items',n,'%.0fs'%(time.time()-t0),flush=True)
    del env,objs,byid
(S/'texts.json').write_text(json.dumps(res,ensure_ascii=False,indent=0),encoding='utf8')
print('total',len(res),'errors',sum(1 for r in res if 'err' in r))
