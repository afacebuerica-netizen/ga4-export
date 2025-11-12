"""
Quick GA4 access checker for all properties defined in properties.py.

Runs a minimal query per property using the service account in config.KEY_FILE_PATH
and reports which properties are accessible vs failing (e.g., 403 permissions).
"""

import sys
from typing import List, Tuple

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

from config import KEY_FILE_PATH
from properties import GA4_PROPERTIES


def check_property(client: BetaAnalyticsDataClient, property_id: str) -> Tuple[bool, str]:
    """Attempt a tiny GA4 query; return (ok, message)."""
    try:
        request = RunReportRequest(
            property=property_id,
            date_ranges=[DateRange(start_date='7daysAgo', end_date='yesterday')],
            dimensions=[Dimension(name='date')],
            metrics=[Metric(name='activeUsers')],
            limit=1,
            offset=0,
        )
        _ = client.run_report(request)
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)}"


def main() -> int:
    print("=" * 70)
    print("GA4 PROPERTY ACCESS CHECKER")
    print("=" * 70)
    print()

    if not GA4_PROPERTIES:
        print("No properties configured in properties.py")
        return 1

    try:
        client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_PATH)
    except Exception as e:
        print(f"[ERROR] Could not initialize GA4 client with key {KEY_FILE_PATH}: {e}")
        return 1

    successes: List[str] = []
    failures: List[Tuple[str, str]] = []

    for idx, (prop_id, details) in enumerate(GA4_PROPERTIES.items(), 1):
        name = details.get('name', prop_id)
        print(f"[{idx}/{len(GA4_PROPERTIES)}] Checking: {name} ({prop_id})")
        ok, msg = check_property(client, prop_id)
        if ok:
            print(f"   ✓ Access OK")
            successes.append(name)
        else:
            print(f"   ✗ Access FAILED - {msg}")
            failures.append((name, msg))
        print()

    print("=" * 70)
    print(f"Accessible: {len(successes)}  |  Inaccessible: {len(failures)}  |  Total: {len(GA4_PROPERTIES)}")
    if failures:
        print("\nFailures:")
        for name, msg in failures:
            print(f" - {name}: {msg}")
    print("=" * 70)

    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())


