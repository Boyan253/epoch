# epoch

> Convert between unix timestamps and human dates in any timezone, both directions.

## Why

A log line says `1763000000`. Is that seconds or milliseconds, and what time is
that where the incident happened? `epoch` answers both without opening a
browser tab.

## Usage

```
python epoch.py 1763000000
python epoch.py 1763000000000 --tz Europe/Sofia   # ms detected automatically
python epoch.py "2026-01-02 15:30" --tz UTC       # the other direction
python epoch.py now --ms
```

## Output

```
unix     1763000000
iso      2025-11-13T04:53:20+02:00
local    2025-11-13 04:53:20 EET
utc      2025-11-13 02:53:20 UTC
```
