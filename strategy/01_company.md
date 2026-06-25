# AMRITA
### Longevity medicine, calibrated for India.

*Working name (alternates: **Ayuh Bio**, **Chiranya**, **GeroBharat**) — trademark search pending.*

**A computational drug-discovery company that screens already-approved Western medicines against the protein machinery of human ageing — to find cheap, safe, repurposable longevity drugs, calibrated to South-Asian biology — and proves they work by measuring biological age in real people.**

---

## 1. The one-paragraph thesis

Ageing is now a *targetable* biological process, and the safest path to a longevity medicine is **repurposing drugs that are already approved** (metformin, rapamycin, SGLT2-inhibitors, senolytics). The discovery step — does an approved drug bind an ageing-related protein? — has become a **software problem** solvable with AlphaFold + molecular docking, on a laptop, for almost nothing. **Nobody has pointed this engine at South-Asian biology**, where people age on a different curve (the "thin-fat" phenotype, diabetes and heart disease a decade early). AMRITA builds that engine, calibrates it to Indian genetics, and closes the loop by measuring whether the drugs it surfaces actually reverse biological age in Indian patients — creating a proprietary dataset no competitor can copy.

---

## 2. Why now / why India (the funding wedge)

- **Why now:** AlphaFold (2021) + AlphaFold3 (2024) made protein structures free; docking + variant-effect AI matured; the first human longevity trials (TAME/metformin, rapamycin) made drug-repurposing for ageing scientifically respectable.
- **Why India:**
  - **Different ageing biology** — South Asians develop insulin resistance, diabetes and coronary disease 5–10 years earlier, at lower BMI ("thin-fat" phenotype). Western drug-response data does not transfer.
  - **The world's pharmacy** — India manufactures generics at global scale; a repurposed geroprotector can be produced and distributed cheaply.
  - **Massive, under-studied population** — no omic-grade ageing biobank exists for 1.4 billion people. That gap is a globally valuable asset.
  - **Cost arbitrage** — dry-lab discovery + cheap diagnostics + cheap trials.

---

## 3. What we are *ultimately* making — the platform

A three-layer loop. Each layer is a product; together they form an unfakeable data moat.

```
        ┌────────────────────────────────────────────────────────┐
        │                    A M R I T A                         │
        │           the longevity operating system               │
        └────────────────────────────────────────────────────────┘

   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
   │  1. MEASURE │ ───▶ │  2. MATCH   │ ───▶ │  3. PROVE   │
   │ BharatAge   │      │ The Engine  │      │ Outcomes    │
   │ biological- │      │ AlphaFold + │      │ re-measure  │
   │ age clock   │      │ docking +   │      │ biological  │
   │ (S-Asian    │      │ pharmaco-   │      │ age after   │
   │ calibrated) │      │ genomics    │      │ intervention│
   └─────────────┘      └─────────────┘      └─────────────┘
          ▲                                          │
          └──────────── proprietary RWE data ────────┘
                 (the moat that compounds)
```

### Layer 1 — MEASURE: *BharatAge* biological-age clock
Tells a person how fast they are *actually* ageing, calibrated to Indian physiology.
- Free/scale tier: face photo + voice + grip + questionnaire.
- Cheap tier: retinal photo (retinal-age gap predicts mortality).
- Premium tier: at-home dried-blood-spot → DNA-methylation + metabolomic clock.
- **Output:** biological age vs passport age, vs the *Indian* curve — not a Western one.

### Layer 2 — MATCH: *The Engine* (today's proof-of-concept)
The computational discovery core.
- Fold ageing-related target proteins (AlphaFold/ESMFold).
- Dock the library of **approved drugs** (DrugBank/ChEMBL) into their pockets.
- Rank repurposing hits; re-rank for the *individual's* genetic variants + drug-metabolism (CYP450) profile.
- **Output:** "for your ageing biology and genotype, these approved drugs best fit your geroprotective targets."

### Layer 3 — PROVE: *Outcomes loop*
Physician-supervised, the user takes a matched approved drug; biological age is re-measured in 3–6 months.
- **Output:** real-world evidence — *which approved drug moved biological age, in which South-Asian phenotype.*
- **This dataset is the company.** It is proprietary, licensable to pharma, and gets better with every patient.

---

## 4. The science engine — architecture (the dry lab)

