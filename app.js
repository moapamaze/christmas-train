'use strict';
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sections = {readiness:'Actual source and build readiness',trackcivil:'Track, survey and station interfaces',systems:'HVAC and electrical reconciliation',coachbody:'Coach space and floor connection audit',propulsion:'Locomotive drive matching',couplings:'Couplings and drawbars',brakeselection:'Truck and brake development',overview:'Project overview',fabrication:'Custom fabrication',wheelset:'Wheelset and brake-mount drawings',phase3k:'Phase 3K air-brake integration',brakes:'Explore the brake controls',phase3j:'Phase 3J structural assembly',framej:'Inspect the coordinated frame',phase3i:'Phase 3I connection development',connections:'Inspect connection details',phase3h:'Phase 3H parts and connections',parts:'Inspect individual parts',phase3g:'Phase 3G pivoting undercarriage',turning:'Watch the bogies turn',phase3f:'Phase 3F prototype integration',integration:'Inspect installation study',phase3e:'Phase 3E clearance and prototype',clearance:'Inspect clearance alternatives',phase3d:'Phase 3D component integration',chassis:'Compare chassis alternatives',phase3c:'Phase 3C assembly development',assembly:'Inspect assembly studies',phase3:'Phase 3A engineering basis',phase3b:'Phase 3B prototype package',mockups:'Compare interior mockups',specification:'Design basis',models:'Rotate 3D models',drawings:'Drawing reader',technical:'Technical pages',views:'Still coach views',build:'Build package status',scope:'Review scope',holds:'Engineering holds',downloads:'Files & response'};
let viewerPromise;
function loadCoachViewer() {
  if (viewerPromise) return;
  viewerPromise=import('./viewer3d.js').then(module=>module.mountCoachViewer($('#coach-model-viewer'))).catch(error=>{
    viewerPromise=null;
    const host=$('#coach-model-viewer');
    host.innerHTML='<div class="card"><h2>The 3D viewer could not load.</h2><p>Check your connection, then try again. The still views remain available.</p><button class="button" type="button" id="retry-viewer">Try again</button> <a class="button" href="#views">Open still views</a></div>';
    $('#retry-viewer').onclick=loadCoachViewer;
    console.error(error);
  });
}
let assemblyViewerPromise;
function loadAssemblyViewer(){
 if(assemblyViewerPromise)return;
 assemblyViewerPromise=import('./assembly3d.js').then(m=>m.mountAssemblyViewer($('#assembly-model-viewer'))).catch(error=>{
  assemblyViewerPromise=null;
  $('#assembly-model-viewer').innerHTML='<div class="card"><h2>The assembly viewer could not load.</h2><p>Static views and dimensioned drawings remain available.</p><button class="button" id="retry-assembly">Try again</button></div>';
  $('#retry-assembly').onclick=loadAssemblyViewer;console.error(error);
 });
}
let mockupViewerPromise;
function loadMockupViewer(){
 if(mockupViewerPromise)return;
 mockupViewerPromise=import('./mockup3d.js').then(m=>m.mountMockupViewer($('#mockup-model-viewer'))).catch(error=>{
  mockupViewerPromise=null;
  $('#mockup-model-viewer').innerHTML='<div class="card"><h2>The mockup viewer could not load.</h2><p>The static views below and dimensioned drawings remain available.</p><button class="button" id="retry-mockup">Try again</button></div>';
  $('#retry-mockup').onclick=loadMockupViewer;console.error(error);
 });
}

let chassisViewerPromise;
function loadChassisViewer(){
 if(chassisViewerPromise)return;
 chassisViewerPromise=import('./chassis3d.js').then(m=>m.mountChassisViewer($('#chassis-model-viewer'))).catch(error=>{
  chassisViewerPromise=null;
  $('#chassis-model-viewer').innerHTML='<div class="card"><h2>The chassis viewer could not load.</h2><p>Still views and drawings remain available below.</p><button class="button" id="retry-chassis">Try again</button></div>';
  $('#retry-chassis').onclick=loadChassisViewer;console.error(error);
 });
}

let turningViewerPromise;
function loadTurningViewer(){
 if(turningViewerPromise)return;
 turningViewerPromise=import('./turning3d.js').then(m=>m.mountTurningViewer($('#turning-model-viewer'))).catch(error=>{
  turningViewerPromise=null;
  $('#turning-model-viewer').innerHTML='<div class="card"><h2>The turning viewer could not load.</h2><p>The drawing sheets and static views remain available.</p><button class="button" type="button" id="retry-turning">Try again</button> <a class="button" href="#phase3g">Open Phase 3G drawings</a></div>';
  $('#retry-turning').onclick=loadTurningViewer;console.error(error);
 });
}

