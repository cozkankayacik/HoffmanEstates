from pathlib import Path
from io import BytesIO
import csv,json,hashlib
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from pypdf import PdfReader,PdfWriter
import pypdfium2 as pdfium

R=Path(__file__).resolve().parents[1]
O=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03';O.mkdir(exist_ok=True)
REF=R/'01_Site_and_Reference/Zoning_and_Code';REF.mkdir(exist_ok=True)
for n,f in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
W,H=landscape(A3);green='#17332F';teal='#27766E';muted='#66736F';red='#A04730'
sources=[
('S01','Village adopted code list','2021 IBC, IRC, IEBC, IFC, IMC and IFGC; 2020 NEC; state codes.','https://www.hoffmanestates.org/services/permits_licenses/building_permits_inspections.php'),
('S02','Local adoption and amendments / Ordinance 5028-2023','R313 replacement (p.10); IFC 903.2 replacement (p.19); IEBC amendments (pp.13-14). Cross-check later ordinances at permit application.','https://mcclibraryfunctions.azurewebsites.us/api/ordinanceDownload/13575/1223302/pdf'),
('S03','Illinois energy rules / 71 IAC 600','Current adopted 2024 energy code and state amendments; effective November 30, 2025.','https://www.ilga.gov/agencies/JCAR/EntirePart?titlepart=07100600'),
('S04','2021 IEBC / Chapter 10','Work-area method change-of-occupancy provisions, including 1006 and 1011.2.1.','https://codes.iccsafe.org/content/IEBC2021V2.0/chapter-10-change-of-occupancy'),
('S05','2021 IRC / Chapter 3','Conditional IRC criteria: R302.2, R310, R311; apply only under the accepted code pathway.','https://codes.iccsafe.org/content/IRC2021P1/chapter-3-building-planning'),
('S06','2021 IRC / townhouse definition','ICC published explanation of R202 and the townhouse-unit definition.','https://shop.iccsafe.org/media/wysiwyg/material/7101S21-Sample.pdf'),
('S07','2021 IBC / occupancy classification','Section 310.3: evaluate R-2 if more than two dwellings are within an IBC-regulated building.','https://codes.iccsafe.org/content/IBC2021V2.0/chapter-3-occupancy-classification-and-use'),
('S08','Village zoning / Chapter 9','Approved zoning and conditions control. Sections 9-1-11 and 9-3-2 address occupancy and parking review.','https://library.municode.com/il/hoffman_estates/codes/code_of_ordinances?nodeId=CH9ZOCO'),
('S09','Illinois accessibility / 71 IAC 400','2018 Illinois Accessibility Code. Determine applicable conversion and residential scoping.','https://www.ilga.gov/commission/jcar/admincode/071/07100400sections.html'),
('S10','Illinois plumbing / 77 IAC 890','Use Illinois plumbing requirements, not a generic IRC plumbing checklist.','https://www.ilga.gov/agencies/JCAR/EntirePart?titlepart=07700890'),
('S11','ICC safety-glazing guidance','2021 IRC R308.4.1, glazing in swinging/sliding doors.','https://www.iccsafe.org/wp-content/uploads/Day-3-2021-IRC-Performing-Residential-Plan-Reviews.pdf'),
('S12','Village business directory','Municipal address spelling is 2360 HASSELL RD. This is address evidence, not permit or ownership evidence.','https://www.hoffmanestates.org/Documents/Business/Business%20Directory/Business%20-%20Directory.pdf?t=202512031025360'),
('S13','2021 IEBC / compliance methods','Section 301.3. Select an approved compliance method before applying chapter-specific tests.','https://codes.iccsafe.org/s/IEBC2021P1/chapter-3-provisions-for-all-compliance-methods/IEBC2021P1-Ch03-Sec301.3'),
('S14','ICC / mechanical ventilation clarification','2021 IRC R303.1 discussion: local kitchen exhaust can substitute for natural ventilation under applicable provisions.','https://www.iccsafe.org/building-safety-journal/bsj-technical/significant-changes-to-mechanical-ventilation-in-the-2021-international-residential-code/')]
issues=[
('C01','All','HOLD','Code pathway','Office-to-residential conversion confirmed. Existing B use is inferred, not documented. IRC townhouse eligibility is not yet established.','Obtain existing occupancy record and classify the complete building; select IEBC compliance method with the Village.','S01/S04/S06/S07/S13'),
('C02','All','HOLD','Approval conditions','Architect confirms zoning/conversion approval. Approved drawings and conditions are absent.','Reconcile total units, bedroom mix, balconies, parking and building outline with the actual approval. Do not infer a new rezoning requirement.','S08'),
('C03','All','HOLD','Sprinklers','Existing sprinkler status is unknown. Architect reports complete interior-wall demolition; assess the local full-interior-renovation trigger.','Resolve local IFC 903.2 and residential R313 with Fire Prevention; document system type, water supply and coverage. No sprinkler exemption assumed.','S02/S04'),
('C04','All','HOLD','Rated unit separation','Shared wall lines have no tested assembly, continuity, roof junction or penetration detail.','Provide rated assembly schedule and coordinated sections. Confirm structural independence/accepted exceptions if IRC applies.','S05/S07'),
('C05','4,5','PARTIAL','Kitchen services','Earlier concepts put sinks against shared walls without a defined service route. This did not prove piping was inside a rated cavity.','R03 reserves a separate 6 in zone on each kitchen side. Route services within each unit; engineer size, firestopping and floor penetrations.','S05'),
('C06','1,3,4,5','HOLD','Door and stair interface','Ground-floor bath doors are close to the first tread. Clear landing and door geometry are not fully dimensioned.','Provide enlarged measured plans and sections. Reposition/rehinge only after fixture clearance and landing geometry are verified.','S05'),
('C07','2','HOLD','Stair/bath overlap','Upper-floor stair lines overlap sanitary fixture graphics. A graphic conflict is visible; a physical conflict is unproven.','Separate floor-below linework and draw stair opening plus headroom section. Original Option 2 stays unchanged.','Drawing evidence'),
('C08','All','HOLD','Stair geometry','Riser count, floor height, tread/landing dimensions and headroom cannot be reconciled from the supplied set.','Survey levels and draw each distinct stair section. Verify handrails, guards and all turning treads under the accepted code.','S05'),
('C09','All','HOLD','Sleeping-room rescue','Bedroom windows are shown, but net clear opening, sill height and operating type are not scheduled.','Check every bedroom. Balcony access alone does not establish a compliant rescue opening or exit route.','S05'),
('C10','All','HOLD','Main entrance / discharge','Doors are drawn without a clear-opening or level schedule. External discharge to a public way is not documented.','Dimension clear openings, thresholds, landings and exterior routes; verify accessible entrance obligations.','S05/S09'),
('C11','3,5','PARTIAL','Balcony access and safety','Option 3 access symbols are ambiguous. Option 5 proposed sliders clarify intent but do not resolve construction.','Option 5 specifies safety glazing. Resolve structural headers, guards, loads, drainage and thresholds before release.','S11/S04'),
('C12','4','PARTIAL','Kitchen enclosure glazing','Earlier new glazing had no safety-glazing specification.','R03 specifies safety glazing at slider; check adjacent panels and the selected tested product. Keep appliance and door operation clear.','S11'),
('C13','All','HOLD','Accessibility','No site access slopes, threshold levels, scoping matrix or accessible-unit details supplied.','Establish state and applicable IBC/IEBC scoping, unit counts and common-area obligations. Ground-floor bedroom alone is not proof of accessibility.','S09/S13'),
('C14','All','HOLD','Existing structure / new floor','Interior walls are already removed, per architect. Existing/new floor structure and stability of the retained exterior shell are undocumented.','Verify retained-shell stability, columns, beams, foundations and any new floor/stair openings. Include dead loads, alterations and balcony support.','S04'),
('C15','All','HOLD','Energy and envelope','No wall/roof build-ups, window performance, air-sealing or compliance calculation supplied.','Prepare conversion-specific 2024 Illinois energy assessment and identify retained versus altered envelope elements.','S03'),
('C16','All','HOLD','Ventilation and utilities','No coordinated residential HVAC, exhaust, fresh air, water/sewer or electrical capacity plan supplied.','Locate equipment and shafts, exhaust outdoors, maintain separation and coordinate laundry/kitchen/bath services.','S01/S10/S14'),
('C17','All','HOLD','Smoke and CO detection','Architectural set does not show a coordinated alarm/detection plan.','Provide device layout, power/interconnection and system coordination under the accepted local/state code pathway.','S01/S02'),
('C18','1,2,3','REVIEW','Kitchen ergonomics','Selected source aisle dimensions are 36 in. Open appliance doors and chairs can reduce usable space.','Test actual equipment and occupied furniture. A 36 in kitchen aisle is not by itself a proven code violation.','Source DXF/PDF'),
('C19','All','REVIEW','Dimensions and furniture','Units differ by row and corner. Complete room/opening chains and measured clearances are missing.','Dimension each unit separately; select real appliances and furniture. Retained source dimensions are not field verification.','Source DXF/PDF'),
('C20','All','REVIEW','Storage and daily use','Laundry/service access, linen/general storage, entry coats and acoustic privacy are not consistently resolved.','Develop storage schedule and maintenance access; review sleeping-room privacy, daylight and demising-wall acoustics.','Architectural review')]

