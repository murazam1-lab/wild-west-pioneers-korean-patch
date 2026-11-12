"""Build patched resources.assets from the (unpatched, updated) original.
Usage: py -I -X utf8 build4.py [--dry]"""
import os
import pathlib,sys,json,hashlib,gc
W=pathlib.Path(os.environ['WWP_WORK'])
R=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'libs'));sys.path.insert(0,str(W))
import UnityPy
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
from i2_data import rebuild,parse
game=pathlib.Path(os.environ['WWP_GAME'])
backup=game/'KoreanPatch_Backup_20261107'/'resources.assets.original'
source=backup if backup.exists() else game/'WWP_Data/resources.assets'
I2,TMPFONT,TMPSET,UITFONT,TTF=113714,113682,113726,113730,4630
dry='--dry' in sys.argv
def nodes(name):
    d=json.loads((W/name).read_text(encoding='utf8'))
    return TypeTreeNode.from_list([TypeTreeNode(x['m_Level'],x['m_Type'],x['m_Name'],0,0,m_MetaFlag=x['m_MetaFlag']) for x in d])
tmp=nodes('TMP_FontAsset.nodes.json');settings=nodes('TMP_Settings.nodes.json');uit=nodes('UnityEngine.TextCore.Text.FontAsset.nodes.json')
env=UnityPy.load(str(source));asset=env.file
objects={o.path_id:o for o in env.objects}
assert objects[I2].peek_name()=='I2Languages' and objects[TMPFONT].peek_name()=='SourceHanSerif-Bold SDF'
assert objects[TMPSET].peek_name()=='TMP Settings' and objects[UITFONT].peek_name().startswith('UIT_NotoSans')
assert objects[TTF].read_typetree()['m_Name']=='SourceHanSerif-Bold'
original={i:hashlib.sha256(o.get_raw_data()).hexdigest() for i,o in objects.items()}
changes={}
if not dry:
    translation=json.loads((R/'final_korean.json').read_text(encoding='utf8'))
    obj=objects[I2];obj.set_raw_data(rebuild(obj.get_raw_data(),translation))
    changes[I2]='English text column replaced with Korean; online sheet sync disabled'
for path,node in [(TMPFONT,tmp),(TMPSET,settings),(UITFONT,uit)]:
    obj=objects[path];raw=obj.get_raw_data();tree=obj.read_typetree(nodes=node)
    assert obj.save_typetree(tree,nodes=node)==raw,('ROUNDTRIP FAILED',path)
    if path==TMPFONT:
        print('TMPFONT multiatlas',tree['m_IsMultiAtlasTexturesEnabled'],'mode',tree.get('m_AtlasPopulationMode'),'src',tree.get('m_SourceFontFile'))
        tree['m_IsMultiAtlasTexturesEnabled']=1
        changes[path]='Enable multiple atlases on the bundled dynamic Source Han Serif font'
    elif path==TMPSET:
        print('TMPSET fallbacks',tree['m_fallbackFontAssets'],'hangul',tree['m_UseModernHangulLineBreakingRules'])
        ptr={'m_FileID':0,'m_PathID':TMPFONT}
        if ptr not in tree['m_fallbackFontAssets']:tree['m_fallbackFontAssets'].append(ptr)
        tree['m_UseModernHangulLineBreakingRules']=1
        changes[path]='Add Korean font to global TextMeshPro fallback and enable Hangul line breaking'
    elif path==UITFONT:
        print('UIT src',tree['m_SourceFontFile'],repr(tree['m_SourceFontFilePath']),'mode',tree['m_AtlasPopulationMode'],'os',tree['InternalDynamicOS'])
        tree['m_SourceFontFile']={'m_FileID':0,'m_PathID':TTF}
        tree['m_SourceFontFilePath']='';tree['m_AtlasPopulationMode']=1;tree['InternalDynamicOS']=0;tree['m_IsMultiAtlasTexturesEnabled']=1
        changes[path]='Point UI Toolkit dynamic font to bundled Source Han Serif with full Korean coverage'
    obj.save_typetree(tree,nodes=node)
if dry:
    print('DRY OK: objects',len(objects),'source',source);sys.exit()
dest=R/'patched'/'resources.assets';dest.parent.mkdir(exist_ok=True)
with dest.open('wb') as f:f.write(asset.save())
print('SAVED',dest,dest.stat().st_size,flush=True)
expected={i:hashlib.sha256(o.data if o.data is not None else o.get_raw_data()).hexdigest() for i,o in objects.items()}
del objects,asset,env;gc.collect()
env=UnityPy.load(str(dest));loaded={o.path_id:o for o in env.objects}
assert set(loaded)==set(original)
changed=[]
for i,o in loaded.items():
    h=hashlib.sha256(o.get_raw_data()).hexdigest()
    assert h==expected[i],('RELOAD MISMATCH',i)
    if h!=original[i]:changed.append(i)
assert set(changed)==set(changes),(changed,changes)
terms,_=parse(loaded[I2].get_raw_data())
assert all(t['langs'][0]==translation[t['key']] for t in terms)
manifest={'source':str(game/'WWP_Data/resources.assets'),'revision':4,'date':'2026-11-07','game_build_guid':'ef21a3ee937241489cb317190668bc9d',
 'original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'patched_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
 'objects_total':len(loaded),'changed_objects':{str(k):v for k,v in changes.items()},'translation_entries_total':len(terms),
 'verified':'All serialized objects reloaded; only the four intended objects changed; other languages, keys, and flags preserved.'}
(R/'patch_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)