let integrationViewerPromise;
function loadIntegrationViewer(){
 if(integrationViewerPromise)return;
 integrationViewerPromise=import('./integration3d.js').then(m=>m.mountIntegrationViewer($('#integration-model-viewer'))).catch(error=>{
  integrationViewerPromise=null;
  $('#integration-model-viewer').innerHTML='<div class="card"><h2>The installation viewer could not load.</h2><p>Static views and dimensioned drawings remain available below.</p><button class="button" id="retry-integration">Try again</button></div>';
  $('#retry-integration').onclick=loadIntegrationViewer;console.error(error);
 });
}

let clearanceViewerPromise;
function loadClearanceViewer(){
 if(clearanceViewerPromise)return;
 clearanceViewerPromise=import('./clearance3d.js').then(m=>m.mountClearanceViewer($('#clearance-model-viewer'))).catch(error=>{
  clearanceViewerPromise=null;
  $('#clearance-model-viewer').innerHTML='<div class="card"><h2>The clearance viewer could not load.</h2><p>Static views and dimensioned drawings remain available below.</p><button class="button" id="retry-clearance">Try again</button></div>';
  $('#retry-clearance').onclick=loadClearanceViewer;console.error(error);
 });
}

let fabricationViewerPromise;
function loadFabricationViewer(){
 if(fabricationViewerPromise)return;
 fabricationViewerPromise=import('./fabrication3d.js').then(m=>m.mountFabricationViewer($('#fabrication-model-viewer'))).catch(error=>{
  fabricationViewerPromise=null;
  $('#fabrication-model-viewer').innerHTML='<div class="card"><h2>The part viewer could not load.</h2><p>Static views and dimensioned sheets remain available.</p><button class="button" type="button" id="retry-fabrication">Try again</button> <a class="button" href="#phase3h-drawings-anchor">Open drawings</a></div>';
  $('#retry-fabrication').onclick=loadFabricationViewer;console.error(error);
 });
}

let connectionsViewerPromise;
function loadConnectionsViewer(){
 if(connectionsViewerPromise)return;
 connectionsViewerPromise=import('./connections3d.js').then(m=>m.mountConnectionsViewer($('#connections-model-viewer'))).catch(error=>{
  connectionsViewerPromise=null;
  $('#connections-model-viewer').innerHTML='<div class="card"><h2>The connection viewer could not load.</h2><p>The static views and dimensioned sheets remain available.</p><button class="button" type="button" id="retry-connections">Try again</button> <a class="button" href="#phase3i-drawings-anchor">Open drawings</a></div>';
  $('#retry-connections').onclick=loadConnectionsViewer;console.error(error);
 });
}

