import {mountFrameJViewer} from './framej3d.js';
import {getModelData} from './model-data.js';
import {buildBrakeDetailC55,addBrakeC55Shortcuts} from './coach-brake-truck.js?v=C55-R0';
const config=JSON.parse(document.querySelector('#c55-view-data').textContent);
const host=document.querySelector('#c55-model'),status=document.querySelector('#c55-model-status');
let viewer,request=0;
async function show(index){
  const token=++request,item=config.models[index];
  status.textContent='Loading '+item.label.toLowerCase()+'…';
  try{
    const model=item.file==='model-nominal.json.gz'?await buildBrakeDetailC55():await getModelData(new URL('./assets/coach-brake-c55/'+item.file,import.meta.url));
    if(token!==request)return;
    viewer?.dispose();
    viewer=mountFrameJViewer(host,{modelData:model,title:'C5.5 · '+item.label,badge:config.badge,groupControls:true,note:config.note});
    addBrakeC55Shortcuts(host,viewer,model);
    document.querySelectorAll('[data-c55-state]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.c55State)===index)));
    status.textContent=item.label+' · one development installation; purchased-part fit remains open';
  }catch(error){
    if(token!==request)return;
    status.textContent='The model could not load. Drawing and CAD downloads remain available.';
    console.error(error);
  }
}
document.querySelectorAll('[data-c55-state]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.c55State))));
show(0);
