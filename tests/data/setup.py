"""Fake setup.py to test format plugin integration"""

from setuptools import setup, find_packages


setup(
    name="setuptools-black",
    packages=find_packages(),
    install_requires=["black>=18.9b0"],
)
