# Project Brain — 2360 Hassel Road

Last updated: 2026-10-08

## Current status at a glance

- Latest revision: **R07** (2026-09-29) — entry identification on Options 4 and 5.
- Current combined PDF: `05_Presentations_and_Issued/Presentations/PROJADES_Island_Options_R07/PROJADES_Options_4_and_5_Island_A3_R07.pdf`.
- Scope: conversion of an existing office building to two-story townhouse-style homes (confirmed by the architect, see R03 section).
- Options 1-3 and the source DWG are unchanged originals. Options 4 and 5 are the developed proposals. No option has been selected.
- The R03 code-review holds remain open; nothing here is a compliance certification.
- The workspace is under version control and pushed to GitHub since 2026-10-07 (see Version control).
- Sections below are kept in the order they were written. Where an early section conflicts with a later revision section, the later one governs.

## Purpose

Maintain the project's working context, confirmed decisions, design observations, and unresolved questions as architectural options develop. Separate verified information from assumptions, and update this file when decisions change.

## Confirmed context

- The user is an architect exploring design options for this project.
- Project address: **2360 Hassel Road, Hoffman Estates, Illinois**.
- The user corrected the initial 2305 street number to 2360 on 2026-09-29.
- Workspace: `C:\Projects\HoffmanEstate`.
- Project code used for new filenames: `HE`.
- Initial material: one DWG and four single-page PDFs, including a baseline and three alternatives.
- Existing files have been organized without changing their contents or original filenames; checksums are recorded in `00_Project_Admin/Source_Inventory.csv`.

## Current design understanding

The supplied PDFs depict first- and second-floor townhouse layout studies. Four mirrored units are detailed in one block, while adjoining blocks are shown as outlines. The overall project unit count and the role of those adjoining blocks are not confirmed.

The detailed units appear to contain one first-floor bedroom and two upstairs bedrooms. This is a preliminary visual interpretation, not a verified program or area schedule.

| Study | Initial visual observations | PDF location |
| --- | --- | --- |
| Baseline | Furnished living/kitchen spaces and central stairs | `02_Design_Options/00_Baseline/PDF/2360 HASSEL RD_townhouse_plan_09.28.2026_1-Model.pdf` |
| Alternative 1 | Revised central stair/bath arrangement and living/kitchen layout | `02_Design_Options/01_Alternative_1/PDF/ALTERNATIVE_1.pdf` |
| Alternative 2 | Kitchens along the outer top/bottom edges of the detailed block; revised dining/living spaces and upstairs bathrooms | `02_Design_Options/02_Alternative_2/PDF/ALTERNATIVE_2.pdf` |
| Alternative 3 | Kitchens closer to the shared center wall; revised upstairs bedroom/bath arrangements; four labeled balconies | `02_Design_Options/03_Alternative_3/PDF/ALTERNATIVE_3.pdf` |

“Top” and “bottom” describe the sheet, not geographic orientation. These observations do not establish a preferred option or code compliance. No option has been selected by the user.

## Shared CAD source

`03_Shared_CAD_and_Models/CAD/2360 HASSEL RD_townhouse_plan_09.29.2026.dwg`

LibreDWG 0.14 converted a copy of the DWG to DXF. The converted file contains the three labeled alternatives, uses inches, and includes 229 DIMENSION entities. Overall wall extents and selected dimensions were inspected; external references and all dynamic blocks remain unverified. Keep it shared until its relationship to the options is understood. Dates embedded in source filenames are not independently verified issue dates.

## Workspace organization

| Folder | Purpose |
| --- | --- |
| `00_Project_Admin` | Brief, decisions, meeting notes, and source inventory |
| `01_Site_and_Reference` | Survey/base maps, zoning/code references, and site photos |
| `02_Design_Options` | Baseline, separate alternative folders, and option comparison |
| `03_Shared_CAD_and_Models` | Shared CAD, Xrefs, and models |
| `04_Visualization` | Working visualization files and exports |
| `05_Presentations_and_Issued` | Presentations and dated issued sets |
| `06_Consultant_Coordination` | Consultant inputs and coordination records |
| `99_Archive` | Superseded revisions |

The root `README.txt` explains file organization and naming. This file records project context and design decisions.

Two working folders sit outside the numbered structure:

