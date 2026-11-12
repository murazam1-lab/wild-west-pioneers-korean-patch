"""원본과 패치본의 SerializedFile 구조(헤더·타입·외부참조·객체표 순서/정렬) 비교"""
import os
import pathlib,sys
W=pathlib.Path(os.environ['WWP_WORK'])
R=pathlib.Path(__file__).parent;sys.path.insert(0,str(W/'libs'))
import UnityPy
D=(pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data');B=D.parent/'KoreanPatch_Backup_20261108'
for p in sorted((R/'patched').iterdir()):
    src=B/(p.name+'.original')
    if not src.exists():src=D/p.name
    a=UnityPy.load(str(src)).file;b=UnityPy.load(str(p)).file
    ha,hb=a.header,b.header
    oa=[(o.path_id,o.type_id,o.class_id) for o in a.objects.values()];ob=[(o.path_id,o.type_id,o.class_id) for o in b.objects.values()]
    ta=[(t.class_id,t.script_type_index,bytes(t.old_type_hash or b'')) for t in a.types];tb=[(t.class_id,t.script_type_index,bytes(t.old_type_hash or b'')) for t in b.types]
    align=all(o.byte_start%8==0 for o in b.objects.values()) if all(o.byte_start%8==0 for o in a.objects.values()) else 'n/a'
    print(p.name,'ver',ha.version,hb.version,'endian',ha.endian==hb.endian,'unity',a.unity_version==b.unity_version,'target',a.target_platform==b.target_platform,
          'types',ta==tb,'externals',[e.path for e in a.externals]==[e.path for e in b.externals],'objtable',oa==ob,'scripttypes',len(a.script_types)==len(b.script_types),
          'refs',len(getattr(a,'ref_types',[]) or [])==len(getattr(b,'ref_types',[]) or []),'align8',align,'size',src.stat().st_size,p.stat().st_size,'datapos',ha.data_offset,hb.data_offset)