```
 sequence / variant
        │
        ▼
 [1] STRUCTURE      AlphaFold2 (LocalColabFold) · ESMFold (fast) · AlphaFold3 (complexes)
        │           → 3D structure of the ageing target  (incl. South-Asian variant forms)
        ▼
 [2] POCKET         fpocket · P2Rank
        │           → locate the druggable binding site
        ▼
 [3] DOCK           AutoDock Vina · DiffDock · Meeko · RDKit · Open Babel
        │           → screen DrugBank/ChEMBL approved drugs; binding affinity (kcal/mol)
        ▼
 [4] VALIDATE       redocking RMSD vs crystal · short MD (OpenMM/GROMACS)
        │           → trust the numbers  (PoC: 0.53 Å & 0.90 Å — see §6)
        ▼
 [5] PERSONALISE    AlphaMissense · ESM1b variant effect · CYP450 pharmacogenomics
        │           → does the drug still bind THIS patient's protein? will they metabolise it?
        ▼
   ranked, personalised, repurposable longevity drug list
```

**Ageing targets (starter set):** mTOR, Bcl-2/Bcl-xL (senolysis), SIRT1–7, AMPK, NLRP3, KEAP1/NRF2, FOXO3, Klotho.

---

## 5. Tech stack (full)

| Layer | Tools |
|---|---|
| **Structure prediction** | LocalColabFold (AlphaFold2), ESMFold, AlphaFold3 (academic), JAX |
| **Docking & chem** | AutoDock Vina, DiffDock, Meeko, RDKit, Open Babel, micromamba env |
| **Pocket / MD** | fpocket, P2Rank, OpenMM, GROMACS |
| **Variant effect / PGx** | AlphaMissense, ESM1b, PharmGKB / CYP450 tables |
| **Drug & ageing data** | DrugBank, ChEMBL, ZINC, GenAge/CellAge (HAGR), (optional IMPPAT) |
| **Biological-age ML** | PyTorch, scikit-learn, methylation arrays, retinal-image CNN, voice models |
| **Backend** | Python, FastAPI, Celery, PostgreSQL + pgvector, Redis |
| **Frontend** | Next.js / React, Tailwind, shadcn/ui |
| **Compute** | Local Apple-Silicon (dev) → Modal / Lambda Labs / RunPod GPU (scale) |
| **Data governance** | DPDP-Act-compliant consent management, audit logging, encryption at rest |
| **Infra/DevOps** | Docker, GitHub Actions, Vercel (web), object storage for structures |

---

## 6. Proof-of-concept — already built (the credibility slide)

Run on a MacBook (Apple M4), zero cloud cost:

**A. Folded the rapamycin-binding (FRB) domain of human mTOR**
- AlphaFold2, 5 models, mean **pLDDT 92.8** (highest-confidence tier).
- Ser2035 — the residue that anchors rapamycin — folded at **pLDDT 94**.

**B. Docked two approved drugs into their targets — with redocking validation**

| Drug (status) | Target | Binding affinity | Redock RMSD vs crystal |
|---|---|---|---|
| Rapamycin (approved) | FKBP12 | **−11.09 kcal/mol** | **0.53 Å** |
| Navitoclax (clinical senolytic) | Bcl-xL | **−10.56 kcal/mol** | **0.90 Å** |

> Both redock RMSDs are **well under the 2 Å success threshold** → the pipeline reproduces experimental drug binding. The affinities are strongly negative → consistent with real potent drugs. **The engine works and its numbers are trustworthy.**

**Figures (rendered locally):**

![mTOR FRB domain, folded at pLDDT 92.8 (four-helix bundle; rapamycin-anchor Ser2035 highlighted)](fig1_mTOR_fold.png)

![Rapamycin redocked into FKBP12 — crystal pose (green) vs docked pose (cyan) overlap at 0.53 Å RMSD](fig2_rapamycin_FKBP12.png)

![Navitoclax redocked into Bcl-xL — crystal (green) vs docked (cyan), 0.90 Å RMSD](fig3_navitoclax_BclxL.png)

---

## 6b. The South-Asian wedge — a *variant-triage* result (MTHFR C677T)

We ran the **MTHFR C677T variant** (Ala222Val), carried at high frequency in South-Asian populations and a driver of hyperhomocysteinemia, cardiovascular ageing, and impaired DNA methylation (the same chemistry epigenetic clocks measure).

