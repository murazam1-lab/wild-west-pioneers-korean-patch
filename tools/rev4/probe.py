import os
import pathlib,sys,hashlib,collections
W=pathlib.Path(os.environ['WWP_WORK'])
sys.path.insert(0,str(W/'libs'));sys.path.insert(0,str(W))
import UnityPy
from i2_data import parse
game=pathlib.Path(os.environ['WWP_GAME'])
env=UnityPy.load(str(game/'WWP_Data/resources.assets'))
print('VERSION',env.file.unity_version,'OBJS',len(env.objects))
for o in env.objects:
    if o.type.name in('MonoBehaviour','Font'):
        try:n=o.peek_name()
        except Exception:n='?'
        if o.type.name=='Font' or any(s in (n or '').lower() for s in ['i2','language','font','tmp settings','tmp_settings','sourcehan','noto']):
            print(o.path_id,o.type.name,repr(n),o.byte_size)