| Folder | Contents |
| --- | --- |
| `tmp` | Python build scripts that generated R02-R07, their data inputs, per-revision render folders, a copy of the DWG/DXF, and an AutoCAD LT profile copy (`cad_profile`). About 2 GB. |
| `tools` | Project-local LibreDWG 0.14 and Python packages (ezdxf). About 150 MB. |

## Version control

- Repository: https://github.com/cozkankayacik/HoffmanEstates (branch `main`), set up 2026-10-07 at the user's request.
- Standing instruction from the user: commit and push regularly after each piece of work, without being asked.
- Git is not on PATH. Use the copy bundled with Codex: `C:\Users\ozkan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe`. It includes Git LFS, and the credential manager already holds working GitHub credentials.
- DWG, DXF, PDF, PPTX, ZIP, JPG and PNG files are stored with Git LFS (`.gitattributes`), matching the user's other project repositories.
- Not in the repository (`.gitignore`): `tools/`, AutoCAD backup/lock/error files, and everything in `tmp/` except the build scripts (`*.py`, `*.scr`) and `dimensions.json` / `shell_points.json`.
- The two ZIP packages entered the first commit without LFS and were converted in the second, leaving about 38 MB of extra history. Removing it would need a force-push; left as is.

## Build pipeline notes

- Each revision was produced by a script in `tmp` (`build_options.py`, `build_code_review.py`, `build_minimal_r04.py`, `build_island_r05.py`, `build_appliances_r06.py`, `build_entries_r07.py`, plus prepare/finalize/QA helpers). A new revision normally starts from the previous revision's script.
- Each revision renders into its own `tmp` subfolder (for example `tmp/entries_r07`) before the PDFs are copied to the option `PDF` folders and the `Presentations` revision folder.
- AutoCAD LT is installed, but a scripted run on 2026-09-29 failed with "Problem with setting up current profile" (`acadlt.err`). DWG reading has relied on LibreDWG and ezdxf since then; DWG output from AutoCAD LT is unproven in this workspace.
- Superseded R01/R02 concept reviews are in `99_Archive/Superseded_Concept_Reviews`.

## Working conventions

- Preserve original source filenames and issued material.
- Keep new option-specific editable drawings in the relevant option's `CAD` folder and exports in its `PDF` folder.
- Use explicit dates and revisions for new files, for example `HE_Alt-01_First-Floor_2026-09-29_R01.pdf`.
- Store issued copies in dated folders under `05_Presentations_and_Issued/Issued_Sets`.
- Retain superseded revisions in the archive rather than overwriting issued files.
- Record the source and date for future site, zoning, dimension, and area findings.

## Open questions

- ~~Is the scope new construction, conversion, or renovation?~~ Resolved 2026-09-29: office-to-townhouse conversion (see R03 section).
- What are the confirmed parcel boundaries and existing site conditions?
- What is the intended total unit count, and what do the outlined blocks represent?
- What are the target unit areas, bedroom mix, accessibility goals, and budget?
- What are the site orientation, access, parking, and outdoor-space requirements?
- Which zoning and building-code requirements apply?
- Which CAD geometry corresponds to each PDF alternative?
- What criteria should determine the preferred option?

## Suggested next steps

1. Confirm the program and project scope with the architect.
2. Review the DWG and validate dimensions and option correspondence.
3. Gather survey and site information and verify applicable requirements.
4. Compare alternatives using agreed criteria such as circulation, furniture fit, daylight/privacy, wet-area coordination, outdoor space, and constructability.
5. Develop the selected direction after the architect's decision.

These are proposed next steps, not completed work or approved design criteria.

## Decision and activity log

| Date | Record |
| --- | --- |
| 2026-09-29 | Reviewed the four PDFs and organized the five supplied source files; verified their contents remained unchanged. |
| 2026-09-29 | User confirmed 2360 Hassel Road as the correct address; updated the project guide. |
| 2026-09-29 | Created this project memory file at the user's request. |
| 2026-09-29 | Issued review sets R02 through R07; details in the revision sections below. |
| 2026-10-07 | Put the workspace under Git with LFS and pushed it to GitHub at the user's request. |
| 2026-10-08 | Added status summary, version control and build pipeline notes; build scripts in `tmp` added to the repository. |

## Review limits

Completed: preliminary PDF visual review, file organization, source integrity checks, and address confirmation with the user.

