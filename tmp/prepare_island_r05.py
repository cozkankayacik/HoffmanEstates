from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tmp/build_minimal_r04.py').read_text(encoding='utf-8')
s=s.replace('minimal_r04','island_r05').replace('Minimalist','Island').replace('MINIMALIST','ISLAND AND TWO-SOFA').replace('R04','R05')
start=s.index(' def furnish(self,op):');end=s.index(' def entry(self,pdfu):',start)
s=s[:start]+''' def furnish(self,op):
  self.rect(0,0,24,18);self.label(12,11,'COAT',4)
  # Three-seat sofa: 84 x 36; two-seat sofa: 60 x 36, perpendicular.
  self.rect(0,self.h-36,84,36);self.rect(4,self.h-32,76,24,None)
  for x in [28,56]:self.line((x,self.h-32),(x,self.h-8),lw=.35)
  self.label(42,self.h-16,'3-SEAT / 84 x 36',4)
  self.rect(0,self.h-105,36,60);self.rect(4,self.h-101,24,52,None)
  self.line((4,self.h-75),(28,self.h-75),lw=.35)
  self.label(18,self.h-73,'2-SEAT',4)
  self.rect(54,self.h-78,36,24,'#F4EEE3')
  self.label(112,self.h-14,'LIVING',4.5)
  front=self.w-30
  il,iw,seats=(72,36,3) if op==4 else (60,30,2)
  ix=front-42-iw;iy=(self.h-il)/2
  self.rect(ix,iy,iw,il,'#F4EEE3')
  self.line((ix+12,iy),(ix+12,iy+il),lw=.35)
  self.label(ix+iw/2,iy+il/2,'ISLAND',4.3)
  # Stool symbols are 16 x 16; dashed envelopes reserve 24 in occupied depth.
  for j in range(seats):
   cy=iy+il/2+(j-(seats-1)/2)*24
   self.rect(ix-20,cy-8,16,16,None)
  self.c.saveState();self.c.setDash(2,2)
  self.rect(ix-24,iy,24,il,None);self.c.restoreState()
  self.dim(ix+iw,front,iy+12,'42 CLR')
  self.dim(ix,ix+iw,iy+il+8,str(iw)+' TOP')
  self.dimv(ix+iw+7,iy,iy+il,str(il)+' LONG')
  self.dim(90,ix-24,self.h-43,str(round(ix-24-90))+' ROUTE')
  self.label(174,self.h-10,'TO CORE',4)
  # Checks cover actual fixed furniture and the proposed occupied stool envelope.
  assert ix-24-90>=36,(op,'route narrower than design target')
  assert iy>=36 and self.h-(iy+il)>=36,(op,'island end clearance')
  return {'island_in':str(il)+' x '+str(iw),'island_seats':seats,'work_aisle_in':42,'occupied_stool_depth_in':24,'living_route_in':round(ix-24-90,2),'island_end_clearance_in':round(iy,2)}
''' + s[end:]
s=s.replace("titles={4:'Linear kitchen / integrated dining',5:'Compact L kitchen / integrated dining'}", "titles={4:'Dining island / two-sofa living',5:'Compact island / two-sofa living'}")
s=s.replace('d.entry(41 if op==4 else 35);d.furnish(op)','d.entry(41 if op==4 else 35);clearances=d.furnish(op)')
start=s.index('  right=d.w-6');end=s.index(' if op==5:',start)
s=s[:start]+'''  right=d.w-6
  d.rect(right,0,6,144,'#F4EEE3');d.label(right+3,75,'S',4)
  yy=0
  for name,length in [('R',30),('SINK',24),('DW',24),('PREP',30),('HOB',24),('END',12)]:
   d.rect(right-24,yy,24,length);d.label(right-12,yy+length/2+2,name,4.1);yy+=length
  assert 144<=d.h,(op,k,'cabinet exceeds room depth')
  register.append({'option':op,'unit_position':k,'room_width_in':round(d.w,2),'room_depth_in':round(d.h,2),'wall_cabinet_run_in':'144 x 24','reserved_service_zone_in':6,'three_seat_sofa_in':'84 x 36','two_seat_sofa_in':'60 x 36','coffee_table_in':'36 x 24',**clearances})
''' + s[end:]
start=s.index('notes={4:');end=s.index('\nfor op in [4,5]:',start)
s=s[:start]+'''notes={4:[('Island kitchen','A 72 x 36 in island faces a 12 ft wall run. Three stools use the living-facing side; the island replaces the separate dining table.'),('Two-sofa living','One 84 x 36 in three-seat sofa and one 60 x 36 in two-seat sofa form an L-shaped seating group around a 36 x 24 in coffee table.'),('Check movement','42 in proposed work aisle; at least 36 in at island ends. Dashed outline reserves 24 in occupied stool depth. These are design checks, not code approval.')],5:[('Compact island','A 60 x 30 in island faces a 12 ft wall run. Two stools reduce the dining footprint and leave more space around the island.'),('Two-sofa living','The same three-seat and two-seat sofa sizes are used as Option 4. Furniture is not scaled down to create artificial clearance.'),('Plan language','An open kitchen, island and L-shaped seating group follow the planning approach of source Options 1-3. Original sources remain unchanged.')]}
''' + s[end:]
s=s.replace('space-saving changes','island and seating changes')
s=s.replace("'48 in is a design target, not a compliance finding. Check appliance doors, occupied chairs and the route into the core. S = service zone. Original Options 1-3 remain unchanged.'", "'Clearances are proposed design dimensions. Check selected appliance doors, stool use and the route into the core. S = separate service zone. Original Options 1-3 remain unchanged.'")
s=s.replace("('Cabinet footprint',('24 sq ft: 144 x 24 in single run.' if op==4 else '26 sq ft: (120 + 60 - 24) x 24 in L-shaped run.')+' This excludes the service zone and circulation.')", "('Island and wall run',('72 x 36 in island with three stools.' if op==4 else '60 x 30 in island with two stools.')+' Both use a 144 x 24 in wall run. The island is for preparation and dining, with no sink or hob.')")
s=s.replace("'Sofa 84 x 36 in; table 60 x 30 in; bench 60 x 18 in; two chairs 18 x 18 in; coffee table 48 x 24 in.'", "'Three-seat sofa 84 x 36 in; two-seat sofa 60 x 36 in; coffee table 36 x 24 in. Stool symbols 16 x 16 in with a 24 in occupied envelope.'")
s=s.replace("('Efficiency claim','The design consolidates furniture at the perimeter and reduces fixed obstructions. It does not increase gross floor area or establish a measured percentage of space saved.')", "('Seating trade-off','Island seating replaces the separate dining table: three places in Option 4 and two in Option 5. Add a separate dining table only after replanning the furniture and movement zones.')")
s=s.replace("('One continuous kitchen run replaces the separate glazed room. The dining bench provides seating and under-seat storage with fewer loose pieces.' if op==4 else 'The compact L retains a separate cooking return while reducing its projection. Dining and lounge furniture use the same measured modules as Option 4.')", "('A larger island provides preparation space and three dining seats. The two separate sofas create an L-shaped living arrangement similar to the supplied alternatives.' if op==4 else 'A smaller island leaves larger end clearances while retaining two dining seats. Both sofas use the same dimensions as Option 4.')")
s=s.replace('The 48 in aisle is a proposed clear zone at the kitchen front. Confirm actual appliance projections and door swings before fixing the joinery.', 'The 42 in work aisle is measured between the island top and wall-counter front. Dashed stool envelopes and the route past the living furniture are checked separately.')
start=s.index("with (R/'brain.md').open");end=s.index('for q in csv.DictReader',start)
s=s[:start]+s[end:]
(R/'tmp/build_island_r05.py').write_text(s,encoding='utf-8')
print('Prepared R05 island and two-sofa layout builder.')
