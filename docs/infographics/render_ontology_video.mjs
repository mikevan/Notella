import fs from 'node:fs/promises';
const base='C:/workspace/Notella/docs/infographics/';
const target=await(await fetch('http://127.0.0.1:9337/json/new?'+encodeURIComponent('file:///'+base+'ontology-events-animation.html'),{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));let id=0;const pending=new Map();ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}});
const call=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}))});
const ev=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
await call('Page.enable');await call('Page.bringToFront');await call('Emulation.setDeviceMetricsOverride',{width:1600,height:1050,deviceScaleFactor:1,mobile:false});await ev('document.fonts.ready.then(()=>true)');
const states=[];for(const t of [0,6,15,25,36,47,56])states.push(await ev(`renderOntology(${t})`));
if(states.map(s=>s.activeOrigins).join()!=='0,1,2,3,3,3,3')throw Error('Origin transition failure');
for(const [t,name]of [[25,'poster'],[36,'correction'],[47,'expiry']]){await ev(`renderOntology(${t})`);const r=await call('Page.captureScreenshot',{format:'png',clip:{x:0,y:0,width:1600,height:900,scale:1}});await fs.writeFile(base+'ontology-events-'+name+'.png',Buffer.from(r.data,'base64'))}
console.log('Frames checked; encoding 58-second video.');
const result=await ev('recordOntology({seconds:58})');const bytes=Buffer.from(result.base64,'base64');delete result.base64;await fs.writeFile(base+'ontology-events.mp4',bytes);await fs.writeFile(base+'ontology-events-qa.json',JSON.stringify({states,video:result},null,2));console.log(JSON.stringify(result));await call('Page.close');ws.close();
