# Learning Version v001

Change summary: Seed Signal learning system with evidence-linked recommendation mode.

Reason for change: Establish the first auditable learning version before automated adaptations are proposed.

Affected templates/rules:

- signal_learning/*
- knowledge_base/*
- signal_execution runner learning hooks

Confidence score: 0.8

Rollback instructions:

Remove or disable the learning hooks in `signal_execution/runner.py` and keep the knowledge base as documentation only.
