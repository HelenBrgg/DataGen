from pathlib import Path
import os
from setuptools import setup, find_packages

HERE = Path(os.path.dirname(__file__)).absolute()
VERSION: str = "0.0.1"  # noqa
README = (HERE / "README.md").read_text(encoding="UTF-8")
DOC_NAME = "DataGen"
PYTHON_NAME = "dataGen"
with open(HERE / "requirements.txt") as fh:
    REQUIRED = fh.read().splitlines()

setup(
    name=PYTHON_NAME,
    version=VERSION,
    description="A datagenerator for dynamic time series",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Helen Brüggmann",
    author_email="brueggmh@students.uni-marburg.de",
    url="https://github.com/HelenBrgg/DataGen",
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    package_data={"dataGen": ["py.typed", "config/schema/*"]},
    install_requires=REQUIRED,
    python_requires=">=3.7",
    test_suite="test",

    zip_safe=False,

    entry_points={
        "console_scripts": [
            "dataGen=dataGen.__main__"
        ]
    }
)
