from build_options import *
from reportlab.lib.pagesizes import A3, landscape
W,H=landscape(A3)
OUT=ROOT/'05_Presentations_and_Issued'/'Presentations'/'PROJADES_Design_Review_R03'
OUT.mkdir(parents=True,exist_ok=True)
BRAND=ROOT/'00_Project_Admin'/'Brand_Templates';BRAND.mkdir(exist_ok=True)
def frame(c,title,sheet,subtitle='',option='ALL'):
    c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(HexColor(INK));c.setLineWidth(.65);c.rect(28,28,W-56,H-56,fill=0,stroke=1)
    text(c,44,H-65,title,23,True);text(c,44,H-88,subtitle,11,color=MUTED)
    c.line(28,95,W-28,95)
    for x in [276,718,900,1038]:c.line(x,28,x,95)
    text(c,44,61,'PROJADES',23,True);text(c,44,42,'ARCHITECTURE / DESIGN STUDY',7.5,color=MUTED)
    text(c,292,73,'2360 HASSELL ROAD',12,True);text(c,292,55,'Hoffman Estates, Illinois',10)
    text(c,292,39,'OFFICE-TO-RESIDENTIAL / CONCEPT ONLY',8,color=AMBER)
    text(c,734,73,'OPTION '+str(option),10,True);text(c,734,54,'A3 / 420 × 297 mm',9)
    text(c,734,38,'FIT TO SHEET / NTS',8)
    text(c,916,73,'29.09.2026',10);text(c,916,52,'REVISION R03',9)
    text(c,1052,70,sheet,14,True);text(c,1052,44,'PROJADES',8)
