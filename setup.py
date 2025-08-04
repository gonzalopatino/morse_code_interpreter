# setup.py
from setuptools import setup, find_packages

setup(
    name="morse_code_interpreter",
    version="0.1",
    description="Morse code GPIO interpreter for Raspberry Pi",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
)
