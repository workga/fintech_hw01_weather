import datetime
from pickle import PickleError

import pytest
from freezegun import freeze_time

from weather import cache
from weather.config import CACHE_FILENAME, CACHE_INTERVAL

DATETIME_NOW = datetime.datetime(2022, 3, 13)


def test_read_cache_empty(mocker):
    mocker.patch('pathlib.Path.exists', return_value=False)

    assert cache.read_cache(CACHE_FILENAME, CACHE_INTERVAL) == {}


def test_read_cache_pickle_exception(mocker):
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('pickle.load', side_effect=PickleError)

    assert cache.read_cache(CACHE_FILENAME, CACHE_INTERVAL) == {}


@pytest.mark.parametrize(
    ('content', 'result'),
    [
        (
            {  # content
                'moscow': {'datetime': DATETIME_NOW, 'result': '+2°'},
                'rostov': {
                    'datetime': DATETIME_NOW - CACHE_INTERVAL,
                    'result': '+3°',
                },
            },
            {  # result
                'moscow': {'datetime': DATETIME_NOW, 'result': '+2°'},
            },
        ),
        (
            {  # content
                'moscow': {
                    'datetime': DATETIME_NOW - CACHE_INTERVAL,
                    'result': '+2°',
                },
                'rostov': {
                    'datetime': DATETIME_NOW - CACHE_INTERVAL,
                    'result': '+3°',
                },
            },
            {},  # result
        ),
    ],
)
@freeze_time(DATETIME_NOW)
def test_read_cache_filtered(mocker, content, result):
    mocker.patch('pathlib.Path.exists', return_value=True)
    mocker.patch('pickle.load', return_value=content)

    assert cache.read_cache(CACHE_FILENAME, CACHE_INTERVAL) == result


def test_write_cache_success(mocker):
    mocker.patch('pickle.dump')

    assert cache.write_cache({}, CACHE_FILENAME)


def test_write_cache_pickle_exception(mocker):
    mocker.patch('pickle.dump', side_effect=PickleError)

    assert not cache.write_cache({}, CACHE_FILENAME)


def func_to_decorate():
    pass


@pytest.mark.parametrize(
    ('content', 'city', 'cached_result'),
    [
        (
            {
                'moscow': {
                    'datetime': DATETIME_NOW - CACHE_INTERVAL / 2,
                    'result': '+2°',
                },
            },
            'moscow',
            '+2°',
        ),
    ],
)
@freeze_time(DATETIME_NOW)
def test_timed_cache_used(mocker, content, city, cached_result):
    mocker.patch('weather.cache.read_cache', return_value=content)
    mocker.patch('weather.cache.write_cache')
    mocked_func = mocker.patch(__name__ + '.func_to_decorate')

    cached_func = cache.timed_cache(['city'])(func_to_decorate)

    assert cached_func(city=city) == cached_result
    mocked_func.assert_not_called()


@pytest.mark.parametrize(
    ('content', 'city', 'func_result'),
    [
        ({}, 'moscow', '+10°'),
    ],
)
@freeze_time(DATETIME_NOW)
def test_timed_cache_unused(mocker, content, city, func_result):
    mocker.patch('weather.cache.read_cache', return_value=content)
    mocker.patch('weather.cache.write_cache')
    mocked_func = mocker.patch(
        __name__ + '.func_to_decorate', return_value=func_result
    )

    cached_func = cache.timed_cache(['city'])(func_to_decorate)

    assert cached_func(city=city) == func_result
    mocked_func.assert_called()
