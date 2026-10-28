import {loadCompressedModel,composeDT3,composeLTFrame} from './lt3-model.js?v=51';
import {mountCanvasModel} from './lt3-canvas.js?v=51';
const host=document.querySelector('#lt3-viewer'),status=document.querySelector('#model-status');
let api,revision=0,current='centre',software=false;
function showSheet(code){document.querySelectorAll('[data-drawing]').forEach(f=>f.hidden=f.dataset.drawing!==code);document.querySelectorAll('[data-sheet]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.sheet===code)));}
document.querySelectorAll('[data-sheet]').forEach(b=>b.addEventListener('click',()=>showSheet(b.dataset.sheet)));
showSheet('LT3-J01');
async function loadModel(kind){
 const data=await loadCompressedModel(new URL('./assets/locomotive-lt3/model.json.gz',import.meta.url));
 if(kind==='centre')data.parts=data.parts.filter(p=>p.id.startsWith('LT3-T1-')&&!/LT3-T1-(D|S|C)/.test(p.id));
 if(kind==='connection')data.parts=data.parts.filter(p=>p.id.startsWith('LT3-T1-'));
 if(kind==='body')data.parts=data.parts.filter(p=>!p.id.startsWith('LT3-T1-'));
 if(kind==='assembly'){
  const [frame,dt]=await Promise.all([loadCompressedModel(new URL('./assets/locomotive-lt2/model.json.gz',import.meta.url)),loadCompressedModel(new URL('./assets/drivetrain-dt3/model.json.gz',import.meta.url))]);
  composeDT3(composeLTFrame(data,frame),dt);
 }
 return data;
}
async function show(){
 const request=++revision;api?.dispose();api=null;host.textContent='Loading CAD geometry…';status.textContent='Loading…';
 document.querySelectorAll('[data-model]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.model===current)));
 try{
  const data=await loadModel(current);if(request!==revision)return;
  if(!software){
   try{
    const {mountFrameJViewer}=await import('./framej3d.js');if(request!==revision)return;
    api=mountFrameJViewer(host,{modelData:data,title:'LT3 · '+document.querySelector('[data-model="'+current+'"]').textContent,badge:'PRELIMINARY',groupControls:true,note:'Nominal CAD geometry · Viewer dimensions are inches. STEP and drawings use millimetres.'});
    if(api.getState().fallback){api.dispose();api=null;}
    else{
     host.querySelector('[data-action=reset]').textContent='Whole assembly';
     const options=host.querySelector('.coach3d-options');if(options)options.hidden=true;
     const link=host.querySelector('.coach3d-error a');if(link){link.href='#drawings';link.textContent='Drawings';}
     host.querySelector('canvas')?.addEventListener('webglcontextlost',()=>{software=true;show();},{once:true});
    }
   }catch(error){api?.dispose();api=null;}
  }
  if(!api){software=true;document.querySelector('#compatibility').checked=true;api=mountCanvasModel(host,data);status.textContent='Compatibility 3D · '+data.parts.length+' parts';}
  else status.textContent='3D · '+data.parts.length+' parts';
 }catch(error){
  if(request!==revision)return;status.textContent='Model unavailable';host.textContent='';
  const p=document.createElement('p');p.textContent=error.message;host.appendChild(p);
  const retry=document.createElement('button');retry.textContent='Retry model';retry.addEventListener('click',show);host.appendChild(retry);
 }
}
document.querySelectorAll('[data-model]').forEach(b=>b.addEventListener('click',()=>{current=b.dataset.model;show();}));
document.querySelector('#compatibility').addEventListener('change',e=>{software=e.target.checked;show();});
show();
