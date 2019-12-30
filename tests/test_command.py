"""FormatCommand unit tests."""

import contextlib
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


@contextlib.contextmanager
def change_dir(new_dir):
    """Change directory to new_dir, and restore afterwards."""
    curdir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(curdir)


class TestFormatCommand:
    @staticmethod
    @mock.patch("subprocess.run")
    def test_run(run_mock: mock.Mock):
        """
        Test basic usage, only relying on find_packages to fill setup packages,
        with no setup.py nor tests.
        """
        dist = Distribution()
        # Switch to fake project's root
        with change_dir(TEST_PATH):
            dist.packages = find_packages("data")
            FormatCommand(dist).run()

        run_mock.assert_called_with(
            [sys.executable, "-m", "black", "fake_package"], check=True, env=mock.ANY,
        )

    @staticmethod
    @mock.patch("subprocess.run")
    @mock.patch("setuptools_black.setuptools_command.pkg_resources")
    def test_run_eggs(pkg_resources_mock: mock.Mock, run_mock: mock.Mock):
        """Test .eggs are added to PYTHONPATH when calling black."""
        # Mock setup behavior for installed egg
        pkg_resources_mock.working_set.entries = [
            os.path.join(os.getcwd(), ".eggs", "fake_black.egg")
        ]
        dist = Distribution()
        FormatCommand(dist).run()

        # Ensure .eggs paths are added to PYTHONPATH
        path = run_mock.call_args[1]["env"]["PYTHONPATH"]
        assert os.path.join(".eggs", "fake_black.egg") in path

    @staticmethod
    @mock.patch("subprocess.run")
    def test_run_check(run_mock: mock.Mock):
        """
        Test check-only run.
        """
        dist = Distribution()
        with change_dir(TEST_PATH):
            dist.packages = find_packages("data")
            command = FormatCommand(dist)
            command.check = True
            command.run()

        run_mock.assert_called_with(
            [sys.executable, "-m", "black", "--check", "fake_package"],
            check=True,
            env=mock.ANY,
        )

    @staticmethod
    def test_distribution_files_additional_files():
        """
        Test setup.py and tests discovery.
        """
        dist = Distribution()
        with change_dir(os.path.join(TEST_PATH, "..")):
            dist.packages = find_packages()
            files = FormatCommand(dist).distribution_files()

            # Ensure data is appended to fake_package
            assert set(files) == {"setup.py", "setuptools_black", "tests"}

    @staticmethod
    def test_distribution_files_package_dir():
        """
        Test packages collection when pacakge_dir is used to get packages from sub-directory.
        """
        dist = Distribution()
        with change_dir(TEST_PATH):
            dist.packages = find_packages("data")
            dist.package_dir = {"": "data"}
            files = FormatCommand(dist).distribution_files()

            # Ensure data is appended to fake_package
            assert list(files) == [os.path.join("data", "fake_package")]

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
