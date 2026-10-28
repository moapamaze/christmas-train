import{loadCompressedModel}from'./lt3-model.js';
import{transformPart}from'./lt30-model.js';
import{ladderPoint,ladderStow}from'./cab-c2-model.js';
import{mountAssemblyModel}from'./assembly-model-viewer.js?v=mobile-r1';

const asset=n=>new URL('./assets/locomotive-cab-c3/'+n,import.meta.url);
const states={deployed:{angle:0,locked:true,label:'Deployed · nominal pins engaged'},release:{angle:0,locked:false,label:'Deployed · pins withdrawn'},travel:{angle:60,locked:false,label:'60° · pins withdrawn'},stowrelease:{angle:ladderStow,locked:false,label:'Stowed · pins withdrawn'},stowed:{angle:ladderStow,locked:true,label:'Stowed · nominal pins engaged'}};
export async function mountC3(host){
 const[lock,reference,study]=await Promise.all([loadCompressedModel(asset('lock-model.json.gz')),loadCompressedModel(new URL('./assets/locomotive-cab-c2/overlay.json.gz',import.meta.url)),fetch(asset('study.json')).then(r=>r.json())]);
 let viewer,seq=0;host.classList.add('cab-study','cab-c3');
 host.innerHTML=`<div class="cab-controls"><label>Inspect<select data-scope><option value="detail">One lock cartridge</option><option value="ladder">Left ladder · hinge datum reference</option></select></label><label>Nominal mechanism state<select data-state>${Object.entries(states).map(([id,s])=>`<option value="${id}">${s.label}</option>`).join('')}</select></label><label>Outer cheek<select data-cutaway><option value="open">Hidden · inspection view</option><option value="closed">Shown · assembled cartridge</option></select></label></div><p data-status role="status">Loading the C3 lock study…</p><div data-renderer></div><p class="cab-note">Pins are animated only at the two indexed positions. Remote release, springs, retention, frame carriers, bearings and the controlled drive are not completed by this animation. The ladder view locates the studies at the inherited hinge datums; it is not an installed assembly.</p>`;
 const q=s=>host.querySelector(s);
 async function show(){
  const token=++seq;host.dataset.ready='false';viewer?.dispose();q('[data-renderer]').replaceChildren();q('[data-status]').textContent='Loading the selected mechanism state…';
  await new Promise(r=>setTimeout(r,50));if(token!==seq)return;
  const scope=q('[data-scope]').value,state=states[q('[data-state]').value],cut=q('[data-cutaway]').value==='open';
  let parts=lock.parts.filter(p=>p.metadata.side===-1&&(scope==='ladder'||p.metadata.unit==='L-F')).filter(p=>!cut||!(p.id.endsWith('F-CHEEK--14')||p.id.endsWith('A-CHEEK-14'))).map(p=>{
   const md=p.metadata;
   if(md.c3_motion==='rotate')return transformPart(p,v=>ladderPoint(v,-1,state.angle));
   if(md.c3_motion==='pin'&&!state.locked){const direction=md.unit.endsWith('F')?-1:1;return transformPart(p,v=>[v[0]+direction*60,v[1],v[2]]);}
   return p;
  });
  if(scope==='ladder')parts.push(...reference.parts.filter(p=>p.metadata.cab_motion==='L-ladder').map(p=>({...transformPart(p,v=>ladderPoint(v,-1,state.angle)),group:'reference',color:'#9ca99b'})));
  const model={schemaVersion:3,units:'inches',title:'C3 isolated lock study',parts,groups:[...lock.groups,{id:'reference',label:'C2 moving ladder reference',default_visible:true,explosion_vector_in:[0,0,0]}].filter(g=>parts.some(p=>p.group===g.id)),compatibility_camera:[-.8,.5]};
  viewer=mountAssemblyModel(q('[data-renderer]'),{modelData:model,title:scope==='detail'?'C3 · two-position lock cartridge':'C3 · cartridge locations on the C2 ladder',badge:'STUDY · NOT INSTALLED',compact:true,groupControls:true,edgeLines:true,orbitDirection:scope==='detail'?[-1.5,-1,.7]:[-1,-1.6,.9],note:'Select a part for nominal dimensions and unfinished interfaces. Outer cheek may be hidden for inspection.'});
  q('[data-status]').textContent=`${state.angle.toFixed(2)}° · ${state.locked?'Index pins shown through both cheeks and the disc. This is geometry, not measured engagement.':'Index pins withdrawn 60 mm. The omitted drive must control the ladder; no free-drop state is acceptable.'} ${cut?'Outer cheek hidden.':''}`;
  host.dataset.ready='true';host.dataset.state=q('[data-state]').value;host.dataset.scope=scope;
 }
 host.querySelectorAll('select').forEach(e=>e.addEventListener('change',()=>show().catch(e=>{q('[data-status]').textContent='Study view unavailable: '+e.message;})));await show();
 const calc=document.querySelector('[data-c3-drive]');if(calc){
  const ratio=study.drive.ratio,torque=study.with_moving_lock_parts.peak_gravity_torque_Nm,turns=study.drive.input_turns;
  calc.innerHTML=`<div class="cab-controls"><label>Assumed total forward efficiency<select data-eff><option value=".25">25%</option><option value=".35" selected>35%</option><option value=".45">45%</option></select></label><label>Assumed cranking speed<select data-rpm><option value="30" selected>30 rev/min</option><option value="60">60 rev/min</option></select></label><div class="cab-note">48:1 overall reduction · 150 mm crank. These inputs are study assumptions, not supplier guarantees or accepted operator limits.</div></div><div class="cab-metrics" data-drive-results aria-live="polite"></div>`;
  function update(){const eff=+calc.querySelector('[data-eff]').value,rpm=+calc.querySelector('[data-rpm]').value;calc.querySelector('[data-drive-results]').innerHTML=[['Peak motoring force',(torque/(ratio*eff*.15)).toFixed(0)+' N'],['Crank travel',turns.toFixed(1)+' turns'],['Cranking alone',(turns/rpm*60).toFixed(1)+' s'],['Net released energy',study.with_moving_lock_parts.stow_to_deployed_energy_J.toFixed(0)+' J']].map(([l,v])=>`<div class="cab-metric warn"><strong>${v}</strong><span>${l}</span></div>`).join('');}
  calc.querySelectorAll('select').forEach(e=>e.addEventListener('change',update));update();
 }
}
const host=document.querySelector('[data-c3-model]');if(host)mountC3(host).catch(e=>{host.textContent='C3 study unavailable: '+e.message;console.error(e);});
