"""Coverage/identity/sequence checks. No physical-test or approval assertions."""
from pathlib import Path
from html.parser import HTMLParser
import collections,hashlib,json,zipfile
P=Path(__file__).resolve().parent;D=P.parent.parent
C=json.loads((P/'current-configuration-crosswalk.json').read_text())
G=json.loads((D/'assets/readiness-s1/release-evidence-register.json').read_text())
checks=[]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
rows=C['records'];manifest=C['source_manifest'];gates={g['id'] for g in G['gates']};byid={s['id']:s for s in manifest}
check('59 unique records',len(rows)==len({r['id'] for r in rows})==59)
check('14E12J20K13TR coverage',dict(collections.Counter(r['group'] for r in rows))=={'E':14,'J':12,'K':20,'TR':13})
raw_sources={}
for s in manifest:
 raw=(D/s['path']).read_bytes();check(s['id']+' source identity',hashlib.sha256(raw).hexdigest()==s['file_sha256'])
 if 'archive_member' in s:
  with zipfile.ZipFile(D/s['path']) as z:raw=z.read(s['archive_member'])
  check(s['id']+' archive member identity',hashlib.sha256(raw).hexdigest()==s['member_sha256'])
  raw_sources[s['id']]=json.loads(raw)
e,j,k=[raw_sources[x] for x in ['S2-EV01','S2-EV02','S2-EV03']]
originals={'E':{t['id']:t for t in e['tests']},'J':{t['id']:t for t in j['prototype_test_matrix']},'K':{t['id']:t for t in k['state_matrix']},'TR':{t['id']:t for t in j['traveler']}}
for r in rows:
 check(r['id']+' exact predecessor preserved',r['predecessor_record']==originals[r['group']][r['predecessor_id']])
 check(r['id']+' no test/limits/approval invented',all(r[f] is None for f in ['approved_protocol','accepted_limits','actual_result','actual_witness']) and r['status']=='development_crosswalk_only_not_ready_to_execute')
 check(r['id']+' known gates and source',bool(r['closure_gate_ids']) and set(r['closure_gate_ids'])<=gates and set(r['evidence_ids'])<=byid.keys())
 check(r['id']+' specific current requirement',len(r['current_requirement'])>70)
byrow={r['id']:r for r in rows}
check('Old E03 hydraulics explicit', 'hydraulic' in byrow['E-E03']['predecessor_record']['title'].lower())
check('Current E03 superseded not relabeled',byrow['E-E03']['disposition']=='superseded_for_current_configuration' and 'DO NOT execute' in byrow['E-E03']['current_requirement'] and 'spring' in byrow['E-E03']['current_requirement'])
check('E13 requires E14 first','E14' in byrow['E-E13']['current_requirement'])
check('JTR03 pilot vs cabin mockup distinct','J-PILOT-01' in byrow['TR-J-TR03']['current_requirement'] and 'not the3E' in byrow['TR-J-TR03']['current_requirement'])
check('20 individual K state corrections',len({r['current_requirement'] for r in rows if r['group']=='K'})==20)
check('K15 no generic caging procedure','No generic caging' in byrow['K-K-ST15']['current_requirement'])
check('K07 both portions and locomotive','both portions' in byrow['K-K-ST07']['current_requirement'] and 'locomotive' in byrow['K-K-ST07']['current_requirement'])
check('Broad gate links are not circular test prerequisites','not a demand to close every train-wide gate' in C['gate_reference_meaning'])
seq=json.loads((P/'manufacture-install-commission-sequence.json').read_text())
steps=seq['sequence'];ids={s['id'] for s in steps}
check('12 unique sequence stages',len(ids)==len(steps)==12)
for i,s in enumerate(steps):
 check(s['id']+' related not blanket closure',set(s['related_gate_ids'])<=gates and 'closure_gate_ids' not in s)
 check(s['id']+' no release/dates/durations',s['status']=='not_released' and all(s[f] is None for f in ['actual_date','release_document','duration']))
 check(s['id']+' sequence identity',s['preceding_sequence_ids']==([] if i==0 else [steps[i-1]['id']]))
check('All actual vehicles before full-consist trial','all3regular coaches plus1accessible coach and locomotive' in steps[9]['development_action'] and 'two additional regular coaches' in steps[9]['development_action'])
check('E14 equipment before E13 participants','E14' in steps[10]['development_action'] and 'then E13' in steps[10]['development_action'])
impact=json.loads((P/'change-impact-crosswalk.json').read_text())
check('8 unique change impacts',len(impact['changes'])==len({c['id'] for c in impact['changes']})==8)
pk=json.loads((D/'assets/readiness-s1/package-and-source-index.json').read_text());pids={p['id'] for p in pk['packages']}
for c in impact['changes']:
 check(c['id']+' known packages/evidence',set(c['affected_packages'])<=pids and set(c['evidence_ids'])<=byid.keys())
 check(c['id']+' no fake change/plan',c['actual_change'] is None and c['accepted_regression_plan'] is None)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.section=None;self.parent={}
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='section':self.section=a.get('id')
  if 'id'in a:self.ids.append(a['id']);self.parent[a['id']]=self.section
  if t=='a' and 'href'in a:self.links.append(a['href'])
 def handle_endtag(self,t):
  if t=='section':self.section=None
page=Page();text=(D/'index.html').read_text();page.feed(text)
check('Whole HTML IDs unique',len(page.ids)==len(set(page.ids)))
check('S2 contained in readiness panel',page.parent.get('readiness-commissioning')=='readiness' and all(page.parent.get('readiness-'+r['id'].lower())=='readiness' for r in rows))
fragment=text.split('<!-- S2 ISSUE START -->')[1].split('<!-- S2 ISSUE END -->')[0]
s2=Page();s2.feed(fragment)
for href in s2.links:
 if href.startswith('#'):check('Anchor '+href,href[1:] in page.ids)
 elif not href.startswith(('http:','https:')):check('Local '+href,(D/href.split('#')[0]).is_file())
check('Every existing record has HTML anchor',all('readiness-'+r['id'].lower() in page.ids for r in rows))
check('Only one S1 and S2 region',text.count('<!-- S1 ISSUE START -->')==text.count('<!-- S2 ISSUE START -->')==1)
check('Scope qualification vs train release explained','separately authorized coupon/component qualification' in fragment)
state=json.loads((D/'assets/engineering-program-state.json').read_text())
check('R18 exact next stage',state['revision']=='PROGRAM-R18' and state['next_worker']['substage']=='3S.3')
check('No pause with remaining independent work',state['continuation_checkpoint']['remaining_independent_work'] is True and state['continuation_checkpoint']['automation_pause'] is False)
save=dict(issue=C['issue'],check_count=len(checks),checks_passed=checks,check_scope='Predecessor identity/coverage, source hashes, current dispositions, sequence consistency, source HTML navigation. Not test execution, drawing completeness, approval or browser verification.',browser_interaction_verified=False,actual_physical_tests_performed=False)
(P/'issue-check.json').write_text(json.dumps(save,indent=2)+'\n')
print(f'Passed {len(checks)} identity/coverage/sequence/link checks; no physical test or operating release.')
