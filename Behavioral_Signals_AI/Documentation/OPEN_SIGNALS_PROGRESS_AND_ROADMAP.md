# Open Signals Progress And Roadmap

## 1. Executive Summary

Open Signals is evolving into a privacy-preserving behavioral economic intelligence system. Its purpose is to detect emerging demand, unmet needs, market pressure, policy concerns, and market opportunities from aggregate signals rather than individual-level behavior.

The system is designed to combine public, anonymized, aggregate, or user-authorized evidence into decision-ready intelligence. It does not aim to become a social media dashboard or a raw analytics console. It is becoming an AI-native economic sensing layer that turns collective signal patterns into policy, business, and opportunity insight.

## 2. What Has Been Implemented So Far

The Open Signals work completed so far includes:

- **Live signal feed:** The Behavioral Signals AI section now presents interpreted signal cards rather than raw behavioral input fields.
- **Green live-status dot:** The Open Signals heading has a small blinking green heartbeat dot to indicate live updating without making the whole feed flicker.
- **Reduced feed flickering:** Feed rendering is cache-aware and avoids unnecessary full-section redraws when the underlying signal ranking has not materially changed.
- **Cache-backed rendering:** The live feed reads from processed signal cache so it never needs to perform heavy source collection during each UI refresh.
- **Adaptive signal scoring:** Signals are ranked using persistence, source agreement, confidence, momentum, urgency, historical recurrence, and related adaptive intelligence fields.
- **Behavioral taxonomy:** Signals are classified into demand, affordability, stress, and opportunity families.
- **Demand, affordability, stress, and opportunity signals:** Open Signals can interpret whether a pattern reflects market demand, constrained affordability, social/economic stress, or opportunity potential.
- **Historical learning memory:** The system can store and compare recurring signal patterns over time.
- **Daily, monthly, and yearly learning:** Historical learning modules support daily, monthly, and yearly summaries and memory structures.
- **Outcome learning:** The system has a mechanism for comparing earlier predictions against later evidence and adapting future confidence.
- **County-aware location dropdown:** The Location filter now includes Global, Kenya, and all 47 Kenyan counties.
- **Kenya geospatial learning layer:** Signals can be enriched with county name, county code, geographic scope, spread risk, forecast direction, geospatial insight, and ML rank score.
- **County codes and aliases:** The geography layer includes official county codes and aliases such as Wote to Makueni, Westlands to Nairobi, and Eldoret to Uasin Gishu.
- **Privacy guardrails:** Mobility/place and signal processing modules reject personal mobility fields and other individual-level identifiers.
- **LLM-ready interpretation:** The architecture supports LLM-assisted interpretation while preserving rule-based fallback when no LLM key is configured.
- **Adaptive category learning:** The Category filter now keeps default categories while learning safe recurring categories from aggregate patterns.
- **Source validation:** Source health, validation, and outcome-related structures have been added to help distinguish stronger signals from weak/noisy patterns.
- **Signal CGE preservation:** Signal CGE has been kept separate and unchanged during Open Signals UI and behavioral-intelligence work.

## 3. Current Architecture

The current Open Signals pipeline follows this flow:

```text
aggregate/public signals
→ normalization
→ behavioral taxonomy
→ geospatial detection
→ adaptive learning
→ historical memory
→ outcome validation
→ LLM/rule-based interpretation
→ live signal feed
```

Operationally:

1. Public or fallback aggregate signals are collected or loaded from cache.
2. Records are normalized into a common signal structure.
3. Behavioral taxonomy classifies signals as demand, affordability, stress, opportunity, or combinations of these families.
4. Geospatial detection maps county names, aliases, towns, or local context to Kenya-wide or county-specific intelligence.
5. Adaptive learning updates persistence, source agreement, momentum, recurrence, and confidence.
6. Historical memory checks whether similar signals have appeared before.
7. Outcome learning tracks whether past signals were later confirmed, partially confirmed, or weak.
8. LLM-ready and rule-based interpretation turns technical signal evidence into readable policy, market, and opportunity insight.
9. The UI displays only interpreted signal cards and summaries.

## 4. Privacy Principles

Open Signals is privacy-first by design. It must not become a surveillance system.

The system follows these principles:

- No individual tracking.
- No device IDs.
- No personal route histories.
- No exact home or work locations.
- No private messages.
- No personal profiles.
- No raw individual-level behavioral histories.
- Only aggregate, anonymized, public, or user-authorized data should be processed.
- Public outputs should remain at county, category, market, policy, or aggregate signal level.

The purpose is to infer aggregate revealed demand and economic pressure, not to identify or profile people.

## 5. Current UI

The current dashboard preserves a simple intelligence-first interface:

- **OpenSignal title:** The main dashboard title is now OpenSignal.
- **Open Signals tab heading:** The Behavioral Signals AI section heading is displayed as Open Signals.
- **Live green heartbeat dot:** A small green dot blinks beside the Open Signals heading.
- **Location filter:** Includes Global, Kenya, and all 47 Kenyan counties.
- **Category filter:** Includes static default categories plus active learned categories promoted from recurring aggregate patterns.
- **Urgency filter:** Allows filtering by All, High, Medium, or Low urgency.
- **Live Signal Feed:** Shows interpreted signal cards rather than raw engagement metrics.
- **Emerging Kenya Signals:** Highlights rising, urgent, or early-warning signals.
- **Signal Interpretation & Opportunity:** Explains what the top signals may mean for markets, policy, business, and risk.
- **Historical Learning Insight:** Summarizes how current signals relate to historical memory and expected next developments.

