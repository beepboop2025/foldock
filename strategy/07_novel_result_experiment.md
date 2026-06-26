# The Novel-Result Experiment — from "tool" to "we found something"

*Everything validated so far **reproduces known** drug–target pairs (rapamycin, navitoclax). That proves the engine is trustworthy, but no one funds re-deriving known science. This designs ONE novel, defensible result that upgrades the whole pitch.*

---

## The bar a "novel result" must clear

1. **Prospective, not retrospective** — predicted *before* knowing the answer.
2. **Non-obvious** — not a drug already known to hit that target.
3. **Independently checkable** — confirmable against evidence you did NOT use to generate it (the key to defensibility).
4. **Honest about limits** — docking ≠ efficacy; framed as a *prioritisation*, with controls.

---

## Recommended experiment: blind-validation repurposing screen

**Idea:** screen a library of **approved drugs** against an ageing target, surface the top *non-obvious* hits, then check the independent literature. If a drug your engine ranks highly turns out to have *independent experimental evidence* of geroprotective / target-relevant activity that you did **not** feed it — that's a **blind rediscovery**: hard evidence the engine finds real biology, not noise.

### Protocol

1. **Pick the target.** A well-characterised ageing target with a crystal-structure pocket and an approved-drug-rich chemical space. Good first choice: **Bcl-xL / Bcl-2 (senolysis)** — clean pocket (you already validated it at 0.90 Å), and senolytic space is active.
2. **Build the library.** ~200–500 approved drugs (DrugBank approved subset; SMILES). Bigger than today's 5-compound set, small enough to run on CPU over a day or two via the `/screen` pipeline.
3. **Positive & negative controls (this is what makes it rigorous):**
   - **Positive:** spike in known binders (navitoclax, ABT-737). They *must* rank near the top — if they don't, the screen is broken.
   - **Negative:** a set of random/irrelevant approved drugs. They should rank low.
4. **Rank** all compounds by affinity; apply the **validation** and **cancer-safety** filters.
5. **Quarantine the obvious.** Remove drugs already known to target Bcl-2 family → leaves the *non-obvious* top hits.
6. **Blind literature check.** For the top 5 non-obvious hits, search PubMed/bioRxiv for *any independent* evidence of senolytic / pro-apoptotic / geroprotective activity you did not use. A match = blind rediscovery.

### Success criteria (state these up front, report honestly either way)

- ✅ **Strong:** ≥1 non-obvious top hit has independent literature support → "our engine blind-rediscovered a known-but-non-obvious senolytic."
- ✅ **Still useful:** controls behave correctly (positives top, negatives bottom) even if no blind hit → "the engine ranks correctly and proposes N testable candidates."
- ❌ **Negative:** positives don't rank → fix the pipeline before claiming anything (and you'll *know*, which is the point).

### The deck sentence it produces
> *"Given only approved-drug structures, the engine ranked [drug X] — not previously associated with senescence in our inputs — among the top senolytic candidates; independent [year] data shows it does [relevant activity]. The engine finds real biology, not just reproduces it."*

---

## Complementary experiment: complete the variant-triage story (ΔΔG-stability)

Your MTHFR C677T result correctly showed docking finds *no* binding change — because it's a **stability** variant. The honest gap: you classified it but didn't *measure* the stability effect. Closing it:

1. Add a **ΔΔG-stability module** (free options: a structure-based predictor like a FoldX-style or ThermoMPNN-style ΔΔG; or short MD).
2. Apply to A222V → it should predict **destabilisation** (matching the known biochemistry: bulkier Val in a packed core, reduced FAD retention).
3. **Result:** the variant-triage loop now *resolves* — docking says "not binding," stability module says "destabilising," matching reality.

### The deck sentence it produces
> *"Our engine doesn't just classify a variant — it routes MTHFR C677T to stability analysis and correctly predicts the destabilisation that docking alone misses. Right method, right answer — population-specific."*

---

## Recommendation & effort

- **Lead with the repurposing screen** (the "we found something" story) — highest pitch impact. ~1–2 days compute on the existing `/screen` pipeline + a few hours of literature checking.
- **Add the ΔΔG-stability module** as the moat-completion (the variant story done right) — a few days of build.

Both are the *only* remaining building tasks worth doing for funding. Everything else (more endpoints, async, UI polish) does not move the round.

> **Honesty discipline:** pre-register the success criteria above before running, and report the actual outcome — including a null. A founder who says "the controls passed and here are 3 testable candidates" is more fundable than one who over-claims a cure, because the first survives diligence.
