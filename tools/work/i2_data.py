import pathlib,struct,json,collections
class Reader:
    def __init__(self,data,pos=0): self.data=data; self.pos=pos
    def i(self): v=struct.unpack_from('<i',self.data,self.pos)[0];self.pos+=4;return v
    def align(self): self.pos=(self.pos+3)&~3
    def s(self):
        n=self.i();assert 0<=n<=len(self.data)-self.pos,(self.pos,n)
        v=self.data[self.pos:self.pos+n].decode('utf-8');self.pos+=n;self.align();return v
    def strings(self): return [self.s() for _ in range(self.i())]
    def blob(self):
        n=self.i();assert 0<=n<=len(self.data)-self.pos,(self.pos,n)
        v=self.data[self.pos:self.pos+n];self.pos+=n;self.align();return v
def parse(data):
    r=Reader(data,56);n=r.i();terms=[]
    for j in range(n):
        start=r.pos
        try:
            key=r.s();kind=r.i();langs=r.strings();flags=r.blob();touch=r.strings()
            terms.append(dict(key=key,kind=kind,langs=langs,flags=list(flags),touch=touch,start=start,end=r.pos))
        except Exception:
            print('BAD',j,start,repr(data[start:start+300]));raise
    return terms,r.pos
def s(value):
    raw=value.encode('utf8');out=struct.pack('<i',len(raw))+raw
    return out+b'\0'*((-len(out))%4)
def strings(values):return struct.pack('<i',len(values))+b''.join(s(x) for x in values)
def rebuild(data,korean):
    terms,end=parse(data);out=bytearray(data[:60])
    for t in terms:
        langs=t['langs'].copy();langs[0]=korean[t['key']]
        out+=s(t['key'])+struct.pack('<i',t['kind'])+strings(langs)
        flags=bytes(t['flags']);out+=struct.pack('<i',len(flags))+flags+b'\0'*((-len(flags))%4)
        out+=strings(t['touch'])
    tail=data[end:]
    # Disable live sheet synchronization, which would replace the local patch.
    r=Reader(tail);r.pos=8;r.s();count=r.i()
    for _ in range(count):r.s();r.s();r.pos+=4
    r.pos+=8;urlstart=r.pos;r.s();r.s();urlend=r.pos
    tail=tail[:urlstart]+s('')+s('')+tail[urlend:]
    out+=tail
    check,_=parse(out)
    assert len(check)==len(terms)
    for a,b in zip(terms,check):
        assert a['key']==b['key'] and a['kind']==b['kind'] and a['langs'][1:]==b['langs'][1:] and a['flags']==b['flags'] and a['touch']==b['touch']
    return bytes(out)
if __name__=='__main__':
    data=pathlib.Path('work/113706.bin').read_bytes();terms,end=parse(data)
    pathlib.Path('work/terms.json').write_text(json.dumps(terms,ensure_ascii=False,indent=2),encoding='utf8')
    print('TERMS',len(terms),'END',end,'TAIL',repr(data[end:]))
    print('KIND',collections.Counter(t['kind'] for t in terms),'CATEGORIES',collections.Counter(t['key'].split('/')[0] for t in terms))
    print('ENGLISH CHARS',sum(len(t['langs'][0]) for t in terms if t['langs']))
    for t in terms[-12:]: print(t['key'],t['langs'][0])
