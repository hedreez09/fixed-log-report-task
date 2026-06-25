# dynamo-canary GUID: keep-the-original-guid-from-the-scaffold

import json
import re
from collections import Counter
from pathlib import Path


ACCESS_LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/log_report.json")

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "(?P<method>\S+) (?P<path>\S+) [^"]+" (?P<status>\d{3}) (?P<size>\S+)'
)

REQUIRED_KEYS = {
    "total_requests",
    "status_counts",
    "top_ip",
    "top_path",
    "error_rate",
}


def _parse_access_log():
    rows = []

    for line in ACCESS_LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue

        match = LOG_PATTERN.match(line)
        if not match:
            continue

        rows.append(
            {
                "ip": match.group("ip"),
                "path": match.group("path"),
                "status": match.group("status"),
            }
        )

    return rows


def _winner(counter):
    max_count = max(counter.values())
    candidates = [key for key, count in counter.items() if count == max_count]
    return sorted(candidates)[0]


def _expected_report():
    rows = _parse_access_log()

    status_counts = Counter(row["status"] for row in rows)
    ip_counts = Counter(row["ip"] for row in rows)
    path_counts = Counter(row["path"] for row in rows)

    error_count = sum(
        1
        for row in rows
        if row["status"].startswith("4") or row["status"].startswith("5")
    )

    return {
        "total_requests": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "top_ip": _winner(ip_counts),
        "top_path": _winner(path_counts),
        "error_rate": round(error_count / len(rows), 4) if rows else 0.0,
    }


def _load_report():
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def test_report_file_exists():
    """Success criterion 1: The agent must create /app/log_report.json."""
    assert REPORT_PATH.exists(), "Expected /app/log_report.json to exist."


def test_report_is_valid_json_object():
    """Success criterion 2: /app/log_report.json must be a valid JSON object."""
    report = _load_report()
    assert isinstance(report, dict), "The report must be a JSON object."


def test_report_has_exact_required_schema():
    """Success criterion 3: The JSON object must contain exactly the required keys."""
    report = _load_report()
    assert set(report.keys()) == REQUIRED_KEYS


def test_report_value_types_are_correct():
    """Success criterion 4: Each report field must use the required data type."""
    report = _load_report()

    assert isinstance(report["total_requests"], int)
    assert isinstance(report["status_counts"], dict)
    assert all(isinstance(key, str) for key in report["status_counts"].keys())
    assert all(isinstance(value, int) for value in report["status_counts"].values())
    assert isinstance(report["top_ip"], str)
    assert isinstance(report["top_path"], str)
    assert isinstance(report["error_rate"], float)


def test_total_requests_is_correct():
    """Success criterion 5: total_requests must equal the number of parsed log entries."""
    report = _load_report()
    expected = _expected_report()

    assert report["total_requests"] == expected["total_requests"]


def test_status_counts_are_correct():
    """Success criterion 6: status_counts must exactly count each HTTP status code."""
    report = _load_report()
    expected = _expected_report()

    assert report["status_counts"] == expected["status_counts"]


def test_top_ip_is_correct():
    """Success criterion 7: top_ip must be the most frequent client IP, using lexicographic tie-breaking."""
    report = _load_report()
    expected = _expected_report()

    assert report["top_ip"] == expected["top_ip"]


def test_top_path_is_correct():
    """Success criterion 8: top_path must be the most frequent request path, using lexicographic tie-breaking."""
    report = _load_report()
    expected = _expected_report()

    assert report["top_path"] == expected["top_path"]


def test_error_rate_is_correct():
    """Success criterion 9: error_rate must equal 4xx/5xx requests divided by total requests, rounded to 4 decimals."""
    report = _load_report()
    expected = _expected_report()

    assert report["error_rate"] == expected["error_rate"]