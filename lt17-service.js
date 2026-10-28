import {loadLT17} from './lt17-model.js?v=LT17';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=CC2';
import {transformModel,rotation} from './drawbar-motion.js';
const host=document.querySelector('[data-retention-view]');let viewer,seq=0;
const messages={assembled:'Installed candidate at straight track, nominal height and zero roll. Gold parts retain the rocker pin; teal/grey parts carry or guide the assembly.',separated:'Retainers are separated for identification. These display offsets are not verified removal paths. The spring must be unloaded with an engineered support arrangement before service.',withdrawn:'Pin translated 87 mm in the longitudinal direction. The checked solid sweep clears the modeled parts after the retainers are removed. This is one withdrawal step; tool access and complete extraction remain open.'};
async function show(mode){const own=++seq;viewer?.dispose();host.replaceChildren();document.querySelector('[data-service-status]').textContent='Loading the rocker-pin detail…';try{let m=await loadLT17('retention');if(own!==seq)return;
 m.parts=m.parts.filter(p=>p.id.startsWith('L16-')&&/(PIN|CLEVIS|ROCKER|CATCH)/.test(p.id));
 m.parts=m.parts.map(p=>({...p,color:/PIN/.test(p.id)?'#d6a64d':/ROCKER/.test(p.id)?'#568e80':'#9caeb4'}));m.compatibility_camera=[-.7,-.22];
 if(mode!=='assembled')m.parts=m.parts.map(p=>{let offset=null;if(p.id.endsWith('PIN-NUT'))offset=[50,-130,0];if(p.id.endsWith('PIN-WASHER'))offset=[20,-90,0];if(p.id.endsWith('PIN-COTTER'))offset=[70,-170,0];if(mode==='withdrawn'&&p.id.endsWith('-PIN'))offset=[-87,0,0];return offset?transformModel({parts:[p]},rotation(),offset.map(n=>n/25.4),[0,0,0]).parts[0]:p});
 m.groups=m.groups.filter(g=>m.parts.some(p=>p.group===g.id));
 viewer=mountAssemblyModel(host,{modelData:m,title:'LT17 · one rocker pin',badge:'DEVELOPMENT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-1.8,.9],note:messages[mode]});
 document.querySelector('[data-service-status]').textContent=messages[mode];document.querySelectorAll('[data-service-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.serviceMode===mode)));
 }catch(e){document.querySelector('[data-service-status]').textContent='Model could not load: '+e.message;}}
document.querySelectorAll('[data-service-mode]').forEach(b=>b.onclick=()=>show(b.dataset.serviceMode));show('assembled');
