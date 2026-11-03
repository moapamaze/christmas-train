// PF-3R1-R0. Data-quality/geometry review, NOT track acceptance or an alignment designer.
export const ISSUE='PF-3R1-R0';
const num=x=>typeof x==='number'&&Number.isFinite(x);
const text=x=>typeof x==='string'&&x.trim().length>0;
const distance=(a,b)=>Math.hypot(b.x-a.x,b.y-a.y);
export function analyze(data){
 const errors=[],warnings=[];
 const fail=s=>errors.push(s);
 if(!data||typeof data!=='object'||Array.isArray(data))return {issue:ISSUE,data_quality:'invalid',errors:['Input must be a JSON object.'],metrics:null,approved_for_construction:false,approved_for_operation:false};
 const meta=data.meta||{};const kind=data.dataset_kind;
 if(data.schema_version!==1)fail('schema_version must be1.');
 if(!['centerline_track_reference','rail_pair_asbuilt'].includes(kind))fail('Unsupported dataset_kind; ground terrain is not rail geometry.');
 for(const k of ['dataset_id','coordinate_system','vertical_datum','benchmark_id','axis_description','station_direction','survey_or_design_author','source_record_reference'])if(!text(meta[k]))fail('Missing metadata: '+k);
 if(meta.units!=='m')fail('Only explicitly declared metre inputs are accepted. Convert legacy units through the responsible surveyor; no guessed foot definition.');
 if(meta.coordinate_distance_basis!=='project_ground')fail('Coordinates must be consistent project-ground distances, not undeclared grid coordinates.');
 if(!['orthometric','local_level'].includes(meta.height_type))fail('Declare orthometric or local_level heights. Raw GNSS ellipsoidal heights are not accepted as level-rail elevations.');
 if(meta.stationing_basis!=='horizontal_plan_chainage')fail('Stationing must be declared horizontal_plan_chainage.');
 if(!['design','surveyed','synthetic'].includes(meta.record_state))fail('Declare record_state: design, surveyed or synthetic.');
 if(kind==='rail_pair_asbuilt'&&meta.record_state==='design')fail('Proposed rail coordinates cannot be labeled as-built.');
 if(!text(meta.elevation_reference))fail('Declare the exact rail/elevation measurement reference.');
 if(typeof meta.closed_loop_intended!=='boolean')fail('closed_loop_intended must be explicitly true or false.');
 if(meta.record_state==='synthetic')warnings.push('SYNTHETIC SOFTWARE TEST DATA — NOT FARM SURVEY OR A PROPOSED SITE ALIGNMENT.');
 if(meta.record_state==='surveyed'&&!text(meta.observation_date))fail('Surveyed data require an observation_date.');
 if(kind==='rail_pair_asbuilt'&&!text(meta.gauge_measurement_reference))warnings.push('Gauge measuring face/depth and instrument reference are not documented.');
 const input=data.rows;
 if(!Array.isArray(input)||input.length<2)fail('At least two ordered records are required.');
 if(Array.isArray(input)&&input.length>10000)fail('Desktop tool resource limit:10000records; split through responsible reviewer.');
 const points=[];const ids=new Set();
 if(Array.isArray(input)&&input.length<=10000)input.forEach((r,i)=>{
  const at='Row'+(i+1)+': ';
  if(!r||typeof r!=='object'){fail(at+'object required');return;}
  if(!text(r.id)||ids.has(r.id))fail(at+'id must be nonblank and unique');ids.add(r.id);
  if(!num(r.station_m))fail(at+'station_m must be finite numeric');
  let p;
  if(kind==='rail_pair_asbuilt'){
   for(const side of ['left','right'])for(const c of ['x_m','y_m','z_m'])if(!num(r[side]?.[c]))fail(at+side+'.'+c+' must be finite numeric');
   if(r.gauge_mm!==null&&r.gauge_mm!==undefined&&(!num(r.gauge_mm)||r.gauge_mm<=0))fail(at+'gauge_mm must be positive numeric or null');
   const a=r.left||{},b=r.right||{};
   const baseline=Math.hypot(b.x_m-a.x_m,b.y_m-a.y_m);
   if(num(baseline)&&baseline<=0)fail(at+'distinct rail-reference plan positions required');
   p={id:r.id,s:r.station_m,x:a.x_m/2+b.x_m/2,y:a.y_m/2+b.y_m/2,z:a.z_m/2+b.z_m/2,left_z:a.z_m,right_z:b.z_m,crosslevel_mm:(b.z_m-a.z_m)*1000,rail_reference_baseline_m:baseline,gauge_mm:r.gauge_mm??null};
   if(p.gauge_mm===null)warnings.push(at+'gauge not measured; it is not inferred from rail-reference coordinate spacing.');
  }else{
   for(const c of ['x_m','y_m','z_m'])if(!num(r[c]))fail(at+c+' must be finite numeric');
   p={id:r.id,s:r.station_m,x:r.x_m,y:r.y_m,z:r.z_m};
  }
  points.push(p);
 });
 if(!errors.length)for(const p of points)for(const [key,v] of Object.entries(p))if(typeof v==='number'&&!Number.isFinite(v))fail('Nonfinite derived point '+p.id+'.'+key+'; no analysis issued.');
 if(!errors.length)for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],ds=b.s-a.s,chord=distance(a,b);
  if(!num(ds)||!num(chord)){fail('Nonfinite derived interval/chord; numeric range cannot be analyzed.');continue;}
  if(ds<=0)fail('Stationing must increase strictly; rows are never silently sorted.');
  if(chord<=0)fail('Consecutive plan positions coincide; geometry cannot resolve a segment.');
  // Numerical roundoff guard only, NOT survey tolerance or acceptance allowance.
  if(ds+1e-7<chord)fail('Station interval is shorter than plan chord at '+a.id+'–'+b.id+'; check stationing/units/grid-ground basis.');
 }
 const source_metadata=Object.fromEntries(['units','coordinate_system','coordinate_distance_basis','axis_description','vertical_datum','height_type','benchmark_id','stationing_basis','station_direction','survey_or_design_author','source_record_reference','observation_date','elevation_reference','gauge_measurement_reference','closed_loop_intended'].map(k=>[k,meta[k]??null]));
 const base={issue:ISSUE,schema_version:1,dataset_id:meta.dataset_id??null,dataset_kind:kind??null,record_state:meta.record_state??null,source_metadata,errors,warnings,approved_for_construction:false,approved_for_operation:false,engineering_acceptance:null,accepted_limits:null};
 if(errors.length)return {...base,data_quality:'invalid',metrics:null};
 const segments=[],curves=[];
 for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i],ds=b.s-a.s;
  const r={from:a.id,to:b.id,from_station_m:a.s,to_station_m:b.s,interval_m:ds,plan_chord_m:distance(a,b),grade_percent:100*(b.z-a.z)/ds,grade_target_percent:0,grade_deviation_from_target_percent:100*(b.z-a.z)/ds};
  if(kind==='rail_pair_asbuilt')Object.assign(r,{left_rail_grade_percent:100*(b.left_z-a.left_z)/ds,right_rail_grade_percent:100*(b.right_z-a.right_z)/ds,rail_grade_basis:'Elevation change per CENTERLINE horizontal chainage, not each curved rail running length.',adjacent_sample_twist_mm_per_m:(b.crosslevel_mm-a.crosslevel_mm)/ds});
  segments.push(r);
 }
 for(let i=1;i<points.length-1;i++){
  const a=points[i-1],b=points[i],c=points[i+1],ab=distance(a,b),bc=distance(b,c),ac=distance(a,c);
  const cross=(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);
  if(!num(ab*bc*ac)||ab*bc*ac<=0||!num(cross)){fail('Nonfinite or underflowed curvature arithmetic at '+b.id+'; numeric range cannot be analyzed.');continue;}
  const k=ac>0?2*cross/(ab*bc*ac):null;
  const resolved=k!==null&&Math.abs(cross)>1e-12*ab*bc;
  curves.push({at:b.id,station_m:b.s,three_point_signed_curvature_per_m:resolved?k:0,three_point_radius_m:resolved?1/Math.abs(k):null,resolution:resolved?'three_sample_circumcircle':'collinear_or_unresolved',sample_window_m:c.s-a.s,meaning:'Three-point chord estimate only, not a designed circular/transition radius or guaranteed minimum between samples.'});
 }
 const first=points[0],last=points.at(-1);
 const closure=meta.closed_loop_intended===true?{last_minus_first_x_m:last.x-first.x,last_minus_first_y_m:last.y-first.y,plan_misclosure_m:distance(first,last),vertical_misclosure_m:last.z-first.z,meaning:'Requires a repeated end observation/station at the start control point and a surveyor closure report. Tool does not invent or append a closing segment.'}:null;
 if(closure&&kind==='rail_pair_asbuilt')Object.assign(closure,{left_rail_vertical_misclosure_m:last.left_z-first.left_z,right_rail_vertical_misclosure_m:last.right_z-first.right_z,crosslevel_misclosure_mm:last.crosslevel_mm-first.crosslevel_mm,independent_gauge_difference_mm:first.gauge_mm===null||last.gauge_mm===null?null:last.gauge_mm-first.gauge_mm});
 if(closure)warnings.push('Closed-loop declaration does not establish closure or a safe loop: inspect the repeated end control and adjustment report. No loop-seam tangent/curvature check is performed.');
 warnings.push('No construction or operating pass/fail: actual vehicle/track geometry limits, sampling density, survey uncertainty and accountable acceptance remain unspecified.');
 if(kind==='rail_pair_asbuilt')warnings.push('Twist is between adjacent samples, NOT a truck-wheelbase acceptance check. Left/right reference equivalence and cross-section orientation must be verified.');
 warnings.push('Zero average grade does not demonstrate zero crosslevel/twist, drainage, bearing capacity, settlement or stability.');
 const metrics={points:points.map(p=>({...p,grade_basis:'track reference, not terrain',gauge_deviation_from_36in_evaluation_mm:p.gauge_mm===undefined||p.gauge_mm===null?null:p.gauge_mm-914.4})),segments,curves,loop_closure:closure,observed_station_extent_m:last.s-first.s};
 function finiteTree(x){if(typeof x==='number')return Number.isFinite(x);if(Array.isArray(x))return x.every(finiteTree);if(x&&typeof x==='object')return Object.values(x).every(finiteTree);return true;}
 if(!finiteTree(metrics))fail('A derived result exceeds finite numeric range; no geometry analysis issued.');
 if(errors.length)return {...base,data_quality:'invalid',metrics:null};
 return {...base,data_quality:'analyzable_not_accepted',metrics,formulas:{grade:'100*(z2-z1)/(s2-s1); chainage declared CENTERLINE horizontal plan, including left/right rail rise rates',crosslevel_mm:'1000*(z_right-z_left); right-high is positive looking in declared increasing-station direction',adjacent_sample_twist:'(crosslevel2-crosslevel1)/(s2-s1),mm/m',three_point_curvature:'2*cross(B-A,C-A)/(AB*BC*AC); sign relative to declared x/y axes',gauge:'Separate physical running-face measurement; rail reference coordinate baseline is not gauge.'}};
}
