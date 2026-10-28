import {loadLT20,lt20Data} from './lt20-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=CC2';
export async function mountLT20(host){
 host.innerHTML='<p role="status">Loading articulated connections…</p>';
 try{
  const [,,,ev]=await lt20Data();
  host.innerHTML=`<div class="actions"><button data-view="whole">Whole locomotive</button><button data-view="cutaway">Machinery cutaway</button><button data-view="pivot">Powered pivot</button><button data-view="rebound">Rebound &amp; guide</button></div><div class="lt19-controls"><label>Checked position<select data-pose>${ev.cases.map((c,i)=>`<option value="${i}">${label(c)}</option>`).join('')}</select></label></div><p data-status role="status"></p><div data-canvas></div><p class="note">Purple roll supports are deformable space reservations. Their stiffness, preload and sliding surfaces are unfinished. Tilt and axle-roll positions are clearance probes, not a running simulation. Red identifies interference.</p><p><a href="locomotive-lt20.html">LT20 connection drawings</a> · <a href="locomotive-lt20-engineering.html">Loads and structural review</a> · <a href="locomotive-lt19.html">Previous rear-support study</a></p>`;
  let viewer,seq=0,kind='whole';const q=s=>host.querySelector(s);
  async function show(){const own=++seq;viewer?.dispose();q('[data-canvas]').replaceChildren();q('[data-status]').textContent='Loading checked position…';try{
   const m=await loadLT20(kind,+q('[data-pose]').value);if(own!==seq)return;const c=m.lt20case;
   viewer=mountAssemblyModel(q('[data-canvas]'),{modelData:m,title:'LT20 · articulated connections',badge:'DEVELOPMENT',compact:true,groupControls:true,edgeLines:false,orbitDirection:[-1,-1.8,.7],note:'Connection geometry for review. Bearing, springs, bolts, welds, fatigue and operating loads require approval before fabrication.'});
   q('[data-status]').textContent=`${c.hits.length} rigid intersections · ${c.full_wheel_disk_hits.length} wheel-envelope intersections · ${c.spring_envelope_hits.length} spring-space intersections. Bearing misalignment ${c.max_bearing_misalignment_deg.toFixed(2)}°. Rebound-stop gaps ${c.rebound_stop_gaps_mm.map(x=>x.toFixed(1)).join(' / ')} mm.`;
   host.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===kind)));
  }catch(e){q('[data-status]').textContent='Model unavailable: '+e.message;}}
  host.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{kind=b.dataset.view;show()});q('[data-pose]').onchange=show;await show();
 }catch(e){host.textContent='Study unavailable: '+e.message;}
}
function label(c){return `${c.radius_mm?c.radius_mm/1000+' m '+(c.hand>0?'left':'right'):'Straight'} · ${c.jounce_mm>0?'+':''}${c.jounce_mm} mm · roll ${c.roll_deg}° / pitch ${c.pitch_deg}°${c.axle_roll_deg?' / axle roll '+c.axle_roll_deg+'°':''}`;}
const host=document.querySelector('[data-lt20-view]');if(host)mountLT20(host);
