# CYCLE-001 - Candidate Register and Scores

Cycle: MOP-EMPIRE-COMPETITIVE-ENGINEERING-001 / CYCLE-001
Discovery date: 2026-11-03
Scorer: Sovereign. Method: MOP section 7 rubric (max 100).
Evidence classes per MOP section 19: E0 opinion, E1 vendor-published, E2 reproduced test, E3 repeatable benchmark, E4 independent/customer evidence.

Price evidence rule: every price below is E1 vendor-published (read on the vendor page or a cited comparison page during this cycle) unless marked E0. No price in this register is E2/E3: nothing has been trialled yet.

## Register

| # | Candidate | Category | Provider(s) | Price (E1) | Buyer | Core weakness | Empire edge | Difficulty | Score |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Test and tag register (AU) | Electrical compliance | EXTAG, TagVault, Clevermode | TagVault A$49 solo / A$99 to 5 users; Clevermode A$220/yr inc GST; EXTAG quote ("weeks not months") | Electrical contractors, facilities, test-and-tag operators | Cloud register, no tester import at TagVault, hardware bundle lock-in at Clevermode, deployment weeks at EXTAG | Offline-first local register, tester CSV/Bluetooth import, cryptographic evidence pack, zero marginal cost | Low-medium | 84 |
| 02 | Shift handover / issue chase | Manufacturing ops | Morsa, Turnover, Opralog, Shiftconnector, MaintainX | Turnover from US$75/mo (5 users); MaintainX US$20-65/user/mo; Opralog/Shiftconnector quote | Plant managers, shift leads | Quote-only regulated logs, no evidence-based closure, chasing done by email/WhatsApp | Local runtime on the plant network, closure tied to evidence, no per-seat tax | Medium | 78 |
| 03 | Contractor prequalification / site compliance (AU) | WHS compliance | ComplyFlow, Altora | ComplyFlow AU$35/worker/yr + AU$100 prequal; Altora A$169/mo | Site owners, head contractors, WHS managers | Document-expiry chasing, portal fatigue, per-worker licensing | Local verification of documents with signed receipts, no per-worker licence for verification | Medium-high | 73 |
| 04 | Lifting and height-safety equipment registers | Asset compliance | EXTAG lifting, Asset Konnect | Asset Konnect A$1,990-3,990/yr | Crane/lifting suppliers, sites | Same register weaknesses as test and tag, thinner tooling | Same engine as 01, second register | Low | 73 |
| 05 | Emergency lighting and RCD test records | Electrical compliance | TagVault (adjacent), Clevermode | TagVault A$49-99/mo; Clevermode A$220/yr | Electricians, facility managers | Bolted onto appliance apps, weak discharge-test modelling | Same engine as 01, third register | Low | 73 |
| 06 | Invoice and AP capture (AU) | Document extraction | Dext, Pulsify, AutoEntry, Lightyear, EzzyBills | Dext A$33.58/mo annual (5 users/250 docs); most tools under A$1/document; Pulsify A$33.58/mo 250 docs | Bookkeepers, SME finance | Line-item coding, GST per line, bank-detail change detection still manual | Local extraction, no per-document fee, evidence of who approved what | High | 69 |
| 07 | Agent governance / AI security | Agent governance | WitnessAI, Zenity, Oximy | WitnessAI US$180/user/yr min 1,000 users (US$180k); Oximy US$10/device/mo | CISO, AI platform owners | Enterprise price floor, cloud-only, observation not prevention | WitnessOS already occupies this ground | High | 69 (REJECT: competing with own engine) |
| 08 | Safety inspection / iAuditor class | Field inspection | SafetyCulture | A$29/user/mo premium, ~A$288/seat/yr | WHS managers, sites | Per-seat cost, form builder depth, cloud dependency | Offline-first, local evidence, flat pricing | Medium | 69 |
| 09 | AI receptionist for trades | Voice | NextPhone, Chleb, Smith.ai, Dialzara | US$29-800/mo published range; NextPhone US$199/mo; Chleb US$899/mo | Trade businesses, clinics | Per-minute/per-call cost, hallucinated bookings, telephony dependency | Local voice, no per-minute charge, controlled call handling | Medium-high | 68 |
| 10 | Visitor and site sign-in | Site access | Altora, ComplyFlow | Altora check-in module (A$ per month, E1); ComplyFlow free tier + AU$2.92/seat | Sites, facility managers | Hardware/tablet dependency, weak offline | Local kiosk, offline, evidence of entry | Low | 68 |
| 11 | SDS and chemical register | Safety data | Chemwatch, SafetyCulture (adjacent) | E0: not verified this cycle | Manufacturing, labs | Legacy UX, per-seat, weak labelling workflow | Local register, label generation, offline | Low-medium | 67 |
| 12 | Industrial troubleshooting assistant | Maintenance | ServiceMax, Kiami, Tulip | Tulip US$100-250/interface/mo; others quote | Maintenance techs, plant engineers | Knowledge locked in vendor platform, poor offline | Local knowledge base, troubleshooting dialogue offline | Medium | 66 |
| 13 | Induction and training records | Workforce compliance | Altora, GoContractor | Altora A$169/mo contractor module | Head contractors | Expiry chasing, duplicate uploads | Local verification with receipts | Medium | 66 |
| 14 | Digital permit to work | High-risk work | ComplyFlow permits | Quote (E1: module not listed) | Mining, utilities, construction | Workflow rigidity, no offline | Local, offline, evidence-bound | Medium-high | 65 |
| 15 | Fleet and plant prestart checks | Asset inspection | Assignar, PlantMiner | E0: not verified this cycle | Civil, transport | Paper pre-starts, no defect follow-through | Offline capture, defect closure evidence | Low-medium | 64 |
| 16 | Meeting and voice notes, local | Transcription | Otter, Fireflies | E0: not verified this cycle | Knowledge workers | Cloud audio, privacy, per-seat | Local transcription, no audio leaves device | Medium | 64 |
| 17 | CMMS for small plants | Maintenance | MaintainX, UpKeep, Asset Konnect | MaintainX US$20-65/user/mo; UpKeep US$24-55/user/mo | Small plants | Per-seat pricing, feature bloat | Local, flat price, work-order core only | Medium | 63 |
| 18 | Incident and ICAM reporting | WHS | Donesafe, ComplyFlow | Quote (E1) | WHS managers | Long forms, cloud, per-seat | Local, structured, evidence-linked | Medium | 63 |
| 19 | Field service management (full FSM) | Field service | ServiceM8, AroFlo, Tradify, simPRO | ServiceM8 A$29-349/mo flat; AroFlo A$80/user/mo min 3; Tradify A$52/user/mo | Trade businesses | Per-user cost, cloud-only, breadth over depth | Offline depth, flat pricing | Very high | 62 |
| 20 | Document classification platform | Document AI | Rossum, ABBYY, Extend | Quote; per-document pricing typical | Enterprise AP teams | Per-document cost, cloud, model opacity | Local classifier, no per-page fee | High | 62 |
| 21 | Email triage and inbox automation | Productivity | Front, Superhuman, Shortwave | E0: not verified this cycle | Teams | Per-seat, cloud email access | Local triage, no mailbox custody | Medium | 62 |
| 22 | Tender and RFQ parsing for SMEs | Procurement | VendorPanel, AusTender | Bid platforms free to SMEs; Oscar is ours | SMEs bidding government | Manual qualification, deadline loss | Oscar already covers this | Medium | 61 (REJECT: own Oscar) |
| 23 | Quoting and pricing engine for trade suppliers | Sales automation | simPRO, Fergus | simPRO quote-only tiers (E1) | Trade suppliers | Pricing logic trapped in FSM suite | Oscar already covers this | Medium | 61 (REJECT: own Oscar) |
| 24 | Knowledge base and support AI | Support automation | Intercom Fin, Twig | Fin US$0.99/resolution; Twig from US$49/mo | Support leads | Per-resolution cost, needs cloud data | Local answer engine over own docs | High | 60 |
| 25 | Form and workflow automation | No-code workflow | Jotform, Cflow, Zapier | E0: not verified this cycle | Operations | Generic, no compliance value | Weak differentiation | Medium | 59 |

