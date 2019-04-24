Custom setuptools command for black formatting tool (see https://github.com/ambv/black).

This package enforces code formatting validation using black at build time, by overriding the `build_py` setup command.
Build will fail if there's any formatting error.

In your setup.py:
```python
...
setuptools.setup(
...
    setup_requires=["setuptools-black"],
...
)
```

It also adds the `format` command to setuptools, which uses black to reformat code:

```bash
> python setup.py format
running format
All done! ✨ 🍰 ✨
5 files left unchanged
```

