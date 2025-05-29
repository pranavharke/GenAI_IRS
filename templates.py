import os
from pathlib import Path
import logging

# This script creates a project structure with specified files and directories 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of files to be created in project structure
list_of_files = [
                    ".env",
                    "setup.py",
                    "README.md",
                    "requirements.txt",
                    "app.py",
                    "src/__init__.py",      
                    "src/helper.py", 
                    "research/trials.ipynb"   ]

# Create a project structure with the specified files
for filepath in list_of_files:
    filepath = Path(filepath)                   # Convert to Path object for better path handling
    filedir, filename = os.path.split(filepath) # Split the path into directory and filename

    # Create directories if they do not exist
    if filedir != "": 
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # Check if file does not exist or is empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0: 
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")

    else: # File already exists and is not empty
        logging.info(f"File already exists and is not empty: {filepath}")