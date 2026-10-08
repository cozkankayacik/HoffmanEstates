from pathlib import Path
import shutil,zipfile,json
from PIL import Image,ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];O=R/'05_Presentations_and_Issued/Presentations/PDF_Exports';O.mkdir(exist_ok=True)
(O/'Archive').mkdir(exist_ok=True)
files=list((R/'tmp/presentation/archive_pdf').glob('slide-*.png'));files.sort()
W,H=landscape(A3);out=O/'Archive/PROJADES_Five_Options_A3_Presentation_R01.pdf'
c=canvas.Canvas(str(out),pagesize=(W,H))
for f in files:c.drawImage(str(f),0,0,W,H);c.showPage()
c.save()
for p in (R/'99_Archive').rglob('*.pptx'):
 pdf=p.with_suffix('.pdf')
 if pdf.exists():shutil.copy2(pdf,O/'Archive'/pdf.name)
p=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03/PROJADES_Five_Options_A3_Review_R03.pdf';shutil.copy2(p,O/p.name)
for j in range(0,len(files),6):
 im=Image.new('RGB',(1800,1280),'#dddddd');d=ImageDraw.Draw(im)
 for k,f in enumerate(files[j:j+6]):
  a=Image.open(f);a.thumbnail((590,600));x=k%3*600;y=k//3*640+25;im.paste(a,(x,y));d.text((x,y-20),f.stem,fill='black')
 im.save(R/f'tmp/presentation/archive_pdf/check_{j//6}.jpg')
res={}
for p in O.rglob('*.pdf'):
 doc=PdfReader(p);assert all(abs(float(pg.mediabox.width)-W)<.1 and abs(float(pg.mediabox.height)-H)<.1 for pg in doc.pages);res[p.name]=len(doc.pages)
(O/'README.txt').write_text('Current presentation: PROJADES_Five_Options_A3_Review_R03.pdf\nArchive contains superseded R01 and R02 presentations, preserved as historical versions.\nAll PDFs use A3 landscape. Original PPTX files remain unchanged.\n',encoding='utf-8')
with zipfile.ZipFile(O.parent/'PROJADES_Presentation_PDFs.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(O))
print(json.dumps(res))
