import pathlib,sys,json,re,time,os
os.environ['PYTHONIOENCODING']='utf-8'
sys.path.insert(0,str(pathlib.Path(__file__).parent/'libs'))
import ctranslate2,sentencepiece
src=sentencepiece.SentencePieceProcessor(model_file='work/model/src.spm.model')
tgt=sentencepiece.SentencePieceProcessor(model_file='work/model/tgt.spm.model')
model=ctranslate2.Translator('work/model',device='cpu',compute_type='int8',intra_threads=6,inter_threads=2)
terms=json.loads(pathlib.Path('work/terms.json').read_text(encoding='utf8'))
token=re.compile(r'(<[^>]+>|\{[^}]+\}|\[[^\]]+\]|%\d*\.?\d*[sdif]|\r?\n|https?://\S+)')
def parts(s): return token.split(s)
allparts=[]
for term in terms:
    if term['key'].split('/')[0] in ('AUDIO_FILES','Assets'):continue
    for i,p in enumerate(parts(term['langs'][0])):
        p=p.strip()
        if i%2==0 and re.search('[a-zA-Z]',p) and p not in allparts: allparts.append(p)
dest=pathlib.Path('work/translations.json')
done=json.loads(dest.read_text(encoding='utf8')) if dest.exists() else {}
pending=[p for p in allparts if p not in done]
pending.sort(key=lambda x:len(x))
print('UNIQUE',len(allparts),'PENDING',len(pending),flush=True)
start=time.monotonic()
for pos in range(0,len(pending),64):
    batch=pending[pos:pos+64]
    results=model.translate_batch([src.encode(p,out_type=str) for p in batch],beam_size=4,max_batch_size=32,no_repeat_ngram_size=3,repetition_penalty=1.1,max_decoding_length=320)
    for p,r in zip(batch,results):
        out=tgt.decode(r.hypotheses[0])
        # Collapse a common short-label repetition in this model.
        words=out.split()
        if len(words)>1 and all(w==words[0] for w in words):out=words[0]
        done[p]=out
    dest.write_text(json.dumps(done,ensure_ascii=False,indent=2),encoding='utf8')
    if pos%256==0: print('PROGRESS',min(pos+64,len(pending)),len(pending),'SECONDS',round(time.monotonic()-start),flush=True)
print('COMPLETE',len(done),'SECONDS',round(time.monotonic()-start),flush=True)
