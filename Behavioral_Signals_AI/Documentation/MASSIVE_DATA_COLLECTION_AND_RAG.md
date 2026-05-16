# Massive Data Collection and Retrieval-Augmented Grounding

Open Signals follows one operating principle: **Collect massive aggregate intelligence, not personal data.**

The system is designed to learn from large volumes of public, aggregate, anonymized, or user-authorized evidence while refusing person-level data. The goal is behavioral, statistical, geospatial, and economic intelligence, not surveillance.

## Source Categories

Open Signals can ingest or prepare connectors for:

- official statistics
- macroeconomic indicators
- agriculture and food-system indicators
- food price and early-warning sources
- public news and reports
- search trend aggregates
- public social metadata
- geospatial public data
- aggregate mobility or place activity indicators

## Kenya Sources

The source registry includes placeholders for KNBS, CBK, Kenya Open Data, KilimoSTAT, FEWS NET, Kenya news/public reports, and county public reports. These sources are expected to provide national, county, sector, price, agriculture, finance, or public-service context.

## Global Sources

The registry also includes World Bank Open Data, IMF Data, UN Data, FAO, Google Trends or SerpAPI, YouTube public metadata, Reddit public metadata, OpenStreetMap, weather/climate APIs, and an aggregate mobility placeholder.

## Privacy Rules

Open Signals may collect:

- topics
- categories
- counties or broad locations
- timestamps
- relative interest
- source type
- confidence
- historical recurrence
- citations or source references

Open Signals must never collect:

- personal names
- phone numbers
- emails
- device IDs
- user IDs
- individual searches
- private messages
- exact personal locations
- personal routes
- individual profiles

The ingestion privacy filter rejects records with person-level fields and redacts private-looking text before records enter retrieval.

## Normalized Record Schema

Every ingested source is normalized into:

```json
{
  "topic": "...",
  "category": "...",
  "source_name": "...",
  "source_type": "...",
  "location": "Global | Kenya | county",
  "county_name": null,
  "county_code": null,
  "timestamp": "ISO datetime",
  "relative_interest": 0,
  "observed_value": null,
  "unit": null,
  "confidence": 0,
  "summary": "...",
  "privacy_level": "aggregate",
  "raw_reference": "source URL or citation only"
}
```

## RAG Architecture

The retrieval index grounds Open Signals chat and interpretation in:

- `ingested_signal_records.json`
- `latest_live_signals.json`
- `historical_signal_memory.json`
- `outcome_learning_memory.json`
- `geospatial_signal_memory.json`
- `behavioral_intelligence_memory.json`

The chat stack retrieves relevant aggregate context before optional LLM reasoning. If evidence is missing, the system should avoid guessing and say it does not have enough current aggregate evidence.

## Adaptive Learning Loop

The learning cycle runs:

aggregate/public sources -> normalization -> privacy filtering -> retrieved evidence index -> live signal cache -> historical/outcome/geospatial memory -> evaluation metrics -> grounded chat/feed outputs

## API Activation

Real APIs should be activated only through environment variables or Hugging Face Secrets. API keys must never be hardcoded or committed. Each connector includes a placeholder and TODO note for compliant activation.

## Why Retrieval Is Better Than Blind Scraping

Retrieval grounding lets Open Signals cite and reuse structured aggregate evidence without scraping private or uncontrolled data. It improves answer quality, reduces hallucination, supports auditability, and keeps privacy rules enforceable.
