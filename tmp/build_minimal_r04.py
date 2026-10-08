from pathlib import Path
from io import BytesIO
import math,hashlib,csv,json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A3,landscape
from pypdf import PdfReader,PdfWriter,Transformation
import pypdfium2 as pdfium

R=Path(__file__).resolve().parents[1];T=R/'tmp/minimal_r04';T.mkdir(exist_ok=True)
O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Minimalist_Options_R04';O.mkdir(exist_ok=True)
for n,f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
INK='#17332F';GREEN='#27766E';MUTED='#66736F';TAN='#B1663C'
W,H=landscape(A3)
def text(c,x,y,s,size=11,bold=False,color=INK):
 c.setFillColor(HexColor(color));c.setFont('Arial-Bold' if bold else 'Arial',size);c.drawString(x,y,s)
def wrap(c,x,y,s,width,size=11,leading=17,color=INK):
 line=''
 for word in s.split():
  test=(line+' '+word).strip()
  if pdfmetrics.stringWidth(test,'Arial',size)>width:text(c,x,y,line,size,color=color);y-=leading;line=word
  else:line=test
 if line:text(c,x,y,line,size,color=color);y-=leading
 return y
def frame(c,title,sheet,sub,op):
 c.setStrokeColor(HexColor(INK));c.setLineWidth(.65);c.rect(28,28,W-56,H-56)
 text(c,44,H-65,title,23,True);text(c,44,H-89,sub,10,color=MUTED)
 c.line(28,95,W-28,95)
 for x in [276,718,900,1038]:c.line(x,28,x,95)
 text(c,44,61,'PROJADES',23,True);text(c,44,42,'ARCHITECTURE / DESIGN STUDY',7.5,color=MUTED)
 text(c,292,73,'2360 HASSELL ROAD',12,True);text(c,292,55,'Hoffman Estates, Illinois',10)
 text(c,292,39,'OFFICE-TO-RESIDENTIAL / CONCEPT ONLY',8,color=TAN)
 text(c,734,73,'OPTION '+str(op),10,True);text(c,734,54,'A3 / 420 x 297 mm',9);text(c,734,38,'FIT TO SHEET / NTS',8)
 text(c,916,73,'29.09.2026',10);text(c,916,52,'REVISION R04',9);text(c,1052,70,sheet,14,True)

class Unit:
 def __init__(self,c,x,y,w,h,s,mx,my):self.c=c;self.x=x;self.y=y;self.s=s;self.w=w/s;self.h=h/s;self.mx=mx;self.my=my
 def pt(self,u,v):return(self.x+(self.w-u if self.mx else u)*self.s,2384-self.y-(self.h-v if self.my else v)*self.s)
 def line(self,a,b,col=GREEN,lw=.65):
  self.c.setStrokeColor(HexColor(col));self.c.setLineWidth(lw);self.c.line(*self.pt(*a),*self.pt(*b))
 def rect(self,x,y,w,h,fill='#E9F0ED'):
  a,b=self.pt(x,y);d,e=self.pt(x+w,y+h);self.c.setStrokeColor(HexColor(GREEN));self.c.setLineWidth(.6)
  if fill:self.c.setFillColor(HexColor(fill))
  self.c.rect(min(a,d),min(b,e),abs(d-a),abs(e-b),stroke=1,fill=bool(fill))
 def label(self,x,y,s,size=4.5):
  a,b=self.pt(x,y);self.c.setFillColor(HexColor(GREEN));self.c.setFont('Arial',size);self.c.drawCentredString(a,b,s)
 def dim(self,x1,x2,y,label):
  self.line((x1,y),(x2,y),INK,.35)
  for x in [x1,x2]:self.line((x-2,y-2),(x+2,y+2),INK,.4)
  self.label((x1+x2)/2,y-4,label,4.6)
 def dimv(self,x,y1,y2,label):
  self.line((x,y1),(x,y2),INK,.35)
  for y in [y1,y2]:self.line((x-2,y-2),(x+2,y+2),INK,.4)
  a,b=self.pt(x-4,(y1+y2)/2);self.c.saveState();self.c.translate(a,b);self.c.rotate(90);self.c.setFont('Arial',4.5);self.c.setFillColor(HexColor(GREEN));self.c.drawCentredString(0,0,label);self.c.restoreState()
 def furnish(self,op):
  # Furniture sizes in inches: no shrinking symbols to make the plan appear to fit.
  self.rect(0,0,24,18);self.label(12,11,'COAT',4)
  self.rect(96,0,60,18);self.label(126,11,'BENCH',4)
  self.rect(96,24,60,30,'#F4EEE3')
  for x in [100,133]:self.rect(x,60,18,18,None)
  self.label(126,42,'DINING',4.3)
  self.rect(0,self.h-36,84,36);self.rect(4,self.h-32,76,24,None)
  for x in [28,56]:self.line((x,self.h-32),(x,self.h-8),lw=.35)
  self.label(42,self.h-16,'84 x 36 SOFA',4.2)
  self.rect(24,self.h-66,48,24,'#F4EEE3')
  self.label(123,self.h-13,'LIVING',5)
  # Design target: reserved route to source core, independent of kitchen work aisle.
  self.dim(self.w-78,self.w-30,87 if op==4 else 70,'48 CLR')
  self.label(174,self.h-18,'TO CORE',4.3)
  self.dim(96,156,22,"5'-0\"")
  self.dimv(89,24,54,"2'-6\"")
 def entry(self,pdfu):
  u=pdfu/self.s;r=29/self.s;self.line((u,0),(u,r),INK)
  prior=(u,r)
  for j in range(1,21):
   a=math.pi/2*(1-j/20);q=(u+r*math.cos(a),r*math.sin(a));self.line(prior,q,INK,.4);prior=q

