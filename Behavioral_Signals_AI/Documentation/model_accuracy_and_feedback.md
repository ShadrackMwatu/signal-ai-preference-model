# Model Accuracy and Feedback

Behavioral Signals AI evaluates predictions by comparing earlier aggregate demand forecasts with later aggregate signal strength. Accuracy is tracked at the signal/category level and used to calibrate future predictions.

## Evaluation Concepts

- **Pending**: no follow-up aggregate signal has been recorded yet.
- **Accurate**: predicted demand is close to follow-up signal strength.
- **Directionally useful**: prediction is not exact but still close enough to inform monitoring.
- **Missed**: prediction diverges from later aggregate signal evidence.

## Backtesting

The `evaluation/` package can backtest prediction memory and compute aggregate metrics such as prediction count, evaluated predictions, average accuracy, and pending predictions.

## Feedback

Feedback is aggregate-only. It can be entered as follow-up signal strength for a topic or category. It must not contain individual-level information.