from setuptools import setup, find_packages

# Function to read dependencies from requirements.txt
def get_requirements(filename):
    """Reads requirements file and returns a list of non-empty, stripped lines. Used to populate install_requires dynamically."""
    try:
        with open(filename, 'r') as file:
            requirements = file.readlines()
            # Strip whitespace and ignore empty lines
        return [req.strip() for req in requirements if req.strip()]
    
    except FileNotFoundError: # If the file is not found, return an empty list
        print(f"Warning: '{filename}' not found")  
        return []
    except Exception as e: # Handle other (global) exceptions
        print(f"Error reading {filename}: {e}")  
        return []

# Call setup() and install the packages
setup(
    name="GenAI-IRS",           # Package name
    version="0.1.0",            # Version number
    author="Pranav Harke",      
    author_email="harkep20@outlook.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