titles={1:'Open kitchen and central core',2:'Perimeter kitchen and dining',3:'Shared-wall kitchen and balconies',4:'Separable kitchen',5:'Open L-shaped kitchen'}
bounds={1:[(80,419,613,964),(80,1549,613,2093)],2:[(32,505,529,1005),(32,1550,529,2054)],3:[(65,496,550,993),(65,1476,550,2057)]}
bounds[4]=bounds[1];bounds[5]=bounds[3]
notes={
1:['Original Option 1 is unchanged. This file is an A3 presentation copy.','Check the 3 ft island aisles with appliance doors open and more than one person using the kitchen.','The first-floor bathroom door opens close to the stair start. Review the door swing and landing together.'],
2:['Original Option 2 is unchanged. Dining arrangements differ between the upper and lower rows of units.','Stair lines overlap bathroom fixtures on the second floor. Clarify the drawing layers and floor opening.','The graphic overlap alone does not prove a physical clash. A stair section is required.'],
3:['Original Option 3 is unchanged. Kitchens move toward the shared wall and four balconies are shown.','The balcony edges do not show clear door symbols. Define the access openings.','Check the 3 ft island aisles together with dining chairs and the entry route.'],
4:['Based on Option 1. A glazed partition and sliding opening separate the kitchen. The island is removed.','Kitchen clear width: 8 ft 6 in plus a 6 in reserved service zone. Proposed depth: 9 ft in the upper row and 7 ft 6 in in the lower row.','SG = safety glazing at the new slider. The source stair/bath core remains unresolved; see the code review.'],
5:['Based on Option 3. The island is removed. An L-shaped counter adds preparation space.','Counter depth: 24 in. Short return: 6 ft. New 6 in service zone keeps kitchen piping outside the shared-wall cavity.','Balcony sliders require safety glazing. Thresholds, guards and structure remain unresolved; see the code review.']}
combined=PdfWriter()
for option in range(1,6):
    ow=PdfWriter();master=sources[option] if option<=3 else TMP/f'option{option}_master.pdf'
    for floor,b in enumerate(bounds[option],1):
        buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));sid=f'A-{option}0{floor}'
        frame(c,f'OPTION {option} / {titles[option]}',sid,f'{floor}. FLOOR PLAN / REVIEW SHEET',option)
        yy=H-139
        for k,note in enumerate(notes[option],1):
            text(c,810,yy,f'{k:02}',11,True,TEAL)
            yy=wrap(c,842,yy,note,280,12,18)-27
        text(c,810,yy,'DIMENSIONS AND SCALE',11,True,AMBER);yy-=24
        yy=wrap(c,810,yy,'Source interior dimensions are retained. Exterior references come from the converted DXF wall geometry. Units: feet / inches.',310,11,17)-15
        yy=wrap(c,810,yy,'The plan is fitted to the A3 sheet. Do not scale the print. New dimensions are proposals. S = 6 in service zone; not a code minimum. See the R03 code review.',310,11,17)-15
        wrap(c,810,yy,'Title block and new notes: Arial. Original drawing lettering is retained. The conversion reported dynamic-block warnings.',310,10,15,MUTED)
        x0,y0,x1,y1=b
        sc=min(660/(x1-x0),560/(y1-y0));dx=83+(660-(x1-x0)*sc)/2;dy=130+(560-(y1-y0)*sc)/2
        shell={1:[(88.08,427.04,604.92,954.68),(88.08,1556.84,604.92,2084.48)],2:[(41.28,513.56,520.92,1003.04),(41.28,1561.76,520.92,2051.24)],3:[(74.64,505.64,543.6,984.44),(74.64,1530.8,543.6,2009.48)]}[1 if option==4 else 3 if option==5 else option][floor-1]
        lx=dx+(shell[0]-x0)*sc;rx=dx+(shell[2]-x0)*sc
        by=dy+(y1-shell[3])*sc;ty=dy+(y1-shell[1])*sc
        # Reference chains connect to the main wall envelope, excluding balconies.
        c.setStrokeColor(HexColor(MUTED));c.setLineWidth(.5)
        c.line(lx,709,rx,709)
        for x in [lx,rx]:
            c.line(x-3,706,x+3,712);c.line(x,ty+4,x,714)
        text(c,(lx+rx)/2-130,717,"MAIN BLOCK / 49'-11\"  [DXF REF.]",9,color=INK)
        c.line(60,by,60,ty)
        for y in [by,ty]:
            c.line(57,y-3,63,y+3);c.line(55,y,lx-4,y)
        c.saveState();c.translate(48,(by+ty)/2-65);c.rotate(90);text(c,0,0,"51'-0 1/8\"  [DXF REF.]",9);c.restoreState()
        text(c,94,113,'Exterior references describe the main wall envelope. Balconies and adjoining blocks are excluded.',8,color=MUTED)
        c.save();dest=PdfReader(buf).pages[0]
        src=PdfReader(master).pages[0];x0,y0,x1,y1=b
        for box in [src.cropbox,src.mediabox]:box.lower_left=(x0,2384-y1);box.upper_right=(x1,2384-y0)
        sc=min(660/(x1-x0),560/(y1-y0));dx=83+(660-(x1-x0)*sc)/2;dy=130+(560-(y1-y0)*sc)/2
        dest.merge_transformed_page(src,Transformation().translate(-x0,-(2384-y1)).scale(sc).translate(dx,dy))
        ow.add_page(dest);combined.add_page(dest)
        crop_png(master,b,TMP/f'option{option}_floor{floor}.png')
    folder=ROOT/f'02_Design_Options/0{option}_Alternative_{option}'/'PDF'
    op=folder/f'PROJADES_Option_{option}_A3_Review_R03.pdf';ow.write(op)
