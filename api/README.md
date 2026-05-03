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

Prediction responses include interpretable drivers, policy signal labels,
CGE/SAM account mapping, centered shock values, and publication notes.
