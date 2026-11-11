import json,math
SEEDS=(11,23,37,53)
def run(seed,mode="triad",gain=.07,shuffle=False,offset=0.,local=0.):
 m=[[1+((seed+7*r+3*i)%11)/20 for i in range(27)] for r in range(3)]
 p=[[2*math.pi*((17*seed+11*r+7*i)%101)/101+offset for i in range(27)] for r in range(3)]
 for t in range(12):
  for i in range(27):
   a=((7*(26-i if shuffle else i)+seed)%27)/27
   w=gain*(.5+a)
   if mode=="triad": f=w*math.sin(p[1][i]+p[2][i]-2*p[0][i])
   elif mode=="pair": f=w*(math.sin(p[1][i]-p[0][i])+math.sin(p[2][i]-p[0][i]))/2
   else: f=0.
   f=max(-.035,min(.035,f))
   if local and i==7: f+=local
   m[0][i]+=f;m[1][i]-=f/2;m[2][i]-=f/2
  for r in range(3):
   for i in range(27):p[r][i]+=.002*(r+1)
 return m
def l1(a,b):return sum(abs(a[r][i]-b[r][i]) for r in range(3) for i in range(27))
def projection(m):return [sum(m[r][i] for r in range(3)) for i in range(27)]
def mae(m,seed):return sum(abs(m[0][i]-(1+((seed+3*i)%11)/20)) for i in range(27))/27
def check(seed):
 a=run(seed);b=run(seed,"pair");z=run(seed,"none");sh=run(seed,shuffle=True);ph=run(seed,offset=1.7);loc=run(seed,local=.005)
 tests={"replay":a==run(seed),"mass":max(abs(x-y) for x,y in zip(projection(a),projection(z)))<1e-11,"phase":l1(a,ph)<1e-10,"noop":z==run(seed,gain=0),"shuffle":l1(a,sh)>1e-5,"triad_pair":l1(a,b)>1e-5,"projection":max(abs(x-y) for x,y in zip(projection(a),projection(b)))<1e-11,"local":sum(abs(loc[r][i]-a[r][i]) for r in range(3) for i in range(27) if i!=7)<1e-10,"positive":min(x for row in a for x in row)>0,"forecast_negative":mae(z,seed)<mae(a,seed)}
 return {"seed":seed,"tests":tests,"l1_triad_pair":l1(a,b),"l1_shuffle":l1(a,sh),"mae_triad":mae(a,seed),"mae_uncoupled":mae(z,seed)}
if __name__=="__main__":
 print(json.dumps({"issue":425,"results":[check(s) for s in SEEDS]},sort_keys=True,indent=2))
