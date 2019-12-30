"""Integration of black tool with Setuptools."""

import distutils.errors
import os
import subprocess
import sys

from distutils.command.build import build as _build
import setuptools
import setuptools.command.build_py
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

    def distribution_files(self):
        """Collect package and module files."""
        build_py = self.get_finalized_command("build_py")
        for package in self.distribution.packages or []:
            # Get the proper package dir when package_dir is used
            yield build_py.get_package_dir(package)

        for additional_file in ["setup.py", "tests"]:
            if os.path.exists(additional_file):
                yield additional_file

    def run(self):
        """Call black using subprocess module."""
        # Sources to format (include setup.py and tests if it exists)
        sources = set(self.distribution_files())
        params = sorted(sources)

        try:
            # Sadly, setup_requires only get eggs, not a proper install
            env = os.environ
            sep = os.path.sep
            python_path = ":".join(
                [
                    path
                    for path in pkg_resources.working_set.entries
                    if f"{sep}.eggs{sep}" in path
                ]
            )
            env.update({"PYTHONPATH": python_path})

            if self.check:
                params.insert(0, "--check")
            subprocess.run(
                [sys.executable, "-m", "black"] + params, check=True, env=env,
            )
        except subprocess.CalledProcessError:
            # Raise exception on formatting error
            raise distutils.errors.DistutilsError(
                f"Invalid format, please run 'python setup.py format'"
            )


class BuildCommand(_build):
    """Customized build command, checking code formatting before build"""

    def run(self):
        """Check format, then build."""
        self.distribution.get_command_obj("format").check = True
        self.run_command("format")
        return _build.run(self)
