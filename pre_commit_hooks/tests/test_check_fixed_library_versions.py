import pytest

from pre_commit_hooks.check_fixed_library_versions import check_file, main
from pre_commit_hooks.exceptions import PreCommitException


def test_check_file_with_fixed_versions(tmpdir):
    # This file should pass without raising an exception
    p = tmpdir.join("fixed_versions.plcproj")
    with open("pre_commit_hooks/tests/data/fixed_versions.plcproj", "r") as f:
        p.write(f.read())
    check_file(str(p))


def test_check_file_with_unfixed_versions(tmpdir):
    p = tmpdir.join("unfixed_versions.plcproj")
    with open("pre_commit_hooks/tests/data/unfixed_versions.plcproj", "r") as f:
        p.write(f.read())
    with pytest.raises(PreCommitException) as excinfo:
        check_file(str(p))
    assert "Tc2_Standard" in str(excinfo.value)


def test_check_file_with_mixed_versions(tmpdir):
    p = tmpdir.join("mixed_versions.plcproj")
    with open("pre_commit_hooks/tests/data/mixed_versions.plcproj", "r") as f:
        p.write(f.read())
    with pytest.raises(PreCommitException) as excinfo:
        check_file(str(p))
    assert "Tc2_EtherCAT" in str(excinfo.value)


def test_main_with_fixed_versions(tmpdir, capsys):
    p = tmpdir.join("fixed_versions.plcproj")
    with open("pre_commit_hooks/tests/data/fixed_versions.plcproj", "r") as f:
        p.write(f.read())

    class Args:
        filenames = [str(p)]

    assert main(Args()) == 0
    captured = capsys.readouterr()
    assert captured.out == ""


def test_main_with_unfixed_versions(tmpdir, capsys):
    p = tmpdir.join("unfixed_versions.plcproj")
    with open("pre_commit_hooks/tests/data/unfixed_versions.plcproj", "r") as f:
        p.write(f.read())

    class Args:
        filenames = [str(p)]

    assert main(Args()) == 1
    captured = capsys.readouterr()
    assert "Library version of Tc2_Standard is not fixed!" in captured.out