import {loadLT11} from './lt11-model.js?v=lt11-r0';
import {mountCanvasModel} from './lt11-canvas.js?v=lt11-r0';
const host=document.querySelector('#lt3-viewer'),status=document.querySelector('#model-status');
let api,revision=0,current='exterior',software=false;
function showSheet(code){document.querySelectorAll('[data-drawing]').forEach(f=>f.hidden=f.dataset.drawing!==code);document.querySelectorAll('[data-sheet]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.sheet===code)));}
document.querySelectorAll('[data-sheet]').forEach(b=>b.addEventListener('click',()=>showSheet(b.dataset.sheet)));
showSheet('LT11-A01');
async function show(){
 const request=++revision;api?.dispose();api=null;host.textContent='Loading CAD geometry…';status.textContent='Loading…';
 document.querySelectorAll('[data-model]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.model===current)));
 try{
  const data=await loadLT11(current,document.querySelector('#exploded').checked);if(request!==revision)return;
  if(!software){
   try{
    const {mountFrameJViewer}=await import('./lt11-viewer3d.js');if(request!==revision)return;
    api=mountFrameJViewer(host,{modelData:data,title:'LT11 · '+document.querySelector('[data-model="'+current+'"]').textContent,badge:'PROPORTION CONCEPT',groupControls:true,note:'Nominal CAD · Viewer dimensions are inches; drawings use mm. Exploded offsets show separation, not an assembly path.'});
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
document.querySelectorAll('[data-model]').forEach(b=>b.addEventListener('click',()=>{current=b.dataset.model;const e=document.querySelector('#exploded');e.disabled=true;if(e.disabled)e.checked=false;show();}));
document.querySelector('#exploded').addEventListener('change',show);
document.querySelector('#compatibility').addEventListener('change',e=>{software=e.target.checked;show();});
show();
