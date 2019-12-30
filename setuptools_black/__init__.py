"""Custom setuptools command to wrap black formatter."""

from setuptools_black.setuptools_command import BuildCommand, FormatCommand

__all__ = ["BuildCommand", "FormatCommand"]
