from pathlib import Path
from io import BytesIO
import hashlib, json, math
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter, Transformation
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'tmp'/'pdfs'; TMP.mkdir(parents=True,exist_ok=True)
for n,f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(Path('C:/Windows/Fonts')/f)))
INK='#17332F'; TEAL='#27766E'; MUTED='#66736F'; PAPER='#F5F3ED'; AMBER='#B1663C'
sources={i:ROOT/f'02_Design_Options/0{i}_Alternative_{i}/PDF/ALTERNATIVE_{i}.pdf' for i in range(1,4)}
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources.values()}
(TMP/'original_hashes.json').write_text(json.dumps(hashes,indent=2))
def text(c,x,y,s,size=11,bold=False,color=INK):
    c.setFillColor(HexColor(color)); c.setFont('Arial-Bold' if bold else 'Arial',size);c.drawString(x,y,s)
def wrap(c,x,y,s,width,size=13,leading=19,color=INK):
    words=s.split();line=''
    for word in words:
        test=(line+' '+word).strip()
        if pdfmetrics.stringWidth(test,'Arial',size)>width:
            text(c,x,y,line,size,color=color);y-=leading;line=word
        else:line=test
    if line:text(c,x,y,line,size,color=color);y-=leading
    return y

# New design geometry is drawn in local PDF units, using the supplied shell.
# It is deliberately not dimensioned as verified CAD geometry.
class Local:
    def __init__(self,c,x,y,w,h,mx=False,my=False): self.c=c;self.x=x;self.y=y;self.w=w;self.h=h;self.mx=mx;self.my=my
    def pt(self,u,v):return (self.x+(self.w-u if self.mx else u),2384-(self.y+(self.h-v if self.my else v)))
    def line(self,a,b,width=.8,col=TEAL):
        self.c.setStrokeColor(HexColor(col));self.c.setLineWidth(width);self.c.line(*self.pt(*a),*self.pt(*b))
    def rect(self,u,v,w,h,fill=None,width=.7):
        xx,yy=self.pt(u,v);xx2,yy2=self.pt(u+w,v+h)
        self.c.setStrokeColor(HexColor(TEAL));self.c.setLineWidth(width)
        if fill:self.c.setFillColor(HexColor(fill))
        self.c.rect(min(xx,xx2),min(yy,yy2),abs(xx2-xx),abs(yy2-yy),stroke=1,fill=bool(fill))
    def label(self,u,v,s,size=5):
        x,y=self.pt(u,v);self.c.setFillColor(HexColor(TEAL));self.c.setFont('Arial',size);self.c.drawCentredString(x,y,s)
    def table(self,u,v):
        self.rect(u-22,v-12,44,24,fill='#F4EEE3')
        for a,b,w,h in [(u-14,v-20,12,7),(u+3,v-20,12,7),(u-14,v+13,12,7),(u+3,v+13,12,7)]:self.rect(a,b,w,h)
    def sofa(self,u,v,w=27,h=63):
        self.rect(u,v,w,h,fill='#E9F0ED');self.rect(u+3,v+4,w-6,h-8)
        for yy in [v+h/3,v+2*h/3]:self.line((u+3,yy),(u+w-3,yy),.4)
    def kitchen(self,u,v,h):
        self.rect(u,v,22,h,fill='#E9F0ED')
        # Four fixture zones, with labels instead of undocumented equipment sizes.
        seg=h/4
        for j,name in enumerate(['R','SINK','DW','HOB']):
            self.line((u,v+j*seg),(u+22,v+j*seg),.5);self.label(u+11,v+(j+.56)*seg,name,4.7)
    def dim(self,u1,u2,v,label):
        self.line((u1,v),(u2,v),.35,col=INK)
        for u in [u1,u2]:self.line((u-1.5,v+1.5),(u+1.5,v-1.5),.6,col=INK)
        self.label((u1+u2)/2,v-3,label,5)
    def dimv(self,u,v1,v2,label):
        self.line((u,v1),(u,v2),.35,col=INK)
        for v in [v1,v2]:self.line((u-1.5,v+1.5),(u+1.5,v-1.5),.6,col=INK)
        x,y=self.pt(u-3,(v1+v2)/2)
        self.c.saveState();self.c.translate(x,y);self.c.rotate(90)
        self.c.setFont('Arial',5);self.c.setFillColor(HexColor(TEAL));self.c.drawCentredString(0,0,label);self.c.restoreState()
    def entry(self,u=42):
        # Swing schematic, same opening as source; local front is v=0.
        self.line((u,0),(u,29),.7,col=INK)
        prev=(u,29)
        for j in range(1,17):
            a=math.pi/2*(1-j/16);p=(u+29*math.cos(a),29*math.sin(a));self.line(prev,p,.45,col=INK);prev=p

