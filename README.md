# MLOps Task

## Overview
This project implements a minimal reporducable MLOps pipeline for a stock market analysis task.

- YAML config-driven execution
- Deterministic results through seeding
- Logging and error handling
- Dockerized environment

## Local Run

```bash
pip install -r requirements.txt
python run.py --input data/input.csv --config config.yaml --output metrics.json --log-file run.log
```

## Docker Run

```bash
docker build -t mlops-task .
docker run --rm -v $(pwd):/app mlops-task
```

## Output

```json
{
  "version": "v1",
  "rows_processed": 100,
  "metric": "signal_rate",
  "value": 0.5,
  "latency_ms": 100,
  "seed": 42,
  "status": "success"
}
```

## Error Output

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Input CSV not found"
}
```
