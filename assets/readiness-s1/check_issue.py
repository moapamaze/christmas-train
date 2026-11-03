"""Source/link/configuration checks only; not a drawing-buildability test."""

# Hosting transport: retain hashes of decoded source bytes after gzip packaging.
import gzip as _transport_gzip
def _transport_bytes(path):
    return path.read_bytes() if path.exists() else _transport_gzip.decompress(path.with_name(path.name + '.gz').read_bytes())

from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,zipfile
P=Path(__file__).resolve().parent;D=P.parent.parent
checks=[]
def check(name,value):
    if not value:raise AssertionError(name)
    checks.append(name)
index=json.loads((P/'package-and-source-index.json').read_text())
reg=json.loads((P/'release-evidence-register.json').read_text())
packages=index['packages'];sources=index['source_manifest'];gates=reg['gates']
check('17 unique package IDs',len(packages)==len({p['id'] for p in packages})==17)
check('19 unique gate IDs',len(gates)==len({g['id'] for g in gates})==19)
check('No complete fabrication-drawing or release claims',all(p['fabrication_drawing_complete'] is False and p['fabrication_release'] is False and p['actual_test_acceptance_evidence'] is None for p in packages))
check('No desktop-program completion claim',index['supportable_desktop_program_complete'] is False)
source_ids={s['id'] for s in sources};gate_ids={g['id'] for g in gates};package_ids={p['id'] for p in packages}
check('Unique source IDs',len(source_ids)==len(sources))
for s in sources:
    raw=_transport_bytes(D/s['path'])
    check(s['id']+' exact file SHA/bytes',hashlib.sha256(raw).hexdigest()==s['file_sha256'] and len(raw)==s['bytes'])
    if 'archive_member' in s:
        with zipfile.ZipFile(D/s['path']) as z:content=z.read(s['archive_member'])
        check(s['id']+' exact member SHA/bytes',hashlib.sha256(content).hexdigest()==s['member_sha256'] and len(content)==s['member_bytes'])
for p in packages:
    check(p['id']+' evidence/gate references',bool(p['evidence_ids']) and set(p['evidence_ids'])<=source_ids and bool(p['release_gate_ids']) and set(p['release_gate_ids'])<=gate_ids)
    check(p['id']+' explicit actual/omitted definition',bool(p['actual_definition']) and bool(p['not_defined_or_not_demonstrated']) and bool(p['responsible_disciplines']) and bool(p['independent_next_work']))
for g in gates:
    expected={p['id'] for p in packages if g['id'] in p['release_gate_ids']}
    check(g['id']+' reverse package coverage',set(g['affected_package_ids'])==expected and bool(expected))
    check(g['id']+' open without fabricated closure',g['state']=='open' and g['accepted_evidence'] is None and g['acceptance_authority_named_person'] is None)
    check(g['id']+' prerequisite identity',set(g['prerequisite_gate_ids'])<=gate_ids and g['id'] not in g['prerequisite_gate_ids'])
bygate={g['id']:g for g in gates};visited=set();active=set();order=[]
def visit(id):
    if id in active:raise AssertionError('Prerequisite cycle at '+id)
    if id in visited:return
    active.add(id)
    for dep in bygate[id]['prerequisite_gate_ids']:visit(dep)
    active.remove(id);visited.add(id);order.append(id)
for id in bygate:visit(id)
check('Gate prerequisite graph acyclic',len(order)==19)
save_order=dict(issue=index['issue'],release_order_aid=order,not_design_iteration_algorithm=True)
(P/'release-order-check.json').write_text(json.dumps(save_order,indent=2)+'\n')
frame=json.loads(_transport_bytes(D/'assets/models3d/frame-J1a.json').decode())
connections=json.loads((D/'assets/models3d/connections-I1.json').read_text())
accessible=json.loads(_transport_bytes(D/'assets/models/accessible-coach.json').decode())
check('J1a actual mesh count110',len(frame['parts'])==110)
check('I1 six local assemblies and160 objects',len(connections['assemblies'])==6 and len(connections['parts'])==160)
check('Accessible Stage2 display31 objects',len(accessible['parts'])==31)
member_source=next(s for s in sources if s.get('archive_member')=='models/Phase3J_J1a_Member_Register_R0.json')
with zipfile.ZipFile(D/member_source['path']) as z:m=json.loads(z.read(member_source['archive_member']))
check('Actual J member register110',len(m['parts'])==110)
check('Register excludes integrated connections',any('No I-BA' in n and 'bogie mounts' in n for n in m['notes']))
check('No released saw lengths in J1a',all(p['actual_saw_cut_length_in'] is None for p in m['parts']))
check('Catalog member mass is subtotal not tare',abs(m['mass_budget']['J1a_catalog_member_mass_kg']-1816.3471427332)<1e-7)
select=json.loads((D/'assets/brake-selection-l2/selection.json').read_text())
check('Current D1 8percoach32coachtotal, loco unknown',select['brakes_per_coach']==8 and select['coach_brakes_total']==32 and select['locomotive_brake_count'] is None)
dispositions=json.loads((P/'configuration-dispositions.json').read_text())
check('8 configuration dispositions without hardware change',len(dispositions['items'])==8 and dispositions['changes_to_selected_hardware'] is False)
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.append(a['id'])
        if t=='a' and 'href'in a:self.links.append(a['href'])
text=(D/'index.html').read_text();page=Page();page.feed(text)
check('Whole page IDs unique',len(page.ids)==len(set(page.ids)))
issue=text.split('<!-- S1 ISSUE START -->',1)[1].split('<!-- S1 ISSUE END -->',1)[0]
s1=Page();s1.feed(issue)
for href in s1.links:
    if href.startswith('#'):check('Anchor '+href,href[1:] in page.ids)
    elif not href.startswith(('http:','https:')):check('Local link '+href,(D/href.split('#')[0]).is_file())
check('17 package anchors',all('readiness-'+p['id'].lower() in s1.ids for p in packages))
check('19 gate anchors',all('readiness-'+g['id'].lower() in s1.ids for g in gates))
app=(D/'app.js').read_text()
check('Readiness tab registration',"readiness:'Actual source and build readiness'"in app)
check('Deep-link tab resolution',"rawTab.startsWith('readiness-') ? 'readiness'"in app)
check('Deep-link scrolling registration',"if(rawTab.startsWith('readiness-')||"in app)
state=json.loads((D/'assets/engineering-program-state.json').read_text())
check('R17 next exact stage',state['revision']=='PROGRAM-R17' and state['next_worker']['substage']=='3S.2')
check('No pause or completed program',state['continuation_checkpoint']['remaining_independent_work'] is True and state['continuation_checkpoint']['automation_pause'] is False)
result=dict(issue=index['issue'],check_count=len(checks),checks_passed=checks,scope='File/member identity, cross-links, representation counts, gate coverage and navigation source checks only. Not a practical reader/buildability review, browser test, engineering approval or physical test.',browser_interaction_verified=False,new_fabrication_geometry=False)
(P/'issue-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'Passed {len(checks)} source/register/navigation checks; drawing completeness and physical acceptance NOT established.')