def overlay(option):
    source=sources[1 if option==4 else 3]
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=(1684,2384))
    if option==4:
        boxes=[(96.8,435.8,245.2,159.2,False,False),(351,435.8,231,159.2,True,False),(96.8,821.1,245.2,124.8,False,True),(351,821.1,245.1,124.8,True,True)]
    else:
        boxes=[(82.55,513.55,222.5,144.5,False,False),(313.2,513.55,209.5,144.5,True,False),(82.55,863.25,222.5,113.15,False,True),(313.2,863.25,222.5,113.15,True,True)]
    for x,y,w,h,mx,my in boxes:
        c.setFillColor(white);c.rect(x,2384-y-h,w,h,fill=1,stroke=0)
        d=Local(c,x,y,w,h,mx,my)
        d.entry(41 if option==4 else 35)
        d.rect(4,5,28,19,fill='#E9F0ED');d.label(18,16,'COAT',4.5)
        if option==4:
            s=245.4/284.74823196608486
            chase=6*s;kw=102*s;depth=(108 if h>140 else 90)*s;right=w-chase;left=right-kw
            d.rect(right,0,chase,depth,fill='#F4EEE3');d.label(right+chase/2,depth/2,'S',4)
            d.kitchen(right-22,20,depth-20)
            d.rect(left+3,3,kw-6,17,fill='#E9F0ED');d.label(left+kw/2,14,'COUNTER / STORAGE',4.5)
            # Glazed kitchen enclosure, sliding opening on the room-facing edge.
            d.line((left,0),(left,depth),1.2);d.line((left+2,0),(left+2,depth),.35)
            d.line((left,depth),(left+8,depth),1.2);d.line((left+62,depth),(right,depth),1.2)
            d.line((left+8,depth+1),(left+35,depth+1),.5);d.line((left+35,depth-1),(left+62,depth-1),.5)
            d.label(left+34,depth-8,'SG / SLIDER',4.5)
            d.label(left+31,45,'KITCHEN',5.5)
            d.dim(left,right,depth+11,"8'-6\" CLEAR")
            d.dimv(left-8,0,depth,"9'-0\"" if h>140 else "7'-6\"")
            d.table(106,35)
            d.sofa(6,h-71,27,64)
            d.rect(52,h-57,23,34,fill='#F4EEE3')
            d.rect(103,h-38,18,20,fill='#E9F0ED')
            d.label(78,h-7,'LIVING',5.5)
        else:
            s=222.72/284.74823196608486;cd=24*s
            chase=6*s;right=w-chase
            d.rect(right,3,chase,h-3,fill='#F4EEE3');d.label(right+chase/2,h/2,'S',4)
            d.rect(right-cd,3,cd,h-3,fill='#E9F0ED')
            d.rect(right-72*s,h-cd,72*s,cd,fill='#E9F0ED')
            yy=3
            for name,inch in [('R',36),('PREP',18),('SINK',30),('DW',24)]:
                hh=inch*s;d.line((right-cd,yy),(right,yy),.5);d.label(right-cd/2,yy+hh/2,name,4.5);yy+=hh
            d.label(right-49*s,h-cd/2,'HOB',4.5)
            d.dim(right-72*s,right,h-cd-9,"6'-0\"")
            d.dimv(right-72*s-6,h-cd,h,"2'-0\"")
            d.table(w-109,34)
            d.sofa(6,h-69,26,63)
            d.rect(51,h-55,22,31,fill='#F4EEE3')
            # Keep the route to the existing stair opening free of an island.
            d.label(110,h-32,'CLEAR ROUTE',4.7)
            d.label(73,h-7,'LIVING',5.5)
    if option==5:
        # Replace the four window symbols at balcony edges with proposed sliders.
        # These are opening proposals; lintel, threshold and facade checks remain.
        for x,y,width in [(118,1530.8,55),(433,1530.8,54),(118,2001.6,55),(446,2001.6,55)]:
            c.setFillColor(white);c.rect(x,2384-y-9,width,12,fill=1,stroke=0)
            c.setStrokeColor(HexColor(TEAL));c.setLineWidth(.85)
            c.line(x,2384-y-2,x+width*.6,2384-y-2)
            c.line(x+width*.4,2384-y-5,x+width,2384-y-5)
            c.line(x,2384-y+2,x,2384-y-9);c.line(x+width,2384-y+2,x+width,2384-y-9)
    c.save(); page=PdfReader(source).pages[0];page.merge_page(PdfReader(buf).pages[0])
    writer=PdfWriter();writer.add_page(page);path=TMP/f'option{option}_master.pdf';writer.write(path)
    return path

def crop_png(path,bounds,out,scale=3):
    doc=pdfium.PdfDocument(str(path));im=doc[0].render(scale=scale).to_pil()
    x0,y0,x1,y1=bounds;im.crop(tuple(round(a*scale) for a in bounds)).save(out)

