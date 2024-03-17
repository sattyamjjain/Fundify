import os
import subprocess

os.chdir(os.path.dirname(__file__))

subprocess.run(["python3", "store/subscriber/subscriber.py"])
