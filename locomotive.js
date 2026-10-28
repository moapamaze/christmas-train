import * as THREE from './assets/vendor/three.module.js';
import {OrbitControls} from './assets/vendor/OrbitControls.js';
import {read,table} from './locomotive-data.js';
const [b,parts,interfaces]=await Promise.all([read('model.json'),read('component-schedule.json'),read('interfaces.json')]);
table('parts-table',['ID','Assembly','Qty','Make / buy','Proposed definition','Unfinished detail'],parts.rows);
table('interfaces-table',['ID','Interface','Retained / proposed','Open input','Coordination owner'],interfaces.rows);
const host=document.getElementById('viewer'),status=document.getElementById('model-status');
try{
const g=b.proposed_geometry, scene=new THREE.Scene();scene.background=new THREE.Color('#e2e8e7');
const camera=new THREE.PerspectiveCamera(38,1,10,150000),renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;host.append(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.target.set(7600,1000,0);controls.maxDistance=52000;controls.minDistance=2000;
scene.add(new THREE.HemisphereLight(0xffffff,0x56696b,2.5));const sun=new THREE.DirectionalLight(0xffffff,3);sun.position.set(-7000,14000,9000);scene.add(sun);
const shell=new THREE.Group(),gear=new THREE.Group(),zones=new THREE.Group(),frame=new THREE.Group();scene.add(shell,gear,zones,frame);zones.visible=false;
const mats={black:new THREE.MeshStandardMaterial({color:0x202a30,roughness:.65}),steel:new THREE.MeshStandardMaterial({color:0x596972,metalness:.65,roughness:.4}),silver:new THREE.MeshStandardMaterial({color:0x9faeb4,metalness:.7,roughness:.3}),glass:new THREE.MeshStandardMaterial({color:0x8eb2c0,transparent:true,opacity:.6}),gold:new THREE.MeshStandardMaterial({color:0xd0a25c,transparent:true,opacity:.7}),green:new THREE.MeshStandardMaterial({color:0x659b89,transparent:true,opacity:.7}),rail:new THREE.MeshStandardMaterial({color:0x7a8586})};
function mesh(group,geom,x,y,z,mat){const m=new THREE.Mesh(geom,mat);m.position.set(x,z,y);group.add(m);return m}
function box(group,x,y,z,l,w,h,mat){return mesh(group,new THREE.BoxGeometry(l,h,w),x,y,z,mat)}
function cyl(group,x,y,z,r,len,axis,mat,r2=r){const m=mesh(group,new THREE.CylinderGeometry(r,r2,len,40),x,y,z,mat);if(axis==='x')m.rotation.z=Math.PI/2;if(axis==='y')m.rotation.x=Math.PI/2;return m}
function bar(group,a,b,width,mat){const A=new THREE.Vector3(a[0],a[2],a[1]),B=new THREE.Vector3(b[0],b[2],b[1]);const d=B.clone().sub(A),m=new THREE.Mesh(new THREE.CylinderGeometry(width,width,d.length(),12),mat);m.position.copy(A.add(B).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());group.add(m);return m}
// Nominal wheel envelopes, not a rail profile or machining model.
function wheel(x,y,r,spoked=true){const wg=new THREE.Group();wg.position.set(x,r,y);gear.add(wg);const ring=new THREE.Mesh(new THREE.TorusGeometry(r-35,35,10,48),mats.silver);wg.add(ring);const hub=new THREE.Mesh(new THREE.CylinderGeometry(95,95,110,28),mats.steel);hub.rotation.x=Math.PI/2;wg.add(hub);
 if(spoked)for(let i=0;i<12;i++){const a=i*Math.PI/6,m=new THREE.Mesh(new THREE.BoxGeometry(45,r-150,45),mats.steel);m.position.set(Math.sin(a)*(r-150)/2,Math.cos(a)*(r-150)/2,0);m.rotation.z=-a;wg.add(m)}
 else{const m=new THREE.Mesh(new THREE.CylinderGeometry(r-40,r-40,70,32),mats.steel);m.rotation.x=Math.PI/2;wg.add(m)}
}
for(const [axles,r] of [[g.drive_axles,500],[g.leading_axles.concat(g.trailing_axles,g.tender_axles),300]])for(const x of axles){for(const y of [-507.2,507.2])wheel(x,y,r,r===500);cyl(gear,x,0,r,65,1110,'y',mats.steel)}
// Running-gear carriers and support symbols. Joint sizing remains open.
for(const [x,l,z] of [[1200,900,720],[3300,1900,1050],[6000,1900,1050],[8300,1600,720],[11400,1800,720],[14000,1800,720]]){
 for(const y of [-730,730])box(gear,x,y,z,l,130,170,mats.steel);
 box(gear,x,0,z,220,1500,160,mats.steel);cyl(gear,x,0,z+140,110,180,'z',mats.silver);
}
for(const x of g.powered_truck_centres)for(const y of [-730,730])for(const dx of [-600,600]){
 for(let k=0;k<5;k++){const ring=mesh(gear,new THREE.TorusGeometry(80,14,8,18),x+dx,y,760+k*45,mats.silver);ring.rotation.x=Math.PI/2;}
}
// Main underframe and tender frame: envelopes only, no member schedule implied.
for(const y of [-850,850]){box(frame,4900,y,990,9200,160,280,mats.steel);box(frame,12700,y,690,5000,160,260,mats.steel)}
for(const x of [600,2100,4600,7100,9300])box(frame,x,0,990,140,1850,220,mats.steel);
for(const x of [10400,11400,12700,14000,15000])box(frame,x,0,690,140,1850,220,mats.steel);
// Boiler shell is a non-pressure removable cover.
cyl(shell,4500,0,2050,850,5800,'x',mats.black);cyl(shell,1560,0,2050,865,90,'x',mats.steel);
cyl(shell,1480,0,2250,150,120,'x',mats.gold);
for(const x of [1900,3500,5200,7000]){const ring=mesh(shell,new THREE.TorusGeometry(855,16,8,40),x,0,2050,mats.steel);ring.rotation.y=Math.PI/2}
cyl(shell,2125,0,3125,175,550,'z',mats.black,145);cyl(shell,3900,0,2980,250,250,'z',mats.black);cyl(shell,5600,0,2970,220,220,'z',mats.black);
// Walking boards and recessed decorative cylinder housings.
for(const y of [-1110,1110]){box(shell,4500,y,1220,5600,380,70,mats.black);cyl(shell,1950,y,750,230,750,'x',mats.black);bar(shell,[2300,y,2500],[6900,y,2500],22,mats.silver)}
box(shell,7600,0,1180,2200,2600,60,mats.black); // corrected cab floor below using shared centre
shell.children.at(-1).position.x=8400;
// Open cab framework, opaque lower panels and visible windows.
for(const y of [-1280,1280]){
 box(shell,8400,y,1650,2200,40,1000,mats.black);
 for(const x of [7340,8270,9460])box(shell,x,y,2600,80,80,1300,mats.black);
 box(shell,8400,y,3160,2200,60,180,mats.black);
 box(shell,7775,y,2575,650,30,750,mats.glass);box(shell,8775,y,2575,850,30,750,mats.glass);
}
box(shell,8400,0,3250,2350,2720,100,mats.black);
// Cab front and rear side strips leave apertures; not a certified entry/egress arrangement.
for(const x of [7340,9460])for(const y of [-1020,1020])box(shell,x,y,2300,60,500,1900,mats.black);
for(const y of [-1100,-800,-500,-200,100,400,700,1000])bar(shell,[0,y,150],[700,y,850],35,mats.steel);
box(shell,600,0,850,250,2450,170,mats.black);
// Tender skins and bunker outline, leaving a genuine cavity when viewed from above.
box(shell,12700,0,830,5000,2600,80,mats.black);
for(const y of [-1280,1280])box(shell,12700,y,1750,5000,40,1900,mats.black);
for(const x of [10220,15180])box(shell,x,0,1750,40,2560,1900,mats.black);
box(shell,13600,0,2700,3200,2600,80,mats.black);box(shell,11100,0,2350,1600,2300,80,mats.black);
for(const y of [-1050,1050])bar(shell,[10400,y,2450],[11800,y,2700],30,mats.steel);
// Unagreed coupler proxy, a positional marker only.
bar(frame,[9600,0,650],[10200,0,650],65,mats.gold);box(frame,15400,0,650,400,140,120,mats.gold);
// Clearly identified equipment reservations. Engine cube uses verified overall OEM envelope.
box(zones,3450,0,2050,2100,1200,1000,mats.gold);box(zones,3500,0,1800,856,557,749,mats.steel);
box(zones,1800,0,2050,800,1100,1000,mats.green);box(zones,5750,0,2050,1700,1200,1000,mats.green);
box(zones,11200,0,1350,1400,1500,900,mats.gold);box(zones,13650,0,1650,2300,1800,1600,mats.green);
for(const x of g.powered_truck_centres)box(zones,x,0,1250,600,500,350,mats.gold);
// Ground and track are context only; 914.4 between visual rail inner faces.
for(const y of [-482.2,482.2])box(frame,7700,y,-35,17500,50,70,mats.rail);
for(let x=-800;x<16500;x+=650)box(frame,x,0,-110,160,1650,110,mats.steel);
const grid=new THREE.GridHelper(24000,24,0xb9c7c8,0xcbd5d4);grid.position.set(7600,-180,0);scene.add(grid);
const labels=[];function label(text,x,y,z,zone=false){const el=document.createElement('span');el.className='label';el.textContent=text;host.append(el);labels.push({el,p:new THREE.Vector3(x,z,y),zone})}
label('Leading axle',1200,-900,950);label('Powered truck A',3300,-900,1400);label('Powered truck B',6000,-900,1400);label('Operator cab',8500,0,3550);label('Tender',13100,0,3000);
label('Engine + pump reservation',3450,0,2900,true);label('Oil / air reservation',5750,0,2900,true);label('Utility / optional generator',13650,0,2600,true);
function view(v){const c={iso:[-5000,10500,17000],side:[7600,3500,23500],top:[7600,23000,1],front:[-12000,2500,0]};camera.position.set(...c[v]);controls.target.set(7600,1100,0);controls.update()}
document.querySelectorAll('[data-view]').forEach(el=>el.onclick=()=>view(el.dataset.view));
document.getElementById('shell').onchange=e=>{shell.visible=e.target.checked};document.getElementById('zones').onchange=e=>{zones.visible=e.target.checked};
document.getElementById('explode').oninput=e=>{shell.position.y=Number(e.target.value)};
const resize=()=>{renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix()};new ResizeObserver(resize).observe(host);resize();view('iso');status.remove();
function render(){requestAnimationFrame(render);controls.update();const show=document.getElementById('labels').checked;for(const l of labels){const p=l.p.clone().project(camera);l.el.hidden=!show||(l.zone&&!zones.visible)||p.z>1||p.z<-1||Math.abs(p.x)>1||Math.abs(p.y)>1;l.el.style.left=(p.x+1)*host.clientWidth/2+'px';l.el.style.top=(1-p.y)*host.clientHeight/2+'px'}renderer.render(scene,camera)}render();
}catch(e){status.textContent='3D could not start on this device. The dimensioned SVG drawings above remain available.';console.error(e)}
