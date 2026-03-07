#!/usr/bin/env python3
"""
Camarilla Pivot Calculator - Multi-Timeframe Support
Supports: 1h, 2h, 4h, 1d, 1w, 1mo timeframes
Usage: python camarilla_bot.py --timeframe 1h (or 2h, 4h, 1d, 1w)
"""

import yfinance as yf
from datetime import datetime, timedelta
import json
import argparse
import sys

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

# Valid timeframes and their Yahoo Finance codes
TIMEFRAMES = {
    '1h': {'interval': '1h', 'period': '7d', 'label': '1 Hour'},
    '2h': {'interval': '2h', 'period': '14d', 'label': '2 Hour'},
    '4h': {'interval': '4h', 'period': '30d', 'label': '4 Hour'},
    '1d': {'interval': '1d', 'period': '30d', 'label': 'Daily'},
    '1w': {'interval': '1wk', 'period': '1y', 'label': 'Weekly'},
    'daily': {'interval': '1d', 'period': '30d', 'label': 'Daily'},
    'weekly': {'interval': '1wk', 'period': '1y', 'label': 'Weekly'}
}

def calculate_camarilla(high, low, close):
    """Calculate Camarilla pivot points (H3/H4/L3/L4)"""
    pp = (high + low + close) / 3
    
    # Camarilla levels
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

def fetch_data(code, info, timeframe_config):
    """Fetch OHLC data for specified timeframe"""
    symbol = yf.Ticker(info['symbol'])
    
    try:
        hist = symbol.history(
            period=timeframe_config['period'],
            interval=timeframe_config['interval']
        )
        
        if hist.empty:
            return None
        
        # Use the most recent complete candle (second to last)
        if len(hist) >= 2:
            candle = hist.iloc[-2]
        else:
            candle = hist.iloc[-1]
        
        return {
            'high': float(candle['High']),
            'low': float(candle['Low']),
            'close': float(candle['Close']),
            'open': float(candle['Open']),
            'volume': int(candle['Volume'])
        }
    except Exception as e:
        print(f"⚠️ Error fetching {code}: {e}")
        return None

def generate_report(timeframe='1d'):
    """Generate Camarilla pivot report for specified timeframe"""
    
    if timeframe not in TIMEFRAMES:
        print(f"❌ Invalid timeframe: {timeframe}")
        print(f"Valid options: {', '.join(TIMEFRAMES.keys())}")
        return
    
    tf_config = TIMEFRAMES[timeframe]
    
    print("="*100)
    print(f"🔥 CAMARILLA PIVOT POINTS - {tf_config['label'].upper()} TIMEFRAME")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p UTC')}")
    print(f"Timeframe: {tf_config['label']} | Interval: {tf_config['interval']}")
    print("="*100 + "\n")
    
    futures_results = []
    crypto_results = []
    
    # Process Futures
    print(f"📈 FUTURES - {tf_config['label']} Levels")
    print("-"*100)
    print(f"{'Symbol':<28} {'Code':<6} {'PP':>10} {'H3':>10} {'H4':>10} {'L3':>10} {'L4':>10}")
    print("-"*100)
    
    for code, info in FUTURES.items():
        data = fetch_data(code, info, tf_config)
        if data:
            pivots = calculate_camarilla(data['high'], data['low'], data['close'])
            
            futures_results.append({
                'Symbol': info['name'],
                'Code': code,
                'PP': f"{pivots['PP']:,.2f}",
                'H3': f"{pivots['H3']:,.2f}",
                'H4': f"{pivots['H4']:,.2f}",
                'L3': f"{pivots['L3']:,.2f}",
                'L4': f"{pivots['L4']:,.2f}"
            })
            
            print(f"{info['name']:<28} {code:<6} {pivots['PP']:>10.2f} {pivots['H3']:>10.2f} {pivots['H4']:>10.2f} {pivots['L3']:>10.2f} {pivots['L4']:>10.2f}")
    
    print(f"\n🪙 CRYPTO TOP 20 - {tf_config['label']} Levels")
    print("-"*100)
    print(f"{'Symbol':<28} {'Code':<6} {'PP':>10} {'H3':>10} {'H4':>10} {'L3':>10} {'L4':>10}")
    print("-"*100)
    
    for code, info in CRYPTOS.items():
        data = fetch_data(code, info, tf_config)
        if data:
            pivots = calculate_camarilla(data['high'], data['low'], data['close'])
            
            crypto_results.append({
                'Symbol': info['name'],
                'Code': code,
                'PP': f"{pivots['PP']:,.2f}",
                'H3': f"{pivots['H3']:,.2f}",
                'H4': f"{pivots['H4']:,.2f}",
                'L3': f"{pivots['L3']:,.2f}",
                'L4': f"{pivots['L4']:,.2f}"
            })
            
            print(f"{info['name']:<28} {code:<6} ${pivots['PP']:>8.2f} ${pivots['H3']:>8.2f} ${pivots['H4']:>8.2f} ${pivots['L3']:>8.2f} ${pivots['L4']:>8.2f}")
        else:
            print(f"⚠️ {info['name']:<28} {code:<6} No data available")
    
    print("\n" + "="*100)
    print("✅ Camarilla Pivot Points Calculated Successfully!")
    print("="*100)
    
    print("""
📊 Key Levels Explained:
   • PP (Pivot Point): Central reference level
   • H3/H4 (Resistance): Price breakout targets above pivot  
   • L3/L4 (Support): Price floor if bearish

💡 Trading Strategy:
   - If price > PP: Bullish bias, watch H3/H4 for targets
   - If price < PP: Bearish bias, watch L3/L4 for floors
   - Strong breakout above H4 = continued bullish momentum
   - Sharp drop below L4 = bearish acceleration

⏰ Timeframe Options: 1h, 2h, 4h, 1d (daily), 1w (weekly)
   Example: python camarilla_bot.py --timeframe 1h
""")
    
    # Save to JSON
    output = {
        'timestamp': datetime.now().isoformat(),
        'timeframe': timeframe,
        'timeframe_label': tf_config['label'],
        'futures': futures_results,
        'crypto': crypto_results
    }
    
    filename = f'camarilla_{timeframe}.json'
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"📁 Data saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Camarilla Pivot Points Calculator')
    parser.add_argument(
        '--timeframe', 
        type=str, 
        default='1d',
        choices=['1h', '2h', '4h', '1d', '1w', 'daily', 'weekly'],
        help='Timeframe for pivot calculation (default: 1d)'
    )
    
    args = parser.parse_args()
    
    # Normalize timeframe
    timeframe = args.timeframe
    if timeframe == 'daily':
        timeframe = '1d'
    elif timeframe == 'weekly':
        timeframe = '1w'
    
    generate_report(timeframe)
