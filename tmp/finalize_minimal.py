from pathlib import Path
import json,hashlib,csv
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Minimalist_Options_R04'
p=R/'brain.md';s=p.read_text(encoding='utf-8');marker='## Minimalist revision R04 / 2026-09-29';parts=s.split(marker)
if len(parts)>2:s=parts[0]+marker+parts[-1];p.write_text(s,encoding='utf-8')
(O/'READ_ME_FIRST.txt').write_text('''PROJADES / MINIMALIST OPTIONS 4 AND 5 / R04
Current plan revision: PROJADES_Options_4_and_5_Minimalist_A3_R04.pdf
6 A3 landscape sheets: first floor, second-floor reference and enlarged social-zone study for each option.
Option 4: 12 ft linear kitchen with integrated dining.
Option 5: 10 ft x 5 ft compact L kitchen with integrated dining.
Dimensions and furniture sizes are proposed; not field or fabrication dimensions.
Upper-floor partitions and stair/bath cores are retained reference proposals and remain unresolved.
Options 1-3 source files remain unchanged.
R03 presentations show the superseded Option 4/5 layouts. Use R04 for current layouts; the unresolved R03 code-review items still apply.
All text is English, using the existing Arial/PROJADES A3 template.
''',encoding='utf-8')
results={}
for p in O.glob('*.pdf'):
 d=PdfReader(p);assert all(abs(float(a.mediabox.width)-1190.551)<.1 and abs(float(a.mediabox.height)-841.89)<.1 for a in d.pages)
 results[p.name]={'pages':len(d.pages),'size':'A3 landscape','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for q in csv.DictReader((R/'00_Project_Admin/Source_Inventory.csv').open(encoding='utf-8-sig')):assert hashlib.sha256((R/q['current_path']).read_bytes()).hexdigest()==q['sha256']
(O/'Validation_R04.json').write_text(json.dumps({'pdfs':results,'original_sources':'all five hashes match','scope':'Ground-floor social zones revised; upper floor/core remain reference proposals.'},indent=2),encoding='utf-8')
print(json.dumps(results))
