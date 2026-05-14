# Behavioral Signals AI Data Provider Strategy

Behavioral Signals AI is an AI-native economic sensing infrastructure, not a social media dashboard. Its provider layer combines aggregate/public signals from multiple classes and converts them into revealed preferences, revealed aggregate demand, unmet demand, economic pressure, market opportunities, and recommended actions.

## Phase 1 Provider Priority

1. **Search trends**: Google Trends-compatible providers, SerpAPI, and optional pytrends. Search is prioritized because people search for what they need, compare, cannot find, or plan to buy.
2. **X aggregate trends**: real-time national public concern and conversation intensity.
3. **News/public information**: GDELT and News API context for economic pressure, shortages, public-service demand, and supply disruptions.
4. **Demo fallback**: deterministic aggregate records when live credentials are absent.

## Standard Aggregate Signal Schema

```json
{
  "signal_name": "",
  "source": "",
  "provider_type": "",
  "category": "",
  "location": "Kenya",
  "timestamp": "",
  "volume": null,
  "growth": null,
  "sentiment": null,
  "engagement_velocity": null,
  "demand_relevance": null,
  "confidence": null,
  "privacy_level": "aggregate_public"
}
```

## Provider Classes

- `providers/search/`: Google Trends, SerpAPI, optional pytrends, and future API partners.
- `providers/social/`: X now; TikTok, YouTube, and Instagram as future aggregate API integrations.
- `providers/news/`: GDELT, News API, and RSS public information feeds.
- `providers/marketplace/`: Jumia and e-commerce price signals for later-stage product and price intelligence.
- `providers/mobility/`: Google Maps style aggregate service-demand indicators.
- `providers/fintech/`: formal partnership-only aggregate liquidity and spending indicators.
- `providers/appstore/`: app demand, digital-service, education, fintech, and delivery demand signals.

## Routing Logic

The provider router checks `SIGNAL_TRENDS_MODE`, active environment variables, and optional provider availability. It tries Phase 1 providers in priority order, normalizes all records, deduplicates overlapping topics, ranks by demand relevance/confidence/volume, and falls back to demo records if no live source works.

Dashboard provider details remain simple: **Live Kenya signals** or **Demo fallback**. Diagnostics stay in backend/provider health checks rather than the public decision layer.

## Environment Variables

- `SIGNAL_TRENDS_MODE=auto|demo|google|serpapi|pytrends|x|gdelt|news`
- `GOOGLE_TRENDS_API_KEY`
- `SERPAPI_API_KEY`
- `X_BEARER_TOKEN`
- `NEWS_API_KEY`
- `APIFY_API_TOKEN`
- `SIGNAL_ENABLE_GDELT=1` for public GDELT context

Future provider variables include `YOUTUBE_API_KEY`, `TIKTOK_API_KEY`, `INSTAGRAM_ACCESS_TOKEN`, `JUMIA_API_KEY`, `GOOGLE_MAPS_API_KEY`, and formal partnership-specific keys.

## Privacy Rules

Signal accepts aggregate/public signals only. It must not collect usernames, user IDs, raw posts, personal profiles, private messages, personal timelines, emails, phone numbers, or individual-level targeting data.