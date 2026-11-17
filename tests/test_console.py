import pytest

from verri import tasty
from verri.console import main


def test_tasty_mango(capsys):
    main(['--no-newline', 'tasty', 'mango'])

    output = capsys.readouterr()
    assert output.out == tasty.mango()


def test_console_fallback(monkeypatch, capsys):
    # break verri.tasty's use of verri.git, force a fallback to mango (which won't use git)
    monkeypatch.setattr(tasty, 'git', None)

    with pytest.warns(UserWarning, match='fallback version'):
        main(['tasty', 'pineapple', '-n'])

    output = capsys.readouterr()
    assert output.out == tasty.mango()


def test_missing_tasty(capsys):
    with pytest.raises(SystemExit) as e:
        main(['pineapple'])

    output = capsys.readouterr()
    assert e.value.code > 0
    assert 'argument tasty' in output.err


def test_unknown_flavour(capsys):
    with pytest.raises(SystemExit) as e:
        main(['tasty', 'banana'])

    output = capsys.readouterr()
    assert e.value.code > 0
    assert 'invalid choice' in output.err
    assert 'banana' in output.err
