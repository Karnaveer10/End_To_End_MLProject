"""
This file turns the project into a proper Python package that others can install via pip.
CRITICAL: All 3 files work together - setup.py + requirements.txt + src/__init__.py
"""

# ========== IMPORTS SECTION ==========
# setuptools: Core library for building/distributing Python packages
# find_packages(): Automatically discovers all packages (folders with __init__.py) in project
# List: Type hint for better code readability (shows function returns list of strings)
from setuptools import find_packages, setup
from typing import List

# ========== CONSTANTS SECTION ==========
# HYPEN_E_DOT = '-e .': pip flag for "editable install" 
# Found in requirements.txt but REMOVED here because it's NOT a real external dependency
HYPEN_E_DOT = '-e .'


# ========== CORE FUNCTION: Reads requirements.txt cleanly ==========
def get_requirements(file_path: str) -> List[str]:
    """
    PURPOSE: Reads ALL dependencies from requirements.txt and returns CLEAN list for setup()
    WORKFLOW:
    requirements.txt: ["pandas\n", "numpy\n", "-e .\n"]
    → get_requirements(): ["pandas", "numpy"]  (removes newlines + "-e .")
    """
    requirements = []  
    

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        
        requirements = [req.replace("\n", "") for req in requirements]

        # CRITICAL: Remove '-e .' because it's a pip INSTALL flag, NOT a PyPI package
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    # Return CLEAN list: ['pandas', 'numpy', 'seaborn']
    return requirements


# ========== PACKAGE SETUP: Defines your project metadata ==========
setup(
    # REQUIRED: Package name (appears on PyPI, pip install ml_project)
    name='ML_Project',
    
    # SEMVER: 0.0.1 = initial development version
    version='0.0.1',
    
    # Metadata: Shows up in pip show ML_Project
    author='Karn',
    author_email='karnaveersisodia@gmail.com',
    
    # AUTO-DETECTS PACKAGES: Finds src/, utils/, etc. (ANY folder with __init__.py)
    # WITHOUT __init__.py in src/: find_packages() ignores that folder
    packages=find_packages(),
    
    # DYNAMIC DEPENDENCIES: Loads from requirements.txt (minus -e .)
    # pip install -r requirements.txt → installs pandas/numpy FIRST
    # THEN -e . runs this setup() → installs your package + its deps
    install_requires=get_requirements('requirements.txt')
)

"""
========== COMPLETE WORKFLOW SUMMARY ==========

1. requirements.txt contains:
   pandas==1.5.0
   numpy==1.24.0
   -e .  ← Installs YOUR project via setup.py

2. User runs: pip install -r requirements.txt
   → pip installs pandas, numpy
   → pip runs: pip install -e . (executes THIS setup.py)

3. setup.py execution:
   find_packages() → ['src'] (because src/__init__.py exists)
   get_requirements() → ['pandas', 'numpy']
   → Creates symlink: site-packages/ML_Project → your/src/

4. RESULT: from ML_Project.src.main import function() WORKS INSTANTLY!

========== FUTURE MAINTENANCE ==========
- Add new dep? → requirements.txt + pip install -r requirements.txt
- Code change? → Live update (no reinstall thanks to -e .)
- Release? → python setup.py sdist bdist_wheel → upload to PyPI

========== TROUBLESHOOTING ==========
❌ ImportError? → Check src/__init__.py exists
❌ Dep missing? → pip install -r requirements.txt
❌ setup.py error? → requirements.txt has no extra spaces/typos
"""
