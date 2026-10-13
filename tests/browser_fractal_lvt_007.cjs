const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({headless:true,args:['--no-sandbox']});
  try {
    const page = await browser.newPage({viewport:{width:390,height:844}});
    const errors=[];page.on('pageerror',e=>errors.push(String(e)));
    await page.setContent(`<!doctype html><html><body>
      <button id="s1" onclick="changeScale(1)">1</button>
      <button id="s10" onclick="changeScale(10)">10</button>
      <button id="s1000" onclick="changeScale(1000)">1000</button>
      <button id="profile" onclick="toggleProfile()">profile</button>
      <button id="manifold" onclick="manifold()">manifold</button>
      <canvas id="grid" width="960" height="600"></canvas><div id="status"></div>
      <script>
      const fixture={S:[0.857204,-8.679167,0.915657],aleph:[0.9283698938043075,-3.1145833333333335,0],resh:[-0.49976804234157146,-1.2249999999999999,0.457828465534935]};
      const canvas=document.querySelector('#grid'),ctx=canvas.getContext('2d');
      const canonical=new Map([['core',[0,0,0]],['resultant',fixture.S],['glyph:aleph',fixture.aleph],['glyph:resh',fixture.resh]]);
      let scale=1,profile='scientific:H',depth=0;const audit=[];
      function project(p,s=scale){if(!(s>0))throw Error('invalid scale');return p.map(x=>x/s)}
      function unproject(p,s=scale){if(!(s>0))throw Error('invalid scale');return p.map(x=>x*s)}
      function draw(){ctx.clearRect(0,0,960,600);ctx.strokeStyle='#e3e8ee';for(let x=0;x<960;x+=30){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,600);ctx.stroke()}for(let y=0;y<600;y+=30){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(960,y);ctx.stroke()}for(const [id,p] of canonical){const q=project(p),x=480+q[0]*35,y=300-q[1]*35;ctx.beginPath();ctx.arc(x,y,id==='core'?8:6,0,Math.PI*2);ctx.fillStyle=id==='core'?'#dd542f':'#3256ba';ctx.fill()}document.querySelector('#status').textContent='Core: (0,0,0) · scale '+scale+' · NVE depth '+depth+' · Aleph profile '+profile}
      function changeScale(s){if(!(s>0))throw Error('invalid scale');scale=s;audit.push({op:'SCALE',s});draw()}
      function toggleProfile(){profile=profile==='scientific:H'?'scientific:He':'scientific:H';audit.push({op:'PROFILE',profile});draw()}
      function manifold(){depth++;audit.push({op:'MANIFOLD_INWARD',depth});draw()}
      draw();window.state=()=>({scale,profile,depth,canonical:[...canonical],audit:[...audit]});
      <\/script></body></html>`);
    const initial=await page.evaluate(()=>window.state());
    if(!initial || initial.canonical[0][1].some(x=>x!==0))throw Error('Origin invalid');
    for(const s of [10,1000,1]){await page.locator('#s'+s).click();if((await page.evaluate(()=>window.state().scale))!==s)throw Error('Scale '+s)}
    await page.locator('#profile').click();
    await page.locator('#manifold').click();
    const after=await page.evaluate(()=>window.state());
    if(after.profile!=='scientific:He'||after.depth!==1)throw Error('Controls did not change state');
    if(JSON.stringify(after.canonical)!==JSON.stringify(initial.canonical))throw Error('Canonical mutation');
    const pixel=await page.evaluate(()=>[...document.querySelector('canvas').getContext('2d').getImageData(480,300,1,1).data]);
    if(pixel[3]===0)throw Error('Canvas origin not painted');
    if(errors.length)throw Error(errors.join(' | '));
    await page.screenshot({path:'canvas_browser_007.png',fullPage:true});
    console.log('PASS: browser canvas paint, origin, three scales, profile, depth, canonical invariance; screenshot saved');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
