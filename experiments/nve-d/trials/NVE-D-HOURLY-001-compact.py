import hashlib
MASK=(1<<64)-1
raws=['(?):(?)::(?):(?)::|#|::(?):(?)::(?):(?)::#::(?)','|{(a<b):(c>d)::(e<d):(f>g)}| :: |x| :: |{(?):(?)::(?):(?)}|','.......←.......#.......→.......']
H=['left_fixture','right_fixture','paired_fixture']
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
def tick(s,salt,depth,h):
 for d in range(depth+1):
  a=(s*6364136223846793005+1442695040888963407+salt+d)&MASK
  b=((s<<7)|(s>>57))&MASK
  s=(a^salt) if h==H[0] else ((a+b)&MASK if h==H[1] else a^b^salt)
 return s
def ref(s,salt,depth,h):
 for d in range(depth+1):
  a=(6364136223846793005*s+1442695040888963407+salt+d)%(1<<64)
  b=((s%(1<<57))*128+(s>>57))%(1<<64)
  s=(a^salt) if h==H[0] else ((a+b)%(1<<64) if h==H[1] else a^b^salt)
 return s
runs=gens=equal=corrupt=0
for raw in raws:
 for h in H:
  for depth in [0,1,3]:
   for seed in [7,31,97]:
    for n in [250,1000,2500,5000,10000]:
     salt=int(sha(raw)[:16],16)
     s=int.from_bytes(hashlib.sha256(f'{sha(raw)}|{seed}|{depth}|{h}'.encode()).digest()[:8],'big')
     r=s
     for _ in range(n//2):s=tick(s,salt,depth,h)
     checkpoint=s
     for _ in range(n-n//2):s=tick(s,salt,depth,h)
     for _ in range(n):r=ref(r,salt,depth,h)
     bad=checkpoint^1
     for _ in range(n-n//2):bad=tick(bad,salt,depth,h)
     equal+=s==r;corrupt+=bad!=s;runs+=1;gens+=n
print({'runs':runs,'generations':gens,'independent_reference_equal':equal,'corrupt_checkpoints_detected':corrupt})
