from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'tmp/build_options.py'
s=p.read_text(encoding='utf-8')
s=s.replace("sources={i:next((ROOT/f'02_Design_Options/0{i}_Alternative_{i}/PDF').glob('*.pdf')) for i in range(1,4)}", "sources={i:ROOT/f'02_Design_Options/0{i}_Alternative_{i}/PDF/ALTERNATIVE_{i}.pdf' for i in range(1,4)}")
s=s.replace("kw=108*s;depth=(108 if h>140 else 90)*s;left=w-kw", "chase=6*s;kw=102*s;depth=(108 if h>140 else 90)*s;right=w-chase;left=right-kw\n            d.rect(right,0,chase,depth,fill='#F4EEE3');d.label(right+chase/2,depth/2,'S',4)")
s=s.replace('d.kitchen(w-22,20,depth-20)', 'd.kitchen(right-22,20,depth-20)')
s=s.replace('(left+62,depth),(w,depth)', '(left+62,depth),(right,depth)')
s=s.replace("'GLASS / SLIDER'", "'SAFETY GLASS / SLIDER'")
s=s.replace('d.dim(left,w,depth+11,"9\'-0\\\"")', 'd.dim(left,right,depth+11,"8\'-6\\\" CLEAR")')
s=s.replace("s=222.72/284.74823196608486;cd=24*s", "s=222.72/284.74823196608486;cd=24*s\n            chase=6*s;right=w-chase\n            d.rect(right,3,chase,h-3,fill='#F4EEE3');d.label(right+chase/2,h/2,'S',4)")
start=s.index('            d.rect(w-cd,3,cd,h-3')
end=s.index('            d.table(w-109,34)',start)
chunk=s[start:end].replace('w-cd','right-cd').replace('w-72*s','right-72*s').replace('w-49*s','right-49*s').replace('(w,yy)','(right,yy)').replace('s,w,','s,right,')
s=s[:start]+chunk+s[end:]
p.write_text(s,encoding='utf-8')
p=r/'tmp/build_a3_package.py';s=p.read_text(encoding='utf-8').replace('R02','R03')
s=s.replace('2360 HASSEL ROAD','2360 HASSELL ROAD').replace('2360 Hassel Road','2360 Hassell Road')
s=s.replace('Proposed kitchen width: 9 ft.', 'Kitchen clear width: 8 ft 6 in plus a 6 in reserved service zone.')
s=s.replace('Proposed counter depth: 24 in. Short return: 6 ft. The dining table remains near the facade.', 'Counter depth: 24 in. Short return: 6 ft. New 6 in service zone keeps kitchen piping outside the shared-wall cavity.')
s=s.replace('The second floor matches source Option 1. The stair and bathroom core has not been redesigned.', 'Safety glazing is required at the new slider. The source stair/bath core remains unresolved; see the code review.')
s=s.replace('Four sliding balcony doors are proposed upstairs. Bedroom and bathroom partitions are retained.', 'Balcony sliders require safety glazing. Thresholds, guards and structure remain unresolved; see the code review.')
s=s.replace('Kitchen width: 108 in.', 'Kitchen clear width: 102 in plus a 6 in reserved service zone.')
s=s.replace('New kitchen dimensions are design proposals requiring detailed CAD development.', 'New dimensions are proposals. S = 6 in service zone; not a code minimum. See the R03 code review.')
s=s.replace('CONCEPT REVIEW / NOT FOR CONSTRUCTION','OFFICE-TO-RESIDENTIAL / CONCEPT ONLY')
p.write_text(s,encoding='utf-8')
p=r/'tmp/presentation/build_deck.mjs';s=p.read_text(encoding='utf-8').replace('R02','R03').replace('validation-english.json','validation-code-r03.json')
s=s.replace('HASSEL ROAD','HASSELL ROAD').replace('Hassel Road','Hassell Road')
s=s.replace('A two-story residential block with four detailed units.', 'Conversion of an existing office building to two-story residential units. The architect confirms municipal conversion/zoning approval; its conditions are not yet in the file. Four units are detailed.')
s=s.replace('regulatory review require further work','resolution of the code-review hold points require further work')
s=s.replace("['9 ft kitchen width','The glazed enclosure allows cooking to be separated from dining and living.']", "['8 ft 6 in clear kitchen width','A 6 in service zone is reserved outside the shared-wall cavity. New sliding glazing must be safety glazing.']")
s=s.replace("['L counter instead of an island','A 24 in counter depth and 6 ft short return establish the proposed working surface.']", "['Counter and service zone','The 24 in counter and 6 ft return move 6 in away from the shared wall to reserve a separate piping zone.']")
s=s.replace("No code compliance findings are asserted. These are project coordination items arising from plan review.", "Read with PROJADES_Code_Review_R03.pdf. Preliminary compliance review; unresolved hold points prevent permit-ready status.")
insert="""
s=slide('Conversion / applicable code basis','Official sources and section references: PROJADES_Code_Review_R03.pdf, source register. Reviewed 29 September 2026.');
items(s,[['Existing office to residential','Use the adopted 2021 IEBC with the applicable IBC or accepted IRC pathway. Townhouse classification is pending confirmation of the complete building arrangement.'],['Local and state requirements','Hoffman Estates lists 2021 I-codes and 2020 NEC. The 2024 Illinois energy code took effect on 30 November 2025. Illinois plumbing and accessibility rules also apply.'],['Approval is recorded','The architect reports municipal conversion/zoning approval. Obtain the approved site plan and conditions before testing the unit mix, parking and site changes.']]);
s=slide('Code review / unresolved hold points','Local sprinkler amendments: Ordinance 5028-2023, pages 10 and 19. IEBC 1011.2.1 exceptions must be reconciled with the local amendments by the authority having jurisdiction.');
items(s,[['Fire protection and separation','Existing sprinkler status is unknown. Resolve local sprinkler requirements and the rated separation system before selecting a wall build-up or service route.'],['Stairs and rescue openings','Floor heights, sections and clear-opening schedules are missing. Close the bathroom/stair conflicts and verify each sleeping room independently.'],['Structure and accessibility','Confirm whether the second floor is existing or added. Establish the accessible route and applicable dwelling-unit requirements from the approved scope.']]);
s=slide('R03 / changes and remaining work','Original Options 1-3 are unchanged. Corrections are limited to supported concept changes; this is not a compliance certification.');
items(s,[['Changes to Options 4 and 5','Reserved separate 6 in kitchen service zones; revised the Option 4 clear width; specified safety glazing for new sliders. Zone width is a design allowance, not a code minimum.'],['Documentation corrections','Project scope now states office-to-residential conversion. Address spelling follows the municipal directory: Hassell Road. Source filenames remain unchanged.'],['Not closed by these changes','Stairs, rated assemblies, sprinkler design, rescue openings, structure, accessibility and approval conditions remain open. See the issue register and code-review drawings.']]);
"""
s=s.replace('await fs.mkdir(out,{recursive:true});',insert+'\nawait fs.mkdir(out,{recursive:true});')
p.write_text(s,encoding='utf-8')
print('Revised builders to R03; source paths made explicit.')
