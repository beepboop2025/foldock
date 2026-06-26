# foldock — the engine for reverse-ageing science

## The problem

Every longevity biotech and academic lab doing structure-based work is rebuilding the same fragile stack: one-off docking scripts, hand-curated target lists, no variant modelling, and no systematic cancer guardrail. The result is slow, redundant, un-validated tooling that burns scarce computational-biology headcount on plumbing.

## The solution

**foldock is a validated, structure-based discovery engine delivered as a service.**

We wrap the full fold → pocket → dock → validate → triage → safety workflow in a single API and dashboard so labs stop maintaining bespoke scripts and start producing reproducible, auditable, citable results.

Think of it as *Schrödinger for longevity*: a specialised, validation-first computational platform for ageing biology, built for India cost.

## Engine modules

| Module | What it does |
|---|---|
| **Target** | Fold (AlphaFold/ColabFold) or retrieve any ageing-target structure, including variants. |
| **Screen** | Dock approved-drug or custom compound libraries and return ranked binding affinities. |
| **Validate** | Auto-redock every result and report RMSD vs crystal pose — the trust layer. |
| **Variant-triage** | Classify variants as pocket, buried-stability, or allosteric and route to the right method. |
| **Cancer-safety filter** | GREEN / AMBER / RED oncogenic-risk verdict based on mechanism, target direction, and off-target signals. |
| **Geroscience knowledge layer** | Curated ageing targets, pathways, telomere / senescence maps, and validation benchmarks. |

## Proof points

- **Rapamycin → FKBP12:** −11.09 kcal/mol, redock RMSD **0.53 Å**
- **Navitoclax → Bcl-xL:** −10.56 kcal/mol, redock RMSD **0.90 Å**
- **mTOR FRB fold:** mean pLDDT **92.8**
- **MTHFR C677T variant:** correctly triaged as a stability (not binding) variant

All validation currently runs CPU-only and reproducibly from RCSB structures.

## Who it is for

| Segment | Why they buy |
|---|---|
| **Longevity biotechs** | Replace fragile in-house scripts; ship validated results faster. |
| **Academic geroscience** | Reproducible, citable, validated structure-based findings. |
| **Pharma geroscience units** | Turnkey repurposing + variant + safety screening, with on-prem / VPC option. |
| **Longevity clinics** | Evidence-graded intervention prioritisation. |
| **Indian / Asian research ecosystem** | First-mover platform at local cost with population-specific variant data. |

## Why foldock wins

- **Validation-first:** every dock ships with a redock RMSD score — trust by construction.
- **Geroscience-specialised:** curated targets and pathways, not generic docking.
- **Variant-aware + cancer-guarded:** model patient variants and the longevity–oncology trade-off.
- **Neutral infrastructure:** we sell the picks and shovels, not the drug.

## Get started

**`POST /dock` → get binding affinity + validation score in one call.**

*Let foldock be the validated engine your reverse-ageing research standardises on.*
