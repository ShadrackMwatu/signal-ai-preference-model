"""Prompt templates for aggregate Behavioral Signals AI interpretation."""

SYSTEM_INSTRUCTION = (
    "You are analyzing aggregate behavioral signals for Kenya. Do not infer individual identity. "
    "Do not profile individuals. Interpret only aggregate public or authorized data. "
    "Produce concise economic, policy, and market intelligence."
)

SIGNAL_INTERPRETATION_TEMPLATE = (
    SYSTEM_INSTRUCTION
    + "\nReturn JSON with: plain_language_meaning, economic_interpretation, "
    "opportunity_interpretation, policy_implication, recommended_action, risk_note."
)

STRATEGIC_SUMMARY_TEMPLATE = (
    SYSTEM_INSTRUCTION
    + "\nSummarize the current aggregate signal set with: main issue emerging, strongest opportunity, "
    "highest policy concern, counties affected, sectors affected, and what to monitor next."
)

SEMANTIC_CLUSTER_TEMPLATE = (
    SYSTEM_INSTRUCTION
    + "\nGroup related aggregate signal topics into concise economic themes without using private data."
)