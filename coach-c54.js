import {mountFrameJViewer} from './framej3d.js';
import {getModelData} from './model-data.js';
import {buildBrakeDetailC54,addBrakeC54Shortcuts} from './coach-brake-truck.js?v=C54-R0';
const config=JSON.parse(document.querySelector('#c54-view-data').textContent);
const host=document.querySelector('#c54-model'),status=document.querySelector('#c54-model-status');
let viewer,request=0;
async function show(index){
  const token=++request,item=config.models[index];
  status.textContent='Loading '+item.label.toLowerCase()+'…';
  try{
    const model=item.file==='model-nominal.json.gz'?await buildBrakeDetailC54():await getModelData(new URL('./assets/coach-brake-c54/'+item.file,import.meta.url));
    if(token!==request)return;
    viewer?.dispose();
    viewer=mountFrameJViewer(host,{modelData:model,title:'C5.4 · '+item.label,badge:config.badge,groupControls:true,note:config.note});
    addBrakeC54Shortcuts(host,viewer,model);
    document.querySelectorAll('[data-c54-state]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.c54State)===index)));
    status.textContent=item.label+' · one development unit; fitted assembly qualification remains open';
  }catch(error){
    if(token!==request)return;
    status.textContent='The CAD model could not load. Drawings and downloadable CAD remain available.';
    console.error(error);
  }
}
document.querySelectorAll('[data-c54-state]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.c54State))));
show(0);
