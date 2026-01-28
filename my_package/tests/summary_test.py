import pytest
from unittest.mock import Mock
import my_package.zadanie_duze_pyth as program
from my_package import Strona, Summary, Table, count_words, dodolu, workfreq


#@pytest.fixture
#def zero():
#    return Ułamek(0, 5, False)


def main(argv=None):
    
    h = Strona("https://bulbapedia.bulbagarden.net/wiki")
    parser = h.parser()
    args = parser.parse_args(argv)
    h.master(args)


#if __name__ == "__main__":
#    main()
#
#@pytest.mark.parametrize("a, expected", [("Team Rocket", "Team Rocket (Japanese: ロケット団 Rocket-dan, literally Rocket Gang) is a villainous team in pursuit of evil and the exploitation of Pokémon. The organization is based in the Kanto and Johto regions, with a small outpost in the Sevii Islands.")])
#def test_summary_flag(monkeypatch, capsys):
#    mock_summary = Mock()
#    monkeypatch.setattr(Summary, "summary", mock_summary)
#
#    program.main(["--summary", a])
#
#    mock_summary.assert_called_once_with(a)
#    captured = capsys.readouterr()
#
#    assert captured.out.strip() == expected



@pytest.mark.parametrize("a, expected", [("Team Rocket", "Team Rocket (Japanese: ロケット団だん Rocket-dan, literally Rocket Gang) is a villainous team in pursuit of evil and the exploitation of Pokémon. The organization is based in the Kanto and Johto regions, with a small outpost in the Sevii Islands.")])
def test_summary_flag(a, expected, monkeypatch, capsys):
    main(["--summary", a])
    captured = capsys.readouterr()

    assert captured.out.strip() == expected

    mock_summary = Mock()
    monkeypatch.setattr(Summary, "summary", mock_summary)

    main(["--summary", a])

    mock_summary.assert_called_once_with(a.replace(" ", "_"))
    #captured = capsys.readouterr()
#
    #assert captured.out.strip() == expected

