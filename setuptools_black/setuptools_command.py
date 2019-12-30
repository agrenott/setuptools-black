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

    def run(self):
        # Sources to format (include setup.py and tests if it exists)
        sources = set(self.distribution.packages or [])
        if os.path.exists("setup.py"):
            sources.add("setup.py")
        if os.path.isdir("tests"):
            sources.add("tests")
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
        self.distribution.get_command_obj("format").check = True
        self.run_command("format")
        return _build.run(self)
