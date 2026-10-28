import {decodeModelResponse} from './lt3-model.js?v=gzip-transport-c2';
import * as THREE from './assets/vendor/three.module.js';
import {OrbitControls} from './assets/vendor/OrbitControls.js';
export async function mountDrivetrain(host){
 host.innerHTML=`<div class="toolbar"><button data-view="iso">Whole truck</button><button data-view="motor">Motor close-up</button><button data-view="top">Top</button><button data-view="side">Side</button><label><input type="checkbox" data-explode>Explode motor</label><label><input type="checkbox" data-context checked>Wheels / frame</label><label><input type="checkbox" data-reserves checked>Unfinished spaces</label></div><div class="dt4-canvas" style="height:520px;position:relative;touch-action:none;background:#e4eaea"><p data-status>Loading R2 assembly…</p></div><p data-part-info>Select a part to see its dimensions and design status.</p>`;
 const canvas=host.querySelector('.dt4-canvas'),status=host.querySelector('[data-status]');
 try{
 const response=await fetch('assets/drivetrain-dt4/model.json.gz?v=DT4-R2');if(!response.ok)throw Error('Model unavailable');const data=await decodeModelResponse(response);
 const scene=new THREE.Scene();scene.background=new THREE.Color('#e4eaea');
 const camera=new THREE.PerspectiveCamera(38,1,1,40000),renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));Object.assign(renderer.domElement.style,{display:"block",width:"100%",height:"100%",touchAction:"none"});canvas.style.overflow="hidden";canvas.append(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.minDistance=180;controls.maxDistance=14000;
 scene.add(new THREE.HemisphereLight(0xffffff,0x536674,2.5));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(-1800,4000,-2500);scene.add(light);
 const meshes=[];
 for(const p of data.parts){
 const geo=new THREE.BufferGeometry(),pos=[];for(const tri of p.triangles)for(const i of tri){const v=p.vertices[i];pos.push(v[0],v[2],-v[1]);}geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geo.computeVertexNormals();
 const reserved=p.category==='reserve',m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:new THREE.Color(...p.color),roughness:.6,metalness:.1,transparent:reserved,opacity:reserved?.14:1,depthWrite:!reserved,side:THREE.DoubleSide}));m.userData=p;scene.add(m);meshes.push(m);
 m.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo,35),new THREE.LineBasicMaterial({color:reserved?new THREE.Color(...p.color):0x263b46,transparent:true,opacity:reserved?.75:.25})));
 }
 const grid=new THREE.GridHelper(4000,20,0xaebfc1,0xc9d4d5);grid.position.y=-15;scene.add(grid);
 let current='motor';
 function update(){const close=current==='motor',explode=host.querySelector('[data-explode]').checked,context=host.querySelector('[data-context]').checked,res=host.querySelector('[data-reserves]').checked;
 for(const m of meshes){const p=m.userData;m.position.z=explode?-p.explode*p.side:0;m.visible=(!close||p.axle===1)&&((p.category!=='frame'&&p.category!=='wheel')||context)&&(p.category!=='reserve'||res);if(close&&(p.id.startsWith('Wheel')||p.id==='Axlebox_reserve_1_0'))m.visible=false;}
 grid.visible=!close;}
 function view(v){current=v;const close=v==='motor';camera.position.set(...{iso:[2700,2200,-3300],motor:[-90,1050,-2200],side:[0,650,-4400],top:[0,5000,.01]}[v]);controls.target.set(...(close?[-700,500,-1080]:[0,550,0]));update();controls.update();}
 host.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));host.querySelectorAll('input').forEach(i=>i.onchange=update);
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down;
 renderer.domElement.addEventListener('pointerdown',e=>down=[e.clientX,e.clientY]);renderer.domElement.addEventListener('pointerup',e=>{if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>8)return;const b=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-b.left)/b.width*2-1,-(e.clientY-b.top)/b.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes.filter(m=>m.visible),false)[0];if(hit)host.querySelector('[data-part-info]').textContent=hit.object.userData.name+' — '+hit.object.userData.status;});
 const resize=()=>{if(!canvas.clientWidth)return;renderer.setSize(canvas.clientWidth,canvas.clientHeight,false);camera.aspect=canvas.clientWidth/canvas.clientHeight;camera.updateProjectionMatrix();};new ResizeObserver(resize).observe(canvas);resize();view('motor');status.remove();
 function draw(){requestAnimationFrame(draw);if(!canvas.clientWidth)return;controls.update();renderer.render(scene,camera);}draw();
 }catch(e){status.textContent='3D could not load on this device. The assembled and exploded drawings are available below.';console.error(e);}
}
const own=document.querySelector('[data-dt4-viewer]');if(own)mountDrivetrain(own);
const modal=document.querySelector('#drawing-dialog');if(modal){document.querySelectorAll('[data-sheet]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();document.querySelector('#full-sheet').src=a.href;document.querySelector('#sheet-title').textContent=a.dataset.sheet+' · reference drawing · mm';modal.showModal();}));document.querySelector('#close-sheet').onclick=()=>modal.close();}
