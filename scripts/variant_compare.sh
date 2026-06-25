#!/bin/bash
VINA=~/micromamba/envs/dock/bin/vina
OBABEL=/opt/homebrew/bin/obabel
LIG=MTHFR_WT_FAD_lig.pdbqt
CX=3.75; CY=33.92; CZ=-35.01; SX=33.4; SY=25.4; SZ=31.4
for pair in "MTHFR_WTpolyA.pdb:WTctrl" "MTHFR_A222V.pdb:VAR"; do
  rec="${pair%%:*}"; pfx="MTHFRc_${pair##*:}"
  $OBABEL "$rec" -O ${pfx}_rec.pdbqt -xr -p 7.4 --partialcharge gasteiger 2>${pfx}_prep.err
  natoms=$(grep -c '^ATOM' ${pfx}_rec.pdbqt 2>/dev/null)
  echo "$pfx receptor pdbqt atoms: $natoms"
  $VINA --receptor ${pfx}_rec.pdbqt --ligand "$LIG" \
    --center_x $CX --center_y $CY --center_z $CZ --size_x $SX --size_y $SY --size_z $SZ \
    --exhaustiveness 8 --num_modes 5 --seed 0 --out ${pfx}_poses.pdbqt > ${pfx}_vina.log 2>&1
  aff=$(grep -m1 "VINA RESULT" ${pfx}_poses.pdbqt | awk '{print $4}')
  echo "RESULT $pfx FAD affinity = $aff kcal/mol"
done
echo CMP2_DONE
