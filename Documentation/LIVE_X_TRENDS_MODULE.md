# Live X Trends Module

## Purpose

Signal's Live Trends module extends the existing dashboard with public aggregate X/Twitter trend intelligence. It helps teams scan high-level public topic momentum and translate those signals into Signal's demand, opportunity, emerging-trend, and unmet-demand views.

This module is designed for:

- market scanning
- policy watching
- opportunity discovery
- early signal monitoring

It does not track or profile individuals.

## Architecture

The Live Trends workflow is:

1. `x_trends.py` loads location settings from `config/locations.json`
2. Signal reads credentials from environment variables only
3. Signal fetches public aggregate trends when `X_BEARER_TOKEN` is available
4. If the API is unavailable, Signal returns safe demo fallback trends
5. `trend_intelligence.py` converts each trend into proxy Signal inputs
6. Signal reuses the existing AI demand engine to generate intelligence outputs
7. `app.py` displays:
   - raw trends
   - trend intelligence
   - an interpretation summary

## X API Credential Setup

Signal reads X credentials from environment variables only:

- `X_BEARER_TOKEN`
- `X_API_KEY`
- `X_API_SECRET`

The current module uses `X_BEARER_TOKEN` as the primary credential. No secrets are committed to the repository.

## Hugging Face Spaces Secret Setup

To enable live trend fetching in Hugging Face Spaces:

1. Open the Space settings page
2. Go to `Settings -> Variables and secrets`
3. Choose `New secret`
4. Add:

```text
X_BEARER_TOKEN
```

Paste the X bearer token as the value and save it.

If the secret is not present, Signal stays operational and uses demo fallback trends.

## Privacy Safeguards

Signal only uses:

- aggregate trends
- topic-level signals
- location-level public indicators
- time-level signals

Signal does not store:

- usernames
- user IDs
- private messages
- individual profiles
- personal timelines

The privacy helpers in `privacy.py` strip blocked fields from incoming records before the records are used.

## Fallback Mode

If the X API credential is missing or the request fails, Signal returns demo trend records labeled:

```text
Demo fallback - X API not connected
```

This keeps the Hugging Face dashboard stable and lets users test the full trend-to-intelligence flow without live credentials.

## How Trends Become Signal Intelligence

Trend records typically expose only a few aggregate fields, such as:

- trend name
- rank
- tweet volume
- location
- fetch timestamp

`trend_intelligence.py` converts those records into proxy Signal inputs:

- likes
- comments
- shares
- searches
- engagement intensity
- purchase intent score
- trend growth

These are proxy estimates derived from:

- trend rank
- tweet volume where available
- freshness
- location relevance

Signal then passes those inputs into the existing ML prediction pipeline. The result includes:

- demand classification
- confidence score
- aggregate demand score
- opportunity score
- emerging trend probability
- unmet demand probability
- investment or policy interpretation
- model source and explanation

## Limitations

- Trend-based inference is indirect and uses proxy inputs
- Trend names alone do not reveal true market demand
- Tweet volume may be unavailable for some trends
- Live X endpoints and policies may change over time
- This module should be treated as directional intelligence, not a substitute for full market validation

## Testing

Run the main verification commands locally:

```powershell
python -c "import app; print('app import OK')"
python -c "import x_trends; print('x_trends import OK')"
python -c "import trend_intelligence; print('trend_intelligence import OK')"
python -m pytest
```

## Deployment Notes

- Keep `app.py` at the repository root for Hugging Face Spaces
- Keep `requirements.txt` at the repository root
- Do not hard-code X credentials
- The dashboard remains deployable even when the X API is disconnected because fallback trends are built in
