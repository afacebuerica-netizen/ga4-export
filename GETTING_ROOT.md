# Quick Start Guide - For New Team Members

Welcome! This guide will help you get up and running with the GA4 Data Extraction Pipeline in under 15 minutes.

## 📋 Before You Start

Make sure you have:
- Python 3.8+ installed
- Access to the Google Cloud Platform project
- Admin access to the GA4 properties you'll be extracting from

## 🚀 Setup in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Credentials
1. Place your `service-account-key.json` in the project root
2. Copy and configure your properties:
   ```bash
   # Copy the example file
   copy properties.py.example properties.py
   ```
3. Edit `properties.py` with your GA4 property IDs

### Step 3: Validate and Test
```bash
# Run setup validation
python setup_guide.py

# Test API connection (after validation passes)
python test_connection.py

# Run your first extraction
python ga4_report_pull.py
```

## 📚 Need More Help?

- **Detailed Setup:** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions
- **Quick Reference:** See [README.md](README.md) for usage and examples
- **5-Minute Guide:** See [QUICKSTART.md](QUICKSTART.md)

## 🎯 Key Files to Know

| File | Purpose |
|------|---------|
| `ga4_report_pull.py` | Main extraction script |
| `setup_guide.py` | Validate your setup |
| `test_connection.py` | Test API connectivity |
| `config.py` | Configuration settings |
| `properties.py` | GA4 properties to extract |
| `SETUP_GUIDE.md` | Complete setup instructions |

## ⚠️ Common Issues

**Issue:** "Service account key file not found"
- **Fix:** Make sure `service-account-key.json` is in the project root

**Issue:** "Permission denied" errors
- **Fix:** Add the service account email to GA4 property access with "Viewer" role

**Issue:** "No data available"
- **Fix:** Check date range in `config.py` and ensure property IDs are correct

For more troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md#-troubleshooting)

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Service account key in place
- [ ] Properties configured in `properties.py`
- [ ] Setup validation passes (`python setup_guide.py`)
- [ ] Connection test passes (`python test_connection.py`)
- [ ] First extraction successful

Once all boxes are checked, you're ready to extract GA4 data!

---

**Need help?** Check the documentation files or contact the team lead.

