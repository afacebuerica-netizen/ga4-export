"""
Setup and validation script for GA4 Data Extraction Pipeline.
Run this before your first extraction to verify configuration.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and provide helpful feedback."""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: NOT FOUND at {filepath}")
        return False


def validate_properties():
    """Check if properties.py is configured."""
    try:
        from properties import GA4_PROPERTIES
        
        if not GA4_PROPERTIES:
            print("❌ properties.py: No properties configured")
            print("   Please edit properties.py and add your GA4 properties.")
            return False
        
        # Check if using example data
        has_example = False
        for prop_id, details in GA4_PROPERTIES.items():
            if 'example.com' in details.get('hostname', '') or 'Example Website' in details.get('name', ''):
                has_example = True
                break
        
        if has_example:
            print("⚠️  properties.py: Contains example data - please replace with your properties")
            return False
        
        # Validate property ID format
        invalid_properties = []
        for prop_id in GA4_PROPERTIES.keys():
            if not prop_id.startswith('properties/'):
                invalid_properties.append(prop_id)
        
        if invalid_properties:
            print("⚠️  properties.py: Some properties have invalid format")
            for prop_id in invalid_properties[:3]:  # Show first 3
                print(f"   - {prop_id}")
            print("   Property IDs should start with 'properties/' (e.g., 'properties/123456789')")
            return False
        
        print(f"✅ properties.py: Configured with {len(GA4_PROPERTIES)} property/properties")
        
        # Show property details
        if len(GA4_PROPERTIES) <= 5:
            for prop_id, details in GA4_PROPERTIES.items():
                print(f"   • {details.get('name', 'Unknown')} ({prop_id})")
        
        return True
    except ImportError:
        print("❌ properties.py: File not found")
        return False
    except Exception as e:
        print(f"❌ properties.py: Error reading file - {type(e).__name__}")
        return False


def validate_config():
    """Validate config.py settings."""
    try:
        from config import KEY_FILE_PATH, DATE_RANGES
        import os
        
        issues = []
        
        # Check date ranges
        if not DATE_RANGES or len(DATE_RANGES) == 0:
            issues.append("No date ranges configured")
        else:
            print(f"✅ Date range configured: {DATE_RANGES[0]['startDate']} to {DATE_RANGES[0]['endDate']}")
        
        # Check key file path
        if not os.path.exists(KEY_FILE_PATH):
            issues.append(f"Service account key not found: {KEY_FILE_PATH}")
        
        if issues:
            for issue in issues:
                print(f"⚠️  {issue}")
            return False
        
        return True
    except ImportError:
        print("❌ config.py: Could not import")
        return False


def validate_requirements():
    """Check if required Python packages are installed."""
    required_packages = {
        'pandas': 'pandas',
        'google.analytics.data_v1beta': 'google-analytics-data',
        'numpy': 'numpy',
    }
    
    all_installed = True
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}: Installed")
        except ImportError:
            print(f"❌ {package_name}: NOT INSTALLED")
            print(f"   Run: pip install {package_name}")
            all_installed = False
    
    return all_installed


def print_next_steps():
    """Print instructions for next steps."""
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Edit properties.py to add your GA4 properties")
    print("   Find Property IDs in GA4 Admin > Property Settings")
    print("\n2. Configure service account access:")
    print("   - Add service account email to GA4 property access")
    print("   - Grant 'Viewer' role")
    print("\n3. Place your service account key file in this directory")
    print("   (Should be named: service-account-key.json)")
    print("\n4. Run the extraction:")
    print("   python ga4_report_pull.py")
    print("\n" + "="*70)


def main():
    """Main validation function."""
    print("="*70)
    print("GA4 DATA EXTRACTION PIPELINE - SETUP VALIDATION")
    print("="*70)
    print()
    
    # Check configuration files
    print("Checking configuration files...")
    properties_ok = validate_properties()
    config_ok = validate_config()
    print()
    
    # Check service account key
    print("Checking credentials...")
    key_ok = check_file_exists('service-account-key.json', 'Service account key')
    print()
    
    # Check Python packages
    print("Checking required Python packages...")
    packages_ok = validate_requirements()
    print()
    
    # Summary
    print("="*70)
    all_checks_passed = properties_ok and config_ok and key_ok and packages_ok
    
    if all_checks_passed:
        print("✅ All checks passed! You're ready to run the extraction.")
        print("\nNext steps:")
        print("1. Test API connection:")
        print("   python test_connection.py")
        print("\n2. Run the extraction:")
        print("   python ga4_report_pull.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print_next_steps()
    print("="*70)


if __name__ == '__main__':
    main()

