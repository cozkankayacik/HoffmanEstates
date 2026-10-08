from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'tmp/build_code_review.py';s=p.read_text(encoding='utf-8')
s=s.replace('Existing sprinkler status is unknown. The full project unit count and existing second-floor status are not confirmed.', 'The architect states all interior walls have been demolished and only exterior walls remain; two-story homes are designed within this shell. Existing sprinkler status, total unit count and floor/roof structure remain unverified.')
s=s.replace('Existing system is unknown; no sprinkler design appears in the reviewed architectural material.', 'Existing sprinkler status is unknown. Architect reports complete interior-wall demolition; assess the local full-interior-renovation trigger.')
s=s.replace('Existing structural survey and status of the proposed second floor are unknown.', 'Interior walls are already removed, per architect. Existing/new floor structure and stability of the retained exterior shell are undocumented.')
s=s.replace('further provisions address existing occupancies and renovation triggers.', '903.2.2 also addresses renovation encompassing all habitable interior space, defined there by removal of all interior-wall drywall, and a separate value-based trigger. Reported demolition makes this directly relevant; confirm its extent across the regulated structure.')
s=s.replace('Confirm whether the second floor already exists. Attach existing architectural drawings and measured levels.', 'Document completed interior demolition, remaining supports and existing/new floor construction. Attach existing drawings and measured levels.')
s=s.replace('Verify columns, beams, foundation capacity and any new floor/stair openings.', 'Verify retained-shell stability, columns, beams, foundations and any new floor/stair openings.')
p.write_text(s,encoding='utf-8')
p=R/'tmp/presentation/build_deck.mjs';s=p.read_text(encoding='utf-8')
s=s.replace('Conversion of an existing office building to two-story residential units. The architect confirms municipal conversion/zoning approval; its conditions are not yet in the file. Four units are detailed.', 'Office-to-residential conversion within the retained exterior shell. The architect reports all interior walls demolished and municipal conversion/zoning approval. Four units are detailed; approval conditions are not in the file.')
s=s.replace('Existing sprinkler status is unknown. Resolve local sprinkler requirements and the rated separation system before selecting a wall build-up or service route.', 'Sprinkler status is unknown. Reported full interior demolition makes the local renovation trigger directly relevant. Resolve sprinklers and rated separations with the Village.')
s=s.replace('validation-code-r03.json','validation-code-r03-final.json')
p.write_text(s,encoding='utf-8')
final=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03/PROJADES_Five_Options_A3_Review_R03.pptx'
if final.exists(): final.rename(R/'tmp/presentation/pre_scope_update_r03.pptx')
with (R/'brain.md').open('a',encoding='utf-8') as f:f.write('''

## Confirmed conversion scope and code review / R03

- Existing office building is being converted to two-story townhouse-style homes.
- Architect confirms municipal conversion/zoning approval; approval documents/conditions have not been supplied.
- Architect reports all interior walls demolished, with exterior walls retained. Previous interior partitions are not existing constraints.
- Existing sprinkler status is unknown. Local full-interior-renovation sprinkler provisions require specific review.
- Existing versus new floor/roof structure, floor heights, shell stability and total unit count remain unverified.
- Official municipal directory spells the address 2360 Hassell Road. New R03 documents use this spelling; original filenames are preserved.
- Current deliverables: PROJADES_Design_Review_R03. Comprehensive review includes 20 issue-register entries, source references and five option review maps.
- Options 4/5 reserve separate 6 in kitchen service zones; this is a design allowance, not a code minimum. Option 4 clear enclosure width is revised to 8 ft 6 in. New sliders specify safety glazing.
- No full compliance certification: classification, sprinkler system, separation details, stairs, rescue openings, structure, accessibility and approval conditions remain open.
- Village published basis: 2021 I-codes / 2020 NEC; 2024 Illinois energy code with amendments effective November 30, 2025. See saved source register for details and verification limits.
''')
print('Scope and project memory updated.')
