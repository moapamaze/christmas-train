import {loadLT36} from './lt36-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=mobile-r1';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export async function mountLT36(host){
 let viewer,seq=0,disposed=false;host.classList.add('lt26-view');
 host.innerHTML=`<div class="lt26-controls"><label>System<select data-system><option value="all">All connections</option><option value="hydraulic">Hydraulic drive and drains</option><option value="air">Brakes and air supply</option><option value="electrical">Electrical and cameras</option></select></label><label>Area<select data-area><option value="all">Whole train</option><option value="front">Front truck</option><option value="rear">Rear truck</option><option value="cab">Cab and supply ends</option><option value="joint">Locomotive–coach joint</option></select></label><label>Position<select data-pose><option value="straight">Level / straight</option><option value="left">50 m left reference</option><option value="right">50 m right reference</option></select></label></div><p data-status role="status">Tracing the current routes…</p><p class="lt27-callout"><strong>These hoses are unfinished.</strong> Red cubes mark open ends, amber cubes mark body-trunk gaps, and purple cubes mark overlapping hose leads. Cubes are display annotations, not fittings or caps. The retained route geometry and mass model are unchanged.</p><div data-viewer></div><details><summary>Connections requiring work</summary><div data-items class="lt36-items"></div></details><p><a href="locomotive-lt36.html">Route destinations and next installation milestone →</a></p>`;
 const q=s=>host.querySelector(s);
 async function show(){const n=++seq;viewer?.dispose();q('[data-viewer]').replaceChildren();q('[data-items]').replaceChildren();q('[data-status]').textContent='Loading and checking route ends…';host.dataset.ready='false';await new Promise(requestAnimationFrame);
  try{const pose=q('[data-pose]').value,m=await loadLT36({system:q('[data-system]').value,area:q('[data-area]').value,caseId:'base/level/flat/'+pose,radius:pose==='straight'?0:50,hand:pose==='right'?-1:1});if(disposed||n!==seq)return;
   const c=m.lt36.counts;viewer=mountAssemblyModel(q('[data-viewer]'),{modelData:m,title:'LT36 · trace the unfinished hose connections',badge:'CONNECTION AUDIT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-.7,-1.6,.85],note:'Red: open endpoint. Amber: disconnected body branch. Purple: overlapping leads. Markers carry no physical mass; route geometry is retained for inspection. Select an annotation to read its intended destination.'});
   q('[data-status]').textContent=`${c.open} highlighted open ends · ${c.gaps} front trunk gaps · ${c.overlaps} overlapping lead pairs in the complete audit. ${m.lt36.shown.length} markers match the current filters.`;
   const items=m.lt36.shown;q('[data-items]').innerHTML=items.length?items.map(x=>`<article style="padding:12px 0;border-bottom:1px solid #c4d1ca"><strong>${esc(x.title)}</strong><p style="margin:4px 0">${esc(x.detail)}</p><small>${esc(x.route_ids.join(' · '))}</small></article>`).join(''):'<p>No audit markers in this filter. This does not establish circuit completion or clearance approval.</p>';
   host.dataset.ready='true';host.dataset.currentSystem=m.lt36.system;host.dataset.currentArea=m.lt36.area;
  }catch(e){q('[data-status]').textContent='Connection view unavailable: '+e.message;}
 }
 for(const s of ['[data-system]','[data-area]','[data-pose]'])q(s).onchange=show;
 await show();return{dispose(){disposed=true;seq++;viewer?.dispose();},refresh(){viewer?.refresh?.();}};
}
const host=document.querySelector('[data-lt36-view]');if(host)mountLT36(host);
