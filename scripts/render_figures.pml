set ray_opaque_background, 0
set ray_shadows, 0
bg_color white
set antialias, 2
set cartoon_transparency, 0.0

# ---------- FIG 1: mTOR FRB fold colored by pLDDT ----------
load mTOR_FRB_top.pdb, m
hide everything
show cartoon, m
# pLDDT is in the B-factor column; high pLDDT -> blue (confident)
spectrum b, red_yellow_green, m, minimum=50, maximum=95
# Ser2035 = residue 11 in the renumbered construct (2025 start)
select anchor, m and resi 11
show sticks, anchor
color blue, anchor
set cartoon_side_chain_helper, 1
orient m
turn y, 20
set ray_trace_mode, 1
ray 1400, 1000
png fig1_mTOR_fold.png, dpi=150
delete all

# ---------- FIG 2: Rapamycin redock into FKBP12 ----------
load FKBP12_RAPA_rec.pdb, rec
load FKBP12_RAPA_lig_native.pdb, nat
load FKBP12_RAPA_pose_top.pdb, dock
hide everything
show cartoon, rec
color grey80, rec
set cartoon_transparency, 0.45, rec
show sticks, nat
show sticks, dock
color green, nat
color cyan, dock
set stick_radius, 0.18, nat
set stick_radius, 0.18, dock
orient nat
zoom nat, 6
ray 1400, 1000
png fig2_rapamycin_FKBP12.png, dpi=150
delete all

# ---------- FIG 3: Navitoclax redock into Bcl-xL ----------
load BCLXL_NAVI_rec.pdb, rec
load BCLXL_NAVI_lig_native.pdb, nat
load BCLXL_NAVI_pose_top.pdb, dock
hide everything
show cartoon, rec
color wheat, rec
set cartoon_transparency, 0.45, rec
show sticks, nat
show sticks, dock
color green, nat
color cyan, dock
set stick_radius, 0.18, nat
set stick_radius, 0.18, dock
orient nat
zoom nat, 6
ray 1400, 1000
png fig3_navitoclax_BclxL.png, dpi=150
delete all

# ---------- FIG 4: MTHFR A222V buried, distal to FAD ----------
load 6FCX.pdb, mt
hide everything
# chain A protein + FAD
create prot, mt and chain A and polymer
create fad, mt and chain A and resn FAD
show cartoon, prot
color grey70, prot
set cartoon_transparency, 0.35, prot
show sticks, fad
color orange, fad
# residue 222 buried in core
select v222, prot and resi 222
show spheres, v222
color magenta, v222
set sphere_scale, 0.5, v222
# label distance
distance dd, v222 and name CB, fad, 12
hide labels
orient prot and resi 179+192+194+218+222
zoom (v222 or fad), 4
ray 1400, 1000
png fig4_MTHFR_variant.png, dpi=150
delete all
