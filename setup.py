import distutils
import os.path

from setuptools import Extension
from setuptools import setup
from setuptools.command.install import install as _install


PTH = (
    'try:\n'
    '    breakpoint\n'
    'except NameError:\n'
    '    try:\n'
    '        import _future_breakpoint\n'
    '    except ImportError:\n'
    '        pass\n'
    '    else:\n'
    '        import builtins\n'
    '        import sys\n'
    '        sys.breakpointhook = _future_breakpoint.breakpointhook\n'
    '        sys.__breakpointhook__ = _future_breakpoint.breakpointhook\n'
    '        builtins.breakpoint = _future_breakpoint.breakpoint\n'
)


class install(_install):
    def initialize_options(self):
        _install.initialize_options(self)
        # Use this prefix to get loaded as early as possible
        name = f'aaaaa_{self.distribution.metadata.name}'

        contents = f'import sys; exec({PTH!r})\n'
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
    ext_modules=[Extension('_future_breakpoint', ['_future_breakpoint.c'])],
    cmdclass={'install': install},
)
