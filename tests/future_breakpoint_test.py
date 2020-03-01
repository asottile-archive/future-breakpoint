"""copied from python/cpython@c87d9f40 Lib/test/test_builtin.py and modified
for compat and pytest
"""
import os
import sys
from unittest import mock

import pytest


class TestBreakpoint:
    @pytest.fixture(autouse=True)
    def restore(self):
        sys.breakpointhook = sys.__breakpointhook__
        with mock.patch.dict(os.environ, {}, clear=True):
            yield
        sys.breakpointhook = sys.__breakpointhook__

    def test_breakpoint(self):
        with mock.patch('pdb.set_trace') as mck:
            breakpoint()
        mck.assert_called_once()

    def test_breakpoint_with_breakpointhook_set(self):
        my_breakpointhook = mock.MagicMock()
        sys.breakpointhook = my_breakpointhook
        breakpoint()
        my_breakpointhook.assert_called_once_with()

    def test_breakpoint_with_breakpointhook_reset(self):
        my_breakpointhook = mock.MagicMock()
        sys.breakpointhook = my_breakpointhook
        breakpoint()
        my_breakpointhook.assert_called_once_with()
        # Reset the hook and it will not be called again.
        sys.breakpointhook = sys.__breakpointhook__
        with mock.patch('pdb.set_trace') as mck:
            breakpoint()
            mck.assert_called_once_with()
        my_breakpointhook.assert_called_once_with()

    def test_breakpoint_with_args_and_keywords(self):
        my_breakpointhook = mock.MagicMock()
        sys.breakpointhook = my_breakpointhook
        breakpoint(1, 2, 3, four=4, five=5)
        my_breakpointhook.assert_called_once_with(1, 2, 3, four=4, five=5)

    def test_breakpoint_with_passthru_error(self):
        def my_breakpointhook():
            raise NotImplementedError()
        sys.breakpointhook = my_breakpointhook
        pytest.raises(TypeError, breakpoint, 1, 2, 3, four=4, five=5)

    def test_envar_good_path_builtin(self):
        os.environ['PYTHONBREAKPOINT'] = 'int'
        with mock.patch('builtins.int') as mck:
            breakpoint('7')
            mck.assert_called_once_with('7')

    def test_envar_good_path_other(self):
        os.environ['PYTHONBREAKPOINT'] = 'sys.exit'
        with mock.patch('sys.exit') as mck:
            breakpoint()
            mck.assert_called_once_with()

    def test_envar_good_path_noop_0(self):
        os.environ['PYTHONBREAKPOINT'] = '0'
        with mock.patch('pdb.set_trace') as mck:
            breakpoint()
            mck.assert_not_called()

    def test_envar_good_path_empty_string(self):
        # PYTHONBREAKPOINT='' is the same as it not being set.
        os.environ['PYTHONBREAKPOINT'] = ''
        with mock.patch('pdb.set_trace') as mck:
            breakpoint()
            mck.assert_called_once_with()

    @pytest.mark.parametrize(
        'envar',
        (
            '.', '..', '.foo', 'foo.', '.int', 'int.'
            'nosuchbuiltin', 'nosuchmodule.nosuchcallable',
        ),
    )
    def test_envar_unimportable(self, envar):
        os.environ['PYTHONBREAKPOINT'] = envar
        with mock.patch('pdb.set_trace') as mck:
            with pytest.warns(RuntimeWarning) as warninfo:
                breakpoint()
        w, = warninfo
        msg = f'Ignoring unimportable $PYTHONBREAKPOINT: "{envar}"'
        assert str(w.message) == msg
        mck.assert_not_called()

    def test_envar_ignored_when_hook_is_set(self):
        os.environ['PYTHONBREAKPOINT'] = 'sys.exit'
        with mock.patch('sys.exit') as mck:
            sys.breakpointhook = int
            breakpoint()
            mck.assert_not_called()
