"""Integration of black tool with Setuptools."""

import distutils.errors
import os
import subprocess
import sys

import setuptools
from distutils.command.build import build as _build
import pkg_resources


class FormatCommand(setuptools.Command):
    """Custom command to format python code using black"""

    description = "Format code using black"

    user_options = [("check", "c", "check only")]

    boolean_options = ["check"]

    def initialize_options(self):
        self.check = None

    def finalize_options(self):
        pass

    def package_files(self):
        """Collect the files/dirs included in the registered modules."""
        seen_package_directories = ()
        directories = self.distribution.package_dir or {}
        empty_directory_exists = '' in directories
        packages = self.distribution.packages or []
        for package in packages:
            package_directory = package
            if package in directories:
                package_directory = directories[package]
            elif empty_directory_exists:
                package_directory = os.path.join(directories[''],
                                                 package_directory)

            if package_directory.startswith(seen_package_directories):
                continue

            seen_package_directories += (package_directory + '.',)
            yield package_directory

    def distribution_files(self):
        """Collect package and module files."""
        for package in self.package_files():
            yield package

        yield 'setup.py'

    def run(self):
        # Sources to format (include setup.py and tests if it exists)
        sources = list(self.distribution_files())
        if os.path.isdir("tests"):
            sources += ["tests"]
        try:
            # Sadly, setup_requires only get eggs, not a proper install
            python_path = ":".join(
                [x for x in pkg_resources.working_set.entries if "/.eggs/" in x]
            )
            if self.check:
                sources.insert(0, "--check")
            subprocess.run(
                [sys.executable, "-m", "black"] + sources,
                check=True,
                env={"PYTHONPATH": python_path},
            )
        except subprocess.CalledProcessError:
            # Raise exception on formatting error
            raise distutils.errors.DistutilsError(
                f"Invalid format, please run 'python setup.py format'"
            )


class BuildCommand(_build):
    """Customized build command, checking code formatting before build"""

    def run(self):
        self.distribution.get_command_obj("format").check = True
        self.run_command("format")
        return _build.run(self)
