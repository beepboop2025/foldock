"""
foldock engine-as-a-service — a minimal REST API over the validated
fold -> dock -> validate pipeline. This is the enterprise surface: a lab calls
POST /dock and gets back a binding affinity AND an automated redock-validation
score, so every result is trustworthy by construction.

Run:
    VINA=$(micromamba run -n dock which vina) OBABEL=$(which obabel) OBRMS=$(which obrms) \
      uvicorn api.main:app --reload
"""
import json
import os
import subprocess
import urllib.request
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from api.cancer_safety import assess as cancer_safety_assess

VINA = os.environ.get("VINA", "vina")
OBABEL = os.environ.get("OBABEL", "obabel")
OBRMS = os.environ.get("OBRMS", "obrms")
WORK = Path(os.environ.get("FOLDOCK_WORK", "/tmp/foldock_api"))
WORK.mkdir(parents=True, exist_ok=True)
DATA = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="foldock — engine for reverse-ageing science",
    version="0.1.0",
    description="Validated structure-based screening as a service. Every dock ships with a redock-validation score.",
)

# --- curated geroscience target layer (the domain moat, not generic docking) ---
TARGETS = [
    {"symbol": "MTOR",   "name": "mTOR kinase",            "pathway": "nutrient sensing",  "role": "rapamycin target / longevity",          "pdb": "1FAP", "example_drug": "rapamycin"},
    {"symbol": "BCL2L1", "name": "Bcl-xL",                 "pathway": "apoptosis",          "role": "senolytic target",                      "pdb": "4QNQ", "example_drug": "navitoclax"},
    {"symbol": "SIRT1",  "name": "Sirtuin 1",              "pathway": "NAD+ / sirtuins",    "role": "geroprotector",                         "pdb": "4IG9", "example_drug": "resveratrol"},
    {"symbol": "PRKAA1", "name": "AMPK (alpha)",           "pathway": "energy sensing",     "role": "geroprotector",                         "pdb": "4CFE", "example_drug": "metformin (indirect)"},
    {"symbol": "KEAP1",  "name": "KEAP1",                  "pathway": "NRF2 / oxidative",   "role": "stress resistance",                     "pdb": "4L7B", "example_drug": "bardoxolone"},
    {"symbol": "TERT",   "name": "Telomerase rev. transcriptase", "pathway": "telomere maintenance", "role": "cancer-longevity hinge",     "pdb": "7BG9", "example_drug": "imetelstat (inhibitor)"},
    {"symbol": "TERF1",  "name": "TRF1 (shelterin)",       "pathway": "telomere protection","role": "telomere capping",                      "pdb": "1W0U", "example_drug": "research compounds"},
    {"symbol": "POT1",   "name": "POT1 (shelterin)",       "pathway": "telomere protection","role": "telomere capping / cancer variant",     "pdb": "1XJV", "example_drug": "research compounds"},
    {"symbol": "TP53",   "name": "p53",                    "pathway": "tumor suppression",  "role": "cancer-safety anchor",                  "pdb": "1TUP", "example_drug": "nutlin (research)"},
    {"symbol": "MTHFR",  "name": "MTHFR",                  "pathway": "methylation",        "role": "vascular ageing / C677T variant",       "pdb": "6FCX", "example_drug": "riboflavin / methylfolate"},
]


class SafetyRequest(BaseModel):
    target_symbol: str = Field(..., pattern=r"^[A-Za-z0-9]{1,10}$", examples=["TERT"],
                               description="gene symbol of the intended target")
    mechanism: str = Field(..., pattern=r"^[A-Za-z0-9_]{1,40}$", examples=["telomerase_activation"],
                           description="mechanism class (e.g. mtor_inhibition, telomerase_activation, senolytic)")
    direction: str = Field("inhibit", pattern=r"^(activate|inhibit)$",
                           description="how the intervention acts on the target")


class DockRequest(BaseModel):
    # Strict patterns: these values flow into filesystem paths and an RCSB URL,
    # so they are constrained to the exact shapes a real PDB id / ligand code /
    # chain can take. This blocks path-traversal (e.g. "../../etc") and URL/arg
    # injection at the validation layer, before any path is built.
    pdb_id: str = Field(..., pattern=r"^[A-Za-z0-9]{4}$", examples=["1FKB"],
                        description="4-character RCSB PDB id of a holo (ligand-bound) structure")
    ligand_resname: str = Field(..., pattern=r"^[A-Za-z0-9]{1,3}$", examples=["RAP"],
                                description="1-3 character residue name of the ligand to (re)dock")
    chain: str = Field("A", pattern=r"^[A-Za-z0-9]$", description="single-character chain id")
    exhaustiveness: int = Field(8, ge=1, le=32, description="Vina search effort")


