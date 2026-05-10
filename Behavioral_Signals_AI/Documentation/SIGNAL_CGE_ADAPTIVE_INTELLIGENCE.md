# Signal CGE Adaptive Intelligence

Signal CGE now includes a deterministic repo-aware intelligence layer. It reads canonical model profiles, reference documentation, equation notes, calibration workflows, closure notes, experiment workflows, diagnostics guidance, and prior simulation metadata.

The adaptive layer improves:

- scenario interpretation,
- scenario-specific knowledge retrieval,
- policy caveats,
- recommended follow-up simulations,
- model-gap detection,
- future solver planning.

Current outputs remain prototype directional indicators. The active backend is still the SAM multiplier/prototype calibration pathway, not a full equilibrium CGE solver.

## Main Components

- `signal_cge/knowledge/document_loader.py`: loads repo knowledge sources.
- `signal_cge/knowledge/reference_index.py`: indexes documents and categories.
- `signal_cge/knowledge/scenario_context.py`: retrieves scenario-specific references.
- `signal_cge/knowledge/semantic_mapping.py`: maps prompt terms to scenario hints.
- `signal_cge/knowledge/knowledge_graph.py`: builds a lightweight topic graph.
- `signal_cge/learning/simulation_memory.py`: stores metadata-only learning events.
- `signal_cge/learning/scenario_pattern_learning.py`: summarizes repeated prompt patterns.
- `signal_cge/learning/model_gap_detector.py`: reports missing mappings, closures, solver gaps, and repeated fallback usage.
- `signal_cge/learning/recommendation_engine.py`: proposes next simulations.

## Safety

The system may recommend improvements but does not rewrite equations, closures, calibration formulas, or solver core without developer review.
