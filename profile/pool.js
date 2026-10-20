(() => {
  const canvas = document.getElementById('pool');
  const ctx = canvas.getContext('2d', { alpha: false });
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let w = 0, h = 0, dpr = 1, t = 0, raf = 0;
  const ripples = [];
  const pointer = { x: 0.5, y: 0.48, active: false };
  function resize() { dpr = Math.min(devicePixelRatio || 1, 2); w = innerWidth; h = innerHeight; canvas.width = w*dpr; canvas.height = h*dpr; canvas.style.width = w+'px'; canvas.style.height = h+'px'; ctx.setTransform(dpr,0,0,dpr,0,0); }
  function addRipple(x,y,power=1){ripples.push({x,y,r:0,life:1,power});if(ripples.length>12)ripples.shift()}
  addEventListener('resize', resize, {passive:true}); resize();
  addEventListener('pointermove', e => { pointer.x=e.clientX/w; pointer.y=e.clientY/h; pointer.active=true; if(Math.random()<.12) addRipple(e.clientX,e.clientY,.36); }, {passive:true});
  addEventListener('pointerdown', e => addRipple(e.clientX,e.clientY,1.3), {passive:true});
  function draw(){
    t += reduce ? .002 : .009;
    const g=ctx.createLinearGradient(0,0,w,h); g.addColorStop(0,'#3b0a15'); g.addColorStop(.42,'#8e1727'); g.addColorStop(1,'#21050e'); ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    const cell = Math.max(9, Math.min(17, Math.round(w/100)));
    for(let y=-cell;y<h+cell;y+=cell){ for(let x=-cell;x<w+cell;x+=cell){
      const nx=x/w, ny=y/h; let wave=Math.sin(nx*24+ny*8-t*2.4)*3+Math.sin(ny*31-nx*10+t*1.7)*2+Math.sin((nx+ny)*56-t*3.7)*1.1;
      wave += Math.sin(nx*9-ny*19+t)*2;
      for(const q of ripples){const dx=x-q.x,dy=y-q.y,dist=Math.hypot(dx,dy);wave += Math.sin(dist*.09-q.r*.09)*q.power*Math.max(0,1-dist/520)*4}
      const shade=Math.max(0,Math.min(1,.5+wave/15)); const hi=Math.max(0,Math.sin(nx*22+ny*17+t*1.3+wave*.12));
      ctx.fillStyle=`rgba(${117+Math.floor(shade*85)},${9+Math.floor(shade*18)},${24+Math.floor(shade*23)},.38)`; ctx.fillRect(x+wave*.4,y+wave*.22,cell+1,cell+1);
      if(hi>.78){ctx.fillStyle=`rgba(255,${80+Math.floor(hi*90)},${95+Math.floor(hi*80)},${(hi-.78)*.32})`;ctx.fillRect(x+wave,y+wave*.5,cell*.7,1)}
    }}
    ctx.globalCompositeOperation='screen'; const glow=ctx.createRadialGradient(pointer.x*w,pointer.y*h,0,pointer.x*w,pointer.y*h,Math.min(w,h)*.42); glow.addColorStop(0,'rgba(255,80,86,.13)');glow.addColorStop(1,'rgba(255,30,50,0)');ctx.fillStyle=glow;ctx.fillRect(0,0,w,h);ctx.globalCompositeOperation='source-over';
    for(const q of ripples){q.r += reduce?1.4:4.6;q.life -= reduce?.006:.016} for(let i=ripples.length-1;i>=0;i--)if(ripples[i].life<=0)ripples.splice(i,1);
    raf=requestAnimationFrame(draw);
  }
  draw();
})();
