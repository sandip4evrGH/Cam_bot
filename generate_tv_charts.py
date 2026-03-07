#!/usr/bin/env python3
"""
Advanced Camarilla Pivot Chart - TradingView Style
Shows price action with pivot levels as horizontal lines
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import numpy as np
import json
from datetime import datetime, timedelta
import yfinance as yf

# Load the weekly data
with open('camarilla_1w.json', 'r') as f:
    data = json.load(f)

def fetch_recent_data(symbol, period='1mo'):
    """Fetch recent price data for charting"""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval='1d')
    return hist

def create_tradingview_style_chart(symbol_code, asset_data, title, filename):
    """Create TradingView-style chart with pivot levels"""
    
    # Get symbol info
    is_crypto = symbol_code in ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'DOGE', 'ADA', 'TRX', 'AVAX', 'LINK', 
                                 'MATIC', 'LTC', 'SHIB', 'DOT', 'ETC', 'XMR', 'ATOM', 'UNI', 'LDO', 'NEAR']
    
    if is_crypto:
        symbol_map = {
            'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'BNB': 'BNB-USD', 'SOL': 'SOL-USD',
            'XRP': 'XRP-USD', 'DOGE': 'DOGE-USD', 'ADA': 'ADA-USD', 'TRX': 'TRX-USD',
            'AVAX': 'AVAX-USD', 'LINK': 'LINK-USD', 'MATIC': 'MATIC-USD', 'LTC': 'LTC-USD',
            'SHIB': 'SHIB-USD', 'DOT': 'DOT-USD', 'ETC': 'ETC-USD', 'XMR': 'XMR-USD',
            'ATOM': 'ATOM-USD', 'UNI': 'UNI-USD', 'LDO': 'LDO-USD', 'NEAR': 'NEAR-USD'
        }
    else:
        symbol_map = {
            'ES': 'ES=F', 'NQ': 'NQ=F', 'YM': 'YM=F', 'RTY': 'RTY=F',
            'CL': 'CL=F', 'GC': 'GC=F', 'SI': 'SI=F', 'ZC': 'ZC=F',
            'ZS': 'ZS=F', 'ZN': 'ZN=F'
        }
    
    symbol = symbol_map.get(symbol_code, symbol_code)
    
    # Fetch price data
    price_data = fetch_recent_data(symbol, period='1mo')
    
    if price_data.empty:
        print(f"⚠️ No price data for {symbol_code}")
        return None
    
    # Parse pivot levels
    pp = float(asset_data['PP'].replace('$', '').replace(',', ''))
    h3 = float(asset_data['H3'].replace('$', '').replace(',', ''))
    h4 = float(asset_data['H4'].replace('$', '').replace(',', ''))
    l3 = float(asset_data['L3'].replace('$', '').replace(',', ''))
    l4 = float(asset_data['L4'].replace('$', '').replace(',', ''))
    
    # Create figure with dark theme (TradingView style)
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#131722')
    ax.set_facecolor('#131722')
    
    # Plot candlesticks
    for i, (date, row) in enumerate(price_data.iterrows()):
        open_p = row['Open']
        high_p = row['High']
        low_p = row['Low']
        close_p = row['Close']
        
        # Determine color
        color = '#26a69a' if close_p >= open_p else '#ef5350'
        
        # Draw wick
        ax.plot([i, i], [low_p, high_p], color=color, linewidth=1)
        
        # Draw body
        height = abs(close_p - open_p)
        bottom = min(open_p, close_p)
        rect = Rectangle((i-0.4, bottom), 0.8, height, 
                         facecolor=color, edgecolor=color)
        ax.add_patch(rect)
    
    # Extend x-axis for future projection
    last_idx = len(price_data) - 1
    future_idx = last_idx + 5
    
    # Plot pivot levels as horizontal lines extending into future
    x_range = list(range(len(price_data))) + list(range(last_idx, future_idx))
    
    # H4 - Strong Resistance (Green)
    ax.plot([last_idx-5, future_idx], [h4, h4], color='#00c853', linewidth=2, 
            linestyle='--', label=f'H4: {h4:,.2f}')
    ax.fill_between([last_idx, future_idx], h4, h4*1.02, alpha=0.1, color='#00c853')
    
    # H3 - Resistance (Light Green)
    ax.plot([last_idx-5, future_idx], [h3, h3], color='#69f0ae', linewidth=2, 
            linestyle='--', label=f'H3: {h3:,.2f}')
    
    # PP - Pivot (Blue)
    ax.plot([last_idx-10, future_idx], [pp, pp], color='#448aff', linewidth=3, 
            linestyle='-', label=f'PP: {pp:,.2f}')
    ax.fill_between([last_idx, future_idx], pp*0.98, pp*1.02, alpha=0.1, color='#448aff')
    
    # L3 - Support (Orange)
    ax.plot([last_idx-5, future_idx], [l3, l3], color='#ffab40', linewidth=2, 
            linestyle='--', label=f'L3: {l3:,.2f}')
    
    # L4 - Strong Support (Red)
    ax.plot([last_idx-5, future_idx], [l4, l4], color='#ff5252', linewidth=2, 
            linestyle='--', label=f'L4: {l4:,.2f}')
    ax.fill_between([last_idx, future_idx], l4*0.98, l4, alpha=0.1, color='#ff5252')
    
    # Add zone labels
    ax.text(future_idx-0.5, h4, 'H4', fontsize=10, color='#00c853', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#131722', edgecolor='#00c853'))
    ax.text(future_idx-0.5, h3, 'H3', fontsize=10, color='#69f0ae', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#131722', edgecolor='#69f0ae'))
    ax.text(future_idx-0.5, pp, 'PP', fontsize=10, color='#448aff', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#131722', edgecolor='#448aff'))
    ax.text(future_idx-0.5, l3, 'L3', fontsize=10, color='#ffab40', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#131722', edgecolor='#ffab40'))
    ax.text(future_idx-0.5, l4, 'L4', fontsize=10, color='#ff5252', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#131722', edgecolor='#ff5252'))
    
    # Styling
    ax.set_title(f'{title}\nCamarilla Pivot Points - Weekly Timeframe', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    ax.set_xlabel('Date', fontsize=12, color='white')
    ax.set_ylabel('Price', fontsize=12, color='white')
    
    # Format y-axis
    ax.tick_params(colors='white')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Grid
    ax.grid(True, alpha=0.2, color='gray', linestyle='--')
    ax.set_axisbelow(True)
    
    # Legend
    legend = ax.legend(loc='upper left', fontsize=10, facecolor='#131722', 
                      edgecolor='gray', labelcolor='white')
    
    # Set x-axis limits
    ax.set_xlim(-1, future_idx + 1)
    
    # Add vertical line at current date
    ax.axvline(x=last_idx, color='yellow', linewidth=2, linestyle=':', alpha=0.7, label='Current')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='#131722')
    plt.close()
    
    return filename

print("📊 Generating TradingView-Style Camarilla Charts...\n")

# Generate charts for top assets
charts_to_generate = [
    ('ES', 'S&P 500 E-mini (ES)', 'tv_chart_es.png'),
    ('BTC', 'Bitcoin (BTC)', 'tv_chart_btc.png'),
    ('ETH', 'Ethereum (ETH)', 'tv_chart_eth.png'),
    ('NQ', 'Nasdaq 100 E-mini (NQ)', 'tv_chart_nq.png'),
    ('GC', 'Gold (GC)', 'tv_chart_gc.png'),
    ('CL', 'Crude Oil (CL)', 'tv_chart_cl.png'),
    ('SOL', 'Solana (SOL)', 'tv_chart_sol.png'),
]

generated = []
for code, title, filename in charts_to_generate:
    try:
        if code in ['ES', 'NQ', 'YM', 'RTY', 'CL', 'GC', 'SI', 'ZC', 'ZS', 'ZN']:
            asset_data = next((item for item in data['futures'] if item['Code'] == code), None)
        else:
            asset_data = next((item for item in data['crypto'] if item['Code'] == code), None)
        
        if asset_data:
            result = create_tradingview_style_chart(code, asset_data, title, filename)
            if result:
                generated.append(filename)
                print(f"✅ {title} chart saved: {filename}")
    except Exception as e:
        print(f"⚠️ Error generating {title}: {e}")

print(f"\n🎨 Generated {len(generated)} TradingView-style charts!")
print("📁 Files:", ', '.join(generated))