combined.write(OUT/'PROJADES_All_Options_A3_Review_R03.pdf')
c=canvas.Canvas(str(BRAND/'PROJADES_A3_Title_Block_Template.pdf'),pagesize=(W,H))
frame(c,'DRAWING TITLE','A-000','DRAWING SUBTITLE',option='00');c.save()
(BRAND/'PROJADES_Wordmark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="720" height="140" viewBox="0 0 720 140"><text x="10" y="95" font-family="Arial, sans-serif" font-size="88" font-weight="700" letter-spacing="4" fill="#17332f">PROJADES</text></svg>',encoding='utf-8')
(BRAND/'Brand_Guidelines.txt').write_text('PROJADES / NEW PROJECT IDENTITY\nCreated for 2360 Hassell Road, 2026-09-29.\nWordmark: Arial Bold. New sheet text: Arial / Arial Bold.\nColors: #17332F, #27766E, #B1663C.\nA3 landscape, 420 x 297 mm, 10 mm border.\nTitle block fixed at bottom. Fit to sheet / NTS.\nOriginal source fonts are retained in options 1-3.\nEnglish filenames only.\n',encoding='utf-8')
issues=[
('R03','1, 2, 3','Kitchen aisles','A 3 ft aisle dimension appears around the islands.','Check the remaining clearance with appliance doors open. This is not a code violation finding.'),
('R03','1, 3','Bathroom door and stair','First-floor bathroom doors open close to the stair starts.','Review door swing, first tread and landing on an enlarged plan.'),
('R03','2','Second-floor graphics','Stair lines overlap bathroom fixture graphics.','Separate below/above-floor graphics. Verify the opening and headroom in section.'),
('R04','3','Balcony access','The balcony connections do not show clearly defined door openings.','Define door type, threshold, waterproofing and structural header.'),
('R05','1, 2, 3','Unit variations','Unit depths and some room dimensions differ between the rows.','Dimension each unit separately. Mirroring does not establish identical geometry.'),
('R06','1–5','Exterior dimension scope','The source sheets do not contain complete exterior dimension chains.','Add facade offsets, wall thicknesses and openings to the overall envelope dimensions.')]
rp=OUT/'PROJADES_Design_Review_and_Dimensions_R03.pdf'
c=canvas.Canvas(str(rp),pagesize=(W,H))
frame(c,'EXISTING OPTIONS / REVIEW NOTES','R-001','VISUAL REVIEW AND DXF DIMENSION REFERENCES')
y=H-137
for issue_index,(_,ops,title,obs,action) in enumerate(issues,1):
    ident=f'R{issue_index:02}'
    text(c,48,y,ident,12,True,AMBER);text(c,102,y,f'Option {ops} / {title}',14,True)
    y=wrap(c,102,y-22,obs,1010,12,17)
    y=wrap(c,102,y,action,1010,11,16,MUTED)-20
c.showPage();frame(c,'DIMENSIONS AND SOURCE CHECKS','R-002','FEET / INCHES / CAD REFERENCE')
y=H-142
for head,body in [
('Exterior envelope reference','Converted DXF wall envelope: approximately 599.04 in wide and 612.08–612.13 in deep. Sheets round to the nearest 1/8 in: 49 ft 11 in × 51 ft 0 1/8 in. Balconies and adjoining blocks are excluded.'),
('Interior dimensions','Source DIMENSION entities use inches. Examples include a 156 in room width, 120 in room depth and 36 in aisle. PDF interior dimensions are retained. New design dimensions are separate proposals.'),
('Option 4','Kitchen clear width: 102 in plus a 6 in reserved service zone. Upper-row depth: 108 in. Lower-row depth: 90 in. Develop the glazing and sliding opening together with appliance and fabrication dimensions.'),
('Option 5','Counter depth: 24 in. Short L return: 72 in. The long run depends on the existing unit depth. Check clearances with appliance doors open and dining chairs in use.'),
('Conversion and fonts','LibreDWG 0.14 produced the DXF. ezdxf 1.4.4 read its units and 229 dimension entities. Dynamic-block warnings require comparison with the source PDFs. Custom font files such as condhand.shx are unavailable.'),
('Outstanding checks','Complete opening chains, stair sections, balcony structure, wall assemblies and field verification remain outstanding. This set supports concept selection and design review.')]:
    text(c,48,y,head,15,True);y=wrap(c,48,y-25,body,1065,13,19)-20
c.save()
for k,v in hashes.items():assert hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v
print('A3 package ready:',OUT)
