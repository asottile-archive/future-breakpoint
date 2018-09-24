[![Build Status](https://travis-ci.org/asottile/future-breakpoint.svg?branch=master)](https://travis-ci.org/asottile/future-breakpoint)
[![Build status](https://ci.appveyor.com/api/projects/status/4b6qu7v13vxc3tue/branch/master?svg=true)](https://ci.appveyor.com/project/asottile/future-breakpoint/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/asottile/future-breakpoint/badge.svg?branch=master)](https://coveralls.io/github/asottile/future-breakpoint?branch=master)

future-breakpoint
=================

A backport of `breakpoint` to python<3.7.

## install

`pip install future-breakpoint`

## supported versions

python2.7+, python3+, (noop on python3.7+)

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
