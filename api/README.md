# API

FastAPI application for serving Signal preference predictions.

Main module:

```text
api.main:app
```

Endpoints:

- `GET /health`
- `POST /predict`
- `POST /predict/batch`
- `POST /export/cge-sam`
- `POST /train`
- `GET /market-intelligence/dashboard`
- `GET /market-intelligence/evaluation`
- `POST /market-intelligence/retrain`
- `GET /dashboard`

Prediction responses include interpretable drivers, policy signal labels,
CGE/SAM account mapping, centered shock values, and publication notes.

Market intelligence endpoints train from anonymized
country/county/category/consumer-segment/time-period behavioral signals and
expose revealed demand, opportunities, model versioning, drift/retraining logs,
competitor gaps, price/service/delivery gaps, market-entry strategy, and
supplier/logistics/payment recommendations.
