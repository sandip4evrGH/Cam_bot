# Camarilla Pivot Strategy - Automated Updates

## Overview
This project provides automated daily updates of Camarilla pivot point calculations for 100 stocks across 4 timeframes (daily, weekly, monthly, quarterly).

## Files Created

### Core Scripts
- `scripts/update_camarilla_data.py` - Main Python script that fetches data and calculates Camarilla pivots
- `run_update.sh` - Bash wrapper script for easy execution
- `test_script.py` - Quick verification script

### Data Storage
- `data/` - Directory where automated updates are stored
  - `camarilla_data_YYYY-MM-DD_HHMM.csv` - Daily timestamped data files
  - `latest_camarilla.json` - Most recent data in JSON format
- `logs/` - Directory for execution logs (to be implemented)
- `scripts/` - Python automation scripts

## How the Automation Works

The system is designed to run twice daily:
- **1:00 AM EST** - Pre-market update
- **12:00 PM EST** - Mid-day update

Each run:
1. Fetches latest data for 100 stocks across 11 sectors
2. Calculates Camarilla pivot points for 4 timeframes:
   - Daily (using previous day's OHLC)
   - Weekly (using previous week's OHLC)
   - Monthly (using previous month's OHLC)
   - Quarterly (using previous quarter's OHLC)
3. Saves results to timestamped CSV files
4. Updates `latest_camarilla.json` for easy access

## Camarilla Formulas Calculated

**Standard Levels:**
- PP = (High + Low + Close) / 3
- R1 = Close + ((High - Low) × 1.1 / 12)
- R2 = Close + ((High - Low) × 1.1 / 6)
- R3 = Close + ((High - Low) × 1.1 / 4)
- R4 = Close + ((High - Low) × 1.1 / 2)
- S1 = Close - ((High - Low) × 1.1 / 12)
- S2 = Close - ((High - Low) × 1.1 / 6)
- S3 = Close - ((High - Low) × 1.1 / 4)
- S4 = Close - ((High - Low) × 1.1 / 2)

**Extended Levels (as requested):**
- R5 = R4 + 1.168 × (R4 - R3)
- R6 = (Previous High / Previous Low) × Previous Close
- S6 = Previous Close - (R6 - Previous Close)
- S5 = S1 - (S2 - S1) [following R5 pattern]

## Setting Up Automated Updates

### Option 1: Using cron (Linux/macOS)
Add these lines to your crontab (`crontab -e`):

```
# Camarilla updates - 1 AM and 12 PM EST
0 1 * * * /path/to/camarilla_trader/run_update.sh >> /path/to/camarilla_trader/logs/camarilla_$(date +\%Y-\%m-\%d).log 2>&1
0 12 * * * /path/to/camarilla_trader/run_update.sh >> /path/to/camarilla_trader/logs/camarilla_$(date +\%Y-\%m-\%d).log 2>&1
```

### Option 2: Using Task Scheduler (Windows)
Create two scheduled tasks:
- Trigger: Daily at 1:00 AM
  Action: Start program → `path\to\run_update.sh`
- Trigger: Daily at 12:00 PM
  Action: Start program → `path\to\run_update.sh`

### Option 3: Manual Execution
For testing or occasional updates:
```bash
cd /path/to/camarilla_trader
source venv/bin/activate  # Activate virtual environment
./run_update.sh
```

## Data Files Explained

### CSV Format (`camarilla_data_YYYY-MM-DD_HHMM.csv`)
| Column | Description |
|--------|-------------|
| Symbol | Stock ticker (e.g., AAPL) |
| Timeframe | daily/weekly/monthly/quarterly |
| Date | Date of the OHLC data used |
| Close | Current closing price |
| Prev_High | Previous period's high |
| Prev_Low | Previous period's low |
| Prev_Close | Previous period's close |
| PP | Pivot Point |
| R1-R6 | Resistance levels 1-6 |
| S1-S6 | Support levels 1-6 |
| Run_Timestamp | When the update was run |

### JSON Format (`latest_camarilla.json`)
```json
{
  "timestamp": "2026-03-14T22:45:00",
  "data": [
    {
      "Symbol": "AAPL",
      "Timeframe": "Daily",
      "Date": "2026-03-12",
      "Close": 250.12,
      "Prev_High": 258.95,
      "Prev_Low": 254.18,
      "Prev_Close": 255.76,
      "PP": 256.30,
      "R1": 256.20,
      "..."
    }
  ]
}
```

## Usage Examples

### Quick Test
```bash
# Test with a few stocks
python test_script.py
```

### Manual Update
```bash
# Run a full update
./run_update.sh
```

### View Latest Data
```bash
# Check the most recent update
ls -la data/latest_camarilla.json
cat data/latest_camarilla.json | head -20
```

## Customization

### Changing Stock Universe
Edit `get_sector_stocks()` in `scripts/update_camarilla_data.py` to modify the list of stocks.

### Changing Timeframes
Modify the `timeframes` list in the `main()` function to add/remove timeframes.

### Adjusting Update Frequency
Change the cron/task scheduler timings to suit your needs.

## Requirements
- Python 3.7+
- Virtual environment with: yfinance, pandas, numpy
- Internet connection for Yahoo Finance data
- ~5-10 minutes per full update run

## Notes
- The script includes rate limiting to avoid overwhelming Yahoo Finance API
- Errors are logged but don't stop the entire process
- Each update creates a new timestamped file for historical tracking
- The `latest_camarilla.json` file is always overwritten with the most recent data
- Virtual environment must be activated before running scripts