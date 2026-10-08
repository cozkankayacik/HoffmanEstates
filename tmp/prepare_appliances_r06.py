from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tmp/build_island_r05.py').read_text(encoding='utf-8').replace('island_r05','appliances_r06').replace('R05','R06')
at=s.index(' def furnish(self,op):')
s=s[:at]+''' def circle(self,x,y,r):
  a,b=self.pt(x,y);self.c.setStrokeColor(HexColor(GREEN));self.c.setLineWidth(.45);self.c.circle(a,b,r*self.s,stroke=1,fill=0)
 def appliance(self,x,y,depth,width,name):
  self.rect(x,y,depth,width)
  if name=='R':
   # Integrated refrigerator: cabinet body, paired doors and recessed pulls.
   self.rect(x+2,y+2,depth-4,width-9,None)
   self.line((x+3,y+width/2-2),(x+depth-3,y+width/2-2),lw=.45)
   self.line((x+4,y+5),(x+4,y+width/2-5),lw=.7)
   self.line((x+4,y+width/2+1),(x+4,y+width-11),lw=.7)
   self.label(x+depth/2,y+width-2,'REF',4)
  elif name=='SINK':
   # Single bowl, drain and faucet, in a 24 in base module.
   self.rect(x+5,y+3,depth-8,width-10,None)
   self.circle(x+13,y+10,1.2)
   self.circle(x+3,y+10,1)
   self.line((x+3,y+10),(x+8,y+10),lw=.65)
   self.label(x+depth/2,y+width-2,'SINK',3.7)
  elif name=='HOB':
   # Four burners in plan; oven is below the cooktop, with front handle.
   self.rect(x+2,y+2,depth-4,width-8,None)
   for xx in [x+7,x+17]:
    for yy in [y+6,y+13]:self.circle(xx,yy,2.2)
   self.line((x+1,y+5),(x+1,y+15),lw=1)
   self.label(x+depth/2,y+width-2,'OVEN',3.7)
  elif name=='DW':
   self.rect(x+2,y+2,depth-4,width-8,None)
   self.line((x+4,y+4),(x+depth-4,y+width-8),lw=.35)
   self.line((x+4,y+width-8),(x+depth-4,y+4),lw=.35)
   self.label(x+depth/2,y+width-2,'DW',3.7)
  else:self.label(x+depth/2,y+width/2+2,name,4)
''' + s[at:]
s=s.replace("d.rect(right-24,yy,24,length);d.label(right-12,yy+length/2+2,name,4.1);yy+=length", "d.appliance(right-24,yy,24,length,name);yy+=length")
s=s.replace('Compact 30 in refrigerator and 24 in hob are design assumptions; confirm selected products.', 'REF = 30 in integrated refrigerator; SINK = 24 in base; OVEN = 24 in oven below four-burner cooktop. DW = dishwasher. Select actual products before fabrication.')
s=s.replace('The island is for preparation and dining, with no sink or hob.', 'The island remains for preparation/dining. The wall run now shows a refrigerator, sink bowl/faucet, dishwasher and oven with cooktop symbols.')
s=s.replace('ENLARGED GROUND-FLOOR SOCIAL ZONES / CONCEPT DIMENSIONS','ENLARGED KITCHEN AND LIVING ZONES / APPLIANCE SYMBOLS')
s=s.replace("'wall_cabinet_run_in':'144 x 24'", "'wall_cabinet_run_in':'144 x 24','appliance_modules_in':{'refrigerator':30,'sink_base':24,'dishwasher':24,'oven_with_cooktop':24},'appliance_status':'Concept symbols; manufacturer and actual projections unselected'")
(R/'tmp/build_appliances_r06.py').write_text(s,encoding='utf-8')
