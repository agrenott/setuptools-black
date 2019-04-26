Custom setuptools command for black formatting tool (see https://github.com/ambv/black).

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