boxes={4:[(96.8,435.8,245.2,159.2,False,False),(351,435.8,231,159.2,True,False),(96.8,821.1,245.2,124.8,False,True),(351,821.1,245.1,124.8,True,True)],5:[(82.55,513.55,222.5,144.5,False,False),(313.2,513.55,209.5,144.5,True,False),(82.55,863.25,222.5,113.15,False,True),(313.2,863.25,222.5,113.15,True,True)]}
sources={4:R/'02_Design_Options/01_Alternative_1/PDF/ALTERNATIVE_1.pdf',5:R/'02_Design_Options/03_Alternative_3/PDF/ALTERNATIVE_3.pdf'}
bounds={4:[(80,419,613,964),(80,1549,613,2093)],5:[(65,496,550,993),(65,1476,550,2057)]}
titles={4:'Linear kitchen / integrated dining',5:'Compact L kitchen / integrated dining'}
register=[]
for op in [4,5]:
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(1684,2384));s=(245.4 if op==4 else 222.72)/284.74823196608486
 for k,(x,y,w,h,mx,my) in enumerate(boxes[op],1):
  c.setFillColor(white);c.rect(x,2384-y-h,w,h,fill=1,stroke=0)
  d=Unit(c,x,y,w,h,s,mx,my);d.entry(41 if op==4 else 35);d.furnish(op)
  right=d.w-6
  if op==4:
   d.rect(right,0,6,144,'#F4EEE3');d.label(right+3,75,'S',4)
   yy=0
   for name,length in [('R',30),('SINK',24),('DW',24),('PREP',30),('HOB',24),('END',12)]:
    d.rect(right-24,yy,24,length);d.label(right-12,yy+length/2+2,name,4.1);yy+=length
   d.dimv(right-34,0,144,"12'-0\"")
   d.dim(right-24,right,151,"2'-0\"") if d.h>160 else None
  else:
   start=d.h-120;d.rect(right,start,6,120,'#F4EEE3');d.label(right+3,start+58,'S',4)
   yy=start
   for name,length in [('R',30),('SINK',24),('DW',24),('PREP',18),('CORNER',24)]:
    d.rect(right-24,yy,24,length);d.label(right-12,yy+length/2+2,name,3.8);yy+=length
   d.rect(right-60,d.h-24,36,24);d.label(right-42,d.h-12,'HOB / END',3.8)
   d.dimv(right-34,start,d.h,"10'-0\"")
   d.dim(right-60,right,d.h-31,"5'-0\"")
  # Clear work aisle is inside the room; dining ends at x=156.
  assert d.w-30-48>=156,(op,k,'work aisle collision')
  assert (144 if op==4 else 120)<=d.h,(op,k,'cabinet exceeds depth')
  register.append({'option':op,'unit_position':k,'room_width_in':round(d.w,2),'room_depth_in':round(d.h,2),'cabinet_footprint_sqft':24 if op==4 else 26,'reserved_service_zone_in':6,'work_aisle_target_in':48,'sofa_in':'84 x 36','table_in':'60 x 30','bench_in':'60 x 18'})
 if op==5:
  for x,y,width in [(118,1530.8,55),(433,1530.8,54),(118,2001.6,55),(446,2001.6,55)]:
   c.setFillColor(white);c.rect(x,2384-y-9,width,12,fill=1,stroke=0);c.setStrokeColor(HexColor(GREEN));c.setLineWidth(.85)
   c.line(x,2384-y-2,x+width*.6,2384-y-2);c.line(x+width*.4,2384-y-5,x+width,2384-y-5)
   c.line(x,2384-y+2,x,2384-y-9);c.line(x+width,2384-y+2,x+width,2384-y-9)
 c.save();pg=PdfReader(sources[op]).pages[0];pg.merge_page(PdfReader(buf).pages[0]);pw=PdfWriter();pw.add_page(pg);pw.write(T/f'option{op}_master.pdf')
 doc=pdfium.PdfDocument(str(T/f'option{op}_master.pdf'));im=doc[0].render(scale=3).to_pil()
 for floor,b in enumerate(bounds[op],1):im.crop(tuple(round(a*3) for a in b)).save(T/f'option{op}_floor{floor}.png')

