import pytest
import csv
import requests
from unittest.mock import Mock, mock_open

from my_package.zadanie_duze_pyth import (
    Summary, Table, Count, Workfreq
)

HTML_TABLE = """
<div class="mw-body-content">
  <table>
    <tr><th>Name</th></tr>
    <tr><td><a>Bulbasaur</a></td></tr>
    <tr><td><a>Ivysaur</a></td></tr>
  </table>
</div>
"""


class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code


@pytest.mark.parametrize(
    "html, expected",
    [
        (
            '<div class="mw-body-content"><p>'
            'Team Rocket (Japanese: '
            '<ruby>ロケット団<rt>だん</rt></ruby> Rocket-dan)'
            '</p></div>',
            'Team Rocket (Japanese: ロケット団だん Rocket-dan)'
        ),
        (
            '<div class="mw-body-content"><p>'
            'Pikachu is an <ruby>電<rt>den</rt>気<rt>ki</rt></ruby> Pokémon.'
            '</p></div>',
            'Pikachu is an 電den気ki Pokémon.'
        ),
    ]
)
def test_summary_ok(html, expected, monkeypatch, capsys):
    monkeypatch.setattr(
        requests,
        "post",
        lambda url: MockResponse(html, 200)
    )

    Summary.summary("Anything", "")

    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize(
    "html, expected_counts",
    [
        (
            '<div class="mw-body-content">Hello world hello</div>',
            {"Hello": 1, "world": 1, "hello": 1},
        ),
        (
            '<div class="mw-body-content">one one one two</div>',
            {"one": 3, "two": 1},
        ),
    ]
)
def test_count(html, expected_counts, monkeypatch):
    monkeypatch.setattr(
        requests,
        "post",
        lambda url: MockResponse(html, 200)
    )

    result, most_freq = Count.count("fake_url", {})

    for word, value in expected_counts.items():
        assert result.get(word, 0) == value


def fake_count(url, _):
    return (
        {
            "hello": 10,
            "world": 5,
            "xyzxyz": 1,
        },
        "hello"
    )


@pytest.mark.parametrize("mode", ["article", "language"])
def test_workfreq_modes(monkeypatch, capsys, mode):
    monkeypatch.setattr(Count, "count", fake_count)

    Workfreq.workfreq(
        mode=mode,
        chart="Cos",
        strona="fake_url",
        count=0
    )

    captured = capsys.readouterr()
    assert captured.out != ""



@pytest.mark.parametrize("jestrue", [False, True])
def test_table_basic(monkeypatch, jestrue):
    monkeypatch.setattr(
        requests,
        "post",
        lambda url: MockResponse(HTML_TABLE, 200)
    )

    m = mock_open()
    monkeypatch.setattr("builtins.open", m)

    Table.table(1, "TestPage", jestrue, "Strona")

    m.assert_called_once_with("TestPage.csv", "w", newline="")

    handle = m()
    written = "".join(
        call.args[0] for call in handle.write.call_args_list
    )

    assert "Bulbasaur" in written
    assert "Ivysaur" in written