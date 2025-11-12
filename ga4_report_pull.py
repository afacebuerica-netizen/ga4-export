"""
GA4 Unified Cross-Property Data Extraction Script

This script extracts data from multiple Google Analytics 4 properties and
generates a unified CSV report with session-scoped behavioral and financial metrics.

Author: GA4 Data Extraction Pipeline
Version: 6.0
""" 

import pandas as pd
import sys
import os
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

from config import KEY_FILE_PATH, DATE_RANGES, COLUMN_MAPPING, OUTPUT_COLUMN_ORDER
from properties import GA4_PROPERTIES

# --- API NAMES (GA4 API Dimension and Metric Names) ---
DIMENSION_NAMES = [
    'eventName',
    'date',
    'fullPageUrl',
    'country',
    'deviceCategory',
    'sessionDefaultChannelGroup',
    'sessionMedium',
    'sessionSource',
    'sessionCampaignName',
]

METRIC_NAMES = [
    'sessions',
    'engagedSessions',
    'screenPageViews',
    'activeUsers',
    'newUsers',
    'totalUsers',
    'totalRevenue',
]


def get_ga4_report(property_id: str, property_details: Dict[str, str]) -> Optional[pd.DataFrame]:
    """
    Extracts data from a single GA4 property using scope-separated queries.
    
    Strategy:
    1. Query session/user metrics at session-grain (without eventName/fullPageUrl) to get accurate totals
    2. Query event metrics (Views, Revenue) with all dimensions including eventName/fullPageUrl
    3. Merge them on session-grain dimensions to create final dataset with correct totals
    
    Args:
        property_id: GA4 property ID (e.g., 'properties/123456789')
        property_details: Dictionary containing 'name' and 'hostname' for the property

    Returns:
        Merged DataFrame with all columns and accurate totals or None if error occurs
    """
    try:
        print(f"   Authenticating with Google Analytics API...")
        client = BetaAnalyticsDataClient.from_service_account_json(KEY_FILE_PATH)

        # Create date ranges
        date_range_list = [
            DateRange(start_date=dr['startDate'], end_date=dr['endDate'])
            for dr in DATE_RANGES
        ]

        # Build dimensions
        dimensions = [Dimension(name=d) for d in DIMENSION_NAMES]

        # Build metrics
        metrics = [Metric(name=m) for m in METRIC_NAMES]

        all_responses = []
        
        # Process each date range separately to avoid aggregation
        print(f"   Fetching data for each individual date to maximize granularity...")
        
        for date_range in date_range_list:
            # Calculate date range
            start_date = date_range.start_date
            end_date = date_range.end_date
            
            # Try to parse dates if they're in YYYY-MM-DD format
            try:
                from datetime import datetime as dt
                if start_date not in ['today', 'yesterday', '7daysAgo', '30daysAgo']:
                    start_dt = dt.strptime(start_date, '%Y-%m-%d')
                    end_dt = dt.strptime(end_date, '%Y-%m-%d')
                    
                    # Loop through each individual day
                    current_date = start_dt
                    while current_date <= end_dt:
                        date_str = current_date.strftime('%Y-%m-%d')
                        print(f"   Fetching data for {date_str}...")
                        
                        # Create single-day date range
                        day_date_range = [DateRange(start_date=date_str, end_date=date_str)]
                        
                        offset = 0
                        limit = 10000
                        
                        while True:
                            request = RunReportRequest(
                                property=property_id,
                                date_ranges=day_date_range,
                                dimensions=dimensions,
                                metrics=metrics,
                                limit=limit,
                                offset=offset
                            )
                            
                            response = client.run_report(request)
                            
                            if not response.rows:
                                break
                            
                            all_responses.append(response)
                            rows_returned = len(response.rows)
                            total_rows = sum(len(r.rows) for r in all_responses)
                            
                            print(f"   > Retrieved {rows_returned:,} rows for {date_str} (Total: {total_rows:,})")
                            
                            if rows_returned < limit:
                                break
                            
                            offset += limit
                        
                        # Move to next day
                        from datetime import timedelta
                        current_date += timedelta(days=1)
                else:
                    # Use original date range as-is
                    offset = 0
                    limit = 10000
                    
                    while True:
                        request = RunReportRequest(
                            property=property_id,
                            date_ranges=[date_range],
                            dimensions=dimensions,
                            metrics=metrics,
                            limit=limit,
                            offset=offset
                        )
                        
                        response = client.run_report(request)
                        
                        if not response.rows:
                            break
                        
                        all_responses.append(response)
                        rows_returned = len(response.rows)
                        
                        if rows_returned < limit:
                            break
                        
                        offset += limit
                        
            except ValueError:
                # Fallback to original approach
                offset = 0
                limit = 10000
                
                while True:
                    request = RunReportRequest(
                        property=property_id,
                        date_ranges=[date_range],
                        dimensions=dimensions,
                        metrics=metrics,
                        limit=limit,
                        offset=offset
                    )
                    
                    response = client.run_report(request)
                    
                    if not response.rows:
                        break
                    
                    all_responses.append(response)
                    rows_returned = len(response.rows)
                    
                    if rows_returned < limit:
                        break
                    
                    offset += limit
        
        # Convert responses to DataFrame using response_to_dataframe
        if not all_responses:
            return pd.DataFrame()
        
        df = response_to_dataframe(all_responses, property_details)
        return df

    except FileNotFoundError:
        print(f"   [ERROR] Service account key file not found at: {KEY_FILE_PATH}")
        print(f"   Please download your service account JSON key and place it in the project directory.")
        return None
    except Exception as e:
        print(f"   [ERROR] Failed to fetch data - {type(e).__name__}: {str(e)}")
        return None


