const logEl=document.querySelector('#log'), statusEl=document.querySelector('#pyStatus'), progress=document.querySelector('#progress');
const log=s=>{logEl.textContent+='\n'+s;logEl.scrollTop=logEl.scrollHeight};
const canvas=document.querySelector('#grid'),ctx=canvas.getContext('2d');
function grid(){const d=devicePixelRatio||1,w=innerWidth,h=innerHeight;canvas.width=w*d;canvas.height=h*d;canvas.style.width=w+'px';canvas.style.height=h+'px';ctx.setTransform(d,0,0,d,0,0);ctx.clearRect(0,0,w,h);ctx.strokeStyle='#e8e8e8';ctx.lineWidth=1;for(let x=0;x<w;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke()}for(let y=0;y<h;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke()}}
addEventListener('resize',grid);grid();
let pyodide, dirHandle=null;
(async()=>{try{pyodide=await loadPyodide();statusEl.textContent='Pyodide: ready';log('Python substrate ready.')}catch(e){statusEl.textContent='Pyodide: unavailable';log(String(e))}})();
async function chooseDir(){if(!window.showDirectoryPicker){log('Directory picker is not supported here; extraction can still be inspected in-browser.');return null}dirHandle=await showDirectoryPicker({mode:'readwrite'});log('Workspace: '+dirHandle.name);return dirHandle}
document.querySelector('#chooseDir').onclick=()=>chooseDir().catch(e=>log(e.message));
document.querySelector('#clearLog').onclick=()=>logEl.textContent='Ready.';
async function ensurePath(root,parts){let d=root;for(const p of parts)d=await d.getDirectoryHandle(p,{create:true});return d}
async function writeEntry(root,path,blob){const parts=path.split('/').filter(Boolean),name=parts.pop();if(!name)return;const d=await ensurePath(root,parts),h=await d.getFileHandle(name,{create:true}),w=await h.createWritable();await blob.stream().pipeTo(w)}
async function unzip(file){
 if(!('DecompressionStream' in window)){log('This browser lacks native ZIP decompression. Pyodide fallback will be added next.');return}
 log('Selected '+file.name+' ('+(file.size/1048576).toFixed(1)+' MB).');
 if(!dirHandle) await chooseDir(); if(!dirHandle)return;
 // ZIP is intentionally not loaded wholly into JS memory. Native ZIP directory parsing is the next layer.
 log('Workspace granted. Large-file path is ready; ZIP directory parser is the next component.');
 progress.value=10;
}
const input=document.querySelector('#zipInput');input.onchange=()=>input.files[0]&&unzip(input.files[0]).catch(e=>log(e.stack||e));
const drop=document.querySelector('#drop');['dragenter','dragover'].forEach(n=>drop.addEventListener(n,e=>{e.preventDefault()}));drop.ondrop=e=>{e.preventDefault();const f=e.dataTransfer.files[0];if(f)unzip(f).catch(x=>log(x.stack||x))};
if('serviceWorker'in navigator)navigator.serviceWorker.register('./sw.js');