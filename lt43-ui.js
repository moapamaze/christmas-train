import {loadTenderPresentation} from './lt43-tender-body.js?v=1';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=tender-r1';
const host=document.querySelector('[data-lt43-view]');let viewer,seq=0,current='exterior';
const notes={exterior:'Insulated coal-tender exterior. Truck geometry is a retained coach reference; tender ratings remain open.',cutaway:'Roof and near-side panels removed. Machinery shown is the earlier two-engine layout; the combined power unit is being selected separately.',insulation:'Protected 50 mm lining and removable roof supports. Thermal, acoustic and ventilation performance remain to be verified.',whole:'Locomotive, enclosed tender and first coach. Four coaches remain in the train; this is a straight visual arrangement.'};
async function show(view=current){
 current=view;const n=++seq;host.dataset.ready='false';host.dataset.view=view;
 host.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===view)));
 host.querySelector('[data-status]').textContent='Loading '+(view==='whole'?'train arrangement':'tender')+'…';
 viewer?.dispose();host.querySelector('[data-model]').replaceChildren();host.querySelector('[data-render-options]').replaceChildren();
 try{
  const m=await loadTenderPresentation(view);if(n!==seq)return;
  viewer=mountAssemblyModel(host.querySelector('[data-model]'),{modelData:m,title:m.title,badge:'DESIGN DEVELOPMENT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-2,.8],note:notes[view]});
  const options=host.querySelector('[data-model]>.actions');if(options)host.querySelector('[data-render-options]').append(options);
  host.querySelector('[data-status]').textContent=notes[view];host.dataset.ready='true';
 }catch(e){host.querySelector('[data-status]').textContent='The view could not load. Use Reload view below. '+e.message;}
}
if(host){
 host.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>show(b.dataset.mode));
 host.querySelector('[data-reload]').onclick=()=>show();
 const actions={iso:['[data-view="orbit"]','[data-action="iso"]'],side:['[data-view="side"]','[data-action="side"]'],top:['[data-view="top"]','[data-action="top"]'],fit:['[data-action="reset"]','[data-action="all"]'],plus:['[data-action="zoom-in"]','[data-action="plus"]'],minus:['[data-action="zoom-out"]','[data-action="minus"]']};
 host.querySelectorAll('[data-camera]').forEach(b=>b.onclick=()=>{for(const selector of actions[b.dataset.camera]){const target=host.querySelector('[data-model] '+selector);if(target){target.click();break;}}});
 show();
}
