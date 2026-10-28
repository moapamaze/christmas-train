import * as THREE from './assets/vendor/three.module.js';
import {OrbitControls} from './assets/vendor/OrbitControls.js';
const modal=document.querySelector('#drawing-dialog');
document.querySelectorAll('[data-sheet]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();document.querySelector('#full-sheet').src=a.href;document.querySelector('#sheet-title').textContent=a.dataset.sheet+' · assembly proposal · mm';modal.showModal();}));
document.querySelector('#close-sheet').onclick=()=>modal.close();
const host=document.querySelector('#viewer'),status=document.querySelector('#model-status');
try{
 const response=await fetch('assets/drivetrain-dt3/model.json.gz');if(!response.ok)throw Error('Model unavailable');const bytes=new Uint8Array(await response.arrayBuffer());const data=(bytes[0]===31&&bytes[1]===139)?await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).json():JSON.parse(new TextDecoder().decode(bytes));
 const scene=new THREE.Scene();scene.background=new THREE.Color('#e4eaea');
 const camera=new THREE.PerspectiveCamera(38,1,1,40000),renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.append(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.target.set(0,600,0);controls.minDistance=400;controls.maxDistance=12000;
 scene.add(new THREE.HemisphereLight(0xffffff,0x536674,2.5));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-1800,4000,2500);scene.add(light);
 const groups={},meshes=[];for(const part of data.parts){if(!groups[part.category]){groups[part.category]=new THREE.Group();scene.add(groups[part.category]);}
 const geo=new THREE.BufferGeometry(),pos=[];for(const tri of part.triangles)for(const i of tri){const v=part.vertices[i];pos.push(v[0],v[2],-v[1]);}geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.computeVertexNormals();
 const envelope=part.id==='DT3-MOTOR';const mat=new THREE.MeshStandardMaterial({color:new THREE.Color(...part.color),metalness:.25,roughness:.56,side:THREE.DoubleSide,transparent:envelope,opacity:envelope?.28:1,depthWrite:!envelope});const m=new THREE.Mesh(geo,mat);m.userData=part;groups[part.category].add(m);meshes.push(m);
 const edge=new THREE.LineSegments(new THREE.EdgesGeometry(geo,35),new THREE.LineBasicMaterial({color:0x263b46,transparent:true,opacity:.3}));m.add(edge);}
 const grid=new THREE.GridHelper(4000,20,0xaebfc1,0xc9d4d5);grid.position.y=-15;scene.add(grid);
 function view(v){const p={iso:[2350,1900,2400],side:[0,650,3400],top:[0,3500,.01],end:[3400,650,0]};camera.position.set(...p[v]);controls.target.set(0,600,0);controls.update();}
 const toggles=['frame','wheel','case','mount','bearing','hose'];for(const c of toggles){const input=document.querySelector('#show-'+c);groups[c].visible=input.checked;input.onchange=()=>groups[c].visible=input.checked;}
 function preset(v){for(const c of ['frame','wheel','case']){groups[c].visible=v==='truck';document.querySelector('#show-'+c).checked=v==='truck';}view('iso');}
 document.querySelectorAll('[data-preset]').forEach(b=>b.onclick=()=>preset(b.dataset.preset));document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
 renderer.domElement.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY]});renderer.domElement.addEventListener('pointerup',e=>{if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>8)return;const b=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-b.left)/b.width*2-1,-(e.clientY-b.top)/b.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes.filter(m=>m.parent.visible),false)[0];if(hit){const p=hit.object.userData;document.querySelector('#part-info').textContent=p.id+' · '+p.name+' — '+p.status;}});
 new ResizeObserver(()=>{renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();}).observe(host);preset('drive');status.remove();
 function draw(){requestAnimationFrame(draw);controls.update();renderer.render(scene,camera);}draw();
}catch(e){status.textContent='3D could not load on this device. The dimensioned sheets and STEP downloads remain available.';console.error(e);}
