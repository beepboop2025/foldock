#!/bin/bash
# redock.sh — structure-based redocking validation with AutoDock Vina.
#
# Given a holo PDB (receptor + bound ligand), this:
#   1. splits the receptor and the native (crystal) ligand
#   2. prepares both for docking (Open Babel)
#   3. defines the search box from the native ligand centroid
#   4. redocks the ligand with AutoDock Vina
#   5. reports binding affinity and the redock RMSD vs the crystal pose
#
# A redock RMSD < 2.0 Å indicates the pipeline reproduces the experimental
# binding mode — the standard validation for a docking workflow.
#
# Usage: redock.sh <pdb> <ligand_resname> <chain> <output_prefix>
#
# Tool paths are configurable via environment variables (sensible defaults):
set +e
VINA="${VINA:-vina}"
OBABEL="${OBABEL:-obabel}"
OBRMS="${OBRMS:-obrms}"

PDB=$1; LIG=$2; CH=$3; PFX=$4
[ -z "$PFX" ] && { echo "usage: redock.sh <pdb> <ligand_resname> <chain> <prefix>"; exit 1; }
echo "===== $PFX : redock $LIG (chain $CH) into $PDB ====="

# 1. split receptor (protein ATOM, chain CH) and native ligand (HETATM)
awk -v ch="$CH" '/^ATOM/ && substr($0,22,1)==ch' "$PDB" > ${PFX}_rec.pdb
awk -v ch="$CH" -v lg="$LIG" '/^HETATM/ && substr($0,18,3)~lg && substr($0,22,1)==ch' "$PDB" > ${PFX}_lig_native.pdb
echo "receptor atoms: $(wc -l < ${PFX}_rec.pdb) ; native ligand atoms: $(wc -l < ${PFX}_lig_native.pdb)"

# 2. prepare receptor (rigid) and ligand as PDBQT
$OBABEL ${PFX}_rec.pdb -O ${PFX}_rec.pdbqt -xr -p 7.4 --partialcharge gasteiger 2>/dev/null
$OBABEL ${PFX}_lig_native.pdb -O ${PFX}_lig.pdbqt -p 7.4 --partialcharge gasteiger 2>/dev/null

# 3. search box from the native ligand bounding box (+16 Å padding)
read CX CY CZ SX SY SZ < <(python3 - "${PFX}_lig_native.pdb" <<'PY'
import sys
xs=[];ys=[];zs=[]
for l in open(sys.argv[1]):
    if l.startswith(("ATOM","HETATM")):
        xs.append(float(l[30:38]));ys.append(float(l[38:46]));zs.append(float(l[46:54]))
cx=(max(xs)+min(xs))/2;cy=(max(ys)+min(ys))/2;cz=(max(zs)+min(zs))/2
print(f"{cx:.2f} {cy:.2f} {cz:.2f} {(max(xs)-min(xs))+16:.1f} {(max(ys)-min(ys))+16:.1f} {(max(zs)-min(zs))+16:.1f}")
PY
)
echo "box center=($CX,$CY,$CZ) size=($SX,$SY,$SZ)"

# 4. dock
$VINA --receptor ${PFX}_rec.pdbqt --ligand ${PFX}_lig.pdbqt \
  --center_x $CX --center_y $CY --center_z $CZ \
  --size_x $SX --size_y $SY --size_z $SZ \
  --exhaustiveness 16 --num_modes 9 --seed 0 \
  --out ${PFX}_poses.pdbqt > ${PFX}_vina.log 2>&1
AFF=$(grep -m1 "VINA RESULT" ${PFX}_poses.pdbqt | awk '{print $4}')
echo "top binding affinity: ${AFF} kcal/mol"

# 5. redock RMSD vs crystal pose
$OBABEL ${PFX}_poses.pdbqt -O ${PFX}_pose_top.pdb -f 1 -l 1 2>/dev/null
echo -n "redock RMSD (heavy atoms): "
$OBRMS ${PFX}_lig_native.pdb ${PFX}_pose_top.pdb 2>&1 | awk '{print $NF" A"}'
echo "===== $PFX DONE ====="