let frameJPromise;
function loadFrameJViewer(){
 if(frameJPromise)return;
 frameJPromise=import('./framej3d.js').then(m=>m.mountFrameJViewer($('#framej-model-viewer'))).catch(error=>{
 frameJPromise=null;$('#framej-model-viewer').innerHTML='<div class="card"><h2>The frame viewer could not load.</h2><p>The static views and dimensioned drawings remain available.</p><button class="button" id="retry-framej">Try again</button></div>';
 $('#retry-framej').onclick=loadFrameJViewer;console.error(error);
 });
}
let brakeKPromise;
function loadBrakeKViewer(){
 if(brakeKPromise)return;
 brakeKPromise=import('./brakesk.js').then(m=>m.mountBrakeViewer($('#brake-model-viewer'))).catch(error=>{
 brakeKPromise=null;$('#brake-model-viewer').innerHTML='<div class="card"><h2>The brake study could not load.</h2><p>The drawings and report remain available.</p><button class="button" id="retry-brakes">Try again</button></div>';
 $('#retry-brakes').onclick=loadBrakeKViewer;console.error(error);
 });
}
let drawbarPromise;
function loadDrawbarViewer(){
 if(!drawbarPromise)drawbarPromise=import('./drawbar3d.js').then(m=>m.mountDrawbar(document.getElementById('drawbar-viewer'))).catch(()=>{drawbarPromise=null;document.querySelector('[data-drawbar-status]').textContent='The3Dmodule could not load; the dimensioned drawing and staticCADview remain available.';});
}
function navigate() {
  const rawTab = location.hash.slice(1).split('/')[0] || 'overview';
  const tab = rawTab.startsWith('coach-c') ? 'coachbody' : rawTab.startsWith('readiness-') ? 'readiness' : rawTab.startsWith('trackcivil-') ? 'trackcivil' : rawTab.startsWith('systems-') ? 'systems' : rawTab.startsWith('coachbody-') ? 'coachbody' : rawTab.startsWith('propulsion-') ? 'propulsion' : rawTab.startsWith('couplings-') ? 'couplings' : rawTab.startsWith('brakeselection-') ? 'brakeselection' : rawTab.startsWith('wheelset-') ? 'wheelset' : rawTab.startsWith('phase3k-') ? 'phase3k' : rawTab.startsWith('phase3j-') ? 'phase3j' : rawTab.startsWith('phase3i-') ? 'phase3i' : rawTab.startsWith('phase3h-') ? 'phase3h' : rawTab.startsWith('phase3g-') ? 'phase3g' : rawTab.startsWith('phase3f-') ? 'phase3f' : rawTab.startsWith('phase3e-') ? 'phase3e' : rawTab.startsWith('phase3d-') ? 'phase3d' : rawTab.startsWith('phase3c-') ? 'phase3c' : rawTab.startsWith('phase3b-') ? 'phase3b' : rawTab.startsWith('phase3-') ? 'phase3' : rawTab;
  const selected = sections[tab] ? tab : 'overview';
  $$('.panel').forEach(el => el.classList.toggle('active', el.id === selected));
  $$('[data-tab]').forEach(el => { const active=el.dataset.tab===selected; el.classList.toggle('active',active); active ? el.setAttribute('aria-current','page') : el.removeAttribute('aria-current'); });
  $('#page-title').textContent=sections[selected];
  document.title=sections[selected]+' · Pulsipher Farms Train Review';
  if(rawTab.startsWith('coach-c')||rawTab.startsWith('readiness-')||rawTab.startsWith('trackcivil-')||rawTab.startsWith('systems-')||rawTab.startsWith('coachbody-')||rawTab.startsWith('propulsion-')||rawTab.startsWith('couplings-')||rawTab.startsWith('brakeselection-')||rawTab.startsWith('wheelset-')||rawTab.startsWith('phase3k-')||rawTab.startsWith('phase3j-')||rawTab.startsWith('phase3i-')||rawTab.startsWith('phase3h-')||rawTab.startsWith('phase3g-')||rawTab.startsWith('phase3f-')||rawTab.startsWith('phase3e-')||rawTab.startsWith('phase3d-')||rawTab.startsWith('phase3-')||rawTab.startsWith('phase3b-')||rawTab.startsWith('phase3c-'))requestAnimationFrame(()=>document.getElementById(rawTab)?.scrollIntoView()); else window.scrollTo(0,0);
  if(selected==='couplings')loadDrawbarViewer();
  if(selected==='models')loadCoachViewer();
  if(selected==='mockups')loadMockupViewer();
  if(selected==='assembly')loadAssemblyViewer();
  if(selected==='chassis')loadChassisViewer();
  if(selected==='clearance')loadClearanceViewer();
  if(selected==='integration')loadIntegrationViewer();
  if(selected==='turning')loadTurningViewer();
  if(selected==='parts')loadFabricationViewer();
  if(selected==='connections')loadConnectionsViewer();
  if(selected==='framej')loadFrameJViewer();
  if(selected==='brakes')loadBrakeKViewer();
}
window.addEventListener('hashchange',navigate);
navigate();