The dashboard flow is intentionally minimal: privacy notice, filters, live intelligence feed, emerging signals, interpretation, and historical learning.

## 6. Current Limitations

Current limitations include:

- Live source connectors are still mostly placeholders, fallback sources, or readiness scaffolds.
- Real API credentials are not yet configured in this environment.
- Hugging Face free Spaces may sleep after inactivity, so continuous 24/7 operation requires paid always-on hardware, an external scheduler, or a separate backend service.
- Persistent storage needs further strengthening for long-running production deployments.
- Geospatial boundaries and shapefiles are not yet fully integrated.
- County heatmap and GIS visualization readiness exists conceptually but is not yet implemented as a full geospatial analytics layer.
- Mobility/place-visit intelligence remains conceptual or metadata-based unless authorized aggregate place activity data is available.
- LLM integration is fallback-ready but not fully active without configured provider credentials.
- Some historical learning and validation modules need more real observed outcomes to become empirically strong.
- Pytest is not installed in the current local virtual environment, limiting automated test execution until dependency setup is completed.

## 7. High-Value Improvements

### A. Real Data Connector Activation

Priority live source activation should include:

- Google Trends or SerpAPI for search-demand signals.
- Public news APIs for public concern and policy/economic context.
- KNBS, CBK, and Kilimostat indicators for official validation.
- Food price datasets for affordability and cost-of-living pressure.
- YouTube, Reddit, and X public signals where legally available and privacy-safe.

This is the highest-value improvement because the intelligence system becomes much stronger when it receives real aggregate evidence rather than fallback sample signals.

### B. Durable Storage

Strengthen memory persistence through:

- storage manager expansion,
- atomic writes,
- backup recovery,
- corruption recovery,
- optional Hugging Face Dataset or repository persistence,
- clear runtime/output ignore rules.

This matters because adaptive intelligence depends on memory surviving restarts and deployments.

### C. Real GIS Boundary Integration

Add geospatial foundations for:

- Kenya national boundary,
- all 47 county GeoJSON boundaries,
- county code registry alignment,
- county heatmap readiness,
- future county stress and opportunity maps.

This will make county intelligence more spatially grounded and future-ready.

### D. Aggregate Mobility Intelligence

Build privacy-preserving mobility/place intelligence around:

- category-level place visitation,
- relative change from baseline,
- minimum aggregation thresholds,
- public/authorized data only,
- no individual tracking,
- no route reconstruction.

This can reinforce demand intelligence when aggregate place activity aligns with digital or public source signals.

### E. LLM-Assisted Interpretation

Activate LLM-assisted interpretation for:

- strategic summaries,
- opportunity reasoning,
- policy implications,
- natural-language question answering,
- explanation of why signals matter.

LLMs should only process sanitized aggregate signal summaries.

### F. Feedback and Validation Console

Add an internal, non-public validation workflow where analysts can:

- confirm a signal,
- reject a signal,
- correct county classification,
- correct category classification,
- mark false positives,
- record observed outcomes.

This would greatly improve learning quality and reduce false positives over time.

### G. Evaluation Metrics

Add measurable intelligence-quality metrics:

- precision of signal detection,
- false positive rate,
- source reliability score,
- outcome confirmation rate,
- forecast accuracy,
- county detection accuracy,
- learned-category promotion accuracy.

Metrics turn the system from a signal display into a model that can be evaluated and improved.

### H. Production Readiness

Strengthen production behavior through:

- structured logging,
- monitoring,
- error handling,
- source diagnostics,
- uptime strategy,
- automated tests,
- CI checks,
- dependency hygiene.

This is necessary before relying on Open Signals as a long-running operational intelligence service.

## 8. Recommended Next 5 Tasks

1. **Add durable storage manager**
   Strengthen runtime memory, backups, corruption recovery, and optional remote persistence.

2. **Activate one real public data source**
   Start with Google Trends/SerpAPI, public news, or an official indicator source to move beyond fallback evidence.

3. **Add real county GeoJSON boundary support**
   Prepare the system for county-level maps, spread detection, and geospatial validation.

4. **Add analyst feedback/validation console**
   Allow trusted analysts to confirm, reject, correct, and annotate signals.

5. **Add evaluation metrics dashboard or backend report**
   Track precision, false positives, source reliability, outcome confirmation, forecast accuracy, and county detection accuracy.

## 9. Technical Debt

Current technical debt to address:

- Remove obsolete labels/functions left from earlier dashboard prototypes.
- Consolidate duplicated signal rendering logic.
- Centralize dropdown options consistently across UI, tests, and backend helpers.
- Centralize the category registry and category learning rules.
- Ensure output folders and runtime memory files are consistently ignored where needed.
- Add pytest to requirements or a development requirements file.
- Separate public UI functions from backend learning side effects where useful.
- Continue tightening text encoding hygiene for cross-platform Windows/Git workflows.

## 10. Implementation Notes For Future Codex Sessions

Future work should follow these rules:

- Do not redesign the UI unless explicitly requested.
- Preserve Signal CGE and avoid touching it during Open Signals tasks unless import compatibility requires it.
- Preserve the privacy-first design.
- Avoid exposing raw behavioral data in the public UI.
- Do not expose raw likes, comments, searches, private messages, identities, device IDs, or exact personal locations.
- Keep all sensitive credentials in environment variables or deployment secrets.
- Prefer deterministic, lightweight, repo-safe improvements unless a heavier dependency is explicitly approved.
- Keep Open Signals focused on aggregate behavioral-economic intelligence: demand, affordability, stress, opportunity, geography, validation, and forward-looking insight.
