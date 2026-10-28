import {loadLT44} from './lt44-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=tender-r1';
const host=document.querySelector('[data-lt44-view]');let viewer,seq=0,current='exterior';
const notes={exterior:'Retained LT43.1 exterior. Combined power package and final tender dimensions remain open.',frame:'Orange outlines identify proposed load-transfer regions from the low couplings into the two main rails. They are not selected steel sections.',fit:'Red is the stock HT150DQV envelope; green is the existing insulated equipment bay. The package is 676 mm too tall before service clearance or generator/compressor additions.',interfaces:'Six proposed fixed connection zones. Colored blocks mark boundaries, not completed hoses. Hydraulic loops end at the locomotive; coach AC continues toward the rear.'};
async function show(view=current){
 current=view;const n=++seq;host.dataset.ready='false';host.dataset.view=view;
 host.querySelectorAll('[data-camera]').forEach(b=>b.disabled=true);
 host.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===view)));
 host.querySelector('[data-status]').textContent='Loading '+(view==='whole'?'train arrangement':'tender')+'…';
 viewer?.dispose();host.querySelector('[data-model]').replaceChildren();host.querySelector('[data-render-options]').replaceChildren();
 try{
  const m=await loadLT44(view);if(n!==seq)return;
  viewer=mountAssemblyModel(host.querySelector('[data-model]'),{modelData:m,title:m.title,badge:'DESIGN DEVELOPMENT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-2,.8],note:notes[view]});
  const options=host.querySelector('[data-model]>.actions');if(options)host.querySelector('[data-render-options]').append(options);
  host.querySelector('[data-status]').textContent=notes[view];host.dataset.ready='true';
  host.querySelectorAll('[data-camera]').forEach(b=>b.disabled=false);
 }catch(e){host.querySelector('[data-status]').textContent='The view could not load. Use Reload view below. '+e.message;}
}
if(host){
 host.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>show(b.dataset.mode));
 host.querySelector('[data-reload]').onclick=()=>show();
 const actions={iso:['[data-view="orbit"]','[data-action="iso"]'],side:['[data-view="side"]','[data-action="side"]'],top:['[data-view="top"]','[data-action="top"]'],fit:['[data-action="reset"]','[data-action="all"]'],plus:['[data-action="zoom-in"]','[data-action="plus"]'],minus:['[data-action="zoom-out"]','[data-action="minus"]']};
 host.querySelectorAll('[data-camera]').forEach(b=>b.onclick=()=>{for(const selector of actions[b.dataset.camera]){const target=host.querySelector('[data-model] '+selector);if(target){target.click();break;}}});
 show();
}