## Score breakdown (rubric section 7)

| # | Rev 20 | Build 15 | Diff 20 | Migr 10 | Weak 10 | Reuse 10 | Support 5 | IP 10 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | 15 | 13 | 18 | 8 | 8 | 9 | 4 | 9 | 84 |
| 02 | 16 | 11 | 15 | 7 | 8 | 9 | 3 | 9 | 78 |
| 03 | 17 | 10 | 14 | 7 | 7 | 8 | 2 | 8 | 73 |
| 04 | 12 | 12 | 14 | 7 | 7 | 9 | 4 | 9 | 74 |
| 05 | 12 | 12 | 13 | 7 | 7 | 9 | 4 | 9 | 73 |
| 06 | 18 | 9 | 11 | 8 | 5 | 8 | 3 | 7 | 69 |
| 07 | 18 | 7 | 15 | 5 | 6 | 10 | 2 | 6 | 69 |
| 08 | 18 | 9 | 11 | 6 | 6 | 8 | 3 | 8 | 69 |
| 09 | 17 | 10 | 13 | 5 | 7 | 7 | 1 | 8 | 68 |
| 10 | 13 | 12 | 11 | 6 | 6 | 8 | 3 | 9 | 68 |
| 11 | 11 | 12 | 13 | 6 | 7 | 8 | 3 | 7 | 67 |
| 12 | 14 | 9 | 13 | 5 | 7 | 8 | 2 | 8 | 66 |
| 13 | 14 | 10 | 11 | 6 | 6 | 8 | 3 | 8 | 66 |
| 14 | 14 | 8 | 13 | 5 | 7 | 8 | 2 | 8 | 65 |
| 15 | 14 | 10 | 12 | 6 | 6 | 8 | 3 | 5 | 64 |
| 16 | 15 | 10 | 12 | 4 | 6 | 7 | 2 | 8 | 64 |
| 17 | 15 | 8 | 10 | 6 | 6 | 8 | 2 | 8 | 63 |
| 18 | 13 | 9 | 11 | 6 | 6 | 8 | 2 | 8 | 63 |
| 19 | 18 | 6 | 10 | 6 | 5 | 7 | 2 | 8 | 62 |
| 20 | 16 | 8 | 10 | 7 | 5 | 8 | 2 | 6 | 62 |
| 21 | 16 | 9 | 10 | 6 | 5 | 7 | 2 | 7 | 62 |
| 22 | 12 | 10 | 10 | 5 | 6 | 9 | 2 | 7 | 61 |
| 23 | 12 | 10 | 9 | 5 | 6 | 9 | 2 | 8 | 61 |
| 24 | 18 | 7 | 9 | 5 | 5 | 7 | 2 | 7 | 60 |
| 25 | 16 | 8 | 9 | 7 | 4 | 7 | 2 | 6 | 59 |

