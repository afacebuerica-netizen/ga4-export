# GA4 Unified Cross-Property Data Extractor

A comprehensive Python pipeline for extracting and consolidating Google Analytics 4 (GA4) data from multiple properties into a unified CSV report.

## 🎯 Overview

This tool extracts key behavioral and financial metrics from multiple GA4 properties and generates a single, clean CSV file containing session-scoped data for cross-property analysis.

**Key Features:**
- Multi-property data extraction in a single run
- Automatic FullURL concatenation
- Standardized column formatting
- Daily or on-demand reporting
- Robust error handling and logging

## 🚀 Quick Start

**New to this project?** Start here:

1. **Read the complete setup guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. **Run the setup validator:** `python setup_guide.py`
3. **Test your connection:** `python test_connection.py`
4. **Run your first extraction:** `python ga4_report_pull.py`

## 📋 Prerequisites

- Python 3.8 or higher
- Access to Google Cloud Platform
- Admin access to GA4 properties you want to extract data from

### 1. Google Cloud Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable the Google Analytics Data API**
   - In the Cloud Console, navigate to "APIs & Services" > "Library"
   - Search for "Google Analytics Data API"
   - Click "Enable"

3. **Create a Service Account**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Name it (e.g., "ga4-data-extractor")
   - Click "Create and Continue"
   - Grant role: "Service Account User" (or "Viewer" for minimal permissions)
   - Click "Done"

4. **Generate and Download JSON Key**
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON"
   - Download the key file
   - **Rename it to `service-account-key.json`**
   - Place it in this project directory

5. **Grant GA4 Access**
   - Open Google Analytics 4
   - Go to "Admin" > "Property Access Management"
   - Click "+" and add the service account email (found in the JSON key file, e.g., `ga4-data-extractor@project-id.iam.gserviceaccount.com`)
   - Grant "Viewer" role
   - Repeat for each GA4 property you want to access

## 📦 Installation

1. **Clone or download this project**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your properties:**
   
   Copy the example file and edit with your properties:
   ```bash
   copy properties.py.example properties.py
   ```
   
   Or create `properties.py` with your GA4 property IDs:
   ```python
   GA4_PROPERTIES = {
       'properties/123456789': {
           'name': 'My Website',
           'hostname': 'https://www.mywebsite.com'
       }
   }
   ```

## 🔧 Configuration

### Step 1: Configure GA4 Properties (`properties.py`)

Edit `properties.py` to include your GA4 properties:

```python
GA4_PROPERTIES = {
    'properties/123456789': {
        'name': 'My Main Website',
        'hostname': 'https://www.mysite.com'
    },
    'properties/987654321': {
        'name': 'My Second Site',
        'hostname': 'https://www.anothersite.com'
    },
}
```

**Finding your Property ID:**
1. Go to Google Analytics 4
2. Navigate to "Admin" > "Property Settings"
3. Find your "Property ID" at the top (e.g., '123456789')

### Step 2: Configure Date Range (`config.py`)

Default is yesterday's data:

```python
DATE_RANGES = [
    {'startDate': 'yesterday', 'endDate': 'yesterday'}
]
```

**Options:**
- `'today'` - Today's data
- `'yesterday'` - Yesterday's data
- `'7daysAgo'` - Last 7 days
- `'YYYY-MM-DD'` - Specific date (e.g., `'2024-01-15'`)

Example for last 7 days:
```python
DATE_RANGES = [
    {'startDate': '7daysAgo', 'endDate': 'yesterday'}
]
```

### Step 3: (Optional) Configure Environment Variables

Copy the environment example file:
```bash
copy env.example .env
```

Edit `.env` to set custom paths:
```
SERVICE_ACCOUNT_KEY_PATH=service-account-key.json
```

## ✅ Validation & Testing

Before running your first extraction, verify your setup:

1. **Run setup validation:**
   ```bash
   python setup_guide.py
   ```
   Checks all configurations, files, and dependencies.

2. **Test API connection:**
   ```bash
   python test_connection.py
   ```
   Verifies service account authentication and property access.

3. **Run first extraction:**
   ```bash
   python ga4_report_pull.py
   ```

## 🚀 Usage

### Basic Execution

```bash
python ga4_report_pull.py
```

### What It Does

