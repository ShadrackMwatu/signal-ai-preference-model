# Behavioral Signals AI Live Trend Intelligence

Live Trend Intelligence converts public, aggregate trend feeds into demand, shortage, price-pressure, public-concern, and market-opportunity signals for the Behavioral Signals AI dashboard.

## Supported Sources

Signal supports a provider router with the following priority when `SIGNAL_TRENDS_MODE=auto`:

1. X aggregate trends, when `X_BEARER_TOKEN` is configured.
2. Google Trends compatible feeds, when `GOOGLE_TRENDS_API_KEY`, `SERPAPI_API_KEY`, or `APIFY_API_TOKEN` plus `APIFY_TRENDS_ENDPOINT` is configured.
3. Demo fallback aggregate trends when credentials are missing or a provider is unavailable.

The dashboard never requires live credentials to start. Hugging Face Spaces should store credentials as Secrets, not in GitHub.

## Environment Variables

- `SIGNAL_TRENDS_MODE=auto|demo|x|google|serpapi|apify`
- `X_BEARER_TOKEN`
- `GOOGLE_TRENDS_API_KEY`
- `SERPAPI_API_KEY`
- `APIFY_API_TOKEN`
- `APIFY_TRENDS_ENDPOINT` for a user-configured Apify aggregate trend endpoint

## Standard Trend Record

Every provider returns records with this normalized schema:

- `trend_name`
- `platform`
- `location`
- `volume`
- `growth_indicator`
- `category`
- `timestamp`
- `confidence`
- `relevance_to_demand`
- `possible_policy_or_business_implication`

The app also preserves compatibility fields such as `source`, `rank`, `tweet_volume`, and `fetched_at` for existing dashboard logic.

## Privacy Rules

Signal uses public aggregate trend data only. It must not collect, store, or display individual user profiles, usernames, user IDs, private messages, personal timelines, email addresses, phone numbers, or raw post text. Provider records are normalized and checked before they enter the dashboard.

## Dashboard Behavior

The Live Trend Intelligence panel shows:

- source label: X, Google Trends, Apify, or Demo fallback;
- last updated timestamp;
- active trend count;
- trend cards and table records;
- category and policy/business implication for each trend;
- a summary of what trends may imply for demand, prices, shortages, public concern, or market opportunity.

If live credentials are absent or a provider call fails, Signal displays demo aggregate trends and a source note explaining the fallback.

## Deployment Notes

No API tokens should be committed to GitHub. Configure live keys through Hugging Face Secrets or local environment variables. The app remains compatible with Hugging Face because all live providers are optional and use only the Python standard library.