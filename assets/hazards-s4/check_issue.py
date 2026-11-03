"""Coverage, identity and exact-link checks—not risk or engineering acceptance."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
P=Path(__file__).resolve().parent;D=P.parent.parent
reg=json.loads((P/'hazard-control-verification-register.json').read_text())
pkg=json.loads((D/'assets/readiness-s1/package-and-source-index.json').read_text())
gate=json.loads((D/'assets/readiness-s1/release-evidence-register.json').read_text())
test=json.loads((D/'assets/commissioning-s2/current-configuration-crosswalk.json').read_text())
pids={p['id'] for p in pkg['packages']};gids={g['id'] for g in gate['gates']};tids={t['id'] for t in test['records']};checks=[]
def check(n,b):
 if not b:raise AssertionError(n)
 checks.append(n)
check('25 unique mechanisms',len(reg['hazards'])==len({h['id'] for h in reg['hazards']})==25)
check('All17packages covered',{p for h in reg['hazards'] for p in h['affected_package_ids']}==pids)
check('All19release subjects covered',{g for h in reg['hazards'] for g in h['related_release_gate_ids']}==gids)
for h in reg['hazards']:
 check(h['id']+' exact package/gate/test IDs',set(h['affected_package_ids'])<=pids and set(h['related_release_gate_ids'])<=gids and set(h['verification_record_ids'])<=tids)
 check(h['id']+' no risk acceptance/score invented',h['status']=='open' and all(h[x] is None for x in ['severity_category','likelihood','risk_score','residual_risk','accepted_evidence','risk_acceptance_signoff']))
 check(h['id']+' specific mechanism and proposed response',len(h['mechanism_and_consequence'])>70 and len(h['design_response_to_define_and_prove'])>70 and 'physical implementation' in h['control_status'])
check('No physically verified mitigation claim',reg['implemented_physical_controls_verified'] is False and reg['accepted_risks']==[])
for e in reg['source_manifest']:check('Source identity '+e['path'],hashlib.sha256((D/e['path']).read_bytes()).hexdigest()==e['sha256'])
audit=json.loads((P/'finish-criteria-audit.json').read_text())
check('8 finish themes remain incomplete',len(audit['criteria'])==8 and all(x['complete'] is False for x in audit['criteria']))
check('New available engineering not false block',audit['all_useful_work_blocked'] is False and audit['pause_automation'] is False and audit['desktop_package_complete'] is False)
inputs=json.loads((D/'assets/suspension-l3/inputs.json').read_text())
check('Actual source explicitly heave only',any('vertical heave only' in s and 'track twist' in s for s in inputs['limitations']))
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
check('HTML unique IDs',len(page.ids)==len(set(page.ids)))
check('Hazards in readiness panel',all(page.parent.get('readiness-'+h['id'].lower())=='readiness' for h in reg['hazards']))
f=text.split('<!-- S4 ISSUE START -->')[1].split('<!-- S4 ISSUE END -->')[0];s4=Page();s4.feed(f)
for href in s4.links:
 if href.startswith('#'):check('Anchor '+href,href[1:] in page.ids)
 elif not href.startswith(('http:','https:')):check('Local '+href,(D/href.split('#')[0]).is_file())
check('Predecessor issue regions retained once',all(text.count('<!-- '+x+' ISSUE START -->')==1 for x in ['S1','S2','S3','S4','R1','R2']))
state=json.loads((D/'assets/engineering-program-state.json').read_text())
check('ExactR20nextnewmechanics',state['revision']=='PROGRAM-R20' and state['next_worker']['substage']=='3L.3-S2')
check('Only3Kcomplete',state['last_completed_stage']=='3K' and state['continuation_checkpoint']['remaining_independent_work'] is True)
out=dict(issue=reg['issue'],check_count=len(checks),checks_passed=checks,scope='Mechanism coverage, source hashes and exact linkage only; not exhaustive hazard analysis, risk acceptance, physical mitigation, browser or engineering verification.',browser_interaction_verified=False)
(P/'issue-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(f'Passed {len(checks)} coverage/source/link checks; no risk acceptance or physical mitigation demonstrated.')
