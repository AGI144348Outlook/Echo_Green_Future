"""Offline synthetic controls for the public-source exact-pin fetch launcher."""
import io, importlib.util, pathlib
p=pathlib.Path(__file__).with_name('F-001-PUBLIC-FETCH-REPLAY-413.py')
spec=importlib.util.spec_from_file_location('fetch413',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Resp(io.BytesIO):
 def __init__(self,data,url):super().__init__(data);self.url=url
 def geturl(self):return self.url
class Opener:
 def __init__(self,data,final=None):self.data=data;self.final=final
 def __call__(self,url,timeout=0):return Resp(self.data,self.final or url)
def rejects(fn):
 try:fn();return False
 except ValueError:return True
b=b'fixed synthetic public bytes';pin=m.blob_hash(b);url=m.raw_url(m.TAM_REPO,m.TAM_COMMIT,'Article 1 Hacksilber')
checks={
 'valid_bytes':m.fetch_verified(url,pin,Opener(b))==b,
 'pin_tamper':rejects(lambda:m.fetch_verified(url,pin,Opener(b'altered'))),
 'redirect':rejects(lambda:m.fetch_verified(url,pin,Opener(b,final='https://elsewhere.example/x'))),
 'disallowed_host':rejects(lambda:m.fetch_verified('https://elsewhere.example/x',pin,Opener(b))),
 'size_cap':rejects(lambda:m.fetch_verified(url,pin,Opener(b'x'*(m.MAX_BYTES+1)))),
 'space_encoded':'Article%201%20Hacksilber' in url,
 'eight_pins':len(m.PINS)==8 and len(set(m.PINS.values()))==8,
 'pinned_runner':len(m.RUNNER_BLOB)==40 and len(m.SCANNER_BLOB)==40,
}
for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
assert all(checks.values()),checks
print('PASS',len(checks),'of',len(checks),'offline synthetic fetch controls')
