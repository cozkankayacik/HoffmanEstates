from pathlib import Path
import csv,hashlib,json,zipfile,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03'
W,H=landscape(A3)
c=canvas.Canvas(str(O/'PROJADES_Five_Options_A3_Review_R03.pdf'),pagesize=(W,H))
slides=sorted((R/'tmp/presentation/print').glob('slide-*.png'));assert len(slides)==22
for im in slides:c.drawImage(str(im),0,0,W,H);c.showPage()
c.save()
ref=R/'01_Site_and_Reference/Zoning_and_Code'
for name in ['PROJADES_Code_Issue_Register_R03.csv','PROJADES_Code_Sources_R03.json']:shutil.copy2(ref/name,O/name)
(O/'READ_ME_FIRST.txt').write_text('''PROJADES / 2360 HASSELL ROAD / R03
All new documents are in English. A3 landscape; plan sheets are fit to sheet / NTS.

START HERE
PROJADES_Comprehensive_Review_Package_R03.pdf
25 pages: 10 plan sheets + 15-page comprehensive architectural/code review.

PRESENTATION
PROJADES_Five_Options_A3_Review_R03.pptx: 22 slides, editable text/tables; embedded plan images.
PROJADES_Five_Options_A3_Review_R03.pdf: matching presentation export.

REVIEW RECORD
PROJADES_Code_Review_R03.pdf: standalone 15-page review.
PROJADES_Code_Issue_Register_R03.csv: 20 issues and close-out actions.
PROJADES_Code_Sources_R03.json: official source URLs.

STATUS
Concept review, not permit-ready or construction information.
Original Options 1-3 and original DWG remain unchanged; hashes checked.
Options 4-5 have separate kitchen service-zone proposals and safety-glazing notes.
Interior demolition and municipal conversion/zoning approval are architect-reported.
Existing sprinkler, structural/floor conditions, sections and approval conditions remain unverified.
New plans are PDF-derived concept overlays, not completed dimensioned construction CAD.
Use the issue register to resolve missing evidence before design release.
''',encoding='utf-8')

# Archive only generated superseded exports; all targets are validated inside this workspace.
archive=R/'99_Archive/Superseded_Concept_Reviews'
targets=[]
for folder in [R/'02_Design_Options',R/'05_Presentations_and_Issued/Presentations']:
 for p in folder.rglob('*'):
  if p.is_file() and ('R01' in p.name or 'R02' in p.name) and p.suffix.lower() in ['.pdf','.pptx'] and (p.name.startswith('PROJADES_') or p.name.startswith('HE_Alternative_')):targets.append(p)
for p in targets:
 dest=archive/p.relative_to(R)
 assert p.resolve().is_relative_to(R.resolve()) and dest.resolve().is_relative_to(archive.resolve())
 dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():shutil.move(str(p),str(dest))

validation={}
for p in O.glob('*.pdf'):
 d=PdfReader(p);assert all(abs(float(pg.mediabox.width)-W)<.05 and abs(float(pg.mediabox.height)-H)<.05 for pg in d.pages)
 validation[p.name]={'pages':len(d.pages),'page_size':'A3 landscape','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for q in csv.DictReader((R/'00_Project_Admin/Source_Inventory.csv').open(encoding='utf-8-sig')):assert hashlib.sha256((R/q['current_path']).read_bytes()).hexdigest()==q['sha256']
(O/'Delivery_Validation.json').write_text(json.dumps({'original_hashes':'all five match','pdfs':validation,'presentation_receipt':'tmp/presentation/validation-code-r03-delivery.json'},indent=2),encoding='utf-8')
z=O.parent/'PROJADES_Review_Package_R03.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in O.iterdir():
  if p.is_file():a.write(p,p.name)
print(json.dumps({'archive_count':len(targets),'files':list(validation),'zip':str(z)}))
