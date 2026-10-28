import {getModelData} from './model-data.js';
import {composeModels,mountIssueControls} from './coach-issue-viewer.js';
import {mountFrameJViewer} from './framej3d.js';
const url=p=>new URL('./assets/'+p,import.meta.url),subset=(m,fn)=>({...m,parts:m.parts.filter(fn)});
export async function buildCW2(mode='axle'){
 const replacements=await getModelData(url('coach-wheelset-cw1/replacement-model.json.gz'));
 const axle=subset(replacements,p=>p.id==='AXLE2');
 if(mode==='axle')return axle;
 const wheelset=await getModelData(url('coach-wheelset-cw1/model.json.gz'));
 if(mode==='wheel')return subset(wheelset,p=>p.id==='A1R-WHEEL-BLANK');
 if(mode==='end')return getModelData(url('coach-wheelset-cw1/end-model.json.gz'));
 const b=await getModelData(url('coach-brake-c55/model-nominal.json.gz'));
 const result=composeModels([{model:subset(wheelset,p=>p.id!=='AXLE1'),prefix:'WHEELSET-',offset:[1200/25.4,0,0]},{model:axle,prefix:'KEYED-'},{model:subset(b,p=>p.group!=='retained-C5-reference'),prefix:'BRAKE-'}],'CW2 wheelset with the current single brake');
 result.parts=result.parts.map(p=>({...p,opacity:1}));return result;
}
export async function mountCW2(host){return mountFrameJViewer(host,{modelData:await buildCW2('axle'),title:'CW2 · axle machining review',badge:'NOMINAL / SUPPLIER HOLDS',note:'Current CW1 nominal solid. Relief, spacer centering, groove, fits and fillets remain unresolved. Read CW2-A01/A02 before using these surfaces as machining instructions.',groupControls:true});}
if(document.querySelector('[data-cw2]'))mountIssueControls({hostId:'cw2-viewer',statusId:'cw2-status',attribute:'data-cw2-view',select:async mode=>({modelData:await buildCW2(mode),title:{axle:'Keyed axle 2',wheel:'Current wheel blank — finished contour held',end:'Bearing end — relief and spacer review',brake:'Wheelset and current brake'}[mode],badge:'CW2 · REVIEW CAD',note:'Geometry is the inherited nominal CW1/C5.5 design. Finished wheel profile and manufacturing fits are not released. Section drawings identify unresolved features.',status:'Select a part for its source dimensions. Whole assembly resets the view; exploded motion is display separation only.'})});
