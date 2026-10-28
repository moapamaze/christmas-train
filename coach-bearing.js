import {getModelData} from './model-data.js';
import {composeModels,mountIssueControls} from './coach-issue-viewer.js';
import {mountFrameJViewer} from './framej3d.js';
const src=p=>new URL('./assets/coach-bearing-cw3/'+p,import.meta.url);
export async function applyCW3(truck){
 const update=await getModelData(src('replacement-model.json.gz'));
 const removed=new Set(update.parts.map(p=>p.metadata.replaces).filter(x=>x&&x!=='NEW'));
 for(const id of removed)if(!truck.parts.some(p=>p.id===id))throw new Error('CW3 source interface changed: '+id);
 return composeModels([{model:{...truck,parts:truck.parts.filter(p=>!removed.has(p.id))},prefix:''},{model:update,prefix:'CW3-'}],'CW3 coach bogie: revised bearing ends');
}
export async function buildCW3(mode='section'){
 const m=await getModelData(src(mode==='section'?'section-model.json.gz':mode==='floating'?'floating-section-model.json.gz':'end-model.json.gz'));
 if(mode!=='exploded')return m;
 const parts=m.parts.map(p=>{
  let dy=0;
  if(p.id.includes('INNER-COVER')||p.id.includes('INNER-BOLT'))dy=-150;
  else if(p.id.includes('FLINGER'))dy=-85;
  else if(p.id.includes('INNER-ABUTMENT'))dy=-40;
  else if(p.id.includes('BRG'))dy=85;
  else if(p.id.includes('SPACER'))dy=130;
  else if(p.id.includes('MB18'))dy=160;
  else if(p.id.includes('KM18'))dy=190;
  else if(p.id.includes('OUTER-ABUT'))dy=235;
  else if(p.id.includes('BLIND-CAP'))dy=280;
  const d=dy/25.4;
  return {...p,positions:p.positions.map((v,i)=>v+(i%3===1?d:0)),bounds_in:{...p.bounds_in,y:p.bounds_in.y.map(v=>v+d)},centre_in:p.centre_in.map((v,i)=>v+(i===1?d:0)),metadata:{...p.metadata,display_separation_mm:dy,warning:'Exploded display is not a collision-free assembly path; follow the numbered sequence.'}};
 });return {...m,parts,title:'CW3 exploded component order'};
}
export async function mountCW3(host){return mountFrameJViewer(host,{modelData:await buildCW3(),title:'CW3 · bearing-end cutaway',badge:'DEVELOPMENT CAD',note:'Pilot-centered spacer, recessed cover and grease labyrinth. Final fits, thread details, seal testing and extraction tooling require release.',groupControls:true});}
if(document.querySelector('[data-cw3]'))mountIssueControls({hostId:'cw3-viewer',statusId:'cw3-status',attribute:'data-bearing-view',select:async mode=>({modelData:await buildCW3(mode),title:mode==='exploded'?'Bearing-end components · exploded':mode==='section'?'Locating bearing · cutaway':mode==='floating'?'Floating bearing · cutaway':'Bearing end · assembled',badge:'CW3 · PROPOSED DETAIL',note:'Geometry is revised. Bearing internals and thread helix remain schematic; do not machine from viewer meshes.',status:mode==='exploded'?'Exploded separation identifies parts. Use the numbered assembly sequence below; this is not the installation motion.':'Use Whole assembly to fit all parts. Select a part for its dimensions.'})});
