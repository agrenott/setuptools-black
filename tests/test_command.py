"""FormatCommand unit tests."""

import os
import subprocess
import sys
import pytest
from setuptools import Distribution, find_packages
from unittest import mock
from setuptools_black import BuildCommand, FormatCommand
import distutils
import setuptools_black


TEST_PATH = os.path.abspath(os.path.dirname(__file__))


class TestFormatCommand:
    @staticmethod
    @mock.patch("subprocess.run")
    def test_run(run_mock: mock.Mock):
        """
        Test basic usage, only relying on find_packages to fill setup packages,
        with no setup.py nor tests.
        """
        dist = Distribution()
        os.chdir(TEST_PATH)
        dist.packages = find_packages("data")
        FormatCommand(dist).run()

        run_mock.assert_called_with(
            [sys.executable, "-m", "black", "fake_package"],
            check=True,
            env={"PYTHONPATH": ""},
        )

    @staticmethod
    @mock.patch("subprocess.run")
    def test_run_check(run_mock: mock.Mock):
        """
        Test check-only run.
        """
        dist = Distribution()
        os.chdir(TEST_PATH)
        dist.packages = find_packages("data")
        command = FormatCommand(dist)
        command.check = True
        command.run()

        run_mock.assert_called_with(
            [sys.executable, "-m", "black", "--check", "fake_package"],
            check=True,
            env={"PYTHONPATH": ""},
        )

    @staticmethod
    @mock.patch("subprocess.run")
    def test_run_additional_files(run_mock: mock.Mock):
        """
        Test setup.py and tests discovery.
        """
        dist = Distribution()
        os.chdir(os.path.join(TEST_PATH, ".."))
        dist.packages = find_packages()
        FormatCommand(dist).run()

        run_mock.assert_called_with(
            [sys.executable, "-m", "black", "setup.py", "setuptools_black", "tests"],
            check=True,
            env={"PYTHONPATH": ""},
        )

    @staticmethod
    @mock.patch("subprocess.run")
    def test_run_invalid_format(run_mock: mock.Mock):
        """Simulate error return from black on invalid format."""
        dist = Distribution()
        run_mock.side_effect = subprocess.CalledProcessError(returncode=1, cmd="black")
        with pytest.raises(distutils.errors.DistutilsError):
            FormatCommand(dist).run()


class TestBuildCommand:
    """Test overridden build command."""

    @staticmethod
    @mock.patch("setuptools_black.setuptools_command._build")
    @mock.patch("setuptools_black.setuptools_command.FormatCommand")
    def test_run(format_mock: mock.Mock, build_mock: mock.Mock):
        """Ensure both format and normal build are called in sequence."""
        dist = Distribution()
        # Simulate setup.py registration
        dist.cmdclass = {
            "format": setuptools_black.setuptools_command.FormatCommand,
        }
        build_command = BuildCommand(dist)
        build_command.run()
        # Format run once, in check-only mode
        format_mock.return_value.run.assert_called_once_with()
        assert format_mock.return_value.check is True
        # Build run once, in check-only mode
        build_mock.run.assert_called_once_with(build_command)
