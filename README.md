[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/asottile.future-breakpoint?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=18&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/18/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=18&branchName=master)

future-breakpoint
=================

A backport of `breakpoint` to python<3.7.

## install

`pip install future-breakpoint`

## supported versions

python3+, (noop on python3.7+)

## usage

Once installed, you should be able to use `breakpoint()` in the same way as in
python3.7+.

```python
def rand():
    breakpoint()  # no need for `import pdb; pdb.set_trace()`
    return 4
```

See [PEP 553](https://www.python.org/dev/peps/pep-0553/) for full usage!

## how though?

- a C extension which implements the PEP
- a `.pth` file executed on startup (see setup.py) patches `sys` / `builtins`

## you may also like

- [future-fstrings](https://github.com/asottile/future-fstrings)
