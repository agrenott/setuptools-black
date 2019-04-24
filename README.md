Custom setuptools command for black formatting tool (see https://github.com/ambv/black).

This package adds the `format` command to setuptools, which uses black to reformat code:

```bash
> python setup.py format
running format
All done! ✨ 🍰 ✨
5 files left unchanged
```


You may also use customize the `build_py` command to enforce format validation at build time.
In your setup.py:
```python
import setuptools_black
...
setuptools.setup(
...
    setup_requires=["setuptools-black"],
...
    cmdclass={
        "build_py": setuptools_black.BuildCommand,
    },
...
)
```