import shutil
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed and in the PATH."""
    dependencies = ['prodigal', 'hmmsearch']
    missing_deps = []
    for dep in dependencies:
        if not shutil.which(dep):
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"Error: The following required dependencies are not installed or not in your PATH: {', '.join(missing_deps)}")
        print("Please install these tools and ensure they are in your PATH before running the program.")
        sys.exit(1)  # Exit the program with an error code
    else:
        print("All required dependencies are installed and in the PATH.")

def create_directory(directory):
    """Create a directory if it does not exist."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)

def run_command(command):
    """Run a command and check for errors."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Command executed successfully: {' '.join(command)}")
        print(f"Output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}")
        print(f"Error output: {e.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(command)}") from e
