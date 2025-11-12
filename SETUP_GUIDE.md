# Complete Setup Guide - GA4 Data Extraction Pipeline

This guide will walk you through setting up the GA4 Data Extraction Pipeline from scratch on your machine.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:
- [ ] Python 3.8 or higher installed
- [ ] Access to Google Analytics 4 accounts you want to extract data from
- [ ] Google Cloud Platform account access
- [ ] Admin access to GA4 properties to grant permissions

**Verify Python installation:**
```bash
python --version
# Should output: Python 3.8.x or higher
```

## 🔧 Step-by-Step Setup

### Step 1: Clone and Navigate to Project

```bash
# Navigate to the project directory
cd "path/to/GA4 data extractor/v6"
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `google-analytics-data` - Google Analytics Data API client
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `python-dotenv` - Environment variable management

### Step 3: Set Up Google Cloud Credentials

#### 3.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "GA4 Data Extractor")
5. Click "Create"

#### 3.2 Enable the Google Analytics Data API

1. In the Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Analytics Data API"
3. Click on the result
4. Click "Enable"

#### 3.3 Create a Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - Name: `ga4-data-extractor`
   - Description: `Service account for GA4 data extraction`
4. Click "Create and Continue"
5. Grant role: "Service Account User" (or "Viewer" for minimal permissions)
6. Click "Continue" then "Done"

#### 3.4 Generate and Download Service Account Key

1. In the Credentials page, click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Click "Create"
6. The JSON file will download automatically

#### 3.5 Place the Key File in Project

1. Rename the downloaded file to `service-account-key.json`
2. Place it in the project root directory

**Example file location:**
```
GA4 data extractor/v6/
├── service-account-key.json  ← Place it here
├── config.py
├── ga4_report_pull.py
└── ...
```

#### 3.6 (Optional) Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   copy env.example .env
   ```

2. Edit `.env` and update if needed:
   ```
   SERVICE_ACCOUNT_KEY_PATH=service-account-key.json
   ```

### Step 4: Grant Service Account Access to GA4 Properties

For **each GA4 property** you want to extract data from:

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select the property
3. Go to "Admin" (gear icon at bottom left)
4. Under "Property" column, click "Property Access Management"
5. Click the "+" button
6. Click "Add users"
7. Enter the service account email (found in `service-account-key.json`, field `client_email`)
   - Example: `ga4-data-extractor@your-project-id.iam.gserviceaccount.com`
8. Select role: "Viewer"
9. Click "Add"

**Repeat for all properties you want to extract data from.**

### Step 5: Configure Your GA4 Properties

Edit the `properties.py` file with your GA4 properties:

```python
GA4_PROPERTIES = {
    'properties/YOUR_PROPERTY_ID': {
        'name': 'Your Website Name',
        'hostname': 'https://www.yourwebsite.com'
    },
    # Add more properties as needed
}
```

**How to find your Property ID:**

1. Go to Google Analytics 4
2. Select your property
3. Go to "Admin" > "Property Settings"
4. Find "Property ID" at the top (e.g., `123456789`)
5. Use format: `'properties/123456789'` (include the "properties/" prefix)

