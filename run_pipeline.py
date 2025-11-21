import subprocess
import logging
import sys
import os

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_script(script_name):
    try:
        logging.info(f"Running: {script_name}")
        result = subprocess.run(["python", script_name], capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"{script_name} FAILED:\n{result.stderr}")
            print(result.stderr)
        else:
            logging.info(f"{script_name} completed successfully")
            print(result.stdout)

    except Exception as e:
        logging.error(f"Error running {script_name}: {e}")
        print(f"Error running {script_name}: {e}")

def main():

    print("starting full ETL + Analytics pipeline...\n")
    logging.info("pipeline execution started")
    run_script("data_extract\firestore_export.py")
    run_script("data_transform\transform_to_csv.py")
    run_script("data_validation\validator.py")
    run_script("analytics\analytics.py")

    logging.info("Ppipeline execution completed")
    print("\n Pipeline Completed Successfully! Check analytics folder for results.")

if __name__ == "__main__":
    main()