1. **Authenticates** with Google Analytics Data API using your service account
2. **Iterates** through each configured GA4 property
3. **Extracts** the following data:

#### Dimensions
- Event name
- Date
- FullURL (constructed from hostname + landing page)
- Country
- Device category
- Session default channel grouping
- Session medium
- Session source
- Session campaign

#### Metrics
- Sessions
- Engaged sessions
- Views (screen/page views)
- Active users
- New users
- Total users
- Total revenue

4. **Transforms** the data:
   - Concatenates hostname with landing page path to form FullURL
   - Renames columns to user-friendly names
   - Converts metrics to numeric types
   - Adds Website Name column for easy filtering

5. **Exports** to CSV file: `GA4_Unified_Report_YYYYMMDD.csv`

## 📊 Output Format

The generated CSV contains 17 columns in this order:

1. **Website Name** - Identifies which GA4 property the row belongs to
2. **Event name** - Event type
3. **Date** - Date of the session
4. **FullURL** - Complete URL (hostname + path + query)
5. **Country** - Visitor country
6. **Device category** - desktop/mobile/tablet
7. **Session default channel grouping** - Acquisition channel
8. **Session medium** - Traffic medium
9. **Session source** - Traffic source
10. **Session campaign** - Campaign name
11. **Sessions** - Number of sessions
12. **Engaged sessions** - Engaged sessions count
13. **Views** - Page/screen views
14. **Active users** - Active user count
15. **New users** - New user count
16. **Total users** - Total users
17. **Total revenue** - Total revenue for the session

## 🔄 Automation

### Daily Execution (Windows Task Scheduler)

1. Open "Task Scheduler" on Windows
2. Create a new task
3. Set trigger to "Daily" at your desired time
4. Set action to: `python C:\path\to\ga4_report_pull.py`
5. Save and enable the task

### Cron Job (Linux/Mac)

Add to crontab to run daily at 9 AM:

```bash
0 9 * * * cd /path/to/project && python ga4_report_pull.py
```

### Cloud Scheduler (Google Cloud)

For enterprise deployment:
- Create a Cloud Scheduler job
- Set HTTP target or Cloud Function trigger
- Configure OAuth for API authentication

## 🐛 Troubleshooting

### "Service account key file not found"
- Ensure `service-account-key.json` is in the project directory
- Check file permissions

### "Permission denied" or 403 errors
- Verify service account email is added to GA4 properties
- Ensure service account has "Viewer" role in GA4
- Check that Google Analytics Data API is enabled in GCP

### "No data available"
- Verify date range is valid (not in the future)
- Check that GA4 property has data for the selected date range
- Ensure property IDs are correct in `properties.py`

### Property ID format
- Use format: `'properties/123456789'` (with "properties/" prefix)
- Do not use GA4 Measurement ID or other identifiers

## 📁 Project Structure

```
ga4-data-extractor/
├── ga4_report_pull.py         # Main extraction script
├── setup_guide.py             # Setup validation script
├── test_connection.py         # API connection test script
├── properties.py              # GA4 property configuration
├── config.py                  # Global settings
├── requirements.txt           # Python dependencies
├── README.md                  # Quick reference (this file)
├── SETUP_GUIDE.md            # Complete setup instructions
├── QUICKSTART.md             # 5-minute quick start
├── env.example               # Environment variables template
├── properties.py.example     # Properties configuration template
├── service-account-key.json.example  # Service account key template
├── .gitignore                # Git ignore rules
├── service-account-key.json  # Your GCP credentials (not in repo)
└── output/                   # Output directory
    └── YYYY-MM-DD/           # Date-stamped subdirectories
        └── *.csv             # Individual property CSV files
```

## 🔒 Security Best Practices

1. **Never commit** `service-account-key.json` to version control
2. Add credentials to `.gitignore` (already configured)
3. Use least-privilege permissions (Viewer role only)
4. Rotate service account keys periodically
5. Store credentials in environment variables for production

## 📚 Additional Resources

- [Google Analytics Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 Dimensions and Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [Service Account Setup Guide](https://cloud.google.com/iam/docs/service-accounts)

## 🆘 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Google Analytics Data API documentation
3. Verify GCP project settings and permissions

## 📝 License

This project is provided as-is for data extraction purposes.

