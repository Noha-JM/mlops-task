# MLOps Task

## Overview

This project implements a minimal reproducible MLOps pipeline for a stock market analysis task.

* YAML config-driven execution
* Deterministic results via seeding
* Robust data validation and error handling
* Structured logging
* Dockerized for deployment

---

## Local Run

```bash
pip install -r requirements.txt

python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
```

---

## Docker Run

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

---

## Example Output (Success)

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 18,
  "seed": 42,
  "status": "success"
}
```

---

## Example Output (Error)

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Input CSV not found"
}
```

---

## Notes

* Only the `close` column is used for computation
* Rolling mean is computed using the configured window
* Initial rows (window-1) are excluded from signal calculation
* Metrics are written in both success and failure cases