**Important notes:**
- Each property needs its own entry in the dictionary
- Use the full URL with protocol (https://) for hostname
- Property IDs are numeric, not Measurement IDs

### Step 6: Configure Date Range

Edit `config.py` to set your desired date range:

```python
# Default: yesterday's data (good for daily automation)
DATE_RANGES = [
    {'startDate': 'yesterday', 'endDate': 'yesterday'}
]
```

**Options:**
- `'yesterday'` - Yesterday's data (default)
- `'today'` - Today's data
- `'7daysAgo'` - Last 7 days
- `'30daysAgo'` - Last 30 days
- `'YYYY-MM-DD'` - Specific date (e.g., `'2024-01-15'`)

### Step 7: Validate Your Setup

Run the setup validation script:

```bash
python setup_guide.py
```

This will check:
- ✅ Required files exist
- ✅ Python packages are installed
- ✅ Service account key is present
- ✅ Properties are configured

**Expected output:**
```
======================================================================
GA4 DATA EXTRACTION PIPELINE - SETUP VALIDATION
======================================================================

Checking configuration files...
✅ properties.py: Configured with 10 property/properties
✅ config.py: Found

Checking credentials...
✅ Service account key: Found

Checking required Python packages...
✅ pandas: Installed
✅ google-analytics-data: Installed
✅ numpy: Installed

======================================================================
✅ All checks passed! You're ready to run the extraction.
======================================================================
```

### Step 8: Test the Connection

Run the connection test script to verify API access:

```bash
python test_connection.py
```

This will:
- Test authentication with Google Analytics API
- Verify service account access to properties
- Check API quota and rate limits

### Step 9: Run Your First Extraction

Once validation passes, run the extraction:

```bash
python ga4_report_pull.py
```

**What happens:**
1. Authenticates with Google Analytics
2. Connects to each configured property
3. Extracts data for the specified date range
4. Saves CSV files to `output/YYYY-MM-DD/` directory

**Expected output:**
```
======================================================================
GA4 UNIFIED CROSS-PROPERTY DATA EXTRACTION
======================================================================
Date Range: yesterday to yesterday
Properties to process: 10
======================================================================

[1/10] Processing: Your Website Name
   Property ID: properties/123 when writing tools_rules
   Authenticating with Google Analytics API...
   Fetching data for each individual date to maximize granularity...
   Fetching data for 2024-01-15...
   > Retrieved 5,234 rows for 2024-01-15 (Total: 5,234)
   [SUCCESS] Total rows fetched: 5,234
   [SUCCESS] Retrieved 5234 rows
   [FILE] Saved to: yourwebsite_com_1705123456.csv

...

[SUCCESS] DATA EXTRACTION COMPLETE!
======================================================================
Successful Properties: 10/10
Failed Properties: 0
Output Directory: output/2024-01-16
======================================================================
```

## 🎯 Output Files

Extracted data is saved in the following structure:

```
output/
└── 2024-01-16/
    ├── yourwebsite_com_1705123456.csv
    ├── anothersite_com_1705123467.csv
    └── ...
```

Each CSV file contains:
- 17 columns of session-scoped data
- Website name, event details, traffic source, metrics, and revenue
- Ready for analysis in Excel, Python, or BI tools

## 🔄 Setting Up Daily Automation

### Windows Task Scheduler

1. Open "Task Scheduler"
2. Create Task (not Basic Task)
3. General tab:
   - Name: `GA4 Daily Data Extract`
   - Select "Run whether user is logged on or not"
4. Triggers tab:
   - New > Daily
   - Start time: `09:00 AM`
   - Enabled: Yes
5. Actions tab:
   - New > Start a program
   - Program: `python`
   - Arguments: `C:\path\to\ga4_report_pull.py`
   - Start in: `C:\path\to\project\directory`
6. Conditions tab:
   - Uncheck "Start the task only if the computer is on AC power"
7. OK and enter credentials

### Linux/Mac Cron Job

Add to crontab:

```bash
crontab -e
```

Add this line (runs daily at 9 AM):

```
0 9 * * * cd /path/to/project && python ga4_report_pull.py
```

## 🐛 Troubleshooting

### "Service account key file not found"

**Solution:**
- Ensure `service-account-key.json` is in the project root directory
- Check the filename matches exactly (case-sensitive)
- Verify file permissions allow reading

### "Permission denied" or 403 errors

**Solution:**
- Verify service account email is added to GA4 property access
- Ensure service account has "Viewer" role in GA4
- Check that Google Analytics Data API is enabled in GCP
- Wait a few minutes after granting access (propagation delay)

### "No data available"

**Solution:**
- Verify date range is valid (not in the future)
- Check that GA4 property has data for the selected date range
- Ensure property IDs are correct in `properties.py`
- Verify the property ID format includes "properties/" prefix

### "Module not found" or import errors

**Solution:**
```bash
pip install -r requirements.txt
```

If using a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Property ID format errors

**Correct format:**
```python
'properties/123456789'  ✅ Correct
```

**Incorrect formats:**
```python
'123456789'                    ❌ Missing "properties/" prefix
'GA-XXXXXXXXX'                 ❌ This is Measurement ID, not Property ID
'properties/UA-XXXXXXXXX'      ❌ Wrong ID format
```

### Rate limiting or quota errors

**Solution:**
- The script includes automatic delays between properties
- For large datasets, increase the delay in `ga4_report_pull.py` (line 419)
- Consider running during off-peak hours
- Check API quotas in Google Cloud Console

## 📚 Additional Resources

- [Google Analytics Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 Dimensions and Metrics Reference](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [Service Account Setup Guide](https://cloud.google.com/iam/docs/service-accounts)
- [Python pandas Documentation](https://pandas.pydata.org/docs/)

## 🆘 Getting Help

If you encounter issues:
1. Run `python setup_guide.py` to check your configuration
2. Run `python test_connection.py` to verify API connectivity
3. Check the troubleshooting section above
4. Review error messages carefully - they often indicate the specific issue
5. Ensure all prerequisites and setup steps are completed

## ✅ Setup Complete Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Google Analytics Data API enabled
- [ ] Service account created
- [ ] Service account key downloaded and placed in project
- [ ] Service account granted Viewer access to all GA4 properties
- [ ] `properties.py` configured with your properties
- [ ] `config.py` date range configured
- [ ] Setup validation passed (`python setup_guide.py`)
- [ ] Connection test passed (`python test_connection.py`)
- [ ] First extraction successful (`python ga4_report_pull.py`)
- [ ] Daily automation configured (optional)

Once all items are checked, you're ready to extract GA4 data!