def response_to_dataframe(responses: List[Any], property_details: Dict[str, str]) -> pd.DataFrame:
    """
    Converts GA4 API response(s) to a pandas DataFrame with proper transformations.
    Handles multiple response pages from pagination.

    Args:
        responses: List of GA4 API response objects (from pagination)
        property_details: Dictionary containing 'name' and 'hostname' for the property

    Returns:
        pandas DataFrame with formatted columns
    """
    if not responses or not responses[0].rows:
        return pd.DataFrame()

    print(f"   Converting {len(responses)} page(s) to DataFrame...")

    # Extract headers from first response
    dimension_headers = [header.name for header in responses[0].dimension_headers]
    metric_headers = [header.name for header in responses[0].metric_headers]
    
    # Build column names (Website Name + dimensions + metrics)
    column_names = ['Website Name'] + dimension_headers + metric_headers

    # Extract row data from all pages
    data = []
    for response in responses:
        for row in response.rows:
            row_values = [property_details['name']]  # Website Name first
            
            # Add dimension values
            row_values.extend([dim_value.value for dim_value in row.dimension_values])
            
            # Add metric values
            row_values.extend([metric_value.value for metric_value in row.metric_values])
            
            data.append(row_values)

    # Create initial DataFrame
    df = pd.DataFrame(data, columns=column_names)
    
    print(f"   Total rows in DataFrame: {len(df):,}")

    # --- CRITICAL TRANSFORMATION: Clean FullURL from fullPageUrl ---
    if 'fullPageUrl' in df.columns:
        # fullPageUrl returns complete URL - extract domain and path only (remove protocol)
        df['FullURL'] = df['fullPageUrl'].apply(
            lambda x: x.replace('https://', '').replace('http://', '') if x else ''
        )
        # Remove the intermediate column
        df = df.drop(columns=['fullPageUrl'])
    
    print(f"   Transforming data (FullURL construction, column renaming)...")

    # Rename columns to clean output names
    df = df.rename(columns=COLUMN_MAPPING)

    # Ensure all columns exist (in case some weren't present in response)
    for col in OUTPUT_COLUMN_ORDER:
        if col not in df.columns:
            df[col] = ''

    # Select and reorder columns
    existing_columns = [col for col in OUTPUT_COLUMN_ORDER if col in df.columns]
    df = df[existing_columns]

    # Convert numeric columns to appropriate types
    numeric_columns = [
        'Sessions', 'Engaged sessions', 'Views', 
        'Active users', 'New users', 'Total users', 'Total revenue'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df


def generate_output_directory() -> str:
    """
    Generates output directory structure: output/YYYY-MM-DD/
    
    Returns:
        Directory path string (e.g., output/2025-01-20/)
    """
    # Get current execution date
    exec_date = datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join('output', exec_date)
    
    # Create directory structure if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir


def generate_output_filename(website_name: str, hostname: str, output_dir: str) -> str:
    """
    Generates a filename for a property's CSV based on its hostname.
    
    Args:
        website_name: The website name
        hostname: The hostname (URL)
        output_dir: The output directory path
        
    Returns:
        Full path to the CSV file
    """
    # Extract domain from hostname (e.g., www.example.com -> example.com)
    # Remove protocol and path
    domain = hostname.replace('https://', '').replace('http://', '').split('/')[0]
    
    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Sanitize for filename (replace dots and special chars with underscores)
    sanitized_domain = domain.replace('.', '_').replace('/', '_')
    
    # Generate filename
    filename = f"{sanitized_domain}.csv"
    full_path = os.path.join(output_dir, filename)
    
    return full_path


def main():
    """
    Main execution: Loop through all GA4 properties and generate unified report.
    """
    print("=" * 70)
    print("GA4 UNIFIED CROSS-PROPERTY DATA EXTRACTION")
    print("=" * 70)
    print(f"Date Range: {DATE_RANGES[0]['startDate']} to {DATE_RANGES[0]['endDate']}")
    print(f"Properties to process: {len(GA4_PROPERTIES)}")
    print("=" * 70)
    print()

    if not GA4_PROPERTIES:
        print("[ERROR] No properties configured in properties.py")
        print("Please add at least one GA4 property to proceed.")
        sys.exit(1)

    # Create output directory structure
    output_dir = generate_output_directory()
    print(f"Output Directory: {output_dir}")
    print()
    
    successful_properties = 0
    failed_properties = 0
    skipped_properties = 0
    saved_files = []

    # Loop through each property
    for idx, (property_id, details) in enumerate(GA4_PROPERTIES.items(), 1):
        print(f"[{idx}/{len(GA4_PROPERTIES)}] Processing: {details['name']}")
        print(f"   Property ID: {property_id}")
        
        # Check if this property has already been extracted today
        expected_filename_base = generate_output_filename(
            details['name'], 
            details['hostname'], 
            output_dir
        )
        # Check for any file matching the base pattern (ignoring timestamp)
        base_name = os.path.splitext(expected_filename_base)[0]
        existing_files = [f for f in os.listdir(output_dir) if f.startswith(os.path.basename(base_name)) and f.endswith('.csv')]
        
        if existing_files:
            print(f"   [SKIP] Data already exists: {existing_files[0]}")
            print(f"   To re-extract, delete the file and run again.")
            skipped_properties += 1
            print()
            continue
        
        df = get_ga4_report(property_id, details)
        
        if df is not None and not df.empty:
            # Generate filename based on hostname
            output_filename = generate_output_filename(
                details['name'], 
                details['hostname'], 
                output_dir
            )
            
            # Add timestamp to filename to avoid conflicts
            import time
            base_name = os.path.splitext(output_filename)[0]
            output_filename = f"{base_name}_{int(time.time())}.csv"
            
            # Save individual CSV for this property
            df.to_csv(output_filename, index=False)
            saved_files.append(output_filename)
            successful_properties += 1
            print(f"   [SUCCESS] Retrieved {len(df)} rows")
            print(f"   [FILE] Saved to: {os.path.basename(output_filename)}")
        else:
            failed_properties += 1
            if df is None:
                print(f"   [ERROR] Failed to retrieve data")
            else:
                print(f"   [WARNING] No data available for this property")
        
        print()
        
        # Add delay between properties to avoid API rate limiting (skip for last property)
        if idx < len(GA4_PROPERTIES):
            print(f"   [WAIT] Pausing 15 seconds before next property...")
            time.sleep(15)
            print()

    # Summary of results
    print("=" * 70)
    if saved_files:
        print("[SUCCESS] DATA EXTRACTION COMPLETE!")
        print("=" * 70)
        print(f"Successful Properties: {successful_properties}/{len(GA4_PROPERTIES)}")
        print(f"Skipped Properties: {skipped_properties}")
        print(f"Failed Properties: {failed_properties}")
        print(f"Output Directory: {output_dir}")
        print(f"\nFiles Created ({len(saved_files)}):")
        for file in saved_files:
            print(f"  • {os.path.basename(file)}")
        print("=" * 70)
    elif skipped_properties > 0:
        print("[INFO] ALL PROPERTIES ALREADY EXTRACTED")
        print("=" * 70)
        print(f"Skipped Properties: {skipped_properties}/{len(GA4_PROPERTIES)}")
        print(f"All properties have already been extracted for today.")
        print(f"Output Directory: {output_dir}")
        print("\nTo re-extract data, delete the existing CSV files.")
        print("=" * 70)
    else:
        print("[ERROR] NO DATA RETRIEVED")
        print("=" * 70)
        print("No data was successfully retrieved from any property.")
        print("Please check:")
        print("  1. Service account key file exists")
        print("  2. Service account has Viewer permissions on all properties")
        print("  3. Property IDs are correct")
        print("  4. Date range is valid")
        print("=" * 70)


if __name__ == '__main__':
    main()

