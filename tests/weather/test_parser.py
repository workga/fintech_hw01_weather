import pytest

from weather import parser


@pytest.mark.parametrize(
    ('html', 'result'),
    [
        ("<div id='weather-now-number'>-2<span>°</span></div>", '-2°'),
        # additional correct options
    ],
)
def test_parse_success(html, result):
    assert parser.parse_html(html) == result


@pytest.mark.parametrize(
    ('html'),
    [
        ("<div id='weather-now-number'></div>)"),
        ("<div id='weather'>-2<span>°</span></div>)"),
        (''),
        (None),
    ],
)
def test_parse_failed(html):
    with pytest.raises(RuntimeError):
        parser.parse_html(html)
