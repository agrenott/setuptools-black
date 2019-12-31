![PyPI](https://img.shields.io/pypi/v/setuptools-black)
![PyPI - Status](https://img.shields.io/pypi/status/setuptools-black)
![PyPI - License](https://img.shields.io/pypi/l/setuptools-black)
![PyPI - Downloads](https://img.shields.io/pypi/dm/setuptools-black)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Build Status](https://travis-ci.com/agrenott/setuptools-black.svg?branch=master)](https://travis-ci.com/agrenott/setuptools-black)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/agrenott/setuptools-black/Python%20package) 
[![Coverage Status](https://coveralls.io/repos/github/agrenott/setuptools-black/badge.svg?branch=master)](https://coveralls.io/github/agrenott/setuptools-black?branch=master)
[![codecov](https://codecov.io/gh/agrenott/setuptools-black/branch/master/graph/badge.svg)](https://codecov.io/gh/agrenott/setuptools-black)
[![Maintainability](https://api.codeclimate.com/v1/badges/b1466b35e85d71825773/maintainability)](https://codeclimate.com/github/agrenott/setuptools-black/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f730201447c24dac81f3ef8a222fd868)](https://www.codacy.com/manual/agrenott/setuptools-black?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=agrenott/setuptools-black&amp;utm_campaign=Badge_Grade)

Custom setuptools command for black formatting tool (see <https://github.com/ambv/black>).

This package adds the `format` command to setuptools, which uses black to reformat code:

```bash
> python setup.py format
running format
All done! ✨ 🍰 ✨
5 files left unchanged
```

You may also use customize the `build` command to enforce format validation at build time.
Build will fail if there's any formatting error.

In your setup.py:
```python
import setuptools_black
...
setuptools.setup(
...
    cmdclass={
        "build": setuptools_black.BuildCommand,
    },
...
)
```

**Note**

You'll have to install setuptools-black first, as setup_requires can't be used to install a package which must be imported by setup.py itself...