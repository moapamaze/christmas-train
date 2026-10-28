import {loadLT26,lt26Data} from './lt26-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=mobile-r1';
const labels={level:'At rest',power_limited_pull_1:'Pulling · 1 mph',power_limited_pull_3:'Pulling · 3 mph','power_limited_pull_3.5':'Pulling · 3.5 mph',service:'All brakes · service demand',emergency:'All brakes · emergency demand',one_coach_service:'One coach unbraked · service demand',one_coach_emergency:'One coach unbraked · emergency demand','all_coach_loss_0.5_demand':'All coaches unbraked · 0.5 m/s² demand','all_coach_loss_0.7_demand':'All coaches unbraked · 0.7 m/s² demand'};
export async function mountLT26(host){
 let kind=host.dataset.initialView||'whole',viewer,seq=0,disposed=false;
 host.classList.add('lt26-view');
 host.innerHTML=`<div class="actions"><button data-view="whole">Whole locomotive</button><button data-view="cutaway">Machinery cutaway</button><button data-view="front">Engine &amp; front truck</button><button data-view="truck">Front truck</button><button data-view="service">Service spaces</button></div><div class="lt26-controls"><label>Track direction<select data-curve><option value="straight">Straight</option><option value="left">50 m left curve</option><option value="right">50 m right curve</option></select></label><label>Mass allowance<select data-mass><option value="base">Base estimate</option><option value="low">Low estimate</option><option value="high">High estimate</option><option value="front-heavy">Front-heavy estimate</option><option value="rear-heavy">Rear-heavy estimate</option><option value="fuel-empty">Fuel empty</option></select></label><label>Load case<select data-duty>${Object.entries(labels).map(([k,v])=>`<option value="${k}">${v}</option>`).join('')}</select></label><label>Rail crosslevel<select data-track><option value="flat">Level rails</option><option value="twist_left">Opposed twist A · ±10 mm</option><option value="twist_right">Opposed twist B · ±10 mm</option></select></label></div><div class="actions"><button data-critical="clearance">Show smallest installation gap</button><button data-critical="slide">Show least pivot travel</button><button data-reset>Reset</button></div><p role="status" data-status></p><p class="lt26-case-note" data-note></p><div data-canvas></div><p class="note">Body held fixed for comparing relative movement. Select a curve to turn the trucks. These are discrete calculated poses; the engine internals and pump remain supplier reservations. Gold marks the package space. Purple service outlines are illustrative and checked only in the nominal maintenance pose.</p><p><a href="locomotive-lt26.html">LT26 movement drawings</a> · <a href="locomotive-lt26-engineering.html">Calculations &amp; limits</a> · <a href="locomotive-lt25.html">Engine installation details</a></p>`;
 const q=s=>host.querySelector(s);
 let a,cl;try{[a,cl]=await lt26Data();}catch(e){q('[data-status]').textContent=e.message;return {dispose(){disposed=true;}};}
 if(disposed)return;
 function setCase(id){const [mass,duty,track,curve]=id.split('/');q('[data-mass]').value=mass;q('[data-duty]').value=duty;q('[data-track]').value=track;q('[data-curve]').value=curve;}
 async function show(){
  const own=++seq;viewer?.dispose();q('[data-canvas]').replaceChildren();
  if(kind==='service')setCase('base/level/flat/straight');
  if(q('[data-duty]').value==='level')q('[data-track]').value='flat';
  q('[data-track]').disabled=q('[data-duty]').value==='level'||kind==='service';
  for(const key of ['curve','mass','duty'])q(`[data-${key}]`).disabled=kind==='service';
  const id=kind==='service'?'base/level/flat/straight':[q('[data-mass]').value,q('[data-duty]').value,q('[data-track]').value,q('[data-curve]').value].join('/');
  q('[data-status]').textContent='Loading calculated position…';
  try{
   const model=await loadLT26(kind,id);if(disposed||own!==seq)return;
   const c=model.lt26case,ev=model.lt26clearance;
   viewer=mountAssemblyModel(q('[data-canvas]'),{modelData:model,title:'LT26 · '+(kind==='service'?'Nominal maintenance pose':labels[c.label]),badge:'DEVELOPMENT STUDY',compact:true,groupControls:true,edgeLines:false,orbitDirection:kind==='front'||kind==='truck'?[-1,-1.8,1]:[-1,-1.8,.7],note:'Finite load poses on the 50 m target. No fabrication or operating release.'});
   q('[data-status]').textContent=kind==='service'?'Nominal maintenance pose · 650 mm pump / 300 mm cooler withdrawal reservations.':`${c.curve==='straight'?'Straight track':'50 m '+c.curve+' curve'} · smallest installation box gap ${ev.minimum.gap_mm.toFixed(1)} mm · pivot travel remaining ${c.slide_margin_mm.toFixed(2)} mm`;
   const flag=c.capacity_flags.length>0;
   q('[data-note]').classList.toggle('is-demand',flag);
   q('[data-note]').textContent=flag?'DEMAND ONLY — '+c.capacity_flags.join('; ')+'. This pose does not demonstrate stopping or pulling capability.':kind==='service'?'Actual tools, lifting, hoses and enclosure openings remain unqualified.':'No adhesion/brake-target flag in this reduced case. Supplier ratings, whole-vehicle fit and structural approval remain open.';
   host.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===kind)));
   host.dataset.currentCase=id;host.dataset.ready='true';
  }catch(e){if(!disposed&&own===seq)q('[data-status]').textContent='Model unavailable: '+e.message;}
 }
 host.querySelectorAll('select').forEach(s=>s.onchange=show);
 host.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{kind=b.dataset.view;show();});
 host.querySelectorAll('[data-critical]').forEach(b=>b.onclick=()=>{kind='front';setCase(b.dataset.critical==='clearance'?cl.minimum.case_id:a.critical[b.dataset.critical]);show();});
 q('[data-reset]').onclick=()=>{kind='whole';setCase('base/level/flat/straight');show();};
 await show();return {dispose(){disposed=true;seq++;viewer?.dispose();},refresh(){viewer?.refresh?.();}};
}
const host=document.querySelector('[data-lt26-view]');if(host)mountLT26(host);
