import * as THREE from './assets/vendor/three.module.js';
import {OrbitControls} from './assets/vendor/OrbitControls.js';
const modal=document.querySelector('#drawing-dialog');
document.querySelectorAll('[data-sheet]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();document.querySelector('#full-sheet').src=a.href;document.querySelector('#sheet-title').textContent=a.dataset.sheet+' · mm';modal.showModal();}));
document.querySelector('#close-sheet').onclick=()=>modal.close();
const host=document.querySelector('#viewer'),status=document.querySelector('#model-status');
try {
const data=await fetch('assets/drivetrain-dt2/model.json.gz').then(r=>new Response(r.body.pipeThrough(new DecompressionStream('gzip'))).json());
const scene=new THREE.Scene();scene.background=new THREE.Color('#e4eaea');
const camera=new THREE.PerspectiveCamera(38,1,1,40000);const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.append(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.target.set(0,600,0);controls.minDistance=1200;controls.maxDistance=12000;
scene.add(new THREE.HemisphereLight(0xffffff,0x536674,2.5));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-1800,4000,2500);scene.add(light);
const frame=new THREE.Group(),wheels=new THREE.Group(),envelopes=new THREE.Group(),conflicts=new THREE.Group();scene.add(frame,wheels,envelopes,conflicts);envelopes.visible=false;conflicts.visible=false;const meshes=[];
for(const part of data.parts){const geom=new THREE.BufferGeometry();const positions=[];for(const tri of part.triangles)for(const i of tri){const v=part.vertices[i];positions.push(v[0],v[2],-v[1]);}geom.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geom.computeVertexNormals();const mat=new THREE.MeshStandardMaterial({color:part.category==='frame'?0x294e64:part.category==='wheel'?0x81949e:0xa4afb4,metalness:.45,roughness:.48,side:THREE.DoubleSide});const mesh=new THREE.Mesh(geom,mat);mesh.userData=part;(part.category==='frame'?frame:wheels).add(mesh);meshes.push(mesh);const edges=new THREE.LineSegments(new THREE.EdgesGeometry(geom,30),new THREE.LineBasicMaterial({color:0x263b46,transparent:true,opacity:.38}));mesh.add(edges);}
function env(group,x,y,z,l,w,h,color){const geom=new THREE.BoxGeometry(l,h,w),mat=new THREE.MeshBasicMaterial({color,transparent:true,opacity:.17,depthWrite:false});const m=new THREE.Mesh(geom,mat);m.position.set(x,z,-y);group.add(m);const e=new THREE.LineSegments(new THREE.EdgesGeometry(geom),new THREE.LineBasicMaterial({color}));e.position.copy(m.position);group.add(e);}
for(const x of [-600,600])for(const y of [-730,730]){env(envelopes,x,y,500,200,180,180,0xb87925);env(envelopes,x,y,782.5,140,140,305,0xb87925);}
env(envelopes,0,0,800,800,500,240,0xb87925);
for(const y of [-850,850])env(conflicts,0,y,990,2600,160,280,0xcc3d32);
const grid=new THREE.GridHelper(5000,25,0xaebfc1,0xc9d4d5);grid.position.y=-15;scene.add(grid);
function view(v){const positions={iso:[2600,2300,2900],side:[0,650,4200],top:[0,4500,.01],end:[4200,650,0]};camera.position.set(...positions[v]);controls.target.set(0,600,0);controls.update();}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));
document.querySelector('#show-frame').onchange=e=>frame.visible=e.target.checked;document.querySelector('#show-wheels').onchange=e=>wheels.visible=e.target.checked;document.querySelector('#show-env').onchange=e=>envelopes.visible=e.target.checked;document.querySelector('#show-conflict').onchange=e=>conflicts.visible=e.target.checked;
const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
renderer.domElement.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY]});renderer.domElement.addEventListener('pointerup',e=>{if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>8)return;const b=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-b.left)/b.width*2-1,-(e.clientY-b.top)/b.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes.filter(m=>m.parent.visible),false)[0];if(hit){const p=hit.object.userData;document.querySelector('#part-info').textContent=p.id+' · '+p.name+' · modeled mass '+p.mass_kg.toFixed(1)+' kg';}});
new ResizeObserver(()=>{renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}).observe(host);view('iso');status.remove();
function draw(){requestAnimationFrame(draw);controls.update();renderer.render(scene,camera)}draw();
}catch(e){status.textContent='3D could not load on this device. Dimensioned drawings and STEP downloads remain available.';console.error(e)}
