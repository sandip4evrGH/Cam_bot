#!/usr/bin/env python3
"""
Clean Pivot Chart Style - Minimalist Design
Matches TradingView clean aesthetic
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import json
from datetime import datetime
import yfinance as yf

# Load the weekly data
with open('camarilla_1w.json', 'r') as f:
    data = json.load(f)

def fetch_recent_data(symbol, period='1mo'):
    """Fetch recent price data for charting"""
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval='1d')
    return hist

def create_clean_chart(symbol_code, asset_data, title, filename):
    """Create clean minimalist chart matching the reference style"""
    
    # Get symbol mapping
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
    price_data = fetch_recent_data(symbol, period='3mo')
    
    if price_data.empty:
        print(f"⚠️ No price data for {symbol_code}")
        return None
    
    # Parse pivot levels
    pp = float(asset_data['PP'].replace('$', '').replace(',', ''))
    h3 = float(asset_data['H3'].replace('$', '').replace(',', ''))
    h4 = float(asset_data['H4'].replace('$', '').replace(',', ''))
    l3 = float(asset_data['L3'].replace('$', '').replace(',', ''))
    l4 = float(asset_data['L4'].replace('$', '').replace(',', ''))
    
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
    ax.set_facecolor('white')
    
    # Get price range for y-axis
    price_min = price_data['Low'].min()
    price_max = price_data['High'].max()
    
    # Add some padding
    y_range = price_max - price_min
    y_min = min(l4 * 0.98, price_min - y_range * 0.05)
    y_max = max(h4 * 1.02, price_max + y_range * 0.05)
    
    # Plot candlesticks
    for i, (date, row) in enumerate(price_data.iterrows()):
        open_p = row['Open']
        high_p = row['High']
        low_p = row['Low']
        close_p = row['Close']
        
        # Determine color
        if close_p >= open_p:
            color = '#26a69a'  # Green for bullish
            edgecolor = '#26a69a'
        else:
            color = '#ef5350'  # Red for bearish
            edgecolor = '#ef5350'
        
        # Draw wick
        ax.plot([i, i], [low_p, high_p], color='black', linewidth=0.8)
        
        # Draw body
        height = abs(close_p - open_p)
        bottom = min(open_p, close_p)
        
        if height == 0:  # Doji
            ax.plot([i-0.3, i+0.3], [open_p, open_p], color='black', linewidth=1)
        else:
            rect = plt.Rectangle((i-0.4, bottom), 0.8, height, 
                                facecolor=color, edgecolor=edgecolor, linewidth=1)
            ax.add_patch(rect)
    
    last_idx = len(price_data) - 1
    future_idx = last_idx + 8
    
    # Plot pivot levels with clean horizontal lines
    # L4 - Deep Support (Red)
    ax.hlines(l4, xmin=0, xmax=future_idx, colors='#d32f2f', linewidth=1.5, 
              linestyle='-', alpha=0.8)
    ax.text(future_idx + 0.5, l4, f'L4  {l4:,.2f}', fontsize=10, color='#d32f2f', 
            va='center', fontweight='bold')
    
    # L3 - Support (Orange)
    ax.hlines(l3, xmin=0, xmax=future_idx, colors='#f57c00', linewidth=1.5, 
              linestyle='-', alpha=0.8)
    ax.text(future_idx + 0.5, l3, f'L3  {l3:,.2f}', fontsize=10, color='#f57c00', 
            va='center', fontweight='bold')
    
    # PP - Pivot (Blue)
    ax.hlines(pp, xmin=0, xmax=future_idx, colors='#1976d2', linewidth=2.5, 
              linestyle='-', alpha=0.9)
    ax.text(future_idx + 0.5, pp, f'PP  {pp:,.2f}', fontsize=11, color='#1976d2', 
            va='center', fontweight='bold')
    
    # H3 - Resistance (Green)
    ax.hlines(h3, xmin=0, xmax=future_idx, colors='#388e3c', linewidth=1.5, 
              linestyle='-', alpha=0.8)
    ax.text(future_idx + 0.5, h3, f'H3  {h3:,.2f}', fontsize=10, color='#388e3c', 
            va='center', fontweight='bold')
    
    # H4 - Strong Resistance (Dark Green)
    ax.hlines(h4, xmin=0, xmax=future_idx, colors='#2e7d32', linewidth=1.5, 
              linestyle='-', alpha=0.8)
    ax.text(future_idx + 0.5, h4, f'H4  {h4:,.2f}', fontsize=10, color='#2e7d32', 
            va='center', fontweight='bold')
    
    # Add current price line
    current_price = price_data['Close'].iloc[-1]
    ax.axvline(x=last_idx, color='#666666', linewidth=1.5, linestyle='--', alpha=0.7)
    
    # Add subtle background zones
    ax.axhspan(l4, l3, alpha=0.05, color='red', label='Support Zone')
    ax.axhspan(h3, h4, alpha=0.05, color='green', label='Resistance Zone')
    
    # Styling
    ax.set_title(f'{title} - Camarilla Pivot Points (Weekly)', 
                 fontsize=16, fontweight='bold', color='#333333', pad=15)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    
    # Grid
    ax.grid(True, alpha=0.3, color='#e0e0e0', linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Format y-axis
    ax.tick_params(colors='#666666', labelsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Set limits
    ax.set_xlim(-1, future_idx + 8)
    ax.set_ylim(y_min, y_max)
    
    # Remove x-axis labels (dates not needed for this chart style)
    ax.set_xticks([])
    
    # Add legend box
    legend_elements = [
        mpatches.Patch(color='#2e7d32', label='H4 Resistance'),
        mpatches.Patch(color='#388e3c', label='H3 Resistance'),
        mpatches.Patch(color='#1976d2', label='PP Pivot'),
        mpatches.Patch(color='#f57c00', label='L3 Support'),
        mpatches.Patch(color='#d32f2f', label='L4 Support')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9, 
             framealpha=0.9, edgecolor='#cccccc')
    
    # Add timestamp
    fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}', 
             ha='right', fontsize=8, color='#999999')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return filename

print("📊 Generating Clean Style Camarilla Charts...\n")

# Generate charts for top assets
charts_to_generate = [
    ('ES', 'S&P 500 E-mini', 'clean_chart_es.png'),
    ('BTC', 'Bitcoin', 'clean_chart_btc.png'),
    ('ETH', 'Ethereum', 'clean_chart_eth.png'),
    ('NQ', 'Nasdaq 100 E-mini', 'clean_chart_nq.png'),
    ('GC', 'Gold', 'clean_chart_gc.png'),
    ('CL', 'Crude Oil', 'clean_chart_cl.png'),
]

generated = []
for code, title, filename in charts_to_generate:
    try:
        if code in ['ES', 'NQ', 'YM', 'RTY', 'CL', 'GC', 'SI', 'ZC', 'ZS', 'ZN']:
            asset_data = next((item for item in data['futures'] if item['Code'] == code), None)
        else:
            asset_data = next((item for item in data['crypto'] if item['Code'] == code), None)
        
        if asset_data:
            result = create_clean_chart(code, asset_data, title, filename)
            if result:
                generated.append(filename)
                print(f"✅ {title} chart saved: {filename}")
    except Exception as e:
        print(f"⚠️ Error generating {title}: {e}")

print(f"\n🎨 Generated {len(generated)} clean style charts!")
print("📁 Files:", ', '.join(generated))
