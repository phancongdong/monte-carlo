import re
from pathlib import Path

from setuptools import setup, find_packages

DESCRIPTION = "A quantitative trading and Monte Carlo simulation framework"
BASE_DIR = Path(__file__).resolve().parent

# The version lives only in montecarlo/version.py. It is read as text because importing the package
# would import dependencies during the build.
_version_match = re.search(
    r"^__version__\s*=\s*['\"]([^'\"]+)['\"]",
    (BASE_DIR / 'montecarlo' / "version.py").read_text(encoding="utf-8"),
    re.MULTILINE,
)
if not _version_match:
    raise RuntimeError("Could not find __version__ in montecarlo/version.py")
VERSION = _version_match.group(1)

with open(BASE_DIR / "requirements.txt", "r", encoding="utf-8") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

with open(BASE_DIR / "README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='montecarlo-framework',
    version=VERSION,
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=REQUIRED_PACKAGES,
    entry_points='''
        [console_scripts]
        montecarlo=montecarlo.cli:cli
        mc=montecarlo.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    include_package_data=True,
    package_data={
        '': ['*.dll', '*.dylib', '*.so', '*.json'],
    },
)
