import distutils
import os.path
import sys

from setuptools import Extension
from setuptools import setup
from setuptools.command.install import install as _install


BUILTINS_MOD = '__builtin__' if sys.version_info < (3,) else 'builtins'
PTH = (
    'try:\n'
    '    breakpoint\n'
    'except NameError:\n'
    '    try:\n'
    '        import _future_breakpoint\n'
    '    except ImportError:\n'
    '        pass\n'
    '    else:\n'
    '        import {} as builtins\n'
    '        import sys\n'
    '        sys.breakpointhook = _future_breakpoint.breakpointhook\n'
    '        sys.__breakpointhook__ = _future_breakpoint.breakpointhook\n'
    '        builtins.breakpoint = _future_breakpoint.breakpoint\n'.format(
        BUILTINS_MOD,
    )
)


class install(_install):
    def initialize_options(self):
        _install.initialize_options(self)
        # Use this prefix to get loaded as early as possible
        name = 'aaaaa_' + self.distribution.metadata.name

        contents = 'import sys; exec({!r})\n'.format(PTH)
        self.extra_path = (name, contents)

    def finalize_options(self):
        _install.finalize_options(self)

        if self.install_lib.endswith(self.extra_path[1]):
            self.install_lib = self.install_libbase
            distutils.log.info(
                "will install .pth to '%s.pth'",
                os.path.join(self.install_lib, self.extra_path[0]),
            )
        else:
            distutils.log.info('skipping install of .pth during easy-install')


setup(
    name='future_breakpoint',
    description='A backport of `breakpoint` to python<3.7',
    url='https://github.com/asottile/future-breakpoint',
    version='1.0.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    ext_modules=[Extension('_future_breakpoint', ['_future_breakpoint.c'])],
    cmdclass={'install': install},
)
