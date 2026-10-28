const $=s=>document.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pages=new Set(['drawings','models','fabrication','overview']);
function route(){
 const [raw,assembly]=location.hash.slice(1).split('/');
 if(raw&&!pages.has(raw)){location.replace('engineering.html'+location.hash);return;}
 const selected=raw==='overview'||!raw?'drawings':raw;
 if(selected!=='models'&&activeModel)clearModel();
 document.querySelectorAll('.shop-panel').forEach(p=>p.hidden=p.id!==selected);
 document.querySelectorAll('[data-page]').forEach(a=>{if(a.dataset.page===selected)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 const title={drawings:'Current drawings',models:'Rotatable 3D models',fabrication:'Fabrication notes'}[selected];$('#shop-title').textContent=title;document.title=title+' · Pulsipher Farms';
 if(selected==='models'&&modelSelect.options.length){
  if(assembly&&!currentModelIds.includes(assembly)){location.replace('archive-drawings.html#models/'+encodeURIComponent(assembly));return;}
  if(assembly&&[...modelSelect.options].some(option=>option.value===assembly))modelSelect.value=assembly;
  showModel();
 }
 if(selected==='drawings'&&catalog){
  if(assembly&&!catalog.packages.some(item=>item.id===assembly)){location.replace('archive-drawings.html#drawings/'+encodeURIComponent(assembly));return;}
  if(assembly&&catalog.packages.some(item=>item.id===assembly))$('#assembly-select').value=assembly;
  sheets();
 }
}
const modelSelect=$('#model-select');
window.addEventListener('hashchange',route);
let catalog,visibleSheets=[];
function sheets(){
 assemblyTabs($('#assembly-select').value);
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
 ['locomotive-lt33','Standard bump stop · LT33','lt33-ui.js?v=LT33','mountLT33','GMT catalog candidate and revised pedestal on current C2/LT32. Fabrication unreleased.'],
 ['locomotive-cab-c2','Cab C2 · cameras and left controls','cab-c2-ui.js?v=C2','mountCabC2','Roof-off, engineer-eye, camera coverage, exits, coach disconnects and reconciled LT32.'],
 ['locomotive-cab-c1','Cab interior · C1','cab-c1-ui.js?v=C1','mountCabC1','Roof-off, driver-eye and dimensioned seat / control layout. Exit, visibility, supplier controls and restraint acceptance remain open.'],
 ['locomotive-lt32','Coordinated locomotive + first coach · LT32','lt32-ui.js?v=LT32','mountLT32','Revised installation, rear connection and updated loads. Live hose articulation and supplier interfaces remain open; fabrication unreleased.'],
 ['locomotive-lt31-installation','Current installation and service · LT31','lt31-install-ui.js?v=LT31','mountLT31Installation','Removable pump joints and duct; checked service paths. Running-gear and supplier interfaces remain open; fabrication unreleased.'],
 ['locomotive-lt31','Locomotive + first coach · LT31','lt31-ui.js?v=LT31','mountLT31','Rear frame mount, turning, step clearance and two brake-line jumpers. Review candidate; fabrication unreleased.'],
 ['locomotive-lt30','Retained emergency restraint · LT30','lt30-ui.js?v=LT30','mountLT30','Captive core with residual pocket, both-truck failure poses and removal sections. Engineer load-path decision open; fabrication unreleased.'],
 ['locomotive-lt29','Archived restraint and connections · LT29','lt29-ui.js?v=LT29','mountLT29','Rigid versus absorbing catch, relieved cheeks, proposed fits and installation connections. No qualified catch; fabrication unreleased.'],
 ['locomotive-lt28','Archived coordinated locomotive · LT28','lt28-ui.js?v=LT28','mountLT28','Unified pivot, cooling, access, supports and routes; updated 50 m mass-based poses. Proposed tolerances and catch loads; fabrication unreleased.'],
 ['locomotive-lt27','Archived pivot candidate · LT27','lt27-ui.js?v=LT27','mountLT27','Compare ±14 mm candidate stops with retained ±10 mm travel. Provisional allowance; supplier ratings and fabrication release remain open.'],
 ['locomotive-lt26-installation','Engine installation & controls · LT26','lt26-install-ui.js?v=LT26I1','mountLT26Installation','Cooling/access candidates, 30 m connection corridors and proposed train brake schematic. Supplier and structural review holds remain.'],
 ['locomotive-lt26','Current locomotive motion · LT26','lt26-ui.js?v=LT26','mountLT26','Engine installation and retained trucks at 504 load positions on straight track and both 50 m curves. Discrete envelope screening; no operating release.'],
 ['locomotive-lt25','Retained AIE installation · LT25','lt25-ui.js?v=LT25','mountLT25','Current supplier-package installation, common skid and retained LT23 trucks. Engine internals are schematic; mount and power qualification remain open.'],
 ['locomotive-lt13','Curve clearance · LT13','lt13-workshop.js?v=LT13-R0','mountCurveClearance','50/30 m conditional placements reveal guide, cylinder, shell and frame clashes.'],
 ['locomotive-lt12','Inboard axle drive · LT12','lt12-workshop.js?v=LT12-R0','mountInboardDrive','Three inboard motor/chain reductions; development and supplier review.'],
 ['locomotive-lt11','Northern Railroad profile · LT11','lt11-workshop.js?v=LT11-R0','mountNorthernProfile','Lower 4-6-4 proportion concept; drivetrain and structure require redesign.'],
 ['coach-bearing-cw3','Bearing-end cutaway & assembly · CW3','coach-bearing.js?v=CW3','mountCW3','Centered spacer, recessed cover, grease labyrinth and retention. Proposed geometry; final qualification pending.'],
 ['coach-wheelset-cw2','Wheel profile & axle detail · CW2','coach-wheel-review.js?v=CW2','mountCW2','Axle machining review with separate wheel-profile, fit and seal holds. Drawings are for supplier review, not fabrication.'],
 ['coach-wheelset-cw1','Wheels & axle retention · CW1','coach-wheelset.js?v=CW1','mountCW1','Pressed wheels, shortened axles and positive bearing-nut locking. Final wheel profile, fits and engineering release pending.'],
 ['coach-assembled','Whole coaches + trucks + hitches','coach-assembled.js?v=CB2','mountConnectedCoaches','Whole regular coach or one accessible coach, with current trucks, brake units and hitch mounts. Use Connected coaches to see the drawbar.'],
 ['drivetrain-dt5','Powered axle mount · DT5','drivetrain-dt5.js?v=DT5-R1','mountDrivetrain','Separate bearing cartridges, roll cradles, motor carrier, coupling and hose routes. Exploded and suspension views; fabrication holds remain.'],
 ['coach-brake-truck','Passenger truck + body-to-truck air lines · C5.7','coach-brake-truck.js?v=CI3','mountBrakeTruckC57','One brake with supply hoses and maintenance details. Supplier matching, loads and full hose/service qualification remain open.'],
 ['coach-c57','Body-to-truck air lines · C5.7','brakec57.js?v=C57-R0','mountBrakeC57','Actual supply connections, supports and service paths; unresolved dimensions remain marked.'],
 ['coach-c56','Brake hoses and service · C5.6','brakec56.js?v=C56-R0','mountBrakeC56','Actual hose anchors and supported leads; service and mounting details with unresolved interfaces marked.'],
 ['coach-c55','Earlier brake ports and hoses · C5.5','brakec55.js?v=C55-R0','mountBrakeC55','Physical-port and hose geometry, with unresolved threaded engagement and supplier matching. One development installation.'],
 ['coach-c54','Earlier brake installation · C5.4','brakec54.js?v=C54-R0','mountBrakeC54','Documented legacy chamber exterior, revised radial and thrust bearings, hub, torque link and frame connection. One development unit; supplier fit and maximum output unresolved.'],
 ['coach-c53','Earlier inboard disc brake · C5.3','brakec53.js?v=C53-V2','mountBrakeC53','Available replacement rotor, custom hub, axle-following carrier and articulated frame reaction. Unrated development assembly.'],
 ['drivetrain-dt4','Locomotive motor & axle · DT4 R2','drivetrain-dt4.js?v=DT4-R2','mountDrivetrain','Updated motor body, mounting flange, pilot and shaft reference parts. Exploded view available; coupling and carrier remain unfinished spaces.'],
 ['coach-c52','Tread-brake mechanism · C5.2','brakec52.js','mountBrakeC52','One-axle development module with purchased component envelopes and fabricated rigging. Released shoe clearance fails; do not fabricate.'],
 ['coach-c5','Sprung passenger-coach trucks · current brake','coach-current.js?v=CI3','mountTruckC5','Current truck with one C5.7 installation. Remaining stations are undeveloped.'],
 ['coach-c4','Accessible coach: side doorway and boarding','coach-current.js','mountAccessC4','Side-loading doorway, removable station bridge and structural securement interfaces; vendor and station reservations are explicit.'],
 ['coach-c31','Folding seats: locks, guards and floor connections','coach-current.js','mountSeatsC31','Actual lock and guard parts with reinforced floor connections; prototype and joint acceptance remain open.'],
 ['accessible-c3','Accessible folding seat · C3','seatsc3.js','mountSeatsC3','Physical folding-seat candidate. Open coach-c3.html for three motion states and all passenger modes.'],
 ['coach-c3','Accessible coach · C3 space layout','seatsc3.js','mountCoachC3','Two physical folding seats with inherited accessible-body and fixed-seat space reservations. Complete accessible coach remains unfinished.'],
 ['seats-c21','Braced bench & compact feet · C2.1','seatsc21.js','mountSeatsC21','Latest bench candidate: four coped braces and compact ribbed floor mounts. Preliminary; local joint and fabrication acceptance remain open.'],
 ['coach-c21','Coach with braced benches · C2.1','seatsc21.js','mountCoachC21','Sixteen copies of the C2.1 bench at retained coach locations. 32 places; complete coach remains unfinished.'],
 ['seats-c2','Bench & floor attachments · C2','seatsc2.js','mountSeatsC2','New physical bench, four-bolt foot proposal, revised floor openings and nominal hardware. Preliminary; joint release, panel fasteners, finishes and tests remain open.'],
 ['coach-c2','Coach with physical benches · C1 + C2','seatsc2.js','mountCoachC2','C2 benches installed at all sixteen retained locations in C1. No change to the regular 32-seat target; complete coach remains unfinished.'],
 ['body-c1','Whole regular coach · C1 + current components','bodyc1.js?v=CB2','mountBodyC1','C1 body, C2.1 benches, current frame, two trucks, brake units and hitch mounts. CB1 removable boarding steps, end decks and guards are now shown; mounting strength, station height and final hardware remain open.'],
 ['frame','Coach underframe · J1a','framej3d.js?v=CI3','mountFrameJViewer','110 nominal member shells; joints, truck mounts and saw-cut lengths remain incomplete.'],
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
const currentModelIds=["locomotive-lt33", "locomotive-cab-c2", "locomotive-cab-c1", "locomotive-lt32", "locomotive-lt31-installation", "locomotive-lt31", "locomotive-lt30", "locomotive-lt29", "locomotive-lt28", "locomotive-lt27", "locomotive-lt26-installation", "locomotive-lt26", "locomotive-lt25", "locomotive-lt13", "locomotive-lt12", "locomotive-lt11", "drivetrain-dt5", "coach-assembled", "coach-brake-truck", "coach-c57", "coach-bearing-cw3", "coach-c5", "coach-c4", "coach-c31", "seats-c21", "coach-c21", "body-c1"];
modelDefinitions.splice(0,modelDefinitions.length,...modelDefinitions.filter(d=>currentModelIds.includes(d[0])).sort((a,b)=>currentModelIds.indexOf(a[0])-currentModelIds.indexOf(b[0])));
let activeModel,activeViewer,modelRequest=0;
function clearModel(){modelRequest++;activeViewer?.dispose?.();activeViewer=undefined;activeModel=undefined;$('#model-hosts').replaceChildren();}
function assemblyTabs(id){document.querySelectorAll('[data-page]').forEach(a=>{const page=a.dataset.page;if(page==='models')a.href='#models/'+(currentModelIds.includes(id)?id:modelSelect.value);if(page==='drawings')a.href='#drawings/'+(catalog?.packages.some(p=>p.id===id)?id:($('#assembly-select').value||''));});}

async function showModel(){
 const d=modelDefinitions.find(x=>x[0]===modelSelect.value);if(!d)return;
 assemblyTabs(d[0]);if($('#locomotive-shortcuts'))$('#locomotive-shortcuts').hidden=!d[0].startsWith('locomotive');$('#model-note').textContent=d[4];if(activeModel===d[0]){activeViewer?.refresh?.();return;}
 clearModel();activeModel=d[0];const request=modelRequest;
 const host=document.createElement('div');host.className='model-pane';host.dataset.model=d[0];host.textContent='Loading rotatable CAD…';$('#model-hosts').append(host);
 try{const m=await import('./'+d[2]);if(request!==modelRequest)return;const viewer=await m[d[3]](host);if(request!==modelRequest){viewer?.dispose?.();return;}activeViewer=viewer;
 }catch(e){if(request!==modelRequest)return;host.innerHTML='<p>The 3D model could not load.</p><button type="button" class="button">Retry 3D</button>';host.querySelector('button').onclick=()=>{clearModel();showModel();};console.error(e);}
}

modelSelect.innerHTML=modelDefinitions.map(d=>'<option value="'+d[0]+'">'+esc(d[1])+'</option>').join('');modelSelect.addEventListener('change',()=>{location.hash='models/'+modelSelect.value;showModel();});route();
fetch('assets/site-organization/current-drawing-catalog.json?v=LT25').then(r=>{if(!r.ok)throw new Error('Drawing catalog unavailable');return r.json();}).then(data=>{
 catalog=data;$('#assembly-select').innerHTML=data.packages.map(p=>'<option value="'+esc(p.id)+'">'+esc(p.title)+'</option>').join('');
 $('#fabrication-cards').innerHTML=data.fabrication.map(f=>'<article class="fab-summary"><h2>'+esc(f.title)+'</h2><dl><dt>Available</dt><dd>'+esc(f.available)+'</dd><dt>Connection / material status</dt><dd>'+esc(f.connection)+'</dd><dt>Resolve before fabrication</dt><dd>'+esc(f.hold)+'</dd></dl><div class="actions"><button type="button" class="button" data-package="'+esc(f.package)+'">Drawings</button><a class="button" href="'+esc(f.engineering)+'">Engineering ↗</a></div></article>').join('');
 document.querySelectorAll('[data-package]').forEach(b=>b.addEventListener('click',()=>{$('#assembly-select').value=b.dataset.package;$('#drawing-search').value='';sheets();location.hash='drawings/'+b.dataset.package;}));route();
}).catch(e=>{$('#sheet-grid').innerHTML='<p>Drawings could not load. <a href="engineering.html#drawings">Open the preserved drawing reader</a>.</p>';console.error(e);});
