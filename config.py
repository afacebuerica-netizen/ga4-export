"""
Configuration settings for GA4 Data Extraction Pipeline.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to the downloaded Service Account key JSON file
# Can be overridden with SERVICE_ACCOUNT_KEY_PATH environment variable
KEY_FILE_PATH = os.getenv('SERVICE_ACCOUNT_KEY_PATH', 'service-account-key.json')

# Date range configuration for reports
# Options: 'today', 'yesterday', '7daysAgo', '30daysAgo', 'YYYY-MM-DD'
# Default is yesterday's data for daily automation
DATE_RANGES = [
    {'startDate': '2025-11-02', 'endDate': '2025-11-08'}
]

# Alternative: Specific date range (uncomment to use) 
# DATE_RANGES = [
#     {'startDate': '2024-01-01', 'endDate': '2024-01-31'}
# ]

# Alternative: Last 7 days (uncomment to use)
# yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
# seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
# DATE_RANGES = [
#     {'startDate': seven_days_ago, 'endDate': yesterday}
# ]

# Column mapping for clean output
COLUMN_MAPPING = {
    'eventName': 'Event name',
    'date': 'Date',
    'country': 'Country',
    'deviceCategory': 'Device category',
    'sessionDefaultChannelGroup': 'Session default channel grouping',
    'sessionMedium': 'Session medium',
    'sessionSource': 'Session source',
    'sessionCampaignName': 'Session campaign',
    'sessions': 'Sessions',
    'engagedSessions': 'Engaged sessions',
    'screenPageViews': 'Views',
    'activeUsers': 'Active users',
    'newUsers': 'New users',
    'totalUsers': 'Total users',
    'totalRevenue': 'Total revenue',
}

# Final column order for CSV output
OUTPUT_COLUMN_ORDER = [
    'Website Name',
    'Event name',
    'Date',
    'FullURL',
    'Country',
    'Device category',
    'Session default channel grouping',
    'Session medium',
    'Session source',
    'Session campaign',
    'Sessions',
    'Engaged sessions',
    'Views',
    'Active users',
    'New users',
    'Total users',
    'Total revenue',
]

