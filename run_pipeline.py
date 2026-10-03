# learned about this in summer research program
# used Google to research more about run pipelines and create one for this project

import os
import subprocess
import sys

os.chmod("download_texts.sh", 0o755)
subprocess.run(["./download_texts.sh"], check=True)
subprocess.run([sys.executable, "parsing.py"], check=True)
subprocess.run([sys.executable, "tf_idf.py"], check=True)
subprocess.run([sys.executable, "analysis.py"], check=True)
