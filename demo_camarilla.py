#!/usr/bin/env python3
"""
Quick Camarilla Pivot Demo - Fetches TODAY's actual market data
"""

import yfinance as yf
from datetime import datetime

# Top 10 US Futures
FUTURES = {
    'ES': {'symbol': 'ES=F', 'name': 'S&P 500 E-mini'},
    'NQ': {'symbol': 'NQ=F', 'name': 'Nasdaq 100 E-mini'},
    'YM': {'symbol': 'YM=F', 'name': 'Dow Jones E-mini'},
    'RTY': {'symbol': 'RTY=F', 'name': 'Russell 2000'},
    'CL': {'symbol': 'CL=F', 'name': 'Crude Oil'},
    'GC': {'symbol': 'GC=F', 'name': 'Gold'},
    'SI': {'symbol': 'SI=F', 'name': 'Silver'},
    'ZC': {'symbol': 'ZC=F', 'name': 'Corn'},
    'ZS': {'symbol': 'ZS=F', 'name': 'Soybeans'},
    'ZN': {'symbol': 'ZN=F', 'name': '10Y Treasury Note'}
}

def calculate_camarilla(high, low, close):
    """Calculate Camarilla pivot points"""
    pp = (high + low + close) / 3
    h4 = close + (close - low) * 1.1 / 2.5
    h3 = close + (close - low) * 1.2 / 1.25
    l3 = close - (high - close) * 1.2 / 1.25
    l4 = close - (high - close) * 1.1 / 2.5
    
    return {
        'PP': pp,
        'H3': h3, 
        'H4': h4,
        'L3': l3,
        'L4': l4
    }

print("="*90)
print("CAMARILLA PIVOT POINTS DEMO - Live Market Data")
print(f"Generated: {datetime.now()}")
print("="*90 + "\n")

results = []

for code, info in FUTURES.items():
    symbol = yf.Ticker(info['symbol'])
    
    # Get historical data
    hist = symbol.history(period='3d')
    
    if hist.empty:
        print(f"❌ {info['name']} ({code}): No data available")
        continue
    
    # Use yesterday's data (last full day)
    yday = hist.iloc[-2]
    high, low, close = yday['High'], yday['Low'], yday['Close']
    
    pivots = calculate_camarilla(high, low, close)
    
    results.append({
        'Symbol': info['name'],
        'Code': code,
        'PP': f"{pivots['PP']:,.2f}",
        'H3': f"{pivots['H3']:,.2f}",
        'H4': f"{pivots['H4']:,.2f}",
        'L3': f"{pivots['L3']:,.2f}",
        'L4': f"{pivots['L4']:,.2f}"
    })

# Print table
if results:
    print(f"{'Name':<25} {'Code':<6} {'PP':>10} {'H3':>10} {'H4':>10} {'L3':>10} {'L4':>10}")
    print("-"*90)
    
    for r in results:
        print(f"{r['Symbol']:<25} {r['Code']:<6} {r['PP']:>10} {r['H3']:>10} {r['H4']:>10} {r['L3']:>10} {r['L4']:>10}")
    
    print("\n" + "="*90)
    print("✅ Sample run complete! Data shows yesterday's OHLC projected to next day")
    print("="*90)
else:
    print("❌ No data available for any futures")
