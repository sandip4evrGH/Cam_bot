#!/bin/bash
# Script to run the Camarilla data update
# This can be called externally at 1 AM and 12 PM EST

echo "[$(date)] Starting Camarilla data update..."
cd /home/sandip/.openclaw/workspace/camarilla_trader
source venv/bin/activate
python scripts/update_camarilla_data.py
echo "[$(date)] Camarilla data update completed."
echo "---"