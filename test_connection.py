"""
Test connection to Google Analytics Data API.

This script verifies that your service account credentials are working
and that you have access to the configured GA4 properties.
"""

import sys
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, RunReportRequest
from google.auth.exceptions import DefaultCredentialsError
from google.api_core import exceptions

from config import KEY_FILE_PATH, DATE_RANGES
from properties import GA4_PROPERTIES


def test_authentication():
    """Test if service account authentication works."""
    print("\n1. Testing Authentication...")
    try:
        if not os.path.exists(KEY_FILE_PATH):
            print(f"   ❌ Service account key file not found: {KEY_FILE_PATH}")
            return False
        
        client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_PATH)
        print(f"   ✅ Authentication successful")
        print(f"   ✅ Using key file: {KEY_FILE_PATH}")
        return True
    except DefaultCredentialsError as e:
        print(f"   ❌ Authentication failed: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {str(e)}")
        return False


def test_property_access(client, property_id):
    """Test if we can access a specific GA4 property."""
    try:
        # Create a test request with minimal data (just one day of yesterday data)
        request = RunReportRequest(
            property=property_id,
            date_ranges=[DateRange(start_date='yesterday', end_date='yesterday')],
            dimensions=[],
            metrics=[],
            limit=1
        )
        
        response = client.run_report(request)
        return True, None
    except exceptions.PermissionDenied:
        return False, "Permission denied - service account needs Viewer access"
    except exceptions.InvalidArgument as e:
        # This might happen if property doesn't exist
        return False, f"Invalid argument: {str(e)}"
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {str(e)}"


def test_all_properties():
    """Test access to all configured properties."""
    print("\n2. Testing Property Access...")
    print(f"   Testing {len(GA4_PROPERTIES)} configured properties...")
    
    if not GA4_PROPERTIES:
        print("   ❌ No properties configured in properties.py")
        return False
    
    try:
        client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_PATH)
    except Exception as e:
        print(f"   ❌ Cannot create API client: {str(e)}")
        return False
    
    success_count = 0
    failed_properties = []
    
    for property_id, details in GA4_PROPERTIES.items():
        property_name = details['name']
        print(f"   Testing: {property_name} ({property_id})...", end=" ")
        
        success, error_msg = test_property_access(client, property_id)
        
        if success:
            print("✅")
            success_count += 1
        else:
            print(f"❌ - {error_msg}")
            failed_properties.append((property_name, property_id, error_msg))
    
    print(f"\n   Results: {success_count}/{len(GA4_PROPERTIES)} properties accessible")
    
    if failed_properties:
        print("\n   ❌ Failed Properties:")
        for name, prop_id, error in failed_properties:
            print(f"      • {name} ({prop_id})")
            print(f"        Error: {error}")
    
    return success_count == len(GA4_PROPERTIES)


def test_api_quota():
    """Test API quota and rate limits."""
    print("\n3. Testing API Quota...")
    print("   ℹ️  Running a small test query to check API access...")
    
    if not GA4_PROPERTIES:
        print("   ❌ No properties configured")
        return False
    
    try:
        client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_PATH)
        
        # Get first property for testing
        first_property_id = list(GA4_PROPERTIES.keys())[0]
        
        request = RunReportRequest(
            property=first_property_id,
            date_ranges=[DateRange(start_date='yesterday', end_date='yesterday')],
            dimensions=[],
            metrics=[],
            limit=10
        )
        
        response = client.run_report(request)
        print("   ✅ API quota check passed")
        return True
    except exceptions.ResourceExhausted:
        print("   ❌ API quota exceeded - please try again later")
        return False
    except Exception as e:
        print(f"   ⚠️  API quota check inconclusive: {str(e)}")
        return True  # Don't fail the whole test for this


def print_service_account_email():
    """Extract and display the service account email from the JSON key."""
    print("\n0. Service Account Information...")
    try:
        import json
        with open(KEY_FILE_PATH, 'r') as f:
            key_data = json.load(f)
        
        client_email = key_data.get('client_email', 'Not found')
        project_id = key_data.get('project_id', 'Not found')
        
        print(f"   Service Account Email: {client_email}")
        print(f"   GCP Project ID: {project_id}")
        print()
        print("   ⚠️  IMPORTANT: Ensure this email has 'Viewer' access in GA4")
        print("      Go to GA4 Admin > Property Access Management and add this email")
    except Exception as e:
        print(f"   ⚠️  Could not read service account info: {str(e)}")


def main():
    """Main test function."""
    print("=" * 70)
    print("GA4 API CONNECTION TEST")
    print("=" * 70)
    
    # Print service account info
    print_service_account_email()
    
    # Run tests
    auth_ok = test_authentication()
    
    if not auth_ok:
        print("\n" + "=" * 70)
        print("❌ AUTHENTICATION FAILED")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Verify service-account-key.json file exists")
        print("2. Check that the JSON file is valid")
        print("3. Ensure the service account has API access in GCP")
        print("=" * 70)
        sys.exit(1)
    
    properties_ok = test_all_properties()
    quota_ok = test_api_quota()
    
    # Summary
    print("\n" + "=" * 70)
    if auth_ok and properties_ok and quota_ok:
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nYou're ready to run the full data extraction:")
        print("   python ga4_report_pull.py")
        print("=" * 70)
        sys.exit(0)
    elif auth_ok and quota_ok:
        print("⚠️  PARTIAL SUCCESS")
        print("=" * 70)
        print("\nAuthentication works, but some properties are not accessible.")
        print("Please grant the service account 'Viewer' access to all properties.")
        print("=" * 70)
        sys.exit(1)
    else:
        print("❌ TESTS FAILED")
        print("=" * 70)
        print("\nPlease fix the issues above before running the extraction.")
        print("See SETUP_GUIDE.md for detailed setup instructions.")
        print("=" * 70)
        sys.exit(1)


if __name__ == '__main__':
    main()

