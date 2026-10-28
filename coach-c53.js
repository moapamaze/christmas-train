import {mountFrameJViewer} from './framej3d.js';
import {getModelData} from './model-data.js';
import {buildBrakeDetailC53} from './coach-brake-truck.js?v=C53-V2';
const config=JSON.parse(document.querySelector('#c53-view-data').textContent);
const host=document.querySelector('#c53-model'),status=document.querySelector('#c53-model-status');
let viewer,request=0;
async function show(index){
  const token=++request,item=config.models[index];
  status.textContent='Loading '+item.label.toLowerCase()+'…';
  try{
    const model=item.file==='model-nominal.json.gz'?await buildBrakeDetailC53():await getModelData(new URL('./assets/coach-brake-c53/'+item.file,import.meta.url));
    if(token!==request)return;
    viewer?.dispose();
    viewer=mountFrameJViewer(host,{modelData:model,title:'C5.3 · '+item.label,badge:config.badge,groupControls:true,note:config.note});
    document.querySelectorAll('[data-c53-state]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.c53State)===index)));
    status.textContent=item.label+' · development geometry; component qualification remains open';
  }catch(error){
    if(token!==request)return;
    status.textContent='The CAD model could not load. Drawings and downloadable CAD remain available.';
  }
}
document.querySelectorAll('[data-c53-state]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.c53State))));
show(0);
