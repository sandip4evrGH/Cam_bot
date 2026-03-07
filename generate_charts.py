#!/usr/bin/env python3
"""
Camarilla Pivot Points Visual Chart Generator
Creates charts showing PP, H3, H4, L3, L4 levels for each asset
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
from datetime import datetime

# Load the weekly data
with open('camarilla_1w.json', 'r') as f:
    data = json.load(f)

def create_pivot_chart(asset_data, title, filename):
    """Create a horizontal bar chart showing pivot levels"""
    
    levels = ['L4', 'L3', 'PP', 'H3', 'H4']
    values = [
        float(asset_data['L4'].replace('$', '').replace(',', '')),
        float(asset_data['L3'].replace('$', '').replace(',', '')),
        float(asset_data['PP'].replace('$', '').replace(',', '')),
        float(asset_data['H3'].replace('$', '').replace(',', '')),
        float(asset_data['H4'].replace('$', '').replace(',', ''))
    ]
    
    # Colors for each level
    colors = ['#ff4444', '#ff8888', '#4444ff', '#88ff88', '#44ff44']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create horizontal bars
    bars = ax.barh(levels, values, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{val:,.2f}', 
                ha='left', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Styling
    ax.set_xlabel('Price Level', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nCamarilla Pivot Points - Weekly Timeframe', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add legend
    red_patch = mpatches.Patch(color='#ff4444', label='Support (L4)')
    pink_patch = mpatches.Patch(color='#ff8888', label='Support (L3)')
    blue_patch = mpatches.Patch(color='#4444ff', label='Pivot (PP)')
    green_patch = mpatches.Patch(color='#88ff88', label='Resistance (H3)')
    dark_green_patch = mpatches.Patch(color='#44ff44', label='Resistance (H4)')
    
    ax.legend(handles=[red_patch, pink_patch, blue_patch, green_patch, dark_green_patch],
              loc='upper right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return filename

# Create charts for top assets
print("📊 Generating Camarilla Pivot Charts...\n")

# Chart 1: S&P 500
es_data = next(item for item in data['futures'] if item['Code'] == 'ES')
create_pivot_chart(es_data, 'S&P 500 E-mini (ES)', 'chart_es.png')
print("✅ S&P 500 E-mini chart saved: chart_es.png")

# Chart 2: Bitcoin
btc_data = next(item for item in data['crypto'] if item['Code'] == 'BTC')
create_pivot_chart(btc_data, 'Bitcoin (BTC)', 'chart_btc.png')
print("✅ Bitcoin chart saved: chart_btc.png")

# Chart 3: Ethereum
eth_data = next(item for item in data['crypto'] if item['Code'] == 'ETH')
create_pivot_chart(eth_data, 'Ethereum (ETH)', 'chart_eth.png')
print("✅ Ethereum chart saved: chart_eth.png")

# Chart 4: Nasdaq
nq_data = next(item for item in data['futures'] if item['Code'] == 'NQ')
create_pivot_chart(nq_data, 'Nasdaq 100 E-mini (NQ)', 'chart_nq.png')
print("✅ Nasdaq 100 chart saved: chart_nq.png")

# Chart 5: Gold
gc_data = next(item for item in data['futures'] if item['Code'] == 'GC')
create_pivot_chart(gc_data, 'Gold (GC)', 'chart_gc.png')
print("✅ Gold chart saved: chart_gc.png")

print("\n🎨 All charts generated successfully!")
print("📁 Files: chart_es.png, chart_btc.png, chart_eth.png, chart_nq.png, chart_gc.png")
