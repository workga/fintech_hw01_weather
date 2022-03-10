import pytest
from requests.exceptions import HTTPError, RequestException

from weather import html_requests


@pytest.fixture()
def session_mock(mocker):
    return mocker.patch('requests.Session.get')


@pytest.mark.parametrize(
    ('text', 'headers'),
    [
        (
            "<div id='weather-now-number'>-2<span>°</span></div>",
            {'content-type': 'text/html; charset=utf-8'},
        ),
    ],
)
def test_get_success(session_mock, text, headers):
    session_mock.return_value.text = text
    session_mock.return_value.headers = headers

    assert html_requests.get('https://...') == text


def test_get_exception_request_failed(session_mock):
    session_mock.side_effect = RequestException

    with pytest.raises(RuntimeError):
        html_requests.get('https://...')


def test_get_exception_bad_status(session_mock):
    session_mock.return_value.raise_for_status.side_effect = HTTPError

    with pytest.raises(RuntimeError):
        html_requests.get('https://...')


@pytest.mark.parametrize(
    ('headers'),
    [
        ({'content-type': 'multipart/form-data; boundary=something'}),
        # additional wrong options
    ],
)
def test_get_exception_content_type(session_mock, headers):
    session_mock.return_value.headers = headers

    with pytest.raises(RuntimeError):
        html_requests.get('https://...')
