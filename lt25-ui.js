import {loadLT25} from './lt25-model.js';
import {mountAssemblyModel} from './assembly-model-viewer.js?v=mobile-r1';
export async function mountLT25(host){
  let kind=host.dataset.initialView||'whole',viewer,seq=0,disposed=false;
  host.innerHTML=`<div class="actions"><button data-view="whole">Whole locomotive</button><button data-view="cutaway">Machinery cutaway</button><button data-view="service">Service paths</button><button data-view="powerunit">Engine &amp; pump</button><button data-view="skid">Common skid</button><button data-view="truck">Retained LT23 truck</button></div><p role="status" data-status></p><div data-canvas></div><p class="note">Gold boundary: conservative package reservation covering both hands of its asymmetric shaft datum. Purple outlines in Service paths are proposed withdrawal spaces, not proven OEM service clearance. Colored internal shapes and the pump are reservations, not supplier solid CAD. The current engine installation is shown at nominal ride height; prior LT23 truck motion checks do not release this installation.</p><p><a href="locomotive-lt25.html">LT25 installation drawings</a> · <a href="locomotive-lt25-engineering.html">Supplier data &amp; calculations</a> · <a href="locomotive-lt23.html">Retained truck connections</a></p>`;
  const q=s=>host.querySelector(s);
  async function show(){
    const own=++seq;viewer?.dispose();q('[data-canvas]').replaceChildren();q('[data-status]').textContent='Loading supplier package and locomotive…';
    try{
      const model=await loadLT25(kind);if(disposed||own!==seq)return;
      viewer=mountAssemblyModel(q('[data-canvas]'),{modelData:model,title:kind==='truck'?'LT23 · retained powered truck':'LT25 · AIE engine installation',badge:'REVIEW CANDIDATE',compact:true,groupControls:true,edgeLines:false,orbitDirection:kind==='powerunit'||kind==='skid'?[-1,-1.8,1]:[-1,-1.8,.7],note:'Dimensional installation study. Supplier mount, cooling and pump qualification remain open.'});
      q('[data-status]').textContent=kind==='service'?'Service study: 650 mm pump withdrawal aft; 300 mm cooler withdrawal forward. Enclosure openings, tools and actual OEM service distances remain open.':kind==='truck'?'Retained LT23 connection geometry; see its original check boundaries.':'AIE package 1,249.7 × 687.1 × 1,027.9 mm; gold reservation width 809.2 mm · one fan · SAE B / 13-tooth interface reservation.';
      host.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===kind)));
    }catch(e){if(!disposed)q('[data-status]').textContent='Model unavailable: '+e.message;}
  }
  host.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{kind=b.dataset.view;show();});
  await show();return {dispose(){disposed=true;seq++;viewer?.dispose();},refresh(){viewer?.refresh?.();}};
}
const host=document.querySelector('[data-lt25-view]');if(host)mountLT25(host);
