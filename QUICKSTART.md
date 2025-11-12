# Quick Start Guide - GA4 Data Extraction Pipeline

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your GA4 Properties

Edit `properties.py` and add your properties:

```python
GA4_PROPERTIES = {
    'properties/YOUR_PROPERTY_ID': {
        'name': 'Your Website Name',
        'hostname': 'https://www.yourwebsite.com'
    },
}
```

**How to find Property ID:**
- Go to Google Analytics 4
- Admin > Property Settings
- Look for "Property ID" (e.g., `123456789`)
- Use format: `'properties/123456789'`

### Step 3: Set Up Service Account (Google Cloud)

1. **Enable API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - APIs & Services > Library
   - Search "Google Analytics Data API"
   - Enable it

2. **Create Service Account:**
   - APIs & Services > Credentials
   - Create Credentials > Service Account
   - Name: "ga4-extractor"
   - Create Key > JSON > Download
   - Rename file to: `service-account-key.json`
   - Place in this project directory

3. **Grant GA4 Access:**
   - Open Google Analytics
   - Admin > Property Access Management
   - Add service account email (from JSON key)
   - Grant "Viewer" role
   - Repeat for each property

### Step 4: Validate Setup
```bash
python setup_guide.py
```

### Step 5: Run Extraction
```bash
python ga4_report_pull.py
```

## 📊 Output

You'll get a CSV file: `GA4_Unified_Report_YYYYMMDD.csv`

Contains 17 columns with all session data from your properties.

## 🔧 Troubleshooting

**"Service account key file not found"**
- Ensure `service-account-key.json` is in the project folder

**"Permission denied"**
- Check service account is added to GA4 properties with Viewer role

**"No data available"**
- Verify date range in `config.py` is valid
- Check property ID is correct

## 📚 Full Documentation

See `README.md` for complete documentation.

