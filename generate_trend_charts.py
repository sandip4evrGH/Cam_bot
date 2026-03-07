#!/usr/bin/env python3
"""
Historical Pivot Trends Chart
Shows PP, H3, L3 trends over last 3 weeks
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from datetime import datetime

# Load historical data
with open('camarilla_historical.json', 'r') as f:
    data = json.load(f)

def create_trend_chart(code, asset_info, title, filename):
    """Create trend chart showing pivot evolution"""
    
    periods = ['2 Weeks Ago', '1 Week Ago', 'Current Week']
    dates = []
    pp_values = []
    h3_values = []
    l3_values = []
    
    for period in periods:
        if period in asset_info['data']:
            dates.append(asset_info['data'][period]['date'])
            pp_values.append(asset_info['data'][period]['PP'])
            h3_values.append(asset_info['data'][period]['H3'])
            l3_values.append(asset_info['data'][period]['L3'])
    
    if len(dates) < 2:
        return None
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    ax.set_facecolor('white')
    
    x = range(len(dates))
    
    # Plot lines
    ax.plot(x, h3_values, 'g-o', linewidth=2.5, markersize=8, label='H3 (Resistance)', color='#2e7d32')
    ax.plot(x, pp_values, 'b-s', linewidth=3, markersize=10, label='PP (Pivot)', color='#1976d2')
    ax.plot(x, l3_values, 'r-^', linewidth=2.5, markersize=8, label='L3 (Support)', color='#d32f2f')
    
    # Fill zones
    ax.fill_between(x, l3_values, pp_values, alpha=0.1, color='blue', label='Support Zone')
    ax.fill_between(x, pp_values, h3_values, alpha=0.1, color='green', label='Resistance Zone')
    
    # Add value labels on points
    for i, (h3, pp, l3) in enumerate(zip(h3_values, pp_values, l3_values)):
        ax.annotate(f'{h3:,.0f}', (i, h3), textcoords="offset points", xytext=(0,10), 
                   ha='center', fontsize=9, color='#2e7d32', fontweight='bold')
        ax.annotate(f'{pp:,.0f}', (i, pp), textcoords="offset points", xytext=(0,10), 
                   ha='center', fontsize=10, color='#1976d2', fontweight='bold')
        ax.annotate(f'{l3:,.0f}', (i, l3), textcoords="offset points", xytext=(0,-15), 
                   ha='center', fontsize=9, color='#d32f2f', fontweight='bold')
    
    # Calculate trend
    if len(pp_values) >= 2:
        trend = pp_values[-1] - pp_values[-2]
        trend_pct = (trend / pp_values[-2]) * 100
        trend_text = f"+{trend_pct:.2f}% 📈" if trend > 0 else f"{trend_pct:.2f}% 📉"
        trend_color = '#2e7d32' if trend > 0 else '#d32f2f'
    else:
        trend_text = "N/A"
        trend_color = '#666666'
    
    # Title with trend
    ax.set_title(f'{title}\nCamarilla Pivot Trends (3 Weeks) | Weekly Change: {trend_text}', 
                 fontsize=14, fontweight='bold', color='#333333', pad=20)
    
    # X-axis
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=0, fontsize=10)
    ax.set_xlabel('Week', fontsize=11, fontweight='bold')
    
    # Y-axis
    ax.set_ylabel('Price Level', fontsize=11, fontweight='bold')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--', color='#cccccc')
    ax.set_axisbelow(True)
    
    # Legend
    ax.legend(loc='best', fontsize=10, framealpha=0.9, edgecolor='#cccccc')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add timestamp
    fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}', 
             ha='right', fontsize=8, color='#999999')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return filename

print("📊 Generating Historical Pivot Trend Charts...\n")

# Generate charts for top assets
charts_to_generate = [
    ('ES', 'futures', 'S&P 500 E-mini', 'trend_es.png'),
    ('BTC', 'crypto', 'Bitcoin', 'trend_btc.png'),
    ('ETH', 'crypto', 'Ethereum', 'trend_eth.png'),
    ('NQ', 'futures', 'Nasdaq 100 E-mini', 'trend_nq.png'),
    ('CL', 'futures', 'Crude Oil', 'trend_cl.png'),
    ('GC', 'futures', 'Gold', 'trend_gc.png'),
]

generated = []
for code, category, title, filename in charts_to_generate:
    try:
        if code in data[category]:
            result = create_trend_chart(code, data[category][code], title, filename)
            if result:
                generated.append(filename)
                print(f"✅ {title} trend chart saved: {filename}")
    except Exception as e:
        print(f"⚠️ Error generating {title}: {e}")

print(f"\n🎨 Generated {len(generated)} trend charts!")
print("📁 Files:", ', '.join(generated))