class ScreenRequest(BaseModel):
    pdb_id: str = Field(..., pattern=r"^[A-Za-z0-9]{4}$", examples=["4QNQ"],
                        description="holo target structure")
    ref_ligand: str = Field(..., pattern=r"^[A-Za-z0-9]{1,3}$", examples=["1XJ"],
                            description="bound ligand that defines the pocket / search box")
    chain: str = Field("A", pattern=r"^[A-Za-z0-9]$")
    exhaustiveness: int = Field(8, ge=1, le=32)


_CACHE: dict = {}


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


@app.get("/", include_in_schema=False)
def home():
    idx = Path(__file__).resolve().parent / "static" / "index.html"
    return FileResponse(idx) if idx.exists() else {"docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "engine": "foldock", "version": "0.1.0"}


@app.get("/targets")
def targets():
    """The curated geroscience target layer — the domain moat (module 6)."""
    db = DATA / "geroscience_targets.json"
    try:
        items = json.loads(db.read_text()) if db.exists() else TARGETS
        source = "curated_db" if db.exists() else "builtin"
    except Exception:
        items, source = TARGETS, "builtin"
    return {"count": len(items), "source": source, "targets": items}


@app.post("/cancer-safety")
def cancer_safety(req: SafetyRequest):
    """
    The longevity-oncology guardrail: score a proposed intervention for oncogenic
    risk (GREEN/AMBER/RED) from curated mechanism + target-direction knowledge.
    """
    return cancer_safety_assess(req.target_symbol, req.mechanism, req.direction)


@app.post("/dock")
def dock(req: DockRequest):
    """
    Redock a ligand into its target and return binding affinity PLUS an
    automated validation score (redock RMSD vs the crystal pose).
    """
    key = f"{req.pdb_id}_{req.ligand_resname}_{req.chain}_{req.exhaustiveness}"
    if key in _CACHE:
        return _CACHE[key]

    pdb = WORK / f"{req.pdb_id.upper()}.pdb"
    # defense in depth: even though pdb_id is regex-validated, confirm the
    # resolved path stays inside the work dir before any write.
    if WORK.resolve() not in pdb.resolve().parents:
        raise HTTPException(400, "invalid path")
    if not pdb.exists():
        try:
            urllib.request.urlretrieve(f"https://files.rcsb.org/download/{req.pdb_id.upper()}.pdb", pdb)
        except Exception as e:
            raise HTTPException(400, f"could not fetch PDB {req.pdb_id}: {e}")

    lines = pdb.read_text().splitlines()
    rec_lines = [l for l in lines if l.startswith("ATOM") and l[21:22] == req.chain]
    nat_lines = [l for l in lines if l.startswith("HETATM") and l[17:20].strip() == req.ligand_resname and l[21:22] == req.chain]
    if not rec_lines:
        raise HTTPException(404, f"no protein atoms for chain {req.chain} in {req.pdb_id}")
    if not nat_lines:
        raise HTTPException(404, f"ligand {req.ligand_resname} (chain {req.chain}) not found in {req.pdb_id}")

    rec = WORK / f"{key}_rec.pdb";   rec.write_text("\n".join(rec_lines) + "\n")
    nat = WORK / f"{key}_nat.pdb";   nat.write_text("\n".join(nat_lines) + "\n")
    recq = WORK / f"{key}_rec.pdbqt"; ligq = WORK / f"{key}_lig.pdbqt"
    _run([OBABEL, str(rec), "-O", str(recq), "-xr", "-p", "7.4", "--partialcharge", "gasteiger"])
    _run([OBABEL, str(nat), "-O", str(ligq), "-p", "7.4", "--partialcharge", "gasteiger"])

    xs = [float(l[30:38]) for l in nat_lines]
    ys = [float(l[38:46]) for l in nat_lines]
    zs = [float(l[46:54]) for l in nat_lines]
    cx, cy, cz = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2
    sx, sy, sz = (max(xs) - min(xs)) + 16, (max(ys) - min(ys)) + 16, (max(zs) - min(zs)) + 16

    poses = WORK / f"{key}_poses.pdbqt"
    _run([VINA, "--receptor", str(recq), "--ligand", str(ligq),
          "--center_x", f"{cx:.2f}", "--center_y", f"{cy:.2f}", "--center_z", f"{cz:.2f}",
          "--size_x", f"{sx:.1f}", "--size_y", f"{sy:.1f}", "--size_z", f"{sz:.1f}",
          "--exhaustiveness", str(req.exhaustiveness), "--num_modes", "9", "--seed", "0",
          "--out", str(poses)])
    if not poses.exists():
        raise HTTPException(500, "docking failed")

    affinity = None
    for l in poses.read_text().splitlines():
        if "VINA RESULT" in l:
            affinity = float(l.split()[3]); break

    pose1 = WORK / f"{key}_pose1.pdb"
    _run([OBABEL, str(poses), "-O", str(pose1), "-f", "1", "-l", "1"])
    rmsd = None
    out = _run([OBRMS, str(nat), str(pose1)]).stdout.strip()
    try:
        rmsd = float(out.split()[-1])
    except Exception:
        pass

    validated = rmsd is not None and rmsd < 2.0
    result = {
        "pdb_id": req.pdb_id,
        "ligand": req.ligand_resname,
        "chain": req.chain,
        "binding_affinity_kcal_mol": affinity,
        "redock_rmsd_angstrom": rmsd,
        "validation": {
            "passed": validated,
            "threshold_angstrom": 2.0,
            "verdict": "reproduces crystal pose — affinity is trustworthy" if validated
            else "pose deviates from crystal — flag for review",
        },
        "exhaustiveness": req.exhaustiveness,
    }
    _CACHE[key] = result
    return result


def _fetch_pdb(pdb_id: str) -> Path:
    pdb = WORK / f"{pdb_id.upper()}.pdb"
    if WORK.resolve() not in pdb.resolve().parents:
        raise HTTPException(400, "invalid path")
    if not pdb.exists():
        try:
            urllib.request.urlretrieve(f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb", pdb)
        except Exception as e:
            raise HTTPException(400, f"could not fetch PDB {pdb_id}: {e}")
    return pdb


@app.post("/screen")
def screen(req: ScreenRequest):
    """
    Virtual-screen the curated geroprotector library against a target pocket,
    rank by binding affinity, and attach a cancer-safety verdict to every hit.
    This is the engine doing real work: discovery + the longevity-oncology guardrail in one call.
    """
    pdb = _fetch_pdb(req.pdb_id)
    lines = pdb.read_text().splitlines()
    rec_lines = [l for l in lines if l.startswith("ATOM") and l[21:22] == req.chain]
    ref_lines = [l for l in lines if l.startswith("HETATM") and l[17:20].strip() == req.ref_ligand and l[21:22] == req.chain]
    if not rec_lines:
        raise HTTPException(404, f"no protein atoms for chain {req.chain} in {req.pdb_id}")
    if not ref_lines:
        raise HTTPException(404, f"reference ligand {req.ref_ligand} (chain {req.chain}) not found")

    rec = WORK / f"screen_{req.pdb_id}_{req.chain}_rec.pdb"
    rec.write_text("\n".join(rec_lines) + "\n")
    recq = WORK / f"screen_{req.pdb_id}_{req.chain}_rec.pdbqt"
    _run([OBABEL, str(rec), "-O", str(recq), "-xr", "-p", "7.4", "--partialcharge", "gasteiger"])

    xs = [float(l[30:38]) for l in ref_lines]
    ys = [float(l[38:46]) for l in ref_lines]
    zs = [float(l[46:54]) for l in ref_lines]
    cx, cy, cz = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2
    sx, sy, sz = (max(xs) - min(xs)) + 16, (max(ys) - min(ys)) + 16, (max(zs) - min(zs)) + 16

    try:
        library = json.loads((DATA / "geroprotector_library.json").read_text())
    except Exception as e:
        raise HTTPException(500, f"library load failed: {e}")

    hits = []
    for i, cpd in enumerate(library):
        ligq = WORK / f"screen_lig_{i}.pdbqt"
        prep = _run([OBABEL, f"-:{cpd['smiles']}", "--gen3d", "-O", str(ligq), "-p", "7.4"])
        if not ligq.exists():
            hits.append({"name": cpd["name"], "error": "ligand prep failed", "stderr": prep.stderr[-200:]})
            continue
        poses = WORK / f"screen_pose_{i}.pdbqt"
        _run([VINA, "--receptor", str(recq), "--ligand", str(ligq),
              "--center_x", f"{cx:.2f}", "--center_y", f"{cy:.2f}", "--center_z", f"{cz:.2f}",
              "--size_x", f"{sx:.1f}", "--size_y", f"{sy:.1f}", "--size_z", f"{sz:.1f}",
              "--exhaustiveness", str(req.exhaustiveness), "--num_modes", "5", "--seed", "0",
              "--out", str(poses)])
        aff = None
        if poses.exists():
            for l in poses.read_text().splitlines():
                if "VINA RESULT" in l:
                    aff = float(l.split()[3]); break
        safety = cancer_safety_assess(cpd["target"], cpd["mechanism"], cpd["direction"])
        hits.append({
            "name": cpd["name"],
            "binding_affinity_kcal_mol": aff,
            "intended_target": cpd["target"],
            "mechanism": cpd["mechanism"],
            "cancer_safety": safety["cancer_safety"],
        })

    ranked = sorted([h for h in hits if h.get("binding_affinity_kcal_mol") is not None],
                    key=lambda h: h["binding_affinity_kcal_mol"])
    failed = [h for h in hits if h.get("binding_affinity_kcal_mol") is None]
    return {
        "target_pdb": req.pdb_id,
        "pocket_from_ligand": req.ref_ligand,
        "library_size": len(library),
        "ranked_hits": ranked,
        "failed": failed,
    }
