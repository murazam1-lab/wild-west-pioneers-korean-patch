"""5차: 씬/프리팹 고정 영어 라벨 한글화 + UI Toolkit 퀘스트 패널 글꼴 한글 대체 연결.
resources.assets(4차 패치)는 건드리지 않음. 대상 파일을 원본에서 읽어 rev5/patched/에 저장하고 전수 검증.
Usage: py -I -X utf8 build5.py"""
import os
import pathlib,sys,json,hashlib,gc,collections
W=pathlib.Path(os.environ['WWP_WORK'])
R=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'libs'));sys.path.insert(0,str(W))
import UnityPy
from UnityPy.streams.EndianBinaryWriter import EndianBinaryWriter
# Unity 원본은 객체 데이터를 16바이트 경계에 둔다. UnityPy 기본값(8)을 원본과 같게 16으로 맞춤
# (SerializedFile.save에서 align_stream(8)은 객체 사이 정렬에만 쓰임).
_align=EndianBinaryWriter.align_stream
def _align16(self,alignment=4):return _align(self,16 if alignment==8 else alignment)
EndianBinaryWriter.align_stream=_align16
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
GAME=pathlib.Path(os.environ['WWP_GAME']);D=GAME/'WWP_Data'
BACKUP=GAME/'KoreanPatch_Backup_20261108'
targets=json.loads((R/'scene_targets.json').read_text(encoding='utf8'))
FONT_FIX={'sharedassets11.assets':(24191,'BarlowCondensed-SemiBold-Toolkit',{'m_FileID':4,'m_PathID':113730})}
g=TypeTreeGenerator('6000.1.17f1');g.load_local_game(str(GAME))
def gen(asm,cls):
    return TypeTreeNode.from_list([TypeTreeNode(x.m_Level,x.m_Type,x.m_Name,0,0,m_MetaFlag=x.m_MetaFlag) for x in g.get_nodes(asm,cls)])
def nodesfile(name):
    d=json.loads((W/name).read_text(encoding='utf8'))
    return TypeTreeNode.from_list([TypeTreeNode(x['m_Level'],x['m_Type'],x['m_Name'],0,0,m_MetaFlag=x['m_MetaFlag']) for x in d])
NODES={'TMPro.TextMeshProUGUI':gen('Unity.TextMeshPro','TMPro.TextMeshProUGUI'),'TMPro.TextMeshPro':gen('Unity.TextMeshPro','TMPro.TextMeshPro')}
UIT=nodesfile('UnityEngine.TextCore.Text.FontAsset.nodes.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
by=collections.defaultdict(list)
for t in targets:by[t['file']].append(t)
files=sorted(set(by)|set(FONT_FIX))
manifest={'revision':5,'date':'2026-11-08','game_build_guid':'ef21a3ee937241489cb317190668bc9d','files':{}}
for f in files:
    src=BACKUP/(f+'.original')
    if not src.exists():src=D/f
    srcbytes=src.read_bytes();src_sha=sha(srcbytes);del srcbytes
    env=UnityPy.load(str(src));sf=env.file
    objs={o.path_id:o for o in env.objects}
    original={i:sha(o.get_raw_data()) for i,o in objs.items()}
    changes={}
    for t in by.get(f,[]):
        o=objs[t['pid']];N=NODES[t['cls']];raw=o.get_raw_data();tree=o.read_typetree(nodes=N)
        assert o.save_typetree(tree,nodes=N)==raw,('ROUNDTRIP',f,t['pid'])
        assert tree['m_text']==t['en'],('TEXT CHANGED',f,t['pid'],tree['m_text'],t['en'])
        tree['m_text']=t['ko'];o.save_typetree(tree,nodes=N);changes[t['pid']]=(t['en'],t['ko'])
    if f in FONT_FIX:
        pid,name,ptr=FONT_FIX[f];o=objs[pid];raw=o.get_raw_data();tree=o.read_typetree(nodes=UIT)
        assert tree['m_Name']==name and o.save_typetree(tree,nodes=UIT)==raw
        assert sf.externals[ptr['m_FileID']-1].path=='resources.assets',sf.externals[ptr['m_FileID']-1].path
        print(f,'font',name,'fallback before',tree['m_FallbackFontAssetTable'])
        if ptr not in tree['m_FallbackFontAssetTable']:tree['m_FallbackFontAssetTable'].append(ptr)
        o.save_typetree(tree,nodes=UIT);changes[pid]=('fallback',str(ptr))
    dest=R/'patched'/f;dest.parent.mkdir(exist_ok=True)
    dest.write_bytes(sf.save())
    expected={i:sha(o.data if getattr(o,'data',None) is not None else o.get_raw_data()) for i,o in objs.items()}
    del objs,sf,env;gc.collect()
    env=UnityPy.load(str(dest));loaded={o.path_id:o for o in env.objects}
    assert set(loaded)==set(original),'object set differs'
    changed=[]
    for i,o in loaded.items():
        h=sha(o.get_raw_data());assert h==expected[i],('RELOAD MISMATCH',f,i)
        if h!=original[i]:changed.append(i)
    assert set(changed)==set(changes),(f,sorted(set(changed)^set(changes)))
    for t in by.get(f,[]):
        assert loaded[t['pid']].read_typetree(nodes=NODES[t['cls']])['m_text']==t['ko']
    if f in FONT_FIX:
        pid,name,ptr=FONT_FIX[f];assert ptr in loaded[pid].read_typetree(nodes=UIT)['m_FallbackFontAssetTable']
    manifest['files'][f]={'original_sha256':src_sha,'patched_sha256':sha(dest.read_bytes()),'objects_total':len(loaded),'changed_objects':len(changed),
        'texts':len(by.get(f,[])),'font_fix':f in FONT_FIX}
    print(f,'objects',len(loaded),'changed',len(changed),'OK',flush=True)
    del loaded,env;gc.collect()
(R/'patch_manifest5.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
