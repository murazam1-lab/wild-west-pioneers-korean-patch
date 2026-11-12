"""4차 resources.assets(내용 그대로)를 원본과 같은 16바이트 객체 정렬로 다시 저장. 객체 내용은 바꾸지 않음."""
import os
import pathlib,sys,json,hashlib,gc
W=pathlib.Path(os.environ['WWP_WORK'])
R=pathlib.Path(__file__).parent;R4=R.parent/'rev4'
sys.path.insert(0,str(W/'libs'))
import UnityPy
from UnityPy.streams.EndianBinaryWriter import EndianBinaryWriter
_align=EndianBinaryWriter.align_stream
def _align16(self,alignment=4):return _align(self,16 if alignment==8 else alignment)
EndianBinaryWriter.align_stream=_align16
sha=lambda b:hashlib.sha256(b).hexdigest()
src=R4/'patched'/'resources.assets'
m4=json.loads((R4/'patch_manifest.json').read_text(encoding='utf8'))
assert sha(src.read_bytes())==m4['patched_sha256'],'rev4 patched file hash mismatch'
env=UnityPy.load(str(src));objs={o.path_id:o for o in env.objects}
h4={i:sha(o.get_raw_data()) for i,o in objs.items()}
dest=R/'patched'/'resources.assets';dest.parent.mkdir(exist_ok=True)
dest.write_bytes(env.file.save());del objs,env;gc.collect()
env=UnityPy.load(str(dest));loaded={o.path_id:o for o in env.objects}
assert set(loaded)==set(h4)
bad=[i for i,o in loaded.items() if sha(o.get_raw_data())!=h4[i]]
assert not bad,bad[:10]
al=sum(o.byte_start%16==0 for o in env.file.objects.values())
print('objects',len(loaded),'all identical to rev4; 16-aligned',al,'/',len(loaded),'size',dest.stat().st_size,'sha',sha(dest.read_bytes()))
