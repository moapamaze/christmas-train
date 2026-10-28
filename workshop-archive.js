const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pages=new Set(['drawings','models','fabrication','overview']);
function route(){
 const [raw,assembly]=location.hash.slice(1).split('/');
 if(raw&&!pages.has(raw)){location.replace('engineering.html'+location.hash);return;}
 const selected=raw==='overview'||!raw?'drawings':raw;
 document.querySelectorAll('.shop-panel').forEach(p=>p.hidden=p.id!==selected);
 document.querySelectorAll('[data-page]').forEach(a=>{if(a.dataset.page===selected)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 const title={drawings:'Previous drawing versions',models:'Earlier 3D alternatives',fabrication:'Earlier fabrication notes'}[selected];$('#shop-title').textContent=title;document.title=title+' · Pulsipher Farms';
 if(selected==='models'&&modelSelect.options.length){
  if(assembly&&[...modelSelect.options].some(option=>option.value===assembly))modelSelect.value=assembly;
  showModel();
 }
 if(selected==='drawings'&&catalog){
  if(assembly&&catalog.packages.some(item=>item.id===assembly))$('#assembly-select').value=assembly;
  sheets();
 }
}
const modelSelect=$('#model-select');
window.addEventListener('hashchange',route);
let catalog,visibleSheets=[];
function sheets(){
 const p=catalog.packages.find(x=>x.id===$('#assembly-select').value),query=$('#drawing-search').value.trim().toLowerCase();
 $('#package-note').innerHTML=esc(p.note)+' <a href="'+esc(p.engineering)+'">Engineering reference ↗</a>'+(p.fabricationPage?' <a href="'+esc(p.fabricationPage)+'">Parts, materials &amp; assembly ↗</a>':'');
 visibleSheets=p.sheets.filter(s=>(s.title+' '+s.id).toLowerCase().includes(query));
 $('#sheet-grid').innerHTML=visibleSheets.length?visibleSheets.map((s,i)=>'<article class="sheet-card"><button class="sheet-preview" data-sheet="'+i+'" aria-label="View '+esc(s.title)+'"><img src="'+esc(s.image)+'" alt="'+esc(s.title)+'" loading="lazy"><span>View drawing ↗</span></button><div class="sheet-caption"><span class="sheet-kind">'+esc(s.id)+' · '+esc(s.kind)+'</span><h2>'+esc(s.title)+'</h2><p>'+esc(s.note||p.note)+'</p><a href="'+esc(s.original||s.image)+'" target="_blank" rel="noopener">'+((s.original||s.image).endsWith('.gz')?'Download vector (gzip)':'Open original')+'</a></div></article>').join(''):'<div class="shop-note">'+(query?'No matching drawings in this assembly.':'Detailed physical drawings are still in development for this assembly.')+'</div>';
 document.querySelectorAll('[data-sheet]').forEach(b=>b.addEventListener('click',()=>openSheet(visibleSheets[Number(b.dataset.sheet)],p)));
}
const dialog=$('#sheet-dialog');let returnFocus;
function openSheet(s,p){returnFocus=document.activeElement;$('#sheet-title').textContent=s.id+' · '+s.title;$('#sheet-image').src=s.image;$('#sheet-image').alt=s.title;$('#sheet-note').textContent=s.note||p.note;$('#sheet-original').href=s.original||s.image;$('#sheet-original').textContent=(s.original||s.image).endsWith('.gz')?'Download vector (gzip)':'Open original ↗';$('.sheet-viewport').classList.remove('enlarged');$('#sheet-zoom').textContent='Enlarge';dialog.showModal();}
$('#sheet-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>returnFocus?.focus());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
$('#sheet-zoom').addEventListener('click',()=>{$('.sheet-viewport').classList.toggle('enlarged');$('#sheet-zoom').textContent=$('.sheet-viewport').classList.contains('enlarged')?'Fit width':'Enlarge';});
$('#assembly-select').addEventListener('change',()=>{location.hash='drawings/'+$('#assembly-select').value;sheets();});$('#drawing-search').addEventListener('input',sheets);
const modelDefinitions=[
 ['coach-wheelset-cw2','Wheel profile & axle detail · CW2','coach-wheel-review.js?v=CW2','mountCW2','Axle machining review with separate wheel-profile, fit and seal holds. Drawings are for supplier review, not fabrication.'],
 ['coach-wheelset-cw1','Wheels & axle retention · CW1','coach-wheelset.js?v=CW1','mountCW1','Pressed wheels, shortened axles and positive bearing-nut locking. Final wheel profile, fits and engineering release pending.'],
 ['coach-assembled','Coaches + bogies + drawbar · CA1','coach-assembled.js?v=CA1-CW1','mountConnectedCoaches','Two passenger coaches on their bogies, connected with a proposed drawbar installation. CW1 shortened axles and bearing retention; design holds remain.'],
 ['drivetrain-dt5','Powered axle mount · DT5','drivetrain-dt5.js?v=DT5-R1','mountDrivetrain','Separate bearing cartridges, roll cradles, motor carrier, coupling and hose routes. Exploded and suspension views; fabrication holds remain.'],
 ['coach-brake-truck','Passenger truck + supported brake hoses · C5.6','coach-brake-truck.js?v=C56-R0','mountBrakeTruckC56','One brake with fixed hose connections and maintenance details. Supplier matching, loads and complete qualification remain open.'],
 ['coach-c56','Brake hoses and service · C5.6','brakec56.js?v=C56-R0','mountBrakeC56','Actual hose anchors and supported leads; service and mounting details with unresolved interfaces marked.'],
 ['coach-c55','Earlier brake ports and hoses · C5.5','brakec55.js?v=C55-R0','mountBrakeC55','Physical-port and hose geometry, with unresolved threaded engagement and supplier matching. One development installation.'],
 ['coach-c54','Earlier brake installation · C5.4','brakec54.js?v=C54-R0','mountBrakeC54','Documented legacy chamber exterior, revised radial and thrust bearings, hub, torque link and frame connection. One development unit; supplier fit and maximum output unresolved.'],
 ['coach-c53','Earlier inboard disc brake · C5.3','brakec53.js?v=C53-V2','mountBrakeC53','Available replacement rotor, custom hub, axle-following carrier and articulated frame reaction. Unrated development assembly.'],
 ['drivetrain-dt4','Locomotive motor & axle · DT4 R2','drivetrain-dt4.js?v=DT4-R2','mountDrivetrain','Updated motor body, mounting flange, pilot and shaft reference parts. Exploded view available; coupling and carrier remain unfinished spaces.'],
 ['coach-c52','Tread-brake mechanism · C5.2','brakec52.js','mountBrakeC52','One-axle development module with purchased component envelopes and fabricated rigging. Released shoe clearance fails; do not fabricate.'],
 ['coach-c5','Sprung passenger-coach trucks · current brake','coach-current.js?v=C56-R0','mountTruckC5','Current truck with one C5.6 installation. Remaining stations are undeveloped.'],
 ['coach-c4','Accessible coach: side doorway and boarding','coach-current.js','mountAccessC4','Side-loading doorway, removable station bridge and structural securement interfaces; vendor and station reservations are explicit.'],
 ['coach-c31','Folding seats: locks, guards and floor connections','coach-current.js','mountSeatsC31','Actual lock and guard parts with reinforced floor connections; prototype and joint acceptance remain open.'],
 ['accessible-c3','Accessible folding seat · C3','seatsc3.js','mountSeatsC3','Physical folding-seat candidate. Open coach-c3.html for three motion states and all passenger modes.'],
 ['coach-c3','Accessible coach · C3 space layout','seatsc3.js','mountCoachC3','Two physical folding seats with inherited accessible-body and fixed-seat space reservations. Complete accessible coach remains unfinished.'],
 ['seats-c21','Braced bench & compact feet · C2.1','seatsc21.js','mountSeatsC21','Latest bench candidate: four coped braces and compact ribbed floor mounts. Preliminary; local joint and fabrication acceptance remain open.'],
 ['coach-c21','Coach with braced benches · C2.1','seatsc21.js','mountCoachC21','Sixteen copies of the C2.1 bench at retained coach locations. 32 places; complete coach remains unfinished.'],
 ['seats-c2','Bench & floor attachments · C2','seatsc2.js','mountSeatsC2','New physical bench, four-bolt foot proposal, revised floor openings and nominal hardware. Preliminary; joint release, panel fasteners, finishes and tests remain open.'],
 ['coach-c2','Coach with physical benches · C1 + C2','seatsc2.js','mountCoachC2','C2 benches installed at all sixteen retained locations in C1. No change to the regular 32-seat target; complete coach remains unfinished.'],
 ['body-c1','Regular coach body · C1 physical assembly','bodyc1.js','mountBodyC1','New physical body and J01 joint proposal with retained J1a members. Seats remain space references; trucks, stairs, couplers, HVAC mounts and finish connections are incomplete.'],
 ['frame','Coach underframe · J1a','framej3d.js','mountFrameJViewer','110 nominal member shells; joints, truck mounts and saw-cut lengths remain incomplete.'],
 ['connections','Frame connections · I1','connections3d.js','mountConnectionsViewer','Local connection studies; these assemblies are not installed in the J1a model.'],
 ['drawbar','Custom drawbar · DB01','drawbar3d.js','mountDrawbar','Nominal one-piece part only; pins, bearings, retention and frame attachments remain open.'],
 ['coach','Regular & accessible coaches','viewer3d.js','mountCoachViewer','Earlier space models; body, floor and suspension details are not a coordinated fabrication design.'],
 ['parts','Individual frame parts · H1','fabrication3d.js','mountFabricationViewer','Earlier part studies; use current J/I comparison and unresolved fabrication notes.'],
 ['turning','Truck turning demonstration','turning3d.js','mountTurningViewer','Display-only motion demonstration; wheel, axle and truck sizes are not selected.'],
 ['integration','Equipment installation study · F1','integration3d.js','mountIntegrationViewer','Earlier packaging only; rooftop HVAC is superseded by the mini-split direction and brakes are now air.'],
 ['clearance','Wheel clearance alternatives','clearance3d.js','mountClearanceViewer','Unselected clearance alternatives; verify actual running gear before use.'],
 ['chassis','Chassis alternatives','chassis3d.js','mountChassisViewer','Earlier comparison models; J1a is the later integrated member study.'],
 ['assembly','Earlier coach assemblies','assembly3d.js','mountAssemblyViewer','Earlier assembly studies; incomplete and superseded interfaces remain visible.'],
 ['mockups','Adult-scale interior mockups','mockup3d.js','mountMockupViewer','Mockup alternatives; occupied trials and accessibility acceptance remain open.']
];
const currentModelIds=["drivetrain-dt5", "coach-assembled", "coach-brake-truck", "coach-c57", "coach-bearing-cw3", "coach-c5", "coach-c4", "coach-c31", "seats-c21", "coach-c21", "body-c1"];
modelDefinitions.splice(0,modelDefinitions.length,...modelDefinitions.filter(d=>!currentModelIds.includes(d[0])));
const mounted=new Map();
async function showModel(){
 const d=modelDefinitions.find(x=>x[0]===modelSelect.value);if(!d)return;
 $('#model-note').textContent=d[4];document.querySelectorAll('.model-pane').forEach(p=>p.hidden=p.dataset.model!==d[0]);
 if(mounted.has(d[0]))return;
 const host=document.createElement('div');host.className='model-pane';host.dataset.model=d[0];host.textContent='Loading model…';$('#model-hosts').append(host);mounted.set(d[0],host);
 try{
  const m=await import('./'+d[2]);
  if(d[0]==='drawbar')host.innerHTML='<div class="actions"><button class="button" data-drawbar-view="iso">Isometric</button><button class="button" data-drawbar-view="top">Top</button><button class="button" data-drawbar-view="side">Side</button></div><div data-drawbar-canvas class="drawbar-canvas"></div><p data-drawbar-status>Loading nominal CAD…</p>';
  await m[d[3]](host);
 }catch(e){host.innerHTML='<p>The model could not load. The drawing sheets remain available.</p><button type="button" class="button">Try again</button>';host.querySelector('button').addEventListener('click',()=>{mounted.delete(d[0]);host.remove();showModel();});console.error(e);}
}
modelSelect.innerHTML=modelDefinitions.map(d=>'<option value="'+d[0]+'">'+esc(d[1])+'</option>').join('');modelSelect.addEventListener('change',()=>{location.hash='models/'+modelSelect.value;showModel();});route();
fetch('assets/site-organization/archive-drawing-catalog.json?v=LT25').then(r=>{if(!r.ok)throw new Error('Drawing catalog unavailable');return r.json();}).then(data=>{
 catalog=data;$('#assembly-select').innerHTML=data.packages.map(p=>'<option value="'+esc(p.id)+'">'+esc(p.title)+'</option>').join('');
 $('#fabrication-cards').innerHTML=data.fabrication.map(f=>'<article class="fab-summary"><h2>'+esc(f.title)+'</h2><dl><dt>Available</dt><dd>'+esc(f.available)+'</dd><dt>Connection / material status</dt><dd>'+esc(f.connection)+'</dd><dt>Resolve before fabrication</dt><dd>'+esc(f.hold)+'</dd></dl><div class="actions"><button type="button" class="button" data-package="'+esc(f.package)+'">Drawings</button><a class="button" href="'+esc(f.engineering)+'">Engineering ↗</a></div></article>').join('');
 document.querySelectorAll('[data-package]').forEach(b=>b.addEventListener('click',()=>{$('#assembly-select').value=b.dataset.package;$('#drawing-search').value='';sheets();location.hash='drawings/'+b.dataset.package;}));route();
}).catch(e=>{$('#sheet-grid').innerHTML='<p>Drawings could not load. <a href="engineering.html#drawings">Open the preserved drawing reader</a>.</p>';console.error(e);});
