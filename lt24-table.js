import {loadCompressedModel} from './lt3-model.js';
const status=document.querySelector('#load-status'),body=document.querySelector('#load-rows');
const mass=document.querySelector('#mass-filter'),kind=document.querySelector('#kind-filter'),event=document.querySelector('#event-filter');
try{
 const data=await loadCompressedModel('assets/locomotive-lt24/analysis.json.gz');
 const f=(n,d=2)=>Number.isFinite(n)?n.toFixed(d):'—';
 function render(){
  const rows=data.scenarios.filter(x=>(mass.value==='all'||x.case===mass.value)&&(kind.value==='all'||x.kind===kind.value)&&(event.value==='all'||(event.value==='contact'?x.events.length:x.capacity_flags.length+x.flags.length)));
  body.replaceChildren();
  for(const x of rows){const tr=document.createElement('tr');const values=[`${x.label.replaceAll('_',' ')} · ${x.case} · ${x.track_label.replaceAll('_',' ')} · ${x.speed_mph} mph`,f(x.rail_force_N.reduce((a,b)=>a+b,0)/1000),`${f(Math.min(...x.primary_compression_mm))} to ${f(Math.max(...x.primary_compression_mm))}`,['bumper_force_N','hard_stop_force_N','rebound_force_N'].map(k=>f(Math.max(...x[k])/1000)).join(' / '),f(x.min_wheel_N/1000),f(x.local_mu_required,3),[...x.events,...x.capacity_flags,...x.flags].join('; ')||'No contact event; capacities unverified'];for(const v of values){const td=document.createElement('td');td.textContent=v;tr.append(td);}if(x.capacity_flags.length||x.flags.length)tr.lastChild.className='flag';body.append(tr);}
  status.textContent=`${rows.length} of ${data.scenarios.length} cases shown`;
 }
 [mass,kind,event].forEach(x=>x.addEventListener('change',render));render();
}catch(e){status.textContent='Calculation table unavailable. Use the CSV link below. '+e.message;}
