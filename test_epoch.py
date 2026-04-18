from datetime import timezone

import pytest

import epoch


def test_detect_unit_seconds():
    assert epoch.detect_unit(1763000000) == "s"

def test_detect_unit_milliseconds():
    assert epoch.detect_unit(1763000000000) == "ms"


def test_detect_unit_microseconds():
    assert epoch.detect_unit(1763000000000000) == "us"

def test_from_timestamp_utc():
    moment, unit = epoch.from_timestamp(0)
    assert unit == "s"
    assert moment.year == 1970
    assert moment.tzinfo == timezone.utc


def test_milliseconds_and_seconds_agree():
    a, _ = epoch.from_timestamp(1763000000)
    b, _ = epoch.from_timestamp(1763000000000)
    assert a == b

def test_parse_human_iso():
    moment = epoch.parse_human("2026-01-02T03:04:05")
    assert (moment.year, moment.month, moment.day) == (2026, 1, 2)


def test_parse_human_plain_date():
    assert epoch.parse_human("2026-01-02").hour == 0

def test_parse_human_rejects_nonsense():
    with pytest.raises(ValueError):
        epoch.parse_human("not a date")