with (REF/'PROJADES_Code_Issue_Register_R03.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['ID','Options','Status','Topic','Evidence','Required_action_or_correction','Source']);w.writerows(issues)
(REF/'PROJADES_Code_Sources_R03.json').write_text(json.dumps({'review_date':'2026-09-29','sources':sources},indent=2),encoding='utf-8')

c=canvas.Canvas(str(O/'PROJADES_Code_Review_R03.pdf'),pagesize=(W,H));page=0
def t(x,y,s,size=12,bold=False,col=green):
 c.setFillColor(HexColor(col));c.setFont('Arial-Bold' if bold else 'Arial',size);c.drawString(x,y,s)
def wrap(x,y,s,width,size=12,leading=18,col=green):
 line=''
 for word in s.split():
  q=(line+' '+word).strip()
  if pdfmetrics.stringWidth(q,'Arial',size)>width:t(x,y,line,size,col=col);y-=leading;line=word
  else:line=q
 if line:t(x,y,line,size,col=col);y-=leading
 return y
def new(title,sub):
 global page
 if page:c.showPage()
 page+=1;c.setStrokeColor(HexColor(green));c.setLineWidth(.6);c.rect(28,28,W-56,H-56)
 t(45,H-60,'PROJADES',22,True);t(45,H-103,title,25,True);t(45,H-129,sub,10,col=muted)
 c.line(28,85,W-28,85);t(45,62,'2360 HASSELL ROAD / HOFFMAN ESTATES, IL',12,True)
 t(45,43,'OFFICE-TO-RESIDENTIAL CONVERSION / PRELIMINARY REVIEW / NOT FOR CONSTRUCTION',8,col=red)
 t(W-255,62,'A3 / 29 SEP 2026 / R03',10);t(W-255,43,f'CR-{page:03}',10,True)
def block(y,head,body):
 t(48,y,head,15,True,teal);return wrap(48,y-26,body,W-100,13,20)-25

new('Comprehensive architectural and code review','Five options / supplied PDF + converted DXF / official municipal, state and ICC sources')
y=H-180
y=block(y,'Review conclusion','The package is suitable for concept discussion, but permit-ready compliance is not established. The principal unresolved matters are code classification, fire protection, rated separation, stair sections, rescue openings, structural conversion and accessibility. No whole-option compliance certification is made.')
y=block(y,'Confirmed project scope','The architect confirms conversion of an existing office building into two-story townhouse-style homes and confirms municipal conversion/zoning approval. The approval document and conditions have not been reviewed. The architect states all interior walls have been demolished and only exterior walls remain; two-story homes are designed within this shell. Existing sprinkler status, total unit count and floor/roof structure remain unverified.')
y=block(y,'What changed in R03','Options 4 and 5 now reserve separate 6 in kitchen service zones outside the shared-wall cavity. Option 4 has 8 ft 6 in clear enclosure width plus that allowance. New sliders carry safety-glazing requirements. Project scope, code basis and address spelling have been corrected. Original Options 1-3 remain unchanged.')
y=block(y,'How findings are classified','HOLD = missing evidence or unresolved design that prevents a compliance conclusion. PARTIAL = a concept/documentation correction made, with engineering or detailing still required. REVIEW = functional or documentation issue, not an established statutory violation. Unsupported dimensional violations are not invented.')
block(y,'Evidence limits','LibreDWG conversion has dynamic-block warnings. Selected dimensions and wall envelopes were checked, not every entity or field condition. Plans do not include a survey, sections, complete elevations or MEP design. The review sheets are fit-to-page / NTS and cannot be scaled for construction.')

new('Regulatory basis and decision path','Latest adopted editions located in official online sources / local rules take precedence over model assumptions')
y=H-180
y=block(y,'Adopted framework [S01, S03]','Village: 2021 IBC, IRC, IEBC, IFC, IMC and IFGC; 2020 NEC; Illinois plumbing and accessibility regulations. Illinois energy rules now use the 2024 code with state amendments, effective November 30, 2025. Do not automatically substitute the latest published IBC edition for the locally adopted one.')
y=block(y,'Existing-building pathway [S04, S13]','This is a change-of-occupancy project. Confirm an IEBC compliance method first; Chapter 10 references in this review describe the work-area pathway and are not a mandate to combine all methods. Existing conditions are not automatically exempt, and not every retained component must automatically be rebuilt as new.')
y=block(y,'Townhouse versus R-2 [S06, S07]','IRC townhouse-unit eligibility includes foundation-to-roof continuity and yard/public-way exposure on at least two sides. Four corner units are not automatically disqualified. Check the entire attached arrangement, including the outlined neighboring blocks. If the project is an IBC building with more than two permanent dwelling units, evaluate R-2. Obtain the Village determination.')
y=block(y,'Local sprinkler difference [S02, S04]','The local IFC 903.2 replacement addresses new buildings, structures and occupancies above 1,000 sq ft with NFPA 13; 903.2.2 also addresses renovation encompassing all habitable interior space, defined there by removal of all interior-wall drywall, and a separate value-based trigger. Reported demolition makes this directly relevant; confirm its extent across the regulated structure. Local R313 also replaces the model text. IEBC 1011.2.1 contains IRC-related exceptions. Their application to this conversion requires a documented Village/Fire Prevention decision; no exemption or system type is assumed here.')
block(y,'Approval and address [S08, S12]','Municipal approval is recorded as architect-provided information. Obtain its approved site plan and conditions, rather than imposing generic zoning limits without knowing the approval. The municipal directory spells the street Hassell Road; R03 uses that spelling. Original source filenames retain their supplied spelling.')

for start in range(0,len(issues),5):
 new('Issue register / '+str(start+1)+'-'+str(min(start+5,len(issues))), 'Evidence, affected options, correction status and close-out action / full editable register supplied as CSV')
 y=H-171
 for ident,opts,status,topic,obs,action,src in issues[start:start+5]:
  t(48,y,f'{ident} / {status}',11,True,red if status=='HOLD' else teal)
  t(200,y,f'{topic} / Options {opts}',14,True)
  y=wrap(200,y-23,obs,W-252,11.5,16)
  y=wrap(200,y,'Action: '+action,W-252,11.5,16)-3
  t(200,y,'Reference: '+src,8.5,col=muted);y-=27
  assert y>90,(ident,y)

new('Dimension criteria and design consequences','Conditional IRC checks / verify the accepted pathway, local amendments and applicable existing-building relief')
y=H-180
y=block(y,'Stair and landing checks [S05]','For an IRC stair, screen for 36 in width above handrails and landings at top/bottom, sized to the flight; straight-run landing depth is at least 36 in. These are not measured pass results. Missing floor heights and sections prevent a reliable stair solution. Do not rehinge a bathroom door without checking the new swing against its fixtures.')
y=block(y,'Bedroom rescue openings [S05]','If IRC R310 applies: net clear area 5.7 sq ft, or 5.0 sq ft for qualifying grade-floor openings; clear width at least 20 in, height at least 24 in, and bottom of clear opening no more than 44 in above floor. All applicable tests must pass together. A 20 by 24 in opening is only 3.33 sq ft and does not satisfy the area test.')
y=block(y,'Shared-wall service correction [S05]','R03 reserves 6 in on the kitchen side of the shared wall in Options 4 and 5. This is a design allowance, not a prescribed minimum or a rated assembly. The IRC common-wall approach restricts services in its cavity. Resolve pipe diameters, fittings and access in the separate zone; retain the rated separation and coordinate other bathroom/laundry services too.')
y=block(y,'Actual dimensional evidence','Converted CAD uses inches. Main first-floor wall envelope is approximately 599.04 by 612.08-612.13 in, excluding balconies/adjoining blocks. Selected source dimensions include 156 in bedroom width, 120 in depth and 36 in aisle. These do not establish net room area, opening clearances, accessibility, or surveyed as-built sizes.')
block(y,'Operational design tests','Use selected appliance sizes and open-door envelopes, occupied dining chairs, bed-side movement and maintenance access. Keep these ergonomic targets distinct from adopted-code minima. No unsupported claim that every 36 in kitchen aisle violates code is made.')

option_notes={
1:[('Strength','Direct entry to a combined living/dining space; source upper plan provides a basis for comparison.'),('Primary conflict','C06/C08: bathroom-door and stair relationship needs enlarged plan and section.'),('Daily use','C18/C19: islands, occupied chairs and appliances must be tested together.'),('Disposition','Original preserved. Do not advance as permit-ready until shared hold points are closed.')],
2:[('Strength','Perimeter kitchen offers a distinct alternative to the shared-wall approach.'),('Primary conflict','C07: upper-floor fixture/stair line overlap is a drawing defect requiring clarification.'),('Daily use','Dining layouts and available depth vary by unit. Check ventilation and furniture independently.'),('Disposition','Original preserved. Verify floor opening/headroom before developing the bathroom arrangement.')],
3:[('Strength','Balcony amenity and shared-wall kitchen arrangement provide a clear alternative.'),('Primary conflict','C11: balcony access is not clearly documented; guards and support are unresolved.'),('Daily use','C06/C18: stair/bath interface and island circulation remain open.'),('Disposition','Original preserved. Added balconies must match the municipal approval conditions.')],
4:[('Strength','Separable cooking space with visual connection to living/dining.'),('R03 correction','C05/C12: 6 in service zone; clear enclosure width 8 ft 6 in; safety-glazing requirement.'),('Trade-off','Glazed enclosure adds joinery and exhaust coordination; verify open appliance and slider clearances.'),('Disposition','Upper floor/core remain based on Option 1. Kitchen correction does not close stair, fire or access holds.')],
5:[('Strength','Island removal opens the living area and provides an L-shaped working surface.'),('R03 correction','C05/C11: counter moves off shared wall for 6 in service zone; balcony sliders require safety glass.'),('Trade-off','Service zone reduces free room width; recheck dining-chair and appliance operation. Balcony detailing is additional scope.'),('Disposition','Candidate for open-plan development, not an approved preference. Core and common hold points remain.')]
}
for op in range(1,6):
 new(f'Option {op} / architectural review map','Circles identify review zones, not measured violations / original plan content is retained for Options 1-3')
 for floor,x in [(1,48),(2,425)]:
  file=R/f'tmp/pdfs/option{op}_floor{floor}.png'
  from PIL import Image
  im=Image.open(file);iw,ih=im.size;sc=min(350/iw,420/ih);dw=iw*sc;dh=ih*sc;xx=x+(350-dw)/2;yy=225+(420-dh)/2
  c.drawImage(str(file),xx,yy,dw,dh,mask='auto');t(x,668,f'FLOOR {floor}',11,True)
  # Broad zones: core in first floor, upper central circulation on second.
  marks=[(.5,.5,'A'),(.5,.83,'B')] if floor==1 else [(.5,.5,'A'),(.19,.9,'C')]
  for nx,ny,l in marks:
   px=xx+nx*dw;py=yy+ny*dh;c.setStrokeColor(HexColor(red));c.setLineWidth(1.6);c.circle(px,py,17,stroke=1,fill=0);t(px-4,py-4,l,11,True,red)
 t(48,199,'A / Stair + unit-separation core: C04, C06-C08',10,True,red)
 t(48,180,'B / Kitchen + service coordination: C05, C12, C18',10,True,red)
 t(48,161,'C / Bedroom openings + facade: C09, C11',10,True,red)
 y=H-180
 for head,body in option_notes[op]:
  t(810,y,head,13,True,teal);y=wrap(810,y-23,body,325,11.5,17)-23
 wrap(810,y,'All options: approval, classification, sprinkler, structure, accessibility and energy items remain open. See the issue register.',325,11,16,red)

new('Close-out package and decision sequence','Needed to turn the review into a coordinated design / responsibilities are proposed for project coordination')
y=H-180
for h,b in [
('01 / Architect and owner','Provide the approval letter, approved site plan, existing occupancy record, total dwelling count and permitted bedroom mix. Document completed interior demolition, remaining supports and existing/new floor construction. Attach existing drawings and measured levels.'),
('02 / Survey and structural coordination','Obtain a measured survey, wall/column/beam locations, floor/roof construction, foundations and balcony constraints. Assess conversion loads and new openings before changing stairs or structural walls.'),
('03 / Village and fire-protection coordination','Document the IRC/IBC pathway, IEBC method and local sprinkler interpretation. Investigate existing sprinkler services and required water capacity; allocate system space after the design is known.'),
('04 / Architectural design development','Resolve stairs and doors in section, select a rated assembly, complete the opening/rescue schedule and accessibility scoping. Develop each unit type with interior/exterior dimension chains, schedules and sections.'),
('05 / MEP and envelope','Coordinate independent or shared service strategy, shafts, exhaust, heating/cooling, alarms, electric capacity, plumbing and the 2024 energy analysis. Check acoustic privacy and maintainable access.'),
('06 / Release criteria','Close each HOLD with a drawing, calculation, survey or authority decision recorded in the issue register. Recheck Options 4/5 after that evidence arrives. Preserve original Options 1-3; use separately identified revisions for any later changes.')]:y=block(y,h,b)

for start in [0,7]:
 new('Official sources / '+('1 of 2' if start==0 else '2 of 2'),'Accessed for this review on 29 September 2026 / URLs are clickable / source dates do not establish project permit vesting')
 y=H-173
 for ident,title,scope,url in sources[start:start+7]:
  t(48,y,ident+' / '+title,12,True);y=wrap(48,y-20,scope,W-100,10.5,15)
  label=url if len(url)<125 else url[:122]+'...'
  t(48,y,label,8.5,col=teal);c.linkURL(url,(48,y-3,W-48,y+11),relative=0);y-=30
c.save()

# Combine the complete updated A3 plan set with the comprehensive review.
w=PdfWriter()
for p in [O/'PROJADES_All_Options_A3_Review_R03.pdf',O/'PROJADES_Code_Review_R03.pdf']:
 for pg in PdfReader(p).pages:w.add_page(pg)
w.write(O/'PROJADES_Comprehensive_Review_Package_R03.pdf')

originals=list(csv.DictReader((R/'00_Project_Admin/Source_Inventory.csv').open(encoding='utf-8-sig')))
assert all(hashlib.sha256((R/q['current_path']).read_bytes()).hexdigest()==q['sha256'] for q in originals)
qa=R/'tmp/pdfs/code_review';qa.mkdir(exist_ok=True)
d=pdfium.PdfDocument(str(O/'PROJADES_Code_Review_R03.pdf'))
for i,pg in enumerate(d):pg.render(scale=1).to_pil().save(qa/f'page_{i+1:02}.png')
print(json.dumps({'review_pages':len(d),'source_integrity':'all five original hashes match','output':str(O)}))
