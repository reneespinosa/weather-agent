import subprocess
import webbrowser
import time
import os
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=env_path)

process = subprocess.Popen(['adk', 'web'], cwd=script_dir)

time.sleep(7)

webbrowser.open('http://localhost:8000')

process.wait()