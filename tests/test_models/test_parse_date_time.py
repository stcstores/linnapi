import datetime as dt

import pytest

from linnapi import models


@pytest.fixture
def date_string():
    return "2022-03-15T14:31:09.103Z"


@pytest.fixture
def short_date_time_string():
    return "2022-04-19T07:01:37Z"


def test_parse_date_time_method(
    date_string,
):
    date = dt.datetime(
        year=2022, month=3, day=15, hour=14, minute=31, second=9, microsecond=103
    )
    assert models.parse_date_time(date_string) == date


def test_parse_date_time_method_with_short_date_time(
    short_date_time_string,
):
    date = dt.datetime(
        year=2022, month=4, day=19, hour=7, minute=1, second=37, microsecond=0
    )
    assert models.parse_date_time(short_date_time_string) == date


def test_parse_date_time_method_ignores_long_microseconds():
    date_string = "2022-03-15T14:31:09.1039999Z"
    assert models.parse_date_time(date_string).microsecond == 103999


def test_parse_date_time_method_raises_value_error_for_invalid_input():
    date_string = "20246542-03-15T14:31:09.1039999Z"
    with pytest.raises(ValueError) as exec_info:
        models.parse_date_time(date_string)
    assert date_string in str(exec_info.value)
