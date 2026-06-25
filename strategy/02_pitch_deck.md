# AMRITA — Pre-Seed Pitch Deck

## Slide 1 — Title

- **AMRITA**
- *Longevity medicine, calibrated for India.*
- Computational drug-repurposing for human ageing, built on South-Asian biology.
- Working names under review: Ayuh Bio, Chiranya, GeroBharat.

## Slide 2 — Problem

- Ageing is now a targetable biological process — but every major longevity drug was validated on Western populations.
- South Asians age on a different curve: the "thin-fat" phenotype drives insulin resistance, diabetes and heart disease 5–10 years earlier.
- Western drug-response data does not transfer; dosing, efficacy and side-effect profiles miss Indian biology.
- Result: a 1.4-billion-person market has no longevity-drug discovery engine built for it.

## Slide 3 — Why Now

- AlphaFold (2021) and AlphaFold3 (2024) made high-quality protein structures free.
- Docking, AI variant-effect prediction and MD validation are now laptop-scale and almost free.
- TAME (metformin), rapamycin and senolytic trials made drug-repurposing for ageing scientifically respectable.
- The shift from blockbuster R&D to repurposing + real-world evidence fits India’s cost and data advantages.

## Slide 4 — Why India

- **Different ageing biology** — earlier cardiometabolic disease at lower BMI.
- **World’s pharmacy** — largest generic-drug manufacturing base; any repurposed geroprotector can be produced and distributed cheaply.
- **Massive, under-studied population** — no omic-grade ageing biobank exists for 1.4 billion people.
- **Cost arbitrage** — dry-lab discovery + cheap diagnostics + low-cost trials.

## Slide 5 — The Product: Measure → Match → Prove

- **BharatAge** — biological-age clock calibrated to Indian physiology, from free face/voice tiers to dried-blood-spot methylation + metabolomics.
- **The Engine** — AlphaFold + docking screens the approved-drug library (DrugBank/ChEMBL) against ageing targets, re-ranked by personal genotype.
- **Outcomes loop** — physician-supervised matched drugs, biological age re-measured in 3–6 months.
- Output: a proprietary, compounding dataset of *which approved drug moved biological age in which South-Asian phenotype*.

## Slide 6 — The Engine + Proof-of-Concept

- Built a fully local dry-lab pipeline: structure prediction → pocket detection → docking → redock validation → variant personalization.
- **mTOR FRB domain folded at mean pLDDT 92.8**; rapamycin-anchoring Ser2035 at pLDDT 94.
- Rapamycin → FKBP12: **−11.09 kcal/mol**, redock RMSD **0.53 Å**.
- Navitoclax → Bcl-xL: **−10.56 kcal/mol**, redock RMSD **0.90 Å**.
- Both RMSDs are well under the 2 Å success threshold — the engine reproduces known binding and its numbers are trustworthy.

## Slide 7 — The South-Asian Wedge: variant triage

- **Demonstrated on MTHFR C677T (Ala222Val)** — high-frequency South-Asian variant driving homocysteine, cardiovascular ageing, and impaired DNA methylation (the chemistry epigenetic clocks measure).
- Our engine folded WT vs variant and redocked the FAD cofactor: **no change in binding affinity (−11.1 vs −11.1)** — and that is the *correct* answer. Residue 222 is 10 Å from the pocket, buried in the core: **C677T is a stability variant, not a binding variant.** Fix = riboflavin (cheap, approved).
- **The moat is variant triage** — classifying each variant (pocket / stability / allosteric) and routing it to the right method (docking vs ΔΔG-stability vs MD). Naive pipelines report a false "harmless" and fail technical diligence.
- First mover on a variant-aware, India-calibrated geroprotector engine — built to *not overclaim*, which is what survives investor due diligence.

## Slide 8 — Business Model

- **B2C:** Biological-age testing + subscription re-measurement.
- **B2B2C:** Life/health insurers — age-adjusted underwriting and wellness incentives.
- **B2B:** Longevity clinics, supplement brands — API access to measurement + matching engine.
- **Pharma/biotech:** License repurposing hits + South-Asian ageing cohort and real-world endpoints.

## Slide 9 — Moat

- **Proprietary South-Asian ageing-outcomes dataset** — compounds × patient × biological-age change; uncopyable once scaled.
- **India-calibrated clock + variant-aware engine** — model + data IP.
- **Regulatory and consent architecture as founder superpower** — DPDP-compliant biobank governance from day one.
- **Full-stack loop** — measure → match → prove — no single-point competitor owns the entire flywheel.

## Slide 10 — Regulatory Path

- Enter through **wellness/diagnostic biological-age testing** — fast path under existing CDSCO diagnostic/nutraceutical rules.
- Enable **off-label, physician-supervised repurposing of already-approved drugs** to generate outcome data legally.
- File **method-of-use / new-indication patents** on old drugs for ageing-related dosing regimens.
- Lawyer-technologist founder de-risks consent, off-label frameworks, biobank governance and DPDP Act compliance.

## Slide 11 — Team

- **Solo founder — lawyer-technologist.**
- Built the working proof-of-concept end-to-end on an Apple Silicon laptop: mTOR fold + two validated docks, zero cloud spend.
- Legal background is a rare, defensible edge for a company that must navigate patient consent, off-label use, biobank governance and drug-regulatory frameworks.
- Now raising pre-seed to add scientific advisors, computational biologists and a clinical operations lead.

## Slide 12 — The Ask

- **Raising a pre-seed round** to reach first South-Asian variant result and BharatAge pilot.
- **Use of funds:**
  - Scale the engine to 25–50 ageing targets × full approved-drug library.
  - Build BharatAge MVP (retinal + dried-blood-spot pilot, 500–1,000 participants).
  - Generate first South-Asian variant differential result.
  - Build regulatory, consent and data-governance architecture.
- **Milestones:**
  - 0–3 months: batch-screened target × drug matrix.
  - 3–6 months: first variant-aware hit prioritisation.
  - 6–12 months: BharatAge pilot launched + first measure→match→prove readout.
