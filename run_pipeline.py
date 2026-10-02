# learned about this in summer research program
# used Google to research more about run pipelines and create one for this project

import subprocess
import sys

def run_pipeline():
    pipeline = [
            "parsing.py",
            "vectorization.py",
            "tf_idf.py"
        ]

    for step in pipeline:
        print(f"Running {step}")

        result = subprocess.run([sys.executable, step], capture_output=True,text=True)

        if result.returncode == 0:
            print(f"Success\n")

            if result.stdout.strip():
                print(result.stdout)

        else:
            print(f"Error occurred in {step}")
            print(result.stderr)
            sys.exit(result.returncode)

if __name__ == "__main__":
    run_pipeline()
