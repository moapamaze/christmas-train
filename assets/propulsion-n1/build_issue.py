"""3N.1 auditable SI calculations. No hardware selection or operation authority.
Run: python build_issue.py --workbook /path/to/original.xlsx
Original workbook is read-only; only generated JSON/SVG/HTML in this issue changes.
"""
from pathlib import Path
import argparse, ast, hashlib, html, itertools, json, math, re, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
def save(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
I=json.loads((ROOT/'inputs.json').read_text())
G=I['g_m_s2']; R=I['wheel_diameter_mm']/2000; ratio=I['motor_to_wheel_ratio']; rpm=I['pump_engine_speed_rpm']
D=I['motor_cc_rev']; dpmax=I['launch_pressure_trial_bar']; aux=I['traction_auxiliary_allowance_kW']
epv=I['pump_volumetric_efficiency']; epm=I['pump_mechanical_efficiency']; emv=I['motor_volumetric_efficiency']; emt=I['motor_torque_efficiency']; eg=I['reduction_efficiency']
hyd_eff=epv*epm*emv*emt; eta=hyd_eff*eg
qmax=I['pump_max_cc_rev']*rpm*epv/1000
vmax=qmax*1000*emv/D/ratio*(2*math.pi*R)/60
force_per_bar=1e5*D/1e6/(2*math.pi)*emt*ratio*eg/R
f300=dpmax*force_per_bar
def point(mph,force):
    v=mph*0.44704; nm=v/(2*math.pi*R)*60*ratio
    q=nm*D/1000/emv; stroke=q*1000/(rpm*epv)
    wheel=force*v/1000; main=wheel/eta
    return dict(speed_mph=mph,speed_m_s=v,motor_rpm=nm,pump_delivered_L_min=q,pump_cc_rev=stroke,pressure_bar=force/force_per_bar,wheel_kW=wheel,main_pump_shaft_kW=main,engine_plus_aux_kW=main+aux,main_loop_oil_heat_kW=main*(1-hyd_eff),gear_heat_kW=main*hyd_eff*(1-eg),flow_feasible=stroke<=I['pump_max_cc_rev']+1e-9,pressure_feasible=force<=f300+1e-9)
def available(mph,budget):
    v=mph*.44704
    return min(f300,(budget-aux)*eta*1000/v)

# Original formulas are evaluated through a restricted arithmetic AST, not eval().
def audit_workbook(path):
    raw=path.read_bytes(); z=zipfile.ZipFile(path); ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    strings=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        strings=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
    sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml')); cells={}
    for c in sheet.findall('.//m:c',ns):
        at=c.attrib['r']; typ=c.attrib.get('t'); v=c.find('m:v',ns); f=c.find('m:f',ns)
        val=v.text if v is not None else None
        if typ=='s':val=strings[int(val)]
        elif typ=='inlineStr':val=''.join(c.find('m:is',ns).itertext())
        elif val is not None and typ not in ('str','e'):val=float(val)
        cells[at]={'value':val}
        if f is not None:cells[at]['formula']=f.text
    memo={}
    def cell(at):
        if at not in memo:
            c=cells[at]
            memo[at]=parse(c['formula']) if 'formula' in c else c['value']
        return memo[at]
    def parse(text):
        text=text.replace('$','').replace('^','**')
        text=re.sub(r'\b([A-Z]+[0-9]+)\b',lambda m:str(cell(m[1])),text)
        def node(n):
            if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
            if isinstance(n,ast.BinOp):
                a,b=node(n.left),node(n.right)
                if isinstance(n.op,ast.Add):return a+b
                if isinstance(n.op,ast.Sub):return a-b
                if isinstance(n.op,ast.Mult):return a*b
                if isinstance(n.op,ast.Div):return a/b
                if isinstance(n.op,ast.Pow):return a**b
            if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -node(n.operand)
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
                if n.func.id=='PI' and not n.args:return math.pi
                if n.func.id=='MIN':return min(node(x) for x in n.args)
            raise ValueError('Unsupported workbook arithmetic: '+ast.dump(n))
        return node(ast.parse(text,mode='eval').body)
    results=[]
    for at,c in cells.items():
        if 'formula' in c:
            value=cell(at); results.append({'cell':at,'formula':c['formula'],'cached':c['value'],'recomputed':value,'absolute_error':abs(value-c['value'])})
    return {'name':path.name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'sheet':'Drive match','modified':False,'cells':cells,'formula_replay':results,'max_absolute_error':max(r['absolute_error'] for r in results),'method':'Read XLSX XML; replay all original arithmetic formulas independently. This does not verify Excel UI behavior or OEM assumptions.'}

def build():
    # Force, energy and input-power calculations at constant positive travel speed.
    steady=[]
    for (case,mass),cr,extra,mph in itertools.product(I['mass_cases_kg'].items(),I['running_resistance_trials'],I['additional_resistance_trials_N'],I['speed_trials_mph']):
        f=mass*G*cr+extra; p=point(mph,f)
        p.update(mass_case=case,mass_kg=mass,resistance_coefficient=cr,extra_N=extra,required_force_N=f,engine_budget_comparisons=[{'budget_kW':b,'power_margin_kW':b-p['engine_plus_aux_kW']} for b in I['engine_budget_trials_kW']])
        steady.append(p)
    launch=[]
    for (case,mass),extra,driven,mu in itertools.product(I['mass_cases_kg'].items(),I['additional_resistance_trials_N'],I['adhesive_mass_trials_kg'],I['adhesion_trials']):
        resist=mass*G*I['starting_resistance_trial']+extra; adhesion=driven*G*mu
        launch.append({'mass_case':case,'mass_kg':mass,'extra_N':extra,'driven_mass_probe_kg':driven,'adhesion_probe':mu,'resistance_N':resist,'adhesion_limit_N':adhesion,'drive_torque_force_proxy_N':f300,'force_proxy_after_adhesion_N':min(f300,adhesion),'acceleration_proxy_m_s2':(min(f300,adhesion)-resist)/mass,'pressure_for_0p1_m_s2_bar':(resist+mass*I['acceleration_probe_m_s2'])/force_per_bar,'driven_mass_for_0p1_m_s2_kg':(resist+mass*I['acceleration_probe_m_s2'])/(G*mu)})
    envelope=[]
    for b in I['engine_budget_trials_kW']:
        for k in range(1,151):
            mph=k*.05; f=available(mph,b)
            envelope.append({'budget_kW':b,'speed_mph':mph,'force_before_adhesion_N':f,'flow_limit_exceeded':mph*.44704>vmax})
    baseline=point(vmax/.44704,I['mass_cases_kg']['upper']*G*.005+2000)
    power_ceiling={'engine_budget_kW':55.4,'main_shaft_kW':45.4,'wheel_kW':45.4*eta,'main_oil_heat_kW':45.4*(1-hyd_eff),'gear_heat_kW':45.4*hyd_eff*(1-eg),'full_stroke_pressure_bar':45.4*600000*epm/(I['pump_max_cc_rev']*rpm),'pump_cc_at_300bar':45.4*600000*epm/(dpmax*rpm)}
    power_ceiling['speed_at_300bar_mph']=vmax/.44704*power_ceiling['pump_cc_at_300bar']/I['pump_max_cc_rev']
    shafts=[]
    for label,power,n in [('2600 rpm gross-ceiling allocation',45.4,2600),('same power at 1600 rpm sensitivity; not engine curve',45.4,1600)]:
        shafts.append({'case':label,'shaft_kW':power,'rpm':n,'torque_Nm':power*1000/(2*math.pi*n/60)})
    for dp in [300,420]:shafts.append({'case':f'full 45 cc at {dp} bar; not necessarily engine feasible','torque_Nm':dp*1e5*45e-6/(2*math.pi*epm)})
    thermal=[]
    for duty,loss in [('upper baseline steady 5 mph',point(5,65100*G*.005+2000)['main_loop_oil_heat_kW']),('upper baseline steady 7.5 mph',point(7.5,65100*G*.005+2000)['main_loop_oil_heat_kW']),('gross-ceiling main drive',power_ceiling['main_oil_heat_kW'])]:
        for other,amb in itertools.product(I['non_drive_oil_heat_trials_kW'],I['cooling_ambient_trials_C']):
            heat=loss+other; dt=I['oil_inlet_temperature_trial_C']-amb
            thermal.append({'case':duty,'main_loss_kW':loss,'extra_oil_heat_probe_kW':other,'total_oil_heat_probe_kW':heat,'ambient_probe_C':amb,'oil_inlet_probe_C':I['oil_inlet_temperature_trial_C'],'delta_T_K':dt,'required_rejection_per_K_kW_K':heat/dt,'not_UA':'Heat divided by inlet temperature difference is a catalog screening requirement, not true exchanger UA or a cooler selection.'})
    charge=[]
    for mph in [5,vmax/.44704]:
        p=point(mph,65100*G*.005+2000)
        pump_leak=p['pump_cc_rev']*rpm/1000-p['pump_delivered_L_min']
        motor_leak=p['pump_delivered_L_min']-p['motor_rpm']*D/1000
        charge.append({'speed_mph':mph,'pump_leakage_proxy_L_min':pump_leak,'motor_leakage_proxy_L_min':motor_leak,'sum_leakage_proxy_L_min':pump_leak+motor_leak,'meaning':'Only the displacement-leakage estimate implied by the constant efficiencies. Not selected charge-pump capacity. Add flushing/control/other losses and check actual maps at cold/hot conditions and all speeds.'})
    speeds=[{'motor_rpm':n,'speed_mph':n/ratio*(2*math.pi*R)/60/.44704} for n in [50,100,150,2900]]
    result={'issue':I['issue'],'model_kind':'Constant-efficiency algebraic sensitivity, not a transient hydrostatic simulation or hardware rating','hydraulic_shaft_to_motor_efficiency':hyd_eff,'shaft_to_wheel_efficiency':eta,'maximum_flow_L_min':qmax,'maximum_speed_at_110cc_mph':vmax/.44704,'force_proxy_at_300bar_N':f300,'baseline_at_original_calculated_speed':baseline,'gross_ceiling':power_ceiling,'shaft_torque_cases':shafts,'creep_and_rated_speed_conversions':speeds,'steady_cases':steady,'launch_cases':launch,'force_speed_cases':envelope,'thermal_cases':thermal,'exclusions':['rotating inertia and transient compression','temperature/pressure/speed-dependent efficiency','stall/cogging torque and stalled heat','charge/control/flushing sizing','hose/filter/cooler pressure losses','measured curve/wind/bearing/brake drag','engine net torque/continuous duty/DPF operation','mechanical drive topology and wheel-load transfer','hotel power','0% grade does not eliminate surveying and as-built tolerances']}
    result['charge_leakage_proxies']=charge
    save('calculations.json',result)
    chart(envelope)
    # Identities and original arithmetic are verification of calculations, not safety.
    errors=[]
    for p in steady:
        mech=p['main_pump_shaft_kW']-p['main_loop_oil_heat_kW']-p['gear_heat_kW']-p['wheel_kW']
        torquep=p['pressure_bar']*force_per_bar-p['required_force_N']
        errors.extend([abs(mech),abs(torquep)])
    assert max(errors)<1e-8
    assert abs(baseline['engine_plus_aux_kW']-35.051399968715174)<1e-9
    assert abs(vmax/.44704-7.495513073518385)<1e-10
    assert abs(f300-13471.67015801348)<1e-8
    zero=point(0,5192.064575)
    assert zero['wheel_kW']==0 # Not an accepted estimate of stall losses.
    save('validation.json',{'date_utc':I['date_utc'],'steady_cases':len(steady),'launch_cases':len(launch),'force_speed_cases':len(envelope),'thermal_cases':len(thermal),'max_force_and_power_identity_error_mixed_units':max(errors),'original_headline_replay':'matched within stated numerical tolerances','engineering_approval':False,'no_stall_heat_claim':True,'browser_interaction_test':'not run; managed preview previously unavailable','not_checked':['OEM maps','hardware installation','traction/braking tests','cooler performance','safety control implementation']})
    return result

def chart(rows):
    x=lambda v:100+v/7.5*830; y=lambda f:430-f/16000*340
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 625"><rect width="1100" height="625" fill="#fff"/><g font-family="sans-serif" fill="#153247"><text x="45" y="38" font-size="23" font-weight="bold">3N.1 · Calculated pull versus speed</text><text x="45" y="65" font-size="14">600 mm wheels · 9:1 · motor 110 cc · 300 bar probe · 10 kW auxiliary allowance</text>']
    for f in [0,4000,8000,12000,16000]:svg.append(f'<path d="M100 {y(f)}H930" stroke="#dde3e7"/><text x="77" y="{y(f)+5}" text-anchor="end" font-size="14">{f/1000:g}</text>')
    for v in [0,1,2.5,5,7.5]:svg.append(f'<path d="M{x(v)} 90V430" stroke="#edf0f2"/><text x="{x(v)}" y="452" text-anchor="middle" font-size="14">{v:g}</text>')
    colors=['#346784','#cc6d28','#24342e']
    for budget,color in zip(I['engine_budget_trials_kW'],colors):
        pts=' '.join(f'{x(r["speed_mph"]):.2f},{y(r["force_before_adhesion_N"]):.2f}' for r in rows if r['budget_kW']==budget)
        svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>')
    for f,label,color in [(65100*G*.005+2000,'Running resistance, upper + 2 kN','#87937b'),(65100*G*.010+2000,'Breakaway resistance probe','#a15555'),(10000*G*.10,'Adhesion probe: 10 t at 0.10','#776794')]:
        svg.append(f'<path d="M100 {y(f)}H930" stroke="{color}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    svg.append('<text x="32" y="240" font-size="14" transform="rotate(-90 32 240)">Wheel pull before adhesion (kN)</text><text x="475" y="477" font-size="15">Speed (mph)</text>')
    for k,(b,c) in enumerate(zip(I['engine_budget_trials_kW'],colors)):
        xx=65+k*330;svg.append(f'<path d="M{xx} 505h30" stroke="{c}" stroke-width="3"/><text x="{xx+40}" y="510" font-size="14">{b:g} kW engine-power budget</text>')
    svg.extend(['<text x="45" y="542" font-size="13">Dashed references: running 5.19 kN (green); breakaway 8.38 kN (red); adhesion 9.81 kN (purple).</text>','<text x="45" y="568" font-size="14" font-weight="bold">35/45 kW are sensitivities; 55.4 kW is gross intermittent, NOT accepted net continuous output.</text>','<text x="45" y="593" font-size="13">Available rail force is limited further by actual adhesion. Near-zero torque, exact 7.5 mph flow and thermal duty remain open.</text>','</g></svg>'])
    (ROOT/'force-speed.svg').write_text(''.join(svg))

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('--workbook');opt=args.parse_args()
    if opt.workbook:
        audit=audit_workbook(Path(opt.workbook));assert audit['max_absolute_error']<1e-8;save('workbook-audit.json',audit)
    result=build();print(json.dumps({'issue':I['issue'],'cruise_5mph_engine_kW':point(5,65100*G*.005+2000)['engine_plus_aux_kW'],'cruise_7p5mph_engine_kW':point(7.5,65100*G*.005+2000)['engine_plus_aux_kW'],'shaft_cases':result['shaft_torque_cases'],'steady_cases':len(result['steady_cases'])}))