def option_pdf(option,master):
    outdir=ROOT/f'02_Design_Options/0{option}_Alternative_{option}/PDF';outdir.mkdir(parents=True,exist_ok=True)
    (outdir.parent/'CAD').mkdir(exist_ok=True)
    title='Separable kitchen' if option==4 else 'Open kitchen without an island'
    crops=([(88,425,609,958),(88,1550,609,2095)] if option==4 else [(72,499,540,990),(72,1478,540,2055)])
    notes=[
      [('TASARIM KARARI','Mutfak, cam bölme ve sürme açıklıkla yaşam alanından ayrılır. Masa ve oturma grubu mutfak dışında kalır.'),('DOLAŞIM','Ada kaldırılır. Girişten mevcut merdiven holüne açık bir geçiş hedeflenir.'),('KORUNAN','Option 1’in dış duvarları, yatak odaları ve merdiven/banyo çekirdeği bu konseptin referansıdır.'),('KONTROL','Cam bölmenin açılımı, cihaz kapakları ve net geçişler DWG üzerinden ölçülmelidir.')],
      [('TASARIM KARARI','Option 1’in üst kat düzeni yeni konseptte referans olarak korunur. Bu katta yeniden planlama önerilmez.'),('PROGRAM','Alt kattaki yatak odası ile üst kattaki iki oda birlikte değerlendirilir. Kesin oda ve alan çizelgesi henüz yoktur.'),('KONTROL','Banyo kapıları, çamaşır dolabı ve merdiven sahanlığı birlikte kontrol edilmelidir. Kesit olmadan baş mesafesi doğrulanamaz.')]
    ] if option==4 else [
      [('TASARIM KARARI','Mutfak ortak duvar boyunca tek hat üzerinde toplanır. Ada kaldırılır ve yemek masası cepheye yakın konumlanır.'),('DOLAŞIM','Mutfak önündeki boş alan, giriş ile merdiven holü arasında daha kesintisiz bir kullanım hedefler.'),('KORUNAN','Option 3’ün dış sınırı, yatak odaları, merdiven ve banyo çekirdeği referans alınır.'),('KONTROL','Yeni tezgâh hattında hazırlık yüzeyi, cihaz ölçüleri ve tesisat yerleri ayrıntılandırılmalıdır.')],
      [('TASARIM KARARI','Dört balkon bağlantısına sürme kapı sembolü önerilir. Kaynakta pencere benzeri görünen bağlantı açıkça tanımlanır.'),('KORUNAN','Option 3’ün yatak odaları ve ıslak hacimleri bu aşamada korunur.'),('KONTROL','Kapı açıklığı, eşik, su yalıtımı, taşıyıcı başlık ve balkon taşıyıcısı ayrıca çözülmelidir. Balkon uygunluğu henüz doğrulanmış değildir.')]
    ]
    writer=PdfWriter()
    for floor,b in enumerate(crops,1):
        buf=BytesIO();c=canvas.Canvas(buf,pagesize=(1190.55,841.89))
        c.setFillColor(HexColor(PAPER));c.rect(0,0,1191,842,fill=1,stroke=0)
        text(c,42,795,'PROJADES',22,True)
        text(c,42,755,f'OPTION {option} / {title}',26,True)
        text(c,42,729,f'2360 Hassel Road, Hoffman Estates, IL  •  {floor}. kat planı',12)
        c.setFillColor(white);c.rect(35,66,706,638,fill=1,stroke=0)
        yy=680
        for heading,body in notes[floor-1]:
            text(c,776,yy,heading,12,True,TEAL);yy-=25
            yy=wrap(c,776,yy,body,365,14,21);yy-=25
        wrap(c,776,135,'Siyah: kaynak plan. Yeşil: yeni konsept önerisi. Plan ölçekli ölçüm için kullanılmaz.',360,11,16,MUTED)
        text(c,42,35,'KONSEPT ÇALIŞMASI / DWG VE KESİT DOĞRULAMASI BEKLİYOR',10,True,AMBER)
        text(c,995,35,f'29.09.2026 / R01 / {floor:02}',10)
        c.save();dest=PdfReader(buf).pages[0]
        src=PdfReader(master).pages[0];x0,y0,x1,y1=b
        src.cropbox.lower_left=(x0,2384-y1);src.cropbox.upper_right=(x1,2384-y0)
        src.mediabox.lower_left=(x0,2384-y1);src.mediabox.upper_right=(x1,2384-y0)
        sc=min(660/(x1-x0),610/(y1-y0));dx=58+(660-(x1-x0)*sc)/2;dy=78+(610-(y1-y0)*sc)/2
        dest.merge_transformed_page(src,Transformation().translate(-x0,-(2384-y1)).scale(sc).translate(dx,dy))
        writer.add_page(dest)
        crop_png(master,b,TMP/f'option{option}_floor{floor}.png')
    output=outdir/f'HE_Alternative_{option}_Concept_R01.pdf';writer.write(output)
    return output

for i in [4,5]:
    overlay(i)

# Source crops for slide evidence: original files remain unchanged.
for i in range(1,4):
    bounds=([(88,425,609,958),(88,1550,609,2095)] if i==1 else [(40,510,520,1030),(40,1610,520,2140)] if i==2 else [(72,499,540,990),(72,1478,540,2055)])
    if i==2:
        # Bounds derived from the source page, covering the entire detailed block.
        bounds=[(37,505,525,1022),(37,1549,525,2058)]
    for f,b in enumerate(bounds,1):crop_png(sources[i],b,TMP/f'option{i}_floor{f}.png')

for key,value in hashes.items():assert hashlib.sha256((ROOT/key).read_bytes()).hexdigest()==value
print('Original alternatives 1-3: SHA256 unchanged.')
