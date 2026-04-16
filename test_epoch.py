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
