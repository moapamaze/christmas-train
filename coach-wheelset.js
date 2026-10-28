import {getModelData} from './model-data.js';
import {composeModels,mountIssueControls} from './coach-issue-viewer.js';
import {mountFrameJViewer} from './framej3d.js';
const src=p=>new URL('./assets/coach-wheelset-cw1/'+p,import.meta.url);
export async function applyCW1(truck){
 const base=await getModelData(src('replacement-model.json.gz'));
 const keyed=truck.parts.filter(p=>/^C5[567]-AXLE2-C54-KEYWAY$/.test(p.id));
 if(keyed.length!==1)throw new Error('Expected exactly one current keyed axle');
 const update={...base,parts:base.parts.map(p=>p.metadata.replaces==='C55-AXLE2-C54-KEYWAY'?{...p,metadata:{...p.metadata,replaces:keyed[0].id}}:p)};
 const removed=new Set(update.parts.map(p=>p.metadata.replaces).filter(x=>x!=='NEW'));
 for(const id of removed)if(!truck.parts.some(p=>p.id===id))throw new Error('CW1 source interface changed: '+id);
 const retained={...truck,parts:truck.parts.filter(p=>!removed.has(p.id))};
 const result=composeModels([{model:retained,prefix:''},{model:update,prefix:'CW1-'}],'Coach bogie with CW1 shortened axles and bearing retention');
 result.wheelset_revision='CW1';return result;
}
export async function buildCW1(mode='whole'){
 return getModelData(src(mode==='section'?'section-model.json.gz':mode==='end'?'end-model.json.gz':'model.json.gz'));
}
export async function mountCW1(host){return mountFrameJViewer(host,{modelData:await buildCW1(),title:'CW1 · coach wheelset and bearing retention',badge:'DEVELOPMENT CAD',note:'Pressed wheels; KM18 locknuts with MB18 tab washers. Final wheel profile, interference and load qualification pending.',groupControls:true});}
if(document.querySelector('[data-cw1]'))mountIssueControls({hostId:'cw1-viewer',statusId:'cw1-status',attribute:'data-wheel-view',select:async mode=>({modelData:await buildCW1(mode),title:'CW1 · wheels pressed onto a rotating axle',badge:'DEVELOPMENT CAD',note:'Wheel press fit and running profile require supplier release. Catalog bearing hardware is dimensioned; washer tab pattern and thread are illustrative. Use the section drawing for the axial stack.',status:'Use Whole assembly to reset the view. The exploded slider separates groups for inspection; it is not an assembly path.'})});
