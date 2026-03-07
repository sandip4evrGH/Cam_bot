#!/usr/bin/env python3
"""
Camarilla Pivot Calculator with Historical Data
Shows last 2 weeks + current week pivot points
"""

import yfinance as yf
from datetime import datetime, timedelta
import json
import pandas as pd

# Top US Futures
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

# Top 20 Cryptocurrencies
CRYPTOS = {
    'BTC': {'symbol': 'BTC-USD', 'name': 'Bitcoin'},
    'ETH': {'symbol': 'ETH-USD', 'name': 'Ethereum'},
    'BNB': {'symbol': 'BNB-USD', 'name': 'BNB'},
    'SOL': {'symbol': 'SOL-USD', 'name': 'Solana'},
    'XRP': {'symbol': 'XRP-USD', 'name': 'XRP'},
    'DOGE': {'symbol': 'DOGE-USD', 'name': 'Dogecoin'},
    'ADA': {'symbol': 'ADA-USD', 'name': 'Cardano'},
    'TRX': {'symbol': 'TRX-USD', 'name': 'TRON'},
    'AVAX': {'symbol': 'AVAX-USD', 'name': 'Avalanche'},
    'LINK': {'symbol': 'LINK-USD', 'name': 'Chainlink'},
    'MATIC': {'symbol': 'MATIC-USD', 'name': 'Polygon'},
    'LTC': {'symbol': 'LTC-USD', 'name': 'Litecoin'},
    'SHIB': {'symbol': 'SHIB-USD', 'name': 'Shiba Inu'},
    'DOT': {'symbol': 'DOT-USD', 'name': 'Polkadot'},
    'ETC': {'symbol': 'ETC-USD', 'name': 'Ethereum Classic'},
    'XMR': {'symbol': 'XMR-USD', 'name': 'Monero'},
    'ATOM': {'symbol': 'ATOM-USD', 'name': 'Cosmos'},
    'UNI': {'symbol': 'UNI-USD', 'name': 'Uniswap'},
    'LDO': {'symbol': 'LDO-USD', 'name': 'Lido DAO'},
    'NEAR': {'symbol': 'NEAR-USD', 'name': 'NEAR Protocol'}
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

def get_weekly_ohlc(symbol, weeks_ago=0):
    """Get OHLC for a specific week (0=current, 1=last week, 2=2 weeks ago)"""
    ticker = yf.Ticker(symbol)
    
    # Get 3 months of weekly data
    hist = ticker.history(period='3mo', interval='1wk')
    
    if hist.empty or len(hist) < weeks_ago + 1:
        return None
    
    # Get the week
    week_data = hist.iloc[-(weeks_ago + 1)]
    week_date = hist.index[-(weeks_ago + 1)]
    
    return {
        'high': float(week_data['High']),
        'low': float(week_data['Low']),
        'close': float(week_data['Close']),
        'open': float(week_data['Open']),
        'date': week_date.strftime('%Y-%m-%d')
    }

def get_historical_pivots(code, info, is_crypto=False):
    """Get pivots for last 3 weeks"""
    results = {}
    
    for weeks_ago in [2, 1, 0]:  # 2 weeks ago, 1 week ago, current
        data = get_weekly_ohlc(info['symbol'], weeks_ago)
        
        if data:
            pivots = calculate_camarilla(data['high'], data['low'], data['close'])
            
            week_label = 'Current Week' if weeks_ago == 0 else f'{weeks_ago} Week{"s" if weeks_ago > 1 else ""} Ago'
            
            results[week_label] = {
                'date': data['date'],
                'PP': pivots['PP'],
                'H3': pivots['H3'],
                'H4': pivots['H4'],
                'L3': pivots['L3'],
                'L4': pivots['L4'],
                'close': data['close']
            }
    
    return results

print("="*110)
print("🔥 CAMARILLA PIVOT POINTS - HISTORICAL VIEW (Last 3 Weeks)")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p UTC')}")
print("="*110 + "\n")

all_data = {'futures': {}, 'crypto': {}}

# Process Futures
print("📈 FUTURES - Historical Weekly Pivots")
print("="*110)

for code, info in FUTURES.items():
    historical = get_historical_pivots(code, info, is_crypto=False)
    
    if historical:
        all_data['futures'][code] = {'name': info['name'], 'data': historical}
        
        print(f"\n🏛️  {info['name']} ({code})")
        print("-"*110)
        print(f"{'Period':<15} {'Date':<12} {'PP':>10} {'H3':>10} {'H4':>10} {'L3':>10} {'L4':>10}")
        print("-"*110)
        
        for period, data in historical.items():
            print(f"{period:<15} {data['date']:<12} {data['PP']:>10.2f} {data['H3']:>10.2f} "
                  f"{data['H4']:>10.2f} {data['L3']:>10.2f} {data['L4']:>10.2f}")

print("\n\n🪙 CRYPTO - Historical Weekly Pivots")
print("="*110)

for code, info in CRYPTOS.items():
    historical = get_historical_pivots(code, info, is_crypto=True)
    
    if historical:
        all_data['crypto'][code] = {'name': info['name'], 'data': historical}
        
        print(f"\n💎 {info['name']} ({code})")
        print("-"*110)
        print(f"{'Period':<15} {'Date':<12} {'PP':>12} {'H3':>12} {'H4':>12} {'L3':>12} {'L4':>12}")
        print("-"*110)
        
        for period, data in historical.items():
            print(f"{period:<15} {data['date']:<12} ${data['PP']:>10.2f} ${data['H3']:>10.2f} "
                  f"${data['H4']:>10.2f} ${data['L3']:>10.2f} ${data['L4']:>10.2f}")

print("\n" + "="*110)
print("✅ Historical Pivot Analysis Complete!")
print("="*110)

print("""
📊 Analysis Tips:
   • Compare Current Week vs Previous Weeks to see level shifts
   • If Current PP > Last Week PP = Bullish trend
   • If Current PP < Last Week PP = Bearish trend
   • Watch for confluence (levels that align across weeks)

💡 Trading Strategy:
   - Strong uptrend: Current H3 above last week's H4
   - Strong downtrend: Current L3 below last week's L4
   - Range bound: Levels overlapping between weeks
""")

# Save to JSON
with open('camarilla_historical.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print("📁 Historical data saved to camarilla_historical.json")

# Create summary table for quick reference
print("\n\n📋 QUICK REFERENCE - Current Week vs Last Week")
print("="*110)
print(f"{'Asset':<25} {'Last Week PP':>12} {'Current PP':>12} {'Change':>10} {'Trend':>8}")
print("-"*110)

for category in ['futures', 'crypto']:
    for code, info in all_data[category].items():
        if '2 Weeks Ago' in info['data'] and '1 Week Ago' in info['data'] and 'Current Week' in info['data']:
            last_pp = info['data']['1 Week Ago']['PP']
            current_pp = info['data']['Current Week']['PP']
            change = current_pp - last_pp
            change_pct = (change / last_pp) * 100
            trend = "📈 UP" if change > 0 else "📉 DOWN" if change < 0 else "➡️ FLAT"
            
            print(f"{info['name']:<25} {last_pp:>12.2f} {current_pp:>12.2f} "
                  f"{change_pct:>+9.2f}% {trend:>8}")

print("="*110)
