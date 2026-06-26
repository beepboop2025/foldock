# AMRITA — The Engine for Reverse-Ageing Science (B2B thesis)

*Private strategy. Supersedes the consumer-app framing in `01_company.md` as the primary go-to-market.*

---

## One-liner

**The validated computational engine that powers reverse-ageing research.**
Longevity labs all rebuild the same stack — fold targets, dock compounds, triage variants, model the cancer trade-off — redundantly and with un-validated academic scripts. AMRITA is the turnkey, geroscience-specific platform they plug into instead.

**Analogy:** *Schrödinger for longevity* — a computational discovery platform (Schrödinger is a multi-billion-dollar public company), but specialised for ageing biology, validation-first, and built at India cost.

---

## The problem we sell against

Every longevity biotech and academic lab doing structure-based work today:
- writes its own one-off docking scripts (no validation, not reproducible, not auditable);
- has no geroscience-curated target/pathway layer — they assemble it by hand;
- cannot easily model **variants** (patient- or population-specific) or the **cancer–longevity trade-off**;
- burns scarce computational-biology headcount on plumbing instead of science.

The result is slow, redundant, un-trustworthy in-house tooling at hundreds of institutions.

---

## Product — the engine, productised into 6 modules

| # | Module | What it does | Status |
|---|---|---|---|
| 1 | **Target** | fold (AlphaFold/ESMFold) or retrieve any ageing-target structure, including variants | ✅ validated |
| 2 | **Screen** | dock approved-drug or custom compound libraries → ranked binding affinities | ✅ validated |
| 3 | **Validate** | automated redocking RMSD + confidence score on every result (the trust layer) | ✅ validated |
| 4 | **Variant-triage** | classify a variant as pocket / buried-stability / allosteric → route to the right method | ✅ validated |
| 5 | **Cancer-safety filter** | GREEN/AMBER/RED oncogenic-risk verdict (mechanism + target oncogene/TSG direction + off-target) | ✅ built |
| 6 | **Geroscience knowledge layer** | curated ageing-target DB (hallmarks, pathways, oncogene/TSG class) served via `/targets` | ✅ built |

**Proof points already in hand (local, CPU-only):**
- mTOR FRB fold, mean pLDDT 92.8.
- Rapamycin → FKBP12: −11.09 kcal/mol, redock RMSD **0.53 Å**.
- Navitoclax → Bcl-xL: −10.56 kcal/mol, redock RMSD **0.90 Å**.
- MTHFR C677T variant-triage: correctly classified as a stability (not binding) variant.

**Delivery:** REST API + web dashboard (cloud SaaS); optional on-prem/VPC deployment for pharma data-sensitivity.

---

## Ideal customer profile (the institutions)

| Segment | Examples | Why they buy |
|---|---|---|
| **Longevity biotechs** | Altos, Calico, Retro, NewLimit, Life Biosciences, Turn Bio, BioAge, Unity, Cambrian, Gero, Shift | Replace fragile in-house scripts; ship validated results faster |
| **Academic geroscience** | Buck Institute, Salk, Barzilai/Einstein, Sinclair/Harvard | Reproducible, citable, validated structure-based results |
| **Pharma geroscience units** | large-pharma ageing programs | Turnkey repurposing + variant + safety screening, on-prem |
| **Longevity clinics** | clinical-side research arms | Evidence-graded intervention prioritisation |
| **Indian / Asian research ecosystem** | emerging institutes | First-mover platform at local cost; population-specific variant data |

---

## Why this is the fundable shape

1. **Picks-and-shovels.** Single-drug bets fail ~90% of the time; the tool sold to everyone making those bets earns regardless of which drug wins.
2. **Recurring revenue.** SaaS subscriptions + usage + enterprise contracts — far more fundable than speculative consumer or single-asset plays.
3. **Domain moat.** The defensibility is the *geroscience layer* (curated targets, cancer-longevity trade-off, validation, variant-triage, cancer-safety) — not the raw docking, which is commodity.
4. **Network/data effects.** Every customer run enriches the curated target/result corpus and the validation benchmarks.
5. **Capital fit.** Appeals to deep-tech VCs (infra + recurring revenue) and to bio-infra investors; the science de-risks via the validation layer.

---

## Competitive landscape & wedge

| Competitor | Gap we exploit |
|---|---|
| **Schrödinger / OpenEye / MOE** | generic, expensive, not ageing-specific, not validation-first; we specialise + undercut on price |
| **Free Vina / academic DIY** | no validation/trust layer, no domain curation, no variant/safety modules, high labour |
| **AI-drug-discovery (Recursion, Insitro)** | they run *their own* pipelines (compete with customers); we are neutral infrastructure |

**Our wedge:** *geroscience-specialised + validation-first + variant-aware + cancer-guarded + India cost.* Not "another docking tool" — the **trusted, longevity-domain engine** labs standardise on.

---

## Business model

- **Tiered SaaS:** seat + usage (compute/jobs). Academic tier (low, for adoption/credibility) → biotech tier → enterprise/pharma (on-prem, contract).
- **Hybrid upside (optional, later):** collaborative discovery with revenue-share/milestones on hits surfaced for partners (the Schrödinger hybrid model).
- **Data products:** licensed access to the curated geroscience target/variant corpus.

---

## Go-to-market

1. **Land via the validation layer** — the wedge feature academics immediately value; seed adoption in academic geroscience (low/free tier) for credibility and citations.
2. **Expand to biotechs** — paid tiers once labs depend on the workflow.
3. **Enterprise/pharma** — on-prem contracts for variant + cancer-safety screening.
4. **Lighthouse content** — publish the validated benchmarks (the redock RMSD results) as the proof artifact; the public `foldock` repo is the top-of-funnel credibility piece.
5. **Scientific advisory board** — recruit a geroscience name to sell into PhD buyers.

---

## Moat (defensible, compounding)

1. Geroscience-curated target/pathway/variant corpus.
2. Validation benchmark library (trust layer + reproducibility).
3. Cancer-longevity trade-off modeling (the safety filter).
4. Population-calibrated variant-triage (incl. South-Asian biology) — a dataset competitors lack.
5. India cost structure for compute + ops.

---

## Roadmap

| Phase | Milestone | Status |
|---|---|---|
| 0 | Validated engine (fold/dock/validate/variant) | ✅ done |
| 1 | Engine-as-a-service API (`POST /dock` → affinity + validation) | 🔜 in progress |
| 2 | Curated ageing-target DB + web dashboard + multi-tenancy/auth | next |
| 3 | Cancer-safety filter (telomere/telomerase) module | next |
| 4 | First 3 design-partner institutions (academic lighthouses) | GTM |

---

## The ask (framing)

Pre-seed to: harden the engine into a multi-tenant API + dashboard, build the curated geroscience layer + cancer-safety module, and land the first academic design partners — turning a validated local engine into the platform reverse-ageing research standardises on.
