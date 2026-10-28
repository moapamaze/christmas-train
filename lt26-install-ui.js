import {loadInstallation,installationData} from './lt26-install-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=mobile-r1';
export async function mountLT26Installation(host){
 let kind=host.dataset.initialView||'whole',viewer,seq=0,disposed=false;
 const[,,a]=await installationData();if(disposed)return;
 const duties=[...new Map(a.cases.map(c=>[c.label,c.label.replaceAll('_',' ')]))],masses=[...new Set(a.cases.map(c=>c.case))];
 host.classList.add('lt26-view');
 host.innerHTML=`<div class="actions"><button data-mode="whole">Whole locomotive</button><button data-mode="bay">Engine bay</button><button data-mode="cooling">Airflow &amp; panels</button><button data-mode="routing">Truck connections</button><button data-mode="pump-service">Pump removed</button><button data-mode="cooler-service">Cooler removed</button></div><div class="lt26-controls"><label>Track<select data-curve><option value="straight">Straight</option><option value="left">30 m left</option><option value="right">30 m right</option></select></label><label>Reference mass<select data-mass>${masses.map(v=>`<option ${v==='base'?'selected':''}>${v}</option>`).join('')}</select></label><label>Reference load<select data-duty>${duties.map(([v,n])=>`<option value="${v}">${n}</option>`).join('')}</select></label><label>Crosslevel<select data-track><option value="flat">Level rails</option><option value="twist_left">Opposed twist A</option><option value="twist_right">Opposed twist B</option></select></label></div><p role="status" data-status></p><div data-canvas></div><p class="lt26-case-note" data-note></p><p class="note">Colored tubes show connection corridors. Supplier hose sizes, constant length, fitting clocking and intermediate supports remain open. Gold is the AIE package allowance. Service views show proposed removal positions after the relevant panels and supports are removed.</p><p><a href="locomotive-lt26-installation.html">Installation drawings</a> · <a href="locomotive-lt26-installation.html#brakes">Proposed brake circuit</a> · <a href="locomotive-lt26-systems-engineering.html">Checks &amp; unresolved items</a> · <a href="locomotive-lt26.html">Retained 50 m motion study</a></p>`;
 const q=s=>host.querySelector(s);
 async function show(){const own=++seq;viewer?.dispose();q('[data-canvas]').replaceChildren();const service=kind.includes('service');
  if(service){q('[data-mass]').value='base';q('[data-duty]').value='level';q('[data-track]').value='flat';q('[data-curve]').value='straight';}
  if(q('[data-duty]').value==='level')q('[data-track]').value='flat';
  host.querySelectorAll('select').forEach(s=>s.disabled=service);q('[data-track]').disabled=service||q('[data-duty]').value==='level';
  const id=[q('[data-mass]').value,q('[data-duty]').value,q('[data-track]').value,q('[data-curve]').value].join('/');q('[data-status]').textContent='Loading installation…';
  try{const m=await loadInstallation(kind,id);if(disposed||own!==seq)return;
   viewer=mountAssemblyModel(q('[data-canvas]'),{modelData:m,title:'LT26 · Installation and controls',badge:'PROVISIONAL LAYOUT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-1.8,.7],note:'Dimensions are for supplier and engineering review. No fabrication release.'});
   q('[data-status]').textContent=service?(kind==='pump-service'?'Pump: 650 mm aft, then 1200 mm left.':'Cooler: 300 mm forward, then 1600 mm up.'):`${m.lt26case.curve==='straight'?'Straight':'30 m '+m.lt26case.curve} · ${q('[data-mass]').value} reference mass · eight drivers retained`;
   q('[data-note]').textContent=service?'Geometric removal study only. Lifting, retained panel fasteners, disconnections and supplier removal instructions remain open.':`Reference-load pose; added fixture and brake-device masses are not yet included.${m.lt26case.capacity_flags.length?' DEMAND ONLY: '+m.lt26case.capacity_flags.join('; ')+'.':''} These poses do not establish stopping capability.`;
   host.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===kind)));host.dataset.ready='true';host.dataset.currentCase=id;
  }catch(e){if(!disposed&&own===seq)q('[data-status]').textContent='Model unavailable: '+e.message;}
 }
 host.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{kind=b.dataset.mode;show();});host.querySelectorAll('select').forEach(s=>s.onchange=show);
 await show();return{dispose(){disposed=true;seq++;viewer?.dispose();},refresh(){viewer?.refresh?.();}};
}
const host=document.querySelector('[data-lt26-install]');if(host)mountLT26Installation(host);
