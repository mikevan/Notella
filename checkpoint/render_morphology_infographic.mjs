import fs from 'node:fs/promises';
const endpoint='http://127.0.0.1:9337';
const url='file:///C:/workspace/Notella/docs/infographics/semantic-morphology-evolution.html';
const target=await (await fetch(endpoint+'/json/new?'+encodeURIComponent(url),{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true})});
let sequence=0;const pending=new Map();const errors=[];
ws.addEventListener('message',event=>{const message=JSON.parse(event.data);if(message.id){const task=pending.get(message.id);pending.delete(message.id);if(message.error)task.reject(Error(JSON.stringify(message.error)));else task.resolve(message.result)}else if(message.method==='Runtime.exceptionThrown')errors.push(message.params.exceptionDetails.text)});
function call(method,params={}){return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))})}
async function evaluate(expression){const result=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.exceptionDetails)throw Error(result.exceptionDetails.text);return result.result.value}
await call('Page.enable');await call('Runtime.enable');await call('Emulation.setDeviceMetricsOverride',{width:1280,height:1000,deviceScaleFactor:1,mobile:false});
await evaluate('document.fonts.ready.then(()=>true)');
const desktop=await evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),title:document.title})');
if(desktop.scrollWidth>desktop.width||!desktop.images)throw Error('Desktop overflow or failed image');
for(const step of [0,1,2,3]){await evaluate(`document.querySelector('[data-step="${step}"]').click()`);const result=await evaluate('({level:document.getElementById("level").textContent,origins:document.getElementById("origins").textContent})');if(result.level!==(step===2?'contextual':'critical'))throw Error('State transition failed');}
await evaluate(`document.querySelector('[data-step="2"]').click()`);
const metrics=await call('Page.getLayoutMetrics');const content=metrics.cssContentSize??metrics.contentSize;
const full=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1280,height:Math.ceil(content.height),scale:1}});
await fs.writeFile('docs/infographics/semantic-morphology-evolution.png',Buffer.from(full.data,'base64'));
const top=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1280,height:1000,scale:1}});
await fs.writeFile('docs/infographics/semantic-morphology-evolution-preview.png',Buffer.from(top.data,'base64'));
const middleY=await evaluate('document.getElementById("evidence").offsetTop');
const middle=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:middleY,width:1280,height:1100,scale:1}});
await fs.writeFile('docs/infographics/semantic-morphology-evolution-results-preview.png',Buffer.from(middle.data,'base64'));
await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
const mobile=await evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})');if(mobile.scrollWidth>mobile.width)throw Error('Mobile overflow');
await call('Emulation.setDeviceMetricsOverride',{width:320,height:844,deviceScaleFactor:1,mobile:true});const narrow=await evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})');if(narrow.scrollWidth>narrow.width)throw Error('Narrow overflow');
const qa={desktop,mobile,narrow,interaction:'All four illustrative states passed',runtimeErrors:errors};if(errors.length)throw Error(JSON.stringify(errors));
await fs.writeFile('docs/infographics/semantic-morphology-evolution-qa.json',JSON.stringify(qa,null,2)+'\n');console.log(JSON.stringify(qa));
await call('Page.close');ws.close();
