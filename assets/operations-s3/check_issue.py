"""Check development scope, identities and links; not operational validation."""
from pathlib import Path
from html.parser import HTMLParser
import ast,hashlib,json
P=Path(__file__).resolve().parent;D=P.parent.parent
checks=[]
def read(n):return json.loads((P/n).read_text())
def check(n,b):
 if not b:raise AssertionError(n)
 checks.append(n)
procedures=read('conditional-procedures.json');roles=read('roles-and-training.json');modes=read('operating-modes.json');energy=read('energy-and-defect-controls.json');maintenance=read('maintenance-development-schedule.json');sources=read('sources-and-basis.json')
check('10 unique conditional procedures',len(procedures['procedures'])==len({p['id'] for p in procedures['procedures']})==10)
check('6 roles, no invented staffing',len(roles['roles'])==6 and roles['staffing_count'] is None)
check('No appointments/qualifications invented',all(r['named_person'] is None and r['qualified_training_record'] is None for r in roles['roles']))
check('8 modes not approved implementation',len(modes['modes'])==8 and all(m['approved_for_use'] is False for m in modes['modes']) and modes['control_mapping'] is None and modes['transition_implementation'] is None)
gates=json.loads((D/'assets/readiness-s1/release-evidence-register.json').read_text());gids={g['id'] for g in gates['gates']};rids={r['id'] for r in roles['roles']}
for p in procedures['procedures']:
 check(p['id']+' no control/limit/result/fielduse invention',p['field_ready'] is False and all(p[x] is None for x in ['actual_control_positions','accepted_numeric_limits','actual_completed_record']))
 check(p['id']+' roles/gates valid',bool(p['role_ids']) and set(p['role_ids'])<=rids and bool(p['related_gate_ids']) and set(p['related_gate_ids'])<=gids)
 check(p['id']+' sequence and stop evidence',len(p['development_sequence'])>=3 and bool(p['stop_or_hold']) and bool(p['existing_records_to_reuse']))
check('8 energy subjects without invented isolation points',len(energy['energy_inventory'])==8 and all(e['actual_isolation_points'] is None for e in energy['energy_inventory']))
check('No degraded passenger mode accepted',energy['accepted_degraded_modes']==[] and energy['accepted_rejection_values'] is None)
check('Spring energy remains at zero pressure','zero gauge pressure' in energy['energy_inventory'][1]['prohibition'])
check('Propulsion hydraulics distinguished from superseded brake','Hydraulic propulsion is not the superseded' in energy['energy_inventory'][6]['prohibition'])
check('10 maintenance families',len(maintenance['items'])==10)
for m in maintenance['items']:
 check(m['id']+' no invented intervals/limits/method/result',all(m[k] is None for k in ['calendar_interval','operating_hours_interval','distance_interval','brake_or_boarding_cycle_interval','accepted_wear_rejection_limit','approved_lubricant_or_service_method','actual_record']))
check('No operation approval',procedures['approved_for_operation'] is False and maintenance['passenger_operation_ready'] is False)
check('3 dated current primary scope references',len(sources['external_primary_sources'])==3 and all(s['retrieved_utc']=='2026-10-19' for s in sources['external_primary_sources']))
check('OSHA147 agriculture/construction exclusion explicit','excludes construction/agriculture' in sources['external_primary_sources'][1]['verified'])
check('OSHA169 transportation exclusion explicit','transportation vehicles' in sources['external_primary_sources'][2]['verified'])
check('Trailer schedule not rail approval','Not a rail maintenance schedule' in sources['external_primary_sources'][0]['application_limit'])
for e in sources['current_configuration_evidence']:
 check('Exact current evidence '+e['path'],hashlib.sha256((D/e['path']).read_bytes()).hexdigest()==e['sha256'])
byproc={p['id']:p for p in procedures['procedures']}
check('Every-vehicle checks not pressure only','not a pressure-only pass' in ' '.join(byproc['OP-02']['development_sequence']))
check('Independent restraint before rescue release','independently restrain' in byproc['OP-09']['development_sequence'][0])
check('Evacuation not solely station return','Do not rely solely on moving back' in byproc['OP-08']['stop_or_hold'])
check('Controlled assisted evacuation held, urgent escape separately prioritized',any('verify and maintain' in s and 'floor/suspension movement' in s and 'without a blanket' in s for s in byproc['OP-08']['development_sequence']))
check('Caging restoration blocks dispatch','Unrestored caging' in byproc['OP-10']['stop_or_hold'])
check('No routine reverse/tow/two train permission','No routine pushing/reversing' in byproc['OP-04']['stop_or_hold'])
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.section=None;self.parent={}
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='section':self.section=a.get('id')
  if 'id'in a:self.ids.append(a['id']);self.parent[a['id']]=self.section
  if t=='a' and 'href'in a:self.links.append(a['href'])
 def handle_endtag(self,t):
  if t=='section':self.section=None
text=(D/'index.html').read_text();page=Page();page.feed(text)
check('Whole page IDs unique',len(page.ids)==len(set(page.ids)))
check('S3 in readiness panel',page.parent.get('readiness-operations')=='readiness' and all(page.parent.get('readiness-'+p['id'].lower())=='readiness' for p in procedures['procedures']))
fragment=text.split('<!-- S3 ISSUE START -->')[1].split('<!-- S3 ISSUE END -->')[0];s3=Page();s3.feed(fragment)
for href in s3.links:
 if href.startswith('#'):check('Anchor '+href,href[1:] in page.ids)
 elif not href.startswith(('http:','https:')):check('Local '+href,(D/href.split('#')[0]).is_file())
check('Each issue region preserved once',all(text.count('<!-- '+x+' ISSUE START -->')==1 for x in ['S1','S2','S3','R1','R2']))
check('Python issuer syntax',bool(ast.parse((P/'build_issue.py').read_text())))
state=json.loads((D/'assets/engineering-program-state.json').read_text())
check('R19 exact continuation',state['revision']=='PROGRAM-R19' and state['next_worker']['substage']=='3S.4')
check('No completion/pause while supportable work remains',state['continuation_checkpoint']['remaining_independent_work'] is True and state['continuation_checkpoint']['automation_pause'] is False and state['last_completed_stage']=='3K')
result=dict(issue=procedures['issue'],check_count=len(checks),checks_passed=checks,scope='Coverage, current source hashes, explicit unapproved settings, source scope and HTML links. Not a field procedure validation, practical exercise, design/operation approval or browser verification.',browser_interaction_verified=False,actual_exercises_performed=False)
(P/'issue-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'Passed {len(checks)} source/scope/coverage/link checks; all procedures remain development-only.')