combined=PdfWriter()
notes={4:[('Simplify','The glazed kitchen enclosure, return storage and loose accent chair are removed. A single 12 ft cabinet run replaces the enclosed layout.'),('Use the perimeter','A 60 x 18 in low dining bench and 60 x 30 in table seat four with two loose chairs. Check sill height before fabrication.'),('Keep usable clearances','A 48 in kitchen work-aisle target is reserved clear of the fixed dining footprint. A 6 in service allowance remains outside the shared wall.')],5:[('Shorten the kitchen','The L becomes 10 ft by 5 ft overall, with a 24 in counter depth. The former 6 ft return is shortened by 12 in.'),('Consolidate furniture','A fixed dining bench replaces two loose chairs. One 84 x 36 in sofa and one 48 x 24 in coffee table define the lounge.'),('Retain flexibility','No island or new enclosing wall. The center remains shared living/circulation space. A separate 6 in service allowance is retained.')]}
for op in [4,5]:
 writer=PdfWriter()
 for floor,b in enumerate(bounds[op],1):
  buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));frame(c,f'OPTION {op} / {titles[op]}',f'A-{op}0{floor}',f'FLOOR {floor} / MINIMALIST PLAN REVISION',op)
  y=H-142
  arr=notes[op] if floor==1 else [('Upper-floor scope','Bedroom/bathroom partitions remain based on source Option '+('1' if op==4 else '3')+'. This revision concentrates the space-saving changes in the ground-floor living zone.'),('No invented area gain','No change to the external envelope or room count is claimed. Upper-floor circulation has not been quantified or redesigned.'),('Development hold points','Stairs, bathroom doors, rated separations, rescue openings and structural floor conditions remain unresolved. See the R03 code review.')]
  for head,body in arr:
   text(c,810,y,head.upper(),11,True,GREEN);y=wrap(c,810,y-22,body,310,11.5,18)-25
  y=wrap(c,810,y,('DIMENSIONS: proposed inches / feet. Compact 30 in refrigerator and 24 in hob are design assumptions; confirm selected products.' if floor==1 else 'Source interior dimensions are retained. Main envelope dimensions are converted-DXF references, excluding balconies and adjoining blocks.'),310,10,16,TAN)-15
  wrap(c,810,y,'48 in is a design target, not a compliance finding. Check appliance doors, occupied chairs and the route into the core. S = service zone. Original Options 1-3 remain unchanged.',310,10,16,MUTED)
  text(c,93,113,'Green: revised concept geometry. Black: source proposal. Dimensions require detailed CAD and field verification.',8,color=MUTED)
  x0,y0,x1,y1=b
  sc=min(660/(x1-x0),575/(y1-y0));dx=83+(660-(x1-x0)*sc)/2;dy=128+(575-(y1-y0)*sc)/2
  shell={4:[(88.08,427.04,604.92,954.68),(88.08,1556.84,604.92,2084.48)],5:[(74.64,505.64,543.6,984.44),(74.64,1530.8,543.6,2009.48)]}[op][floor-1]
  lx=dx+(shell[0]-x0)*sc;rx=dx+(shell[2]-x0)*sc;by=dy+(y1-shell[3])*sc;ty=dy+(y1-shell[1])*sc
  c.setStrokeColor(HexColor(MUTED));c.setLineWidth(.4);c.line(lx,719,rx,719)
  for x in [lx,rx]:c.line(x-3,716,x+3,722);c.line(x,ty+3,x,722)
  text(c,(lx+rx)/2-112,727,"MAIN BLOCK / 49'-11\" [DXF REF.]",9,color=MUTED)
  c.line(61,by,61,ty)
  for yy in [by,ty]:c.line(58,yy-3,64,yy+3);c.line(58,yy,lx-3,yy)
  c.saveState();c.translate(51,(by+ty)/2-63);c.rotate(90);text(c,0,0,"51'-0 1/8\" [DXF REF.]",9,color=MUTED);c.restoreState()
  c.save();dest=PdfReader(buf).pages[0];src=PdfReader(T/f'option{op}_master.pdf').pages[0]
  for bb in [src.cropbox,src.mediabox]:bb.lower_left=(x0,2384-y1);bb.upper_right=(x1,2384-y0)
  sc=min(660/(x1-x0),575/(y1-y0));dx=83+(660-(x1-x0)*sc)/2;dy=128+(575-(y1-y0)*sc)/2
  dest.merge_transformed_page(src,Transformation().translate(-x0,-(2384-y1)).scale(sc).translate(dx,dy));writer.add_page(dest);combined.add_page(dest)
 # Enlarged upper/lower units reveal the actual furniture and cabinet dimensions.
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));frame(c,f'OPTION {op} / space-use study',f'A-{op}03','ENLARGED GROUND-FLOOR SOCIAL ZONES / CONCEPT DIMENSIONS',op)
 doc=pdfium.PdfDocument(str(T/f'option{op}_master.pdf'));im=doc[0].render(scale=4).to_pil()
 for idx,xsheet in [(0,48),(2,425)]:
  x,y,w,h,mx,my=boxes[op][idx];crop=im.crop(tuple(round(a*4) for a in (x-3,y-3,x+w+12,y+h+4)));p=T/f'detail_{op}_{idx}.png';crop.save(p)
  iw,ih=crop.size;sc=min(350/iw,450/ih);c.drawImage(str(p),xsheet,660-ih*sc,iw*sc,ih*sc)
  text(c,xsheet,707,'UPPER ROW' if idx==0 else 'LOWER ROW',11,True)
 y=H-145
 for head,body in [('Cabinet footprint',('24 sq ft: 144 x 24 in single run.' if op==4 else '26 sq ft: (120 + 60 - 24) x 24 in L-shaped run.')+' This excludes the service zone and circulation.'),('Furniture schedule','Sofa 84 x 36 in; table 60 x 30 in; bench 60 x 18 in; two chairs 18 x 18 in; coffee table 48 x 24 in.'),('Efficiency claim','The design consolidates furniture at the perimeter and reduces fixed obstructions. It does not increase gross floor area or establish a measured percentage of space saved.'),('Remaining coordination','Core layout and upper floor still need design development. Do not treat the retained source stair or bath as approved or as-built.')]:
  text(c,810,y,head,12,True,GREEN);y=wrap(c,810,y-23,body,310,11,17)-24
 text(c,48,269,'DESIGN INTENT',12,True,GREEN)
 wrap(c,48,246,('One continuous kitchen run replaces the separate glazed room. The dining bench provides seating and under-seat storage with fewer loose pieces.' if op==4 else 'The compact L retains a separate cooking return while reducing its projection. Dining and lounge furniture use the same measured modules as Option 4.'),700,12,19)
 wrap(c,48,176,'The 48 in aisle is a proposed clear zone at the kitchen front. Confirm actual appliance projections and door swings before fixing the joinery.',700,11,17,MUTED)
 c.save();pg=PdfReader(buf).pages[0];writer.add_page(pg);combined.add_page(pg)
 path=O/f'PROJADES_Option_{op}_Minimalist_A3_R04.pdf';writer.write(path)
 import shutil
 shutil.copy2(path,R/f'02_Design_Options/0{op}_Alternative_{op}/PDF'/path.name)
