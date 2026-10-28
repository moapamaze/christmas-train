import {loadLT13,curveEvidence} from './lt13-model.js';
import {mountCanvasModel} from './lt12-canvas.js';
const host=document.querySelector('#lt3-viewer'),status=document.querySelector('#model-status');
let api,revision=0;
function showSheet(code){document.querySelectorAll('[data-drawing]').forEach(f=>f.hidden=f.dataset.drawing!==code);document.querySelectorAll('[data-sheet]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.sheet===code)));}
document.querySelectorAll('[data-sheet]').forEach(b=>b.addEventListener('click',()=>showSheet(b.dataset.sheet)));showSheet('LT13-A01');
async function show(){
 const request=++revision;api?.dispose();api=null;host.textContent='Loading curve CAD…';status.textContent='Loading…';
 const r=document.querySelector('#radius').value,radius=r==='straight'?null:Number(r),hand=Number(document.querySelector('#hand').value),dz=Number(document.querySelector('#travel').value),kind=document.querySelector('#focus').value;
 document.querySelector('#hand').disabled=radius===null;
 try{
  const [data,ev]=await Promise.all([loadLT13(kind,radius,hand,dz),curveEvidence()]);if(request!==revision)return;
  const c=ev.cases.find(c=>c.radius_mm===radius&&c.hand===(radius===null?0:hand)&&c.dz_mm===dz);
  document.querySelector('#case-result').textContent=c.positive_intersections.length?`${c.positive_intersections.length} intersecting CAD part pairs in this whole-locomotive sample. Red marks involved parts. Wheel and tire-ring pairs are counted separately.`:'No intersections in the specified moving-to-fixed pairs at this sampled position. This does not approve a turning radius.';
  const list=document.querySelector('#clash-list');list.replaceChildren();
  for(const h of c.positive_intersections){const li=document.createElement('li');li.textContent=h.moving+' / '+h.fixed;list.appendChild(li);}
  if(!document.querySelector('#compatibility').checked){
   try{
    const {mountFrameJViewer}=await import('./lt11-viewer3d.js');if(request!==revision)return;
    api=mountFrameJViewer(host,{modelData:data,title:'LT13 curve clearance',badge:'CONDITIONAL PLACEMENT',groupControls:true,note:'Red: sampled collision. Motion mechanism is not designed. Dimensions in inches.'});
    if(api.getState().fallback){api.dispose();api=null;}
    else {const options=host.querySelector('.coach3d-options');if(options)options.hidden=true;host.querySelector('canvas')?.addEventListener('webglcontextlost',()=>{document.querySelector('#compatibility').checked=true;show();},{once:true});}
   }catch(e){api?.dispose();api=null;}
  }
  if(!api){api=mountCanvasModel(host,data);document.querySelector('#compatibility').checked=true;status.textContent='Compatibility 3D · '+data.parts.length+' parts';}else status.textContent='3D · '+data.parts.length+' parts';
 }catch(e){if(request!==revision)return;status.textContent='Model unavailable';host.textContent=e.message;const retry=document.createElement('button');retry.textContent='Retry';retry.addEventListener('click',show);host.appendChild(retry);}
}
document.querySelectorAll('#radius,#hand,#travel,#focus,#compatibility').forEach(e=>e.addEventListener('change',show));show();
