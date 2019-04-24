"""black command for setuptools"""

from setuptools import setup, find_packages


__version__ = "0.1.2"
with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name="setuptools-black",
    version=__version__,
    description=__doc__,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["black>=18.9b0"],
    zip_safe=True,
    entry_points={
        "distutils.commands": [
            "format = setuptools_black.setuptools_command:FormatCommand",
            "build_py = setuptools_black.setuptools_command:BuildCommand",
        ]
    },
    author="Aurelien Grenotton",
    author_email="agrenott@gmail.com",
    url="https://github.com/agrenott/setuptools-black",
    license="MIT",
    keywords="black setuptools plugin",
    classifiers=[
        "Framework :: Setuptools Plugin",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
