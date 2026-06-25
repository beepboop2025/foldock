# Appendix — The Build: Prompt Library

A sequenced set of prompts to build AMRITA toward a fundable demo. Each is written to be pasted into an AI coding agent (Claude Code). Run them roughly in order; each phase produces a tangible artifact for the pitch.

---

## Phase 0 — Science engine (✅ mostly done this session)

**P0.1 — Fold an ageing target**
> "Using LocalColabFold at ~/localcolabfold, fold the [DOMAIN] of [PROTEIN] (UniProt [ID]). Extract the domain sequence from UniProt, run 5 models, and report mean pLDDT and the confidence at the key catalytic/binding residue."

**P0.2 — Validate a docking pipeline by redocking**
> "In the `dock` micromamba env, redock the native ligand [CODE] from PDB [ID] into its receptor: extract receptor + native ligand, prep with Open Babel/Meeko, build the search box from the native ligand centroid, run AutoDock Vina (exhaustiveness 16), then report binding affinity and the redock RMSD vs the crystal pose using obrms."

**P0.3 — Screen approved drugs against one target**
> "Download the approved-drug subset of DrugBank (SMILES). For target [PROTEIN] structure, prep each ligand with Meeko, dock all with Vina against the validated pocket, and output a ranked table of binding affinities. Flag the top 20 and any known geroprotectors."

---

## Phase 1 — Engine at scale (the discovery product)

**P1.1 — Target database**
> "Build a PostgreSQL schema for ageing targets: protein, UniProt ID, structure path, pocket coordinates, pathway, GenAge/CellAge annotation. Seed it with mTOR, Bcl-2, Bcl-xL, SIRT1-7, AMPK, NLRP3, KEAP1, FOXO3, Klotho."

**P1.2 — Automated fold→pocket→dock pipeline**
> "Write a Python pipeline (Celery + FastAPI) that, given a target and a drug library, runs: ESMFold (or cached AlphaFold) → fpocket pocket detection → Vina batch docking → results to Postgres. Make it resumable and parallel."

**P1.3 — Hit ranking + report**
> "Build a ranking module that scores (target × drug) pairs by affinity, druggability, known geroprotector status, and clinical-approval level. Generate an HTML report per target with top hits and binding-pose thumbnails."

**P1.4 — Validation harness**
> "For every new target, automatically redock a known co-crystallised ligand and store the RMSD as a per-target confidence score. Block hits from targets that fail validation (RMSD > 2.5 Å)."

---

## Phase 2 — The South-Asian differentiator (the wedge)

**P2.1 — Variant-aware folding**
> "Given a list of coding variants common in South-Asian populations (from GenomeAsia/IndiGen) in an ageing target, generate the mutant sequence and fold it with ESMFold. Compare the binding pocket to the wild type (RMSD + pocket-volume change)."

**P2.2 — Differential drug binding**
> "Re-dock the top drug hits against both wild-type and South-Asian-variant structures of the target. Output drugs whose predicted binding changes most by genotype — these are the personalised/precision candidates."

**P2.3 — Pharmacogenomic layer**
> "Integrate CYP450 metaboliser status (from PharmGKB) for South-Asian allele frequencies. For each candidate drug, annotate predicted metabolism (poor/normal/rapid) to flag dosing concerns."

---

## Phase 3 — BharatAge measurement MVP (the moat starts)

**P3.1 — Retinal-age model**
> "Build a CNN (PyTorch) that predicts age from retinal fundus images using an open dataset; expose the 'retinal age gap' (predicted minus chronological) as a biological-age proxy. Wrap it in a FastAPI endpoint."

**P3.2 — Multimodal clock**
> "Combine face-age, voice-age, grip, and questionnaire features into a single biological-age estimate with a calibration layer that can be re-fit on Indian data. Output uncertainty bounds."

**P3.3 — Consumer app**
> "Build a Next.js app: user uploads a selfie + retinal photo + answers a short form, gets a biological-age dashboard vs the Indian curve, and a personalised report. DPDP-compliant consent flow and encrypted storage."

**P3.4 — Outcomes loop**
> "Add longitudinal tracking: store baseline biological age, the matched intervention, and re-measurement at 3/6 months; compute the delta and aggregate anonymised cohort-level results."

---

## Phase 4 — Fundraising materials

**P4.1 — Pitch deck**
> "From AMRITA_company.md, generate a 12-slide pre-seed deck: problem, why-now, why-India, the engine (with the PoC validation numbers), the measure→match→prove loop, moat, business model, regulatory path, team, ask, use of funds, milestones."

**P4.2 — Demo money-slides**
> "Render publication-quality figures: (1) the folded mTOR FRB domain coloured by pLDDT, (2) rapamycin redocked into FKBP12 with the 0.53 Å overlay, (3) navitoclax in Bcl-xL at 0.90 Å. Use PyMOL (pymol-open-source)."

**P4.3 — One-pager + data room**
> "Produce a one-page executive summary and a data-room checklist (cap table, IP/patent strategy memo, regulatory memo, consent framework, technical validation report)."

**P4.4 — Investor list + outreach**
> "Draft a target list of India deep-tech + global longevity VCs, and a warm-intro outreach email tailored to a lawyer-technologist solo founder with a working dry-lab engine."

---

## Suggested order
P0 (done) → P1.1–1.4 → P2.1–2.2 → P4.1–4.2 (deck with the wedge) → raise → P2.3, P3.* with funding.

> **Principle:** build only as far as the *next* fundraising conversation requires. The engine + one South-Asian variant result + a clean deck is enough to raise pre-seed. Don't build the full app before the cheque.
