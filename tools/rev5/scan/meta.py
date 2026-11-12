import os
import struct,pathlib,json,re
p=pathlib.Path(os.environ['WWP_GAME'])/'WWP_Data/il2cpp_data/Metadata/global-metadata.dat'
b=p.read_bytes()
san,ver=struct.unpack_from('<Ii',b,0);print(hex(san),ver,len(b))
h=struct.unpack_from('<16i',b,8);print(h)
lo,ls_,do,ds=h[0],h[1],h[2],h[3]
lits=[]
for i in range(ls_//8):
    ln,di=struct.unpack_from('<Ii',b,lo+i*8)
    lits.append(b[do+di:do+di+ln].decode('utf8','replace'))
print('literals',len(lits))
pathlib.Path(__file__).with_name('literals.json').write_text(json.dumps(lits,ensure_ascii=False,indent=0),encoding='utf8')
# candidate UI strings: contain space-separated words, start uppercase, no path/code-like chars
cand=[s for s in lits if re.fullmatch(r"[A-Z][A-Za-z ,.'!?:%\-]{2,}",s) and ' ' in s and not re.search(r'_|/|\|\.cs|\(|\)',s)]
print('cand',len(cand))
for s in cand[:400]:print(repr(s))