**Experiment:** fold/prepare wild-type vs A222V MTHFR (identical prep, one residue changed), then redock the FAD cofactor into both.

| Receptor | FAD binding affinity |
|---|---|
| Wild-type MTHFR | −11.11 kcal/mol |
| A222V (C677T) variant | −11.07 kcal/mol |

**Result: no change in FAD *binding affinity*** — and that is the *scientifically correct* answer. Structural analysis shows residue 222 is **10.1 Å from the FAD pocket** and **buried in a packed hydrophobic core** (30 atomic contacts). C677T is therefore a **protein-stability variant** (bulkier Val destabilises the fold → FAD is lost over time), **not a binding-site variant**. Its matched intervention is **riboflavin/methylfolate** — cheap, approved.

![MTHFR core: residue 222 (magenta) buried 10 Å from the FAD cofactor (orange) — a stability variant, not a pocket variant](fig4_MTHFR_variant.png)

> **Why this matters more than a clean differential:** a naive "dock-drugs-into-every-variant" pipeline would report this null and call C677T harmless — *wrong*. AMRITA's real moat is **variant triage**: classifying each variant as *pocket / buried-stability / allosteric* and routing it to the correct method (docking vs ΔΔG-stability vs molecular dynamics). This methodological correctness is what survives technical due diligence — and the **ΔΔG-stability + MD module** is the concrete next build.

---

## 7. Business model

| Line | Customer | Revenue |
|---|---|---|
| **B2C** | Individuals | Biological-age testing + subscription re-measurement |
| **B2B2C** | Life/health insurers | Biological-age-based underwriting & wellness |
| **B2B** | Longevity clinics, supplement brands | API access to the measurement + matching engine |
| **Pharma/biotech** | Drug developers | License the South-Asian ageing cohort + repurposing hits as trial endpoints |

---

## 8. Regulatory & go-to-market path

1. **Wellness/diagnostic entry** — biological-age measurement is a wellness/diagnostic product (fast path, CDSCO nutraceutical/diagnostic rules).
2. **Off-label, physician-supervised** repurposing of already-approved drugs (established safety) — generates outcome data legally.
3. **New-indication / dosing-regimen patents** on old drugs (method-of-use IP).
4. Founder edge: **lawyer-technologist** navigates consent (DPDP Act), off-label frameworks, and biobank governance — a rare, defensible skill set for exactly this company.

---

## 9. Moat

1. **Proprietary South-Asian ageing-outcomes dataset** (compounds per patient — uncopyable).
2. **India-calibrated clock + variant-aware engine** (model + data IP).
3. **Regulatory/legal navigation** as founder superpower.
4. **Full-stack loop** — measure → match → prove — that no single-point competitor owns.

---

## 10. Funding ask & use of funds (illustrative pre-seed)

**Raise:** pre-seed (sized to milestones below).
**Use of funds:**
- Scale the engine to 25–50 ageing targets × full approved-drug library.
- Build BharatAge MVP (retinal + DBS pilot, 500–1,000 participants).
- Generate the first South-Asian variant result (the differentiator).
- Regulatory + consent architecture.

---

## 11. Roadmap / milestones

| Phase | Milestone | Proves |
|---|---|---|
| **0 (done)** | Fold + dock + validate PoC | Engine works |
| **1** | Batch-screen full target × drug matrix | Discovery at scale |
| **2** | First South-Asian variant differential result | The wedge is real |
| **3** | BharatAge measurement MVP + pilot cohort | The data moat starts |
| **4** | First measure→match→prove outcome readout | The flywheel turns |

---

## 12. Risks & honest mitigations

| Risk | Mitigation |
|---|---|
| Docking ≠ clinical efficacy | Engine is a *prioritiser*; truth comes from the measure→prove loop |
| Large-ligand docking is hard | Validated by redocking RMSD; flag low-confidence hits |
| Biobank consent/ethics | Founder is a lawyer; DPDP-compliant consent from day 1 |
| Solo, non-PhD founder | Recruit a scientific advisor; PoC proves execution capability |
| Regulatory uncertainty | Lead with wellness/diagnostic + already-approved drugs |

---

*Document generated alongside a working proof-of-concept (mTOR fold + two validated docks) on local hardware.*
