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

## Example

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
