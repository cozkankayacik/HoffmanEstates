from pathlib import Path
import json,csv,hashlib
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Island_Options_R05'
data=json.loads((O/'Furniture_and_Cabinet_Schedule_R05.json').read_text())
report={'original_sources':'unchanged','pdfs':{},'design_checks':{}}
for op in [4,5]:
 rows=[a for a in data if a['option']==op]
 report['design_checks'][str(op)]={'minimum_living_route_in':min(a['living_route_in'] for a in rows),'minimum_island_end_clearance_in':min(a['island_end_clearance_in'] for a in rows),'counter_to_island_in':42}
for p in O.glob('*.pdf'):
 d=PdfReader(p);assert all(abs(float(pg.mediabox.width)-1190.551)<.1 and abs(float(pg.mediabox.height)-841.89)<.1 for pg in d.pages)
 report['pdfs'][p.name]={'pages':len(d.pages),'size':'A3 landscape'}
for q in csv.DictReader((R/'00_Project_Admin/Source_Inventory.csv').open(encoding='utf-8-sig')):assert hashlib.sha256((R/q['current_path']).read_bytes()).hexdigest()==q['sha256']
(O/'Validation_R05.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(O/'READ_ME_FIRST.txt').write_text('''PROJADES / OPTIONS 4 AND 5 / ISLAND AND TWO-SOFA REVISION R05
Current combined drawing set: PROJADES_Options_4_and_5_Island_A3_R05.pdf
6 A3 English sheets: first floor, upper-floor reference and enlarged study for each option.
Option 4: 72 x 36 in island, three stools; 84 x 36 in three-seat sofa plus 60 x 36 in two-seat sofa.
Option 5: 60 x 30 in island, two stools; same sofa sizes.
Both: 144 x 24 in wall kitchen run, 42 in proposed work aisle, separate 6 in service allowance.
Island seating replaces the separate dining table. The island has no sink or hob.
The Turkish request for sofa and three-seat sofa was interpreted as a two-seat plus a three-seat sofa.
Upper-floor partitions and the stair/bath cores are retained proposals, not verified existing construction.
R05 supersedes R04 ground-floor layouts. R03 code-review hold points remain open.
Original Options 1-3 and the source DWG are unchanged.
''',encoding='utf-8')
with (R/'brain.md').open('a',encoding='utf-8') as f:f.write('''

## Island and two-sofa revision R05 / 2026-09-29
- User requests island kitchens and sofa plus three-seat seating, using the planning approach of Options 1-3.
- Interpreted seating as one 60 x 36 in two-seat sofa and one 84 x 36 in three-seat sofa; communicated that assumption.
- Option 4: 72 x 36 in preparation/dining island, three stools; Option 5: 60 x 30 in island, two stools.
- Both use 12 ft wall kitchen runs, proposed 42 in work aisles and 6 in service allowances.
- Separate dining tables are replaced by island seating; this capacity trade-off is disclosed on the sheets.
- Drawing geometry checks include all four unit positions per option, occupied stool envelopes and island end clearance. They are not regulatory compliance certification.
- Current files: PROJADES_Island_Options_R05. Upper-floor/core scope and R03 code-review holds remain unchanged. Original Options 1-3 preserved.
''')
print(json.dumps(report['design_checks']))