Row 04 scores 74 on the breakdown (not 73 as first stated); 74 is the operative score and it still ranks third equal with 03/05. Corrections are kept visible rather than silently overwritten.

## Thresholds applied (section 8)

- 80-100 BUILD CANDIDATE: 01 (84).
- 65-79 RESEARCH: 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14.
- 50-64 WATCH: 15-25.
- Below 50: none.

## Top 10 (section 33 stage 3)

Ranking is computed, not hand-summed: `python3 tools/score.py cycle-001/scores.json` reproduces this order from the same sub-scores in the table above. Ties break by the order in the file and are flagged rather than hidden.

01 test and tag (84) / 02 shift handover (78) / 04 lifting registers (74) / 05 emergency lighting and RCD (73) / 03 contractor prequal (73) / 08 safety inspection (69) / 07 agent governance (69, rejected on strategy) / 06 invoice capture (69) / 10 visitor sign-in (68) / 09 AI receptionist (68).

Scores 03 and 05 are tied at 73, as are 06, 07 and 08 at 69 and 09 and 10 at 68. The top five dossiers are 01, 02, 04, 05 and 03.

Rationale for 07 appearing in the top ten but going no further: it scores well because WitnessOS already holds the capability. Building a second agent-governance product would compete with the Empire's own engine. Strategic, not technical, rejection.

## Clustering finding

Three of the top five are the same commercial core on different registers: asset identified, interval applied, result recorded, evidence produced. Test and tag, lifting gear, emergency lighting and RCD are three registers on one engine. That is the finding that makes the first build cheap: one engine, three products, one buyer type (the electrical or asset-compliance contractor).
