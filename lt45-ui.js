import {loadLT45} from './lt45-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=tender-r1';
const host=document.querySelector('[data-lt45-view]');let viewer,seq=0,current='exterior';
const notes={exterior:'Retained coal-style exterior. The existing AIE engine and separate Kubota generator are shown in Cutaway. Vent openings and service-panel details await the selected generator drawing.',cutaway:'Existing AIE engine and hydraulic pump on the left; 35 kW Kubota generator space on the right. Brown is an available-space reservation; exact package fit, rating and weight remain to be confirmed.',equipment:'Equipment layout with the 1700 × 800 × 1000 mm generator procurement envelope in brown. The generator box reserves space for 35 kW continuous output; the compressor and electrical panel are space provisions.',service:'Green outlines mark the 600 mm-wide, restricted-height maintenance strip. Brown marks the generator procurement envelope. These are reservations, not verified OEM service or removal clearances.',connections:'Retained LT44 fixed service zones: hydraulics toward the locomotive; AC power toward the coaches; air and controls at both ends. Actual moving hoses and cables still need routing.'};
async function show(view=current){
 current=view;const n=++seq;host.dataset.ready='false';host.dataset.view=view;
 host.querySelectorAll('[data-camera]').forEach(b=>b.disabled=true);
 host.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===view)));
 host.querySelector('[data-status]').textContent='Loading '+(view==='whole'?'train arrangement':'tender')+'…';
 viewer?.dispose();host.querySelector('[data-model]').replaceChildren();host.querySelector('[data-render-options]').replaceChildren();
 try{
  const m=await loadLT45(view);if(n!==seq)return;
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