const specification = [
 ['Train configuration','1 locomotive + 4 coaches','Three regular coaches and one separate accessible coach; diesel propulsion.'],
 ['Longitudinal grade','0% level-track design target','Owner direction. Engineer-set tolerances and surveyed as-built elevations remain required; drainage is separate.'],
 ['Brake direction · CR-G01','Air service + spring parking','Investigate commonly sourced semi-truck combination chambers. Chamber force/stroke, rail foundation brake, reservoirs, controls and emergency/separation behavior require a coordinated design.'],
 ['Track gauge','36 in / 914.4 mm candidate','Confirm wheel–rail geometry, axle loads, CG, stability and route compatibility before selection.'],
 ['Regular coach cabin','26 ft outside / 104 in clear width','312 in outside length; provisional 3 in end walls give 306 in clear length. Outside width 110 in.'],
 ['Regular seating','32 fixed places','8 rows; two 40 in benches per row; 24 in nominal centre aisle. Comfort and evacuation are unverified.'],
 ['Accessible coach','11 fixed seats + 2 wheelchair bays','36 in continuous route; 60 in front turning circle; 36 × 60 in bays. Classification, securement and evacuation remain open.'],
 ['Coach envelope','33 ft 4 in overall study length','26 ft cabin plus 44 in end platform at each end. All clearances and stair interfaces require review.'],
 ['Bogie / floor reference','216 in centres; baseline 28 in / J1a study 32 in floor','Phase 3J retains the F1/E1 raised-floor study. No actual bogie or suspension is selected; floor height remains unapproved.'],
 ['Doors','Regular: 32 in / accessible ends: 36 in','Clear-width study inputs. Accessible front side openings are 42 in. Mechanisms, occupied approaches and rescue interfaces need verification.'],
 ['Hotel power','Scenario-dependent; equipment selection open','Phase 3D separates thermal demand from electrical input. Confirm exact HVAC running/starting loads, heater type, generator derating, protection and equipment space.'],
 ['Planning curve reference','50 m radius','Vehicle-specific minimum radius and all steady/reverse-curve swept envelopes require verification.']
];
$('#spec-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Interface</th><th>Current study</th><th>Qualification</th></tr></thead><tbody>'+specification.map(r=>'<tr>'+r.map(v=>'<td>'+escapeHtml(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';

const trades = [
 {title:'Locomotive & propulsion',scope:'Existing engineered locomotive or custom diesel propulsion beneath a steam-era body. Treat the complete train and hotel-power packaging as coordinated loads.',evidence:'Exact manufacturer/model; continuous and starting tractive effort; driven mass and adhesion basis; speed/grade/curve limits; cooling, emissions/exhaust, reverse duty and maintenance access.',interfaces:'Wheel–rail geometry, drawbar height, brake controls, electrical supply, operating visibility and loaded train mass.'},
 {title:'Frames, bogies & running gear',scope:'Engineered undercarriages and a frame load path for the regular and accessible coaches. Compare purchased assemblies with specialist fabrication.',evidence:'Rated axle and truck loads; wheel profile/back-to-back; bearings, suspension and fatigue basis; material and fabrication requirements; measured/predicted mass and CG.',interfaces:'Rail head, turnouts/check rails, body mounts, brake equipment, coupler loads, platform supports and dynamic clearances.'},
 {title:'Brakes & inter-car connections',scope:'Complete service, emergency, parking and separation response on the locomotive and every car. CR-G01: air service and spring-applied, air-released parking are now preferred; evaluate readily sourced combination chambers with engineered rail foundation brakes.',evidence:'Documented brake architecture and ratings; power/line failure response; brake balance, heat and holding capacity; coupling tension/compression, articulation, retention, wear and inspection.',interfaces:'Control continuity, stored energy, hoses/jumpers, frame attachments and curve/reverse-curve envelope. No pin or weld size is approved.'},
 {title:'Coach bodies & accessibility',scope:'Light, durable enclosed bodies, benches, doors, glazing, platforms and protected stairs. Develop a complete accessible boarding and evacuation solution.',evidence:'Structural/fire/egress basis; materials and weight takeoff; six-adult occupied mockup; representative mobility-device trials; boarding equipment and rescue procedure.',interfaces:'Frame/body load transfer, floor height, station gaps, stair swept envelope, doors/guards/gates, HVAC ducts, lighting and service access.'},
 {title:'HVAC & electrical systems',scope:'Heating, cooling and ventilation for Southern Nevada conditions; train power distribution, protected emergency lighting and independent emergency supply.',evidence:'Performance curves at actual ambient/altitude; ventilation basis; sensible/latent loads; starting currents; continuous generator rating and derating; protection and bonding design.',interfaces:'Equipment volume/mass, condensate, vibration/noise, flexible inter-car connections, exhaust/intake separation and maintenance access.'},
 {title:'Track, stations & installation',scope:'Survey-led alignment and track design, drainage/subgrade, turnouts, crossings, stations, storage and maintenance access. Plan qualified farm-crew installation tasks.',evidence:'Design criteria and tolerances; wheel–rail interface; curve/grade limits; installation sequence; training/pilot section; inspection records and independent release requirements.',interfaces:'Vehicle swept envelope, station access, boarding height/gap, buried utilities, emergency access and multi-train operations if later adopted.'}
];
$('#trade-grid').innerHTML=trades.map((t,i)=>'<article class="card trade-card"><span class="trade-number">PACKAGE '+String(i+1).padStart(2,'0')+'</span><h2>'+t.title+'</h2><p>'+t.scope+'</p><h3>Evidence to provide</h3><p>'+t.evidence+'</p><h3>Interfaces to coordinate</h3><p>'+t.interfaces+'</p></article>').join('');

const holds = [
 ['H01','Authority & design basis','Confirm the applicable vehicle/service classification, approval pathway and responsible engineering disciplines.','Document the authority decisions, standards basis, design loads and responsibility matrix.'],
 ['H02','Gauge, running gear & stability','36 in gauge and the 104 in clear cabin are study choices. Matching gauge alone does not establish compatibility.','Close wheel–rail/turnout geometry, axle loads, CG, wheel unloading, suspension, wind/crosslevel and buff-force cases.'],
 ['H03','Traction & adhesion','The owner requires level track. Actual driven axle mass, curve resistance and wet/contaminated rail still govern the 14.5 tonne locomotive assembly study.','Provide an integrated mass, grade, curve, start/reverse and continuous-duty performance case with documented derating.'],
 ['H04','Complete braking system','CR-G01 prefers air service and spring parking. Actual chamber, foundation brake and complete failure response remain unresolved.','Demonstrate service, emergency, parking, continuity and breakaway behavior, including delay, balance, heat and power/line loss.'],
 ['H05','Connections & swept envelope','The 30 in end gap, 14 in pin setbacks and 58 in reference line are unvalidated articulation inputs.','Engineer tension/compression, slack impact, fatigue, combined loads, retention, frame attachment and full articulation.'],
 ['H06','Occupied interior & evacuation','Seat counts and nominal aisles are not approved occupant loads. End zones shrink when occupied legs and feet are included.','Test full-size rows with varied adults in winter clothing; verify occupied door approaches, evacuation and emergency exits.'],
 ['H07','Accessible boarding & rescue','Two wheelchair bays and a continuous route reserve space; they do not complete the accessible system.','Verify classification, representative devices, boarding lift/ramp, securement/orientation, companion use and route-side rescue.'],
 ['H08','Power, HVAC & equipment envelope','Generator packages cannot be assumed to fit under the provisional 28 in coach floor.','Resolve delivered performance, starting loads, protection/bonding, emergency supply, ventilation/exhaust and service access.'],
 ['H09','Track & installation release','No surveyed alignment or construction tolerances are approved by these drawings.','Complete survey/geotechnical and track design; define permitted crew work, specialist supervision, pilot section, inspections and as-built records.'],
 ['H10','Prototype & commissioning','Geometry files and calculation screens do not authorize passenger operation.','Complete fabrication QA, staged empty/ballasted trials, braking/parking/separation tests, boarding/evacuation drills and release documentation.']
];
$('#hold-list').innerHTML=holds.map(h=>'<article class="hold"><span class="hold-id">'+h[0]+'</span><div><h2>'+h[1]+'</h2><p>'+h[2]+'</p></div><div><label>EVIDENCE TO CLOSE</label><p>'+h[3]+'</p></div></article>').join('');

function setupReader(element, doc) {
  if(!element)return;
  if(!doc){element.innerHTML='<p>This document is unavailable in the loaded revision. Reload the page to update it.</p>';return;}
  let current=0, mode='image', zoom='fit';
  element.innerHTML='<div class="reader"><div class="reader-toolbar"><button type="button" data-action="prev" aria-label="Previous page">←</button><select aria-label="Choose document page">'+doc.pages.map((p,i)=>'<option value="'+i+'">'+(p.originalPage ? 'Report p. '+p.originalPage : 'Sheet '+p.number)+' · '+escapeHtml(p.title)+'</option>').join('')+'</select><button type="button" data-action="next" aria-label="Next page">→</button><button type="button" data-action="zoom">Enlarge</button><button type="button" data-action="text">Read text</button><input class="search" type="search" aria-label="Search this document" placeholder="Search document…"></div><div class="search-results" aria-live="polite"></div><div class="reader-viewport"><img class="reader-image" alt=""><pre class="reader-text" hidden></pre></div><div class="reader-caption"><span class="page-caption"></span><a class="text-link" href="'+doc.pdf+'" target="_blank" rel="noopener">Open PDF ↗</a></div></div>';
  const image=$('.reader-image',element), text=$('.reader-text',element), select=$('select',element), viewport=$('.reader-viewport',element);
  function show() {
    const p=doc.pages[current];
    image.src=p.image;image.alt=p.title+' — '+(p.originalPage ? 'original report page '+p.originalPage : 'sheet '+p.number);
    image.style.setProperty('--zoom-width',p.width+'px');image.classList.toggle('zoom',zoom==='large');
    image.hidden=mode==='text';text.hidden=mode!=='text';text.textContent=p.text;select.value=String(current);
    $('.page-caption',element).textContent=(p.originalPage ? 'Original report page '+p.originalPage : 'Sheet '+p.number)+' · '+(current+1)+' of '+doc.pages.length+' · R0';
    $('[data-action="prev"]',element).disabled=current===0;$('[data-action="next"]',element).disabled=current===doc.pages.length-1;
    $('[data-action="text"]',element).textContent=mode==='text'?'View page':'Read text';
    $('[data-action="zoom"]',element).textContent=zoom==='large'?'Fit width':'Enlarge';$('[data-action="zoom"]',element).disabled=mode==='text';
    viewport.scrollTo({top:0,left:0});
  }
  $('[data-action="prev"]',element).onclick=()=>{if(current>0){current--;show();}};
  $('[data-action="next"]',element).onclick=()=>{if(current<doc.pages.length-1){current++;show();}};
  $('[data-action="zoom"]',element).onclick=()=>{zoom=zoom==='fit'?'large':'fit';show();};
  $('[data-action="text"]',element).onclick=()=>{mode=mode==='image'?'text':'image';show();};
  select.onchange=()=>{current=Number(select.value);show();};
  $('.search',element).oninput=event=>{
    const query=event.target.value.trim().toLowerCase(),results=$('.search-results',element);
    if(!query){results.innerHTML='';return;}
    const matches=doc.pages.map((p,i)=>({p,i})).filter(({p})=>(p.title+' '+p.text).toLowerCase().includes(query));
    results.innerHTML=matches.length ? matches.map(({p,i})=>'<button type="button" data-page="'+i+'">'+escapeHtml((p.originalPage?'Report p. '+p.originalPage:'Sheet '+p.number)+' · '+p.title)+'</button>').join('') : '<p>No matching pages.</p>';
    $$('[data-page]',results).forEach(button=>button.onclick=()=>{current=Number(button.dataset.page);show();});
  };
  show();
}
const dialog=$('#image-dialog');
$('#dialog-close').onclick=()=>dialog.close();
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
import('./lt3-model.js').then(({loadCompressedModel})=>loadCompressedModel(new URL('assets/documents.json.gz',document.baseURI))).then(data=>{
  $('#connection-option-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Study</th><th>Defined geometry</th><th>Engineering decision</th></tr></thead><tbody>'+(data.connectionOptions||[]).map(r=>'<tr>'+r.map(c=>'<td>'+escapeHtml(c)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
  setupReader($('#brake-page-drawing-reader'),data.documents.find(d=>d.id==='phase3k-drawings'));
  setupReader($('#phase3k-report-reader'),data.documents.find(d=>d.id==='phase3k-report'));
  setupReader($('#phase3k-drawing-reader'),data.documents.find(d=>d.id==='phase3k-drawings'));
  setupReader($('#phase3j-report-reader'),data.documents.find(d=>d.id==='phase3j-report'));
  setupReader($('#phase3j-drawing-reader'),data.documents.find(d=>d.id==='phase3j-drawings'));
  $('#framej-static-views').innerHTML=(data.frameJViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
  setupReader($('#phase3i-report-reader'),data.documents.find(d=>d.id==='phase3i-report'));
  setupReader($('#phase3i-drawing-reader'),data.documents.find(d=>d.id==='phase3i-drawings'));
  $('#connections-static-views').innerHTML=(data.connectionViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
  setupReader($('#phase3h-report-reader'),data.documents.find(d=>d.id==='phase3h-report'));
  setupReader($('#phase3h-drawing-reader'),data.documents.find(d=>d.id==='phase3h-drawings'));
  renderPhase3H(data);
  setupReader($('#phase3g-report-reader'),data.documents.find(d=>d.id==='phase3g-report'));
  setupReader($('#phase3g-drawing-reader'),data.documents.find(d=>d.id==='phase3g-drawings'));
  renderPhase3G(data);
  setupReader($('#phase3f-report-reader'),data.documents.find(d=>d.id==='phase3f-report'));
  setupReader($('#phase3f-drawing-reader'),data.documents.find(d=>d.id==='phase3f-drawings'));
  renderPhase3F(data);
  setupReader($('#phase3e-report-reader'),data.documents.find(d=>d.id==='phase3e-report'));
  setupReader($('#phase3e-drawing-reader'),data.documents.find(d=>d.id==='phase3e-drawings'));
  renderPhase3E(data);
  setupReader($('#phase3d-report-reader'),data.documents.find(d=>d.id==='phase3d-report'));
  setupReader($('#phase3d-drawing-reader'),data.documents.find(d=>d.id==='phase3d-drawings'));
  $('#chassis-static-views').innerHTML=(data.chassisViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
  $('#chassis-comparison-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Study</th><th>Steel members</th><th>Maximum cabin grid</th><th>Bare steel mass</th></tr></thead><tbody>'+(data.chassisComparison||[]).map(a=>'<tr><td>'+escapeHtml(a.id+' — '+a.label)+'</td><td>'+a.member_count+'</td><td>'+a.cabin_grid_max_in+' in</td><td>'+Math.round(a.bare_steel_mass_kg).toLocaleString()+' kg</td></tr>').join('')+'</tbody></table></div>';
  setupReader($('#phase3c-report-reader'),data.documents.find(d=>d.id==='phase3c-report'));
  setupReader($('#phase3c-drawing-reader'),data.documents.find(d=>d.id==='phase3c-drawings'));
  $('#assembly-static-views').innerHTML=(data.assemblyViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
  setupReader($('#phase3b-report-reader'),data.documents.find(d=>d.id==='phase3b-report'));
  setupReader($('#phase3b-drawing-reader'),data.documents.find(d=>d.id==='phase3b-drawings'));
  $('#mockup-static-views').innerHTML=(data.mockupViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
  setupReader($('#phase3-report-reader'),data.documents.find(d=>d.id==='phase3-report'));
  setupReader($('#phase3-drawing-reader'),data.documents.find(d=>d.id==='phase3-drawings'));
  setupReader($('#drawing-reader'),data.documents.find(d=>d.id==='stage2-drawings'));
  setupReader($('#technical-reader'),data.documents.find(d=>d.id==='stage2-technical'));
  $('#view-grid').innerHTML=data.views.map((view,i)=>'<button class="view-card" type="button" data-view="'+i+'"><img src="'+view.image+'" alt="'+escapeHtml(view.title)+'" loading="lazy"><span class="view-label">'+escapeHtml(view.title)+'<span aria-hidden="true">↗</span></span></button>').join('');
  $$('#view-grid [data-view]').forEach(button=>button.onclick=()=>{
    const view=data.views[Number(button.dataset.view)];$('#dialog-title').textContent=view.title;$('#dialog-image').src=view.image;$('#dialog-image').alt=view.title;dialog.showModal();
  });
  $('#download-list').innerHTML=data.downloads.map(file=>'<article class="download-item"><span class="filetype">'+file.type+'</span><div><h2>'+escapeHtml(file.title)+'</h2><p>'+escapeHtml(file.detail)+'</p></div><span class="file-size">'+(file.bytes>1048576 ? (file.bytes/1048576).toFixed(1)+' MB' : Math.ceil(file.bytes/1024)+' KB')+'</span><a class="button" href="'+file.url+'" download>Download ↓</a></article>').join('');
}).catch(error=>{
  for(const id of ['brake-page-drawing-reader','phase3k-report-reader','phase3k-drawing-reader','phase3j-report-reader','phase3j-drawing-reader','phase3i-report-reader','phase3i-drawing-reader','phase3h-report-reader','phase3h-drawing-reader','phase3g-report-reader','phase3g-drawing-reader','phase3f-report-reader','phase3f-drawing-reader','phase3e-report-reader','phase3e-drawing-reader','phase3d-report-reader','phase3d-drawing-reader','phase3c-report-reader','phase3c-drawing-reader','phase3b-report-reader','phase3b-drawing-reader','phase3-report-reader','phase3-drawing-reader','drawing-reader','technical-reader','download-list'])$('#'+id).innerHTML='<div class="card"><h2>Document data could not load.</h2><p>Reload the page to try again. The drawing PDF is available below.</p><a class="button" href="assets/files/Christmas_Train_Stage2_Drawings_R0.pdf">Open drawing PDF</a></div>';
  console.error(error);
});


function renderPhase3E(data){
 const compare=data.clearanceComparison||[];
 $('#clearance-comparison-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Study</th><th>Finished floor</th><th>Bare steel</th><th>Modeled steel members</th></tr></thead><tbody>'+compare.map(a=>'<tr><td>'+escapeHtml(a.id+' — '+a.label)+'</td><td>'+a.finished_floor_in+' in</td><td>'+Math.round(a.bare_steel_mass_kg).toLocaleString()+' kg</td><td>'+a.member_count+'</td></tr>').join('')+'</tbody></table></div>';
 $('#clearance-static-views').innerHTML=(data.clearanceViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
 const profiles=data.clearanceProfiles||[];
 const select=$('#clearance-profile');
 function showProfile(){
  const rows=profiles.filter(r=>r.case.profile_id===select.value);
  $('#clearance-profile-result').innerHTML='<div class="table-wrap"><table><thead><tr><th>Frame</th><th>Worst sampled gap / bound</th><th>What it establishes</th><th>Illustrative floor for 25.4 mm reserve</th></tr></thead><tbody>'+rows.map(r=>{
   const exact=r.worst.method==='EXACT_ZERO_ROLL_CYLINDER';
   const finding=exact?(r.worst.gap_mm<0?'Cylinder proxy intersects modeled member':'Cylinder proxy clears at sampled positions'):(r.worst.gap_mm<0?'Bounding envelopes overlap; exact fit unresolved':'Positive gap between bounding envelopes at sampled positions');
   return '<tr><td>'+escapeHtml(r.alternative_id)+'</td><td>'+r.worst.gap_mm.toFixed(1)+' mm</td><td>'+finding+'</td><td>'+r.floor_for_25p4mm_proxy_gap_in.toFixed(2)+' in</td></tr>';
  }).join('')+'</tbody></table></div><p>Illustrative floor values translate the frame vertically with the trial wheel envelope fixed. The 25.4 mm reserve is a comparison input, not an approved clearance requirement. Other components, continuous motion, support height and stability still require engineering.</p>';
 }
 select.onchange=showProfile;showProfile();
 const packs=data.verificationPackages||[];
 $('#verification-packages').innerHTML=packs.map(p=>'<details class="card"><summary><strong>'+escapeHtml(p.id+' · '+p.title)+'</strong></summary><p>'+escapeHtml(p.scope)+'</p><h3>Evidence to return</h3><ul>'+p.evidence.map(t=>'<li>'+escapeHtml(t)+'</li>').join('')+'</ul><p><strong>Review lead:</strong> '+escapeHtml(p.owner)+'</p><p class="fineprint">UNSENT · Actual offered configuration, ratings, price, availability and acceptance remain blank in the editable records.</p></details>').join('');
}

function renderPhase3F(data){
 const zones=data.installationZones||[];
 const range=a=>a.map(n=>Number(n.toFixed(1))).join(' to ');
 $('#installation-zone-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Reservation</th><th>Purpose</th><th>X / Y / Z limits, inches</th><th>Coordination</th></tr></thead><tbody>'+zones.map(z=>'<tr><td>'+escapeHtml(z.id+' · '+z.name)+'</td><td>'+escapeHtml(z.kind)+'</td><td>'+escapeHtml(['x','y','z'].map(k=>k.toUpperCase()+': '+range(z.bounds_in[k])).join('; '))+'</td><td>'+escapeHtml(z.coordination_note||z.status)+'</td></tr>').join('')+'</tbody></table></div>';

 $('#integration-static-views').innerHTML=(data.integrationViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
 $('#prototype-work-packages').innerHTML=(data.prototypeWorkPackages||[]).map(p=>'<details class="card"><summary><strong>'+escapeHtml(p.id+' · '+p.title)+'</strong></summary><p>'+escapeHtml(p.work)+'</p><p><strong>Responsible:</strong> '+escapeHtml(p.owner)+'</p><p><strong>Release evidence:</strong> '+escapeHtml(p.release)+'</p><p class="fineprint">'+escapeHtml(p.status)+'</p></details>').join('');
}

function renderPhase3G(data){
 $('#turning-static-views').innerHTML=(data.turningViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
 $('#bogie-interface-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Interface</th><th>Evidence needed</th><th>Status</th></tr></thead><tbody>'+(data.bogieInterfaces||[]).map(r=>'<tr><td>'+escapeHtml(r.title)+'</td><td>'+escapeHtml(r.evidence)+'</td><td>'+escapeHtml(r.status||'OPEN')+'</td></tr>').join('')+'</tbody></table></div>';
}

function renderPhase3H(data){
 $('#fabrication-static-views').innerHTML=(data.fabricationViews||[]).map(v=>'<figure class="card"><img src="'+v.image+'" alt="'+escapeHtml(v.title)+'" loading="lazy" style="width:100%"><figcaption>'+escapeHtml(v.title)+'</figcaption></figure>').join('');
 $('#frame-cut-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Group</th><th>Nominal section</th><th>Quantity</th><th>Length each</th><th>Material candidate</th></tr></thead><tbody>'+(data.frameCutGroups||[]).map(r=>'<tr><td>'+escapeHtml(r.id)+'</td><td>'+escapeHtml(r.section_name)+'</td><td>'+r.quantity+'</td><td>'+r.cut_envelope_length_in+' in / '+Number(r.cut_envelope_length_mm.toFixed(2))+' mm</td><td>'+escapeHtml(r.material_candidate)+'</td></tr>').join('')+'</tbody></table></div>';
 $('#connection-table').innerHTML='<div class="table-wrap"><table><thead><tr><th>Family</th><th>Parts that meet</th><th>Located ends</th><th>Release status</th></tr></thead><tbody>'+(data.frameConnectionFamilies||[]).map(r=>'<tr><td>'+escapeHtml(r.id)+'</td><td>'+escapeHtml(r.name)+'</td><td>'+r.connection_count+'</td><td>'+escapeHtml(r.release_status)+'</td></tr>').join('')+'</tbody></table></div>';
}

// Fabrication drawings remain visible without optional model code.
document.querySelectorAll('[data-fab-zoom]').forEach(button=>button.addEventListener('click',()=>{const sheet=button.closest('.fab-sheet');const on=sheet.classList.toggle('enlarged');button.textContent=on?'Fit drawing to width':'Enlarge drawing';button.setAttribute('aria-pressed',String(on));}));

import('./brake-selection.js').then(m=>m.mountBrakeSelection(document.getElementById('brake-selection-calculator'))).catch(()=>{const h=document.getElementById('brake-selection-calculator');if(h)h.insertAdjacentHTML('beforeend','<p>The interactive calculation could not load. Open the traceable calculation record below.</p>');});

import('./assets/track-r1/checker-ui.mjs').then(m=>m.mount(document.getElementById('track-geometry-checker'))).catch(()=>{const h=document.getElementById('track-geometry-checker');if(h)h.textContent='The browser tool could not load. Use the linked input templates and offline source.';});
