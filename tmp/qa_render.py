from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[1];T=R/'tmp/pdfs';O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03'
for op in [4,5]:
 im=Image.open(T/f'option{op}_floor1.png');im.crop((0,0,im.width,round(im.height*.56))).save(T/f'detail{op}.png')
for name in ['PROJADES_All_Options_A3_Review_R03','PROJADES_Design_Review_and_Dimensions_R03']:
 d=pdfium.PdfDocument(str(O/(name+'.pdf')));folder=T/name;folder.mkdir(exist_ok=True)
 for i,p in enumerate(d):p.render(scale=1).to_pil().save(folder/f'page_{i+1:02}.png')
folders=[T/'code_review',T/'PROJADES_All_Options_A3_Review_R03',T/'PROJADES_Design_Review_and_Dimensions_R03',R/'tmp/presentation/rendered']
for folder in folders:
 files=sorted(folder.glob('*.png'))
 for j in range(0,len(files),4):
  sheet=Image.new('RGB',(1600,1180),'#d7d7d7');draw=ImageDraw.Draw(sheet)
  for k,f in enumerate(files[j:j+4]):
   im=Image.open(f).convert('RGB');im.thumbnail((780,550));x=10+(k%2)*800;y=30+(k//2)*590
   sheet.paste(im,(x,y));draw.text((x,y-20),f.name,fill='black')
  sheet.save(T/f'qa_{folder.name}_{j//4+1}.jpg')
print('QA contact sheets and updated plan details ready')
