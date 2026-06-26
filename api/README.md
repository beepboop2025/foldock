# foldock engine API

Engine-as-a-service over the validated fold -> dock -> validate pipeline.
Every `/dock` response includes a **redock-validation score** — the trust layer.

## Run

```bash
# deps (into the same env that has vina; obabel must be on PATH)
micromamba install -n dock -c conda-forge fastapi uvicorn

export VINA=$(micromamba run -n dock which vina)
export OBABEL=$(which obabel)
export OBRMS=$(which obrms)
micromamba run -n dock uvicorn api.main:app --port 8000
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET  | `/health`  | liveness |
| GET  | `/targets` | curated geroscience target layer (the domain moat) |
| POST | `/dock`    | redock a ligand; returns affinity + validation score |
| POST | `/cancer-safety` | longevity-oncology guardrail; GREEN/AMBER/RED oncogenic-risk verdict |
| POST | `/screen`  | virtual-screen the geroprotector library vs a target pocket; ranked hits + per-hit cancer-safety |
| GET  | `/`        | web dashboard (UI over the endpoints above) |

## Example — `/dock`

```bash
curl -s -X POST localhost:8000/dock -H 'content-type: application/json' \
  -d '{"pdb_id":"1FKB","ligand_resname":"RAP","chain":"A"}'
```

```json
{
  "binding_affinity_kcal_mol": -11.09,
  "redock_rmsd_angstrom": 0.53,
  "validation": {"passed": true, "verdict": "reproduces crystal pose — affinity is trustworthy"}
}
```

## Example — `/cancer-safety`

```bash
curl -s -X POST localhost:8000/cancer-safety -H 'content-type: application/json' \
  -d '{"target_symbol":"TERT","mechanism":"telomerase_activation","direction":"activate"}'
```

```json
{
  "cancer_safety": "RED",
  "risk_score": 90,
  "verdict": "BLOCK — mechanism/target pushes a known cancer-promoting direction ...",
  "caveats": ["Docking gives binding affinity, not agonist-vs-antagonist direction ..."]
}
```

Multi-signal risk model (mechanism + target oncogene/TSG direction + optional off-target
docking). It correctly GREENs rapamycin/navitoclax/metformin/imetelstat, REDs the
telomerase-activation trap / p53-inhibition / IGF-1 boosting, and AMBERs NAD+ and NRF2.

## Example — `/screen`

```bash
curl -s -X POST localhost:8000/screen -H 'content-type: application/json' \
  -d '{"pdb_id":"4QNQ","ref_ligand":"1XJ","chain":"A"}'
```

Docks the curated geroprotector library into the target pocket, ranks by affinity, and
attaches a cancer-safety verdict to every hit (discovery + guardrail in one call).
