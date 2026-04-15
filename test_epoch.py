from datetime import timezone

import pytest

import epoch


def test_detect_unit_seconds():
    assert epoch.detect_unit(1763000000) == "s"

def test_detect_unit_milliseconds():
    assert epoch.detect_unit(1763000000000) == "ms"