combined.write(O/'PROJADES_Options_4_and_5_Minimalist_A3_R04.pdf')
(O/'Furniture_and_Cabinet_Schedule_R04.json').write_text(json.dumps(register,indent=2),encoding='utf-8')
with (R/'brain.md').open('a',encoding='utf-8') as f:f.write('''

## Minimalist revision R04 / 2026-09-29
- User requested less wasted space and minimalist layouts for Options 4 and 5.
- Option 4: removed kitchen enclosure; 12 ft single cabinet run, integrated dining bench, consolidated lounge furniture.
- Option 5: shortened L kitchen to 10 ft x 5 ft; integrated dining bench and consolidated lounge furniture.
- Both retain 6 in service allowances and show a 48 in kitchen work-aisle design target. Cabinet footprints are 24/26 sq ft, excluding service zones and circulation.
- Upper-floor partitions and stair/bath cores remain reference proposals pending sections, floor heights and code/structural coordination. They are not existing walls.
- Current focused option drawings: PROJADES_Minimalist_Options_R04. R03 presentation is superseded for Options 4/5 layout only; its unresolved code-review items still apply.
- Original Options 1-3 remain unchanged. All new sheets are English, A3 landscape, Arial, PROJADES title block.
''')
for q in csv.DictReader((R/'00_Project_Admin/Source_Inventory.csv').open(encoding='utf-8-sig')):assert hashlib.sha256((R/q['current_path']).read_bytes()).hexdigest()==q['sha256']
d=pdfium.PdfDocument(str(O/'PROJADES_Options_4_and_5_Minimalist_A3_R04.pdf'))
for i,p in enumerate(d):p.render(scale=1.3).to_pil().save(T/f'page_{i+1}.png')
print('R04 complete: 6 A3 sheets. Original source hashes match.')
