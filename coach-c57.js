import {mountFrameJViewer} from './framej3d.js';
import {getModelData} from './model-data.js';
import {buildBrakeDetailC57,buildBrakeTruckC57,addBrakeC57Shortcuts} from './coach-brake-truck.js?v=C57-R0';
const config=JSON.parse(document.querySelector('#c57-view-data').textContent);
const host=document.querySelector('#c57-model'),status=document.querySelector('#c57-model-status');
let viewer,request=0;
async function show(index){
  const token=++request,item=config.models[index];
  if(!item)return;
  status.textContent='Loading '+item.label.toLowerCase()+'…';
  host.setAttribute('aria-busy','true');
  try{
    const model=item.kind==='truck'?await buildBrakeTruckC57():item.kind==='detail'?await buildBrakeDetailC57():await getModelData(new URL('./assets/coach-brake-c57/'+item.file,import.meta.url));
    if(token!==request)return;
    viewer?.dispose();
    viewer=mountFrameJViewer(host,{modelData:model,title:'C5.7 · '+item.label,badge:config.badge,groupControls:true,note:item.note||config.note});
    addBrakeC57Shortcuts(host,viewer,model);
    document.querySelectorAll('[data-c57-state]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.c57State)===index)));
    status.textContent=item.label+' · one brake installation under development';
  }catch(error){
    if(token!==request)return;
    status.textContent='The model could not load. The drawings and CAD downloads remain available below.';
    console.error(error);
  }finally{
    if(token===request)host.setAttribute('aria-busy','false');
  }
}
document.querySelectorAll('[data-c57-state]').forEach(button=>button.addEventListener('click',()=>show(Number(button.dataset.c57State))));
show(0);
