"""
Cancer-safety filter — the longevity-oncology guardrail.

The central trap in reverse-ageing R&D: interventions that extend healthspan can
also be pro-cancer (telomerase reactivation is the immortalization step in
~85-90% of tumors; suppressing p53 removes the master tumor-suppressor; etc.).

This module scores a proposed pro-longevity intervention for oncogenic risk using
THREE independent signals, and is explicit about what each can and cannot say:

  1. MECHANISM risk   — curated longevity-oncology knowledge (mechanism class -> risk)
  2. TARGET risk      — is the target an oncogene / tumor-suppressor, and is the
                        intervention pushing it in the tumour-SAFE direction?
  3. OFF-TARGET risk  — (optional) high-affinity binding to a cancer-guardrail
                        protein, supplied by the docking engine.

Honest limit: docking yields binding affinity, not agonist-vs-antagonist DIRECTION.
So this is a TRIAGE signal (prioritise / flag for functional assay), never a
clinical safety determination.
"""
from typing import Optional

GREEN, AMBER, RED = "GREEN", "AMBER", "RED"
_RANK = {GREEN: 0, AMBER: 1, RED: 2}
_SCORE = {GREEN: 15, AMBER: 55, RED: 90}


# --- signal 1: mechanism class -> intrinsic oncogenic risk (curated) ---
MECHANISM_RISK = {
    "telomerase_activation": (RED,   "Telomerase reactivation is the immortalization step in ~85-90% of cancers."),
    "telomere_lengthening":  (RED,   "Extending replicative capacity is the hallmark cancers exploit."),
    "p53_inhibition":        (RED,   "p53 is the master tumor suppressor; inhibiting it removes a core cancer brake."),
    "apoptosis_inhibition":  (RED,   "Evading apoptosis is a defining hallmark of cancer."),
    "igf1_increase":         (RED,   "Elevated GH/IGF-1 signalling is pro-proliferative and epidemiologically cancer-linked."),
    "nrf2_activation":       (AMBER, "Acute NRF2 activation is cytoprotective, but chronic activation aids tumour survival/chemoresistance."),
    "sirtuin_activation":    (AMBER, "SIRT1 is context-dependent — both tumour-suppressive and oncogenic roles reported."),
    "nad_boost":             (AMBER, "NAD+ repletion is broadly beneficial but may fuel existing-tumour metabolism; monitor."),
    "autophagy_induction":   (AMBER, "Autophagy is tumour-suppressive early but can sustain established tumours."),
    "senolytic":             (GREEN, "Clears senescent cells via pro-apoptotic action — mechanism shared with anti-cancer therapy."),
    "mtor_inhibition":       (GREEN, "mTOR inhibition (rapalogs) is also developed as anti-cancer therapy."),
    "ampk_activation":       (GREEN, "AMPK activation (e.g. metformin) is associated with reduced cancer incidence."),
    "telomerase_inhibition": (GREEN, "Telomerase inhibition is itself an anti-cancer strategy (e.g. imetelstat)."),
    "partial_reprogramming": (AMBER, "Epigenetic reprogramming risks dedifferentiation/teratoma if uncontrolled; transient protocols mitigate."),
}

# --- signal 2: target cancer-gene class + the tumour-SAFE direction ---
# safe direction: the direction that does NOT promote cancer.
TARGET_CLASS = {
    "TERT":   ("telomere-maintenance (oncogenic when active)", "inhibit"),
    "TP53":   ("tumor suppressor",                              "activate"),
    "MDM2":   ("oncogene (p53 antagonist)",                     "inhibit"),
    "BCL2L1": ("anti-apoptotic oncogene (Bcl-xL)",              "inhibit"),
    "BCL2":   ("anti-apoptotic oncogene",                       "inhibit"),
    "MTOR":   ("proliferation oncogene",                        "inhibit"),
    "PRKAA1": ("metabolic / tumour-suppressive (AMPK)",         "activate"),
    "FOXO3":  ("tumor suppressor",                              "activate"),
    "SIRT1":  ("context-dependent",                             "caution"),
    "KEAP1":  ("NRF2 regulator (context-dependent)",            "caution"),
    "POT1":   ("telomere capping; loss is oncogenic",           "preserve"),
    "TERF1":  ("telomere capping",                              "preserve"),
}


def _worst(*levels: str) -> str:
    return max(levels, key=lambda l: _RANK[l])


def assess(target_symbol: str,
           mechanism: str,
           direction: str = "inhibit",
           offtarget_hits: Optional[list] = None) -> dict:
    """
    Score an intervention's oncogenic risk.

    target_symbol : gene symbol of the intended target (e.g. "MTOR", "TERT")
    mechanism     : mechanism class key from MECHANISM_RISK
    direction     : "activate" | "inhibit" (how the intervention acts on the target)
    offtarget_hits: optional list of {"target","affinity_kcal_mol"} from docking the
                    compound against the cancer-guardrail panel
    """
    signals = []
    mechanism = mechanism.lower().strip()
    direction = direction.lower().strip()

    # signal 1: mechanism
    mech_level, mech_reason = MECHANISM_RISK.get(mechanism, (AMBER, "Unrecognised mechanism — defaulting to caution."))
    signals.append({"signal": "mechanism", "level": mech_level, "detail": f"{mechanism}: {mech_reason}"})

    # signal 2: target class x direction
    tgt_level = GREEN
    sym = target_symbol.upper()
    if sym in TARGET_CLASS:
        klass, safe_dir = TARGET_CLASS[sym]
        if safe_dir in ("caution", "preserve"):
            tgt_level = AMBER
            signals.append({"signal": "target", "level": AMBER,
                            "detail": f"{sym} is {klass}; direction-of-effect must be confirmed ({safe_dir})."})
        elif direction == safe_dir:
            tgt_level = GREEN
            signals.append({"signal": "target", "level": GREEN,
                            "detail": f"{sym} is {klass}; '{direction}' is the tumour-safe direction."})
        else:
            tgt_level = RED
            signals.append({"signal": "target", "level": RED,
                            "detail": f"{sym} is {klass}; '{direction}' pushes the cancer-PROMOTING direction (safe = '{safe_dir}')."})
    else:
        signals.append({"signal": "target", "level": GREEN,
                        "detail": f"{sym} not on the cancer-gene panel (no direct oncogene/TSG flag)."})

    # signal 3: off-target binding to the guardrail panel (optional)
    off_level = GREEN
    for hit in (offtarget_hits or []):
        aff = hit.get("affinity_kcal_mol")
        if aff is not None and aff <= -9.0 and hit.get("target", "").upper() != sym:
            off_level = _worst(off_level, AMBER)
            signals.append({"signal": "off_target", "level": AMBER,
                            "detail": f"Strong off-target binding to {hit['target']} ({aff} kcal/mol) — investigate oncogenic liability."})

    overall = _worst(mech_level, tgt_level, off_level)
    return {
        "target": sym,
        "mechanism": mechanism,
        "direction": direction,
        "cancer_safety": overall,
        "risk_score": _SCORE[overall],
        "verdict": {
            GREEN: "PROCEED — no oncogenic red flag (still triage, not a clinical clearance).",
            AMBER: "CAUTION — context-dependent; confirm direction-of-effect with a functional assay before advancing.",
            RED:   "BLOCK — mechanism/target pushes a known cancer-promoting direction; do not advance without strong justification.",
        }[overall],
        "signals": signals,
        "caveats": [
            "Docking gives binding affinity, not agonist-vs-antagonist direction — direction-of-effect needs a functional assay.",
            "This is a prioritisation/triage signal, not a clinical safety determination.",
        ],
    }
