import os
import shutil
import subprocess
from pathlib import Path

def check_dependencies():
    dependencies = ['prodigal', 'hmmsearch']
    for dep in dependencies:
        if not shutil.which(dep):
            raise RuntimeError(f"{dep} is not installed or not in your PATH.")

def create_directory(directory):
    """Create a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_command(command):
    """Run a command and check for errors."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(command)}") from e
