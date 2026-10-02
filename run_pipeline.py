# learned about this in summer research program
# used Google to research more about run pipelines and create one for this project

import subprocess
import sys

def run_pipeline():
    pipeline_steps = [
            "tokenization.py",
            "vectorization.py",
            "tf_idf.py"
        ]
