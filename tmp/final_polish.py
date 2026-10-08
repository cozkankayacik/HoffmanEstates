from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'tmp/build_options.py';s=p.read_text(encoding='utf-8').replace("d.label(left+kw/2,depth-8,'SAFETY GLASS / SLIDER',4.5)","d.label(left+34,depth-8,'SG / SLIDER',4.5)");p.write_text(s,encoding='utf-8')
p=R/'tmp/build_a3_package.py';s=p.read_text(encoding='utf-8').replace('Safety glazing is required at the new slider.', 'SG = safety glazing at the new slider.');p.write_text(s,encoding='utf-8')
p=R/'tmp/presentation/build_deck.mjs';s=p.read_text(encoding='utf-8').replace('validation-code-r03-final.json','validation-code-r03-delivery.json');p.write_text(s,encoding='utf-8')
f=R/'05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R03/PROJADES_Five_Options_A3_Review_R03.pptx'
f.rename(R/'tmp/presentation/pre_polish_r03.pptx')
