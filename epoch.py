#!/usr/bin/env python3
"""Convert unix timestamps to dates and back."""

import argparse
import sys
from datetime import datetime, timezone

__version__ = "0.1.0"

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
]


def detect_unit(value):
    """Guess whether a number is in seconds, milliseconds or microseconds."""
    magnitude = abs(value)
    if magnitude >= 1e17:
        return "ns"
    if magnitude >= 1e14:
        return "us"
    if magnitude >= 1e11:
        return "ms"
    return "s"


def to_seconds(value):
    unit = detect_unit(value)
    return value / {"s": 1, "ms": 1e3, "us": 1e6, "ns": 1e9}[unit], unit


def get_zone(name):
    if name in (None, "", "utc", "UTC"):
        return timezone.utc
    if ZoneInfo is None:
        raise ValueError("zoneinfo unavailable -- use UTC")
    return ZoneInfo(name)


def from_timestamp(value, tz=None):
    seconds, unit = to_seconds(float(value))
    moment = datetime.fromtimestamp(seconds, get_zone(tz))
    return moment, unit


def parse_human(text, tz=None):
    zone = get_zone(tz)
    text = text.strip()
    if text.lower() in ("now", "today"):
        return datetime.now(zone)
    cleaned = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(cleaned)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=zone)
    except ValueError:
        pass
    for fmt in FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=zone)
        except ValueError:
            continue
    raise ValueError("cannot parse %r as a date" % text)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("value", nargs="?", default="now",
                    help="a unix timestamp, a date, or 'now'")
    ap.add_argument("--tz", default="UTC", help="IANA timezone, e.g. Europe/Sofia")
    ap.add_argument("--ms", action="store_true", help="print milliseconds")
    args = ap.parse_args(argv)

    text = args.value.strip()
    try:
        if text.lstrip("-").replace(".", "", 1).isdigit():
            moment, unit = from_timestamp(text, args.tz)
            print("input read as %s" % unit, file=sys.stderr)
        else:
            moment = parse_human(text, args.tz)
    except ValueError as exc:
        print("epoch: %s" % exc, file=sys.stderr)
        return 2

    stamp = moment.timestamp()
    print("unix     %d" % int(stamp))
    if args.ms:
        print("unix ms  %d" % int(stamp * 1000))
    print("iso      %s" % moment.isoformat())
    print("local    %s" % moment.strftime("%Y-%m-%d %H:%M:%S %Z"))
    print("utc      %s" % moment.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
