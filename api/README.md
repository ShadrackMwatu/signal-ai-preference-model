# API

FastAPI application for serving modular Signal market intelligence.

Main module:

```text
api.app:app
```

Endpoints:

- `GET /health`
- `GET /predict-demand`
- `GET /county-demand`
- `GET /opportunities`
- `GET /segments`
- `GET /market-access`

Outputs are aggregate-only country/county/category/consumer-segment/time-period
records. The API does not expose `signal_id`, raw text, PII, or user-level data.