Not yet completed: site research, exhaustive CAD/dimension verification, area takeoff, stair sections, zoning/code review, or selection of a preferred design.


## Current design review deliverables (2026-09-29)

- User requires all new drawings, documents, file names and folder names in English.
- Options 1-3 and the original DWG remain unchanged.
- Option 4: separable glazed kitchen based on Option 1; original second-floor layout retained.
- Option 5: open L-shaped kitchen without an island based on Option 3, with proposed balcony sliding doors.
- Five options use matching A3 landscape review sheets with a new PROJADES title block.
- Plans fit within the available A3 sheet area. Sheet scale is FIT TO SHEET / NTS; do not scale the print.
- Current English deliverables are in 05_Presentations_and_Issued/Presentations/PROJADES_Design_Review_R02.
- The presentation contains 19 A3 slides, with editable text and comparison tables.
- Source first-floor wall envelopes: 599.0413 in wide; 612.0813 in deep for Options 1/3 and 612.1280 in for Option 2. These are converted-CAD references, excluding balconies and adjoining blocks.
- New interior dimensions are proposed concept geometry, not field or fabrication dimensions. Complete opening chains and stair/structural coordination remain outstanding.
- Review concerns: 3 ft island aisles under appliance operation; bathroom door swings near stair starts; Option 2 stair/bath graphic overlap; Option 3 balcony door definition. These are review items, not established code violations.
- LibreDWG and ezdxf are installed in the project-local tools directory. Conversion reported dynamic-block warnings.
- New PROJADES brand assets and templates are proposed project assets, created because the user has no existing company templates available.


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


## Minimalist revision R04 / 2026-09-29
- User requested less wasted space and minimalist layouts for Options 4 and 5.
- Option 4: removed kitchen enclosure; 12 ft single cabinet run, integrated dining bench, consolidated lounge furniture.
- Option 5: shortened L kitchen to 10 ft x 5 ft; integrated dining bench and consolidated lounge furniture.
- Both retain 6 in service allowances and show a 48 in kitchen work-aisle design target. Cabinet footprints are 24/26 sq ft, excluding service zones and circulation.
- Upper-floor partitions and stair/bath cores remain reference proposals pending sections, floor heights and code/structural coordination. They are not existing walls.
- Current focused option drawings: PROJADES_Minimalist_Options_R04. R03 presentation is superseded for Options 4/5 layout only; its unresolved code-review items still apply.
- Original Options 1-3 remain unchanged. All new sheets are English, A3 landscape, Arial, PROJADES title block.


## Island and two-sofa revision R05 / 2026-09-29
- User requests island kitchens and sofa plus three-seat seating, using the planning approach of Options 1-3.
- Interpreted seating as one 60 x 36 in two-seat sofa and one 84 x 36 in three-seat sofa; communicated that assumption.
- Option 4: 72 x 36 in preparation/dining island, three stools; Option 5: 60 x 30 in island, two stools.
- Both use 12 ft wall kitchen runs, proposed 42 in work aisles and 6 in service allowances.
- Separate dining tables are replaced by island seating; this capacity trade-off is disclosed on the sheets.
- Drawing geometry checks include all four unit positions per option, occupied stool envelopes and island end clearance. They are not regulatory compliance certification.
- Current files: PROJADES_Island_Options_R05. Upper-floor/core scope and R03 code-review holds remain unchanged. Original Options 1-3 preserved.

## Appliance symbols R06 / 2026-09-29
- Options 4/5 now show refrigerator cabinet/door symbols, sink bowl/drain/faucet, and oven with four-burner cooktop; dishwasher also shown.
- Island and two-sofa arrangements are unchanged from R05. Appliance dimensions remain concept assumptions pending product selection.
- Current combined PDF: PROJADES_Island_Options_R06/PROJADES_Options_4_and_5_Island_A3_R06.pdf. Original Options 1-3 remain unchanged.

## Entry identification R07 / 2026-09-29
- Added ENTRY labels and inward arrows at all four dwelling entrances on A-401 and A-501.
- Added upper-floor access notes on A-402 and A-502 referring to the ground-floor entrance sheets and internal stairs.
- Current combined PDF: PROJADES_Island_Options_R07/PROJADES_Options_4_and_5_Island_A3_R07.pdf. Original Options 1-3 preserved; source hashes verified.

