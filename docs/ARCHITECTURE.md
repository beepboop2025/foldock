# foldock technical architecture

foldock is a validated structure-based discovery engine exposed as a REST API. The pipeline folds or retrieves a target structure, prepares the pocket, docks the ligand, validates the pose, triages variants, and filters for cancer safety.

## Data-flow overview

```
                +----------------+        +----------------+
                |  Input sources |        |  Curated layer |
                |  RCSB PDB      |        |  Ageing targets|
                |  AlphaFold DB  |        |  Pathways      |
                |  User PDB      |        |  Variant rules |
                +--------+-------+        +--------+-------+
                         |                         |
                         v                         v
+--------+       +-------+-------+       +---------+--------+
| fold   |------>| pocket prep   |------>| dock (Vina)      |
| module |       | (RDKit/Meeko  |       | library or       |
|        |       |  + Open Babel)|       | single ligand    |
+--------+       +-------+-------+       +---------+--------+
                                         |
                         +---------------v---------------+
                         | validate                      |
                         | redock RMSD vs crystal pose   |
                         | threshold: 2.0 Å              |
                         +---------------+---------------+
                                         |
            +-----------------------------+-----------------------------+
            |                                                           |
            v                                                           v
+-------------------+                                       +-------------------+
| variant-triage    |                                       | cancer-safety     |
| pocket / buried   |                                       | GREEN/AMBER/RED   |
| / allosteric      |                                       | mechanism + target|
+-------------------+                                       | direction + off-  |
                                                            | target signal     |
                                                            +-------------------+
```

## Pipeline stages

| Stage | Tool / library | Purpose |
|---|---|---|
| **1. Fold** | AlphaFold / ColabFold / ESMFold, RCSB fetch | Obtain a 3-D target structure for a protein or variant. |
| **2. Pocket prep** | Open Babel, RDKit, Meeko | Convert receptor and ligand to PDBQT, protonate at pH 7.4, assign partial charges. |
| **3. Dock** | AutoDock Vina | Sample ligand poses and score binding affinity (kcal/mol). |
| **4. Validate** | Open Babel + `obrms` | Compute redock RMSD of top pose vs co-crystal ligand; pass if RMSD < 2.0 Å. |
| **5. Variant-triage** | Custom rules + structural features | Classify variants into pocket, buried-stability, or allosteric categories. |
| **6. Cancer-safety** | Curated mechanism + target-direction model | Return GREEN / AMBER / RED oncogenic-risk verdict with rationale. |

## Tech stack

| Layer | Choice |
|---|---|
| Web framework | FastAPI + Uvicorn |
| Validation / schema | Pydantic |
| Structure prediction | AlphaFold / ColabFold / ESMFold |
| Molecular docking | AutoDock Vina |
| Chemistry toolkit | RDKit, Meeko, Open Babel |
| RMSD validation | Open Babel `obrms` |
| Deployment | Cloud SaaS; optional on-prem / VPC for pharma |

## REST API surface

| Method | Path | Purpose | Request body (excerpt) | Response (excerpt) |
|---|---|---|---|---|
| GET | `/health` | Liveness probe | — | `{"status":"ok","engine":"foldock","version":"0.1.0"}` |
| GET | `/targets` | Curated geroscience target layer | — | `{"count":10,"targets":[...]}` |
| POST | `/dock` | Dock a ligand and get affinity + validation | `{"pdb_id":"1FKB","ligand_resname":"RAP","chain":"A"}` | `{"binding_affinity_kcal_mol":-11.09,"redock_rmsd_angstrom":0.53,"validation":{...}}` |
| POST | `/cancer-safety` | Oncogenic-risk guardrail | `{"target_symbol":"TERT","mechanism":"telomerase_activation","direction":"activate"}` | `{"cancer_safety":"RED","risk_score":90,"verdict":"...","caveats":[...]}` |
| POST | `/screen` | Dock a compound library and return ranked results *(planned)* | `{"pdb_id":"1FKB","library":"approved_drugs"}` | ranked list of affinity + validation scores |

## Validation guarantee

Every `/dock` response includes:

- `binding_affinity_kcal_mol` — Vina docking score.
- `redock_rmsd_angstrom` — RMSD between top pose and co-crystal ligand.
- `validation.passed` — `true` when RMSD < 2.0 Å.
- `validation.verdict` — human-readable trust assessment.

This is the trust layer: results are trustworthy only when the pose reproduces the experimental structure.

## Cancer-safety model

The `/cancer-safety` endpoint combines three signals:

1. **Mechanism class** — e.g. `mtor_inhibition`, `telomerase_activation`, `senolytic`.
2. **Target direction** — whether the intervention activates or inhibits the target, relative to the target’s oncogene / tumour-suppressor role.
3. **Optional off-target docking** — high-affinity hits on known cancer drivers raise the risk band.

Output is a single `GREEN` / `AMBER` / `RED` verdict with `risk_score` and explanatory `caveats`.

## Notes

- PDB IDs and ligand residue names are validated with strict regex patterns before any filesystem or network call to block path traversal and injection.
- API work directory defaults to `/tmp/foldock_api` and can be overridden with `FOLDOCK_WORK`.
- Binary paths for `vina`, `obabel`, and `obrms` are configurable via environment variables.
