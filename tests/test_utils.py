import os
import stat
import pytest
from pathlib import Path

from dotops import utils

EXEC_PERM = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
NO_EXEC_PERM = stat.S_IRUSR | stat.S_IWUSR 


@pytest.fixture
def exec_file(tmpdir):
    path = tmpdir / 'executable'
    with open(path, 'w') as f:
        f.write('#!/bin/bash')
    os.chmod(path, EXEC_PERM)
    return path


@pytest.fixture
def no_exec_file(tmpdir):
    path = tmpdir / 'noexec'
    with open(path, 'w') as f:
        f.write('no_exec')
    os.chmod(path, NO_EXEC_PERM)
    return path


def test_is_executable(tmpdir, exec_file, no_exec_file):
    assert not utils.path_is_executable(tmpdir / 'absent')
    assert not utils.path_is_executable(no_exec_file)
    assert utils.path_is_executable(exec_file)


def test_find_executable(tmpdir, no_exec_file, exec_file):
    additional_roots = utils.find_executable(
        'noexec',
        'executable',
        additional_roots=[tmpdir])

    assert additional_roots == exec_file
    assert utils.find_executable('bash') == Path('/bin/bash')
