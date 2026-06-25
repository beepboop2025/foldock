# strategy — PRIVATE

The competitive core. Not for public release.

- **01_company.md** — full company map: thesis, the measure→match→prove platform, tech stack, business model, moat, regulatory path, roadmap, risks.
- **02_pitch_deck.md** — 12-slide pre-seed pitch deck.
- **03_build_prompts.md** — phased prompt library to build the whole product.
- **AMRITA_master.pdf** — the above, rendered with all figures embedded.

## The wedge (kept out of the public engine repo)

The defensible edge is **population-calibrated variant triage** for South-Asian ageing biology:
classify each variant (binding-pocket vs buried-stability vs allosteric) and route it to the
correct method (docking vs ΔΔG-stability vs MD).

Demonstrated on **MTHFR C677T (Ala222Val)** — high frequency in South-Asian populations:
redocking the FAD cofactor showed **no binding-affinity change (−11.1 vs −11.1 kcal/mol)**, which
is the *correct* result — residue 222 is 10.1 Å from the pocket and buried in the core (30 contacts),
so C677T is a **stability variant, not a binding variant** (matched fix: riboflavin). See
`../scripts/variant_compare.sh` and `../figures/MTHFR_C677T_variant.png`.

**Next build:** the ΔΔG-stability + MD module (the correct tool for A222V), then scale to the
full ageing-target × approved-drug matrix.
