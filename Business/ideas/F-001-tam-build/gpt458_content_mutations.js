const fs=require('fs'),{audit}=require(process.argv[2]);
const base=fs.readFileSync(process.argv[3],'utf8').trimEnd().split('\n');
function t(name,f){const a=base.slice();f(a);let r;try{audit(a.join('\n')+'\n');r='ACCEPTED'}catch(e){r='REFUSED: '+e.message}console.log(name+' -> '+r)}
t('M1 proposal text replaced',a=>{const z=a[1].split('\t');z[4]='Keep unchanged; claim verified.';a[1]=z.join('\t')});
t('M2 quoted short_text replaced',a=>{const z=a[1].split('\t');z[3]='"something the source never said"';a[1]=z.join('\t')});
t('M3 section swapped to another allowed section',a=>{const z=a[1].split('\t');z[2]='§142';a[1]=z.join('\t')});
t('M4 extra tab column',a=>{a[1]=a[1]+'\tx'});
