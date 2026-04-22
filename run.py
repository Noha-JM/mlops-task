import argparse
import yaml
import pandas as pd
import numpy as np
import json
import sys
import csv
from pathlib import Path
import logging
import time

#log file

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


#write metrics
def write_metrics(output_path,data):
    with open(output_path,"W")as f:
        json.dump(data,f,indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",required= True)
    parser.add_argument("--config",required=True)
    parser.add_arguement("--output",required= True)
    parser.add_argument("--log-file",required = True)
    args = parser.parse_args()

    start_time = time.time()
    setup_logging(args.log_file)

    logging.info("Starting training")

    try:
        #load data
        if not Path(args.config).exists():
            raise FileNotFoundError("Config file not found")
    
        with open(args.config,"r") as f:
            config = yaml.safe_load(f)
        if not isinstance(config,dict):
            raise ValueError("Invalid config format")

        required_keys = ["seed","window","version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required key: {key}")
        
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        if not isinstance(ssed,int):
            raise ValueError("seed must be an integer")
        if not isinstance(window,int) or window<=0:
            raise ValueError("window must be a positive integer")
        
        np.random.seed(seed)

        logging.info(f"Config validate: seed={seed},window={window},version={version}")
        
        #load data
        if not Path(args.imput).exists():
            raise FileNotFoundError("Input CSV not found")

        try:
            df = pd.read_csv(
                args.input,
                sep = ",",
                quoting=csv.QUOTE_NONE,
                engine = "python"
            )
        except Exception:
            raise ValueError("Invalid CSV format")

        if df.empty:
            raise ValueError("Input CSV is empty")
        
        df.columns = df.columns.str.strip().str.lower()

        logging.info(f"Columns detected: {list(df.colums)}")

        if "close" not in df.columns:
            raise ValueError("Missing 'close' column")
        
        logging.info(f"Rows loaded: {len(df)}")

        #rolling mean

        df["rolling_mean"] = df['close'].rolling(window=window).mean()

        logging.info("Rolling mean computed")

        #signal generation

        df['signal'] = np.where(
            df['close']>df['rolling_mean'],1,0
        )

        #removing NaN
        valid_mask = df['rolling_mean'].notna()
        valid_signals = df.loc[valid_mask,'signal']

        if len(valid_signals) == 0:
            raise ValueError("No valid rows after rolling window")
        
        signal_rate = valid_signals.mean()
        logging.info(f"Signal generated on {len(valid_signals)}")

        #metrics
        latency_ms = int((time.time() - start_time)*1000)

        metrics = {
            "version":version,
            "rows_processed":int(len(df)),
            "metric": "signal_rate",
            "value": round(float(signal_rate),4),
            "latency_ms":latency_ms,
            "seed":seed,
            "status":"success"
        }


        write_metrics(args.output,metrics)
        
        logging.info(f"Metrics:{metrics}")
        logging.info("Success")

        print(json.dumps(metrics,indent=2))
        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time)*1000)

        error_metrics = {
            "version":version,
            "status":'error',
            "error_message": str(e)
        }

        write_metrics(args.output,error_metrics)

        logging.info(f"Error: {str(e)}")
        logging.info("Failed")
        
        print(json.dumps(error_metrics,indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()