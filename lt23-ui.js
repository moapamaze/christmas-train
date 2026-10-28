import {loadLT23,lt23Data} from './lt23-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=CC2';
export async function mountLT23(host){
 host.innerHTML='<p role="status">Loading powered-truck development…</p>';
 try{
  const [,,,ev]=await lt23Data();let kind=host.dataset.initialView||'whole';
  host.innerHTML=`<div class="actions"><button data-view="whole">Whole locomotive</button><button data-view="truck">Complete powered truck</button><button data-view="connections">Body connections</button><button data-view="roll">Roll cartridge</button><button data-view="primary">Primary &amp; rebound</button><button data-view="cutaway">Machinery cutaway</button></div><div class="lt19-controls"><label>Clearance position<select data-pose>${ev.cases.map((c,i)=>`<option value="${i}">${label(c)}</option>`).join('')}</select></label></div><p data-status role="status"></p><div data-canvas></div><p class="note">Spring coils illustrate the specified envelope. Positions are geometric clearance checks; the separate load study identifies travel limits. This model does not simulate running on track.</p><p><a href="locomotive-lt24.html">LT24 supplier review</a> · <a href="locomotive-lt23.html">LT23 drawings and complete truck</a> · <a href="locomotive-lt23-engineering.html">Calculations and structural review</a> · <a href="locomotive-lt22.html">LT22 record</a></p>`;
  let viewer,seq=0;const q=s=>host.querySelector(s);
  async function show(){const own=++seq;viewer?.dispose();q('[data-canvas]').replaceChildren();q('[data-status]').textContent='Loading clearance position…';try{
   const m=await loadLT23(kind,+q('[data-pose]').value);if(own!==seq)return;const c=m.lt23case;
   viewer=mountAssemblyModel(q('[data-canvas]'),{modelData:m,title:'LT23 · powered-truck support and traction',badge:'REVIEW CANDIDATE',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-1.8,.7],note:'Connection and spring candidates for structural review. Modified parts are not released for fabrication.'});
   q('[data-status]').textContent=`${c.hits.length} rigid / ${c.full_wheel_disk_hits.length} wheel / ${c.spring_envelope_hits.length} spring-envelope intersections. Maximum pivot slide ${Math.max(...['FRONT','REAR'].map(g=>Math.abs(c.placements[g].slide_mm))).toFixed(2)} mm; bearing tilt ${c.max_bearing_misalignment_deg.toFixed(2)}°; roll-capture reserve ${c.roll_capture_margin_mm.toFixed(1)} mm.`;
   host.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===kind)));
  }catch(e){q('[data-status]').textContent='Model unavailable: '+e.message;}}
  host.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{kind=b.dataset.view;show()});q('[data-pose]').onchange=show;await show();
 }catch(e){host.textContent='Study unavailable: '+e.message;}
}
function label(c){if(c.truck_states)return `30 m ${c.hand>0?'left':'right'} · load-derived: ${c.load_label||'critical suspension position'}`;return `${c.radius_mm?c.radius_mm/1000+' m '+(c.hand>0?'left':'right'):'Straight'} · ${c.jounce_mm>0?'+':''}${c.jounce_mm} mm · roll ${c.roll_deg}° / pitch ${c.pitch_deg}°${c.axle_roll_deg?' / axle roll '+c.axle_roll_deg+'°':''}`;}
const host=document.querySelector('[data-lt23-view]');if(host)mountLT23(host);
