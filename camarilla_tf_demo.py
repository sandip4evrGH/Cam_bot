import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def calculate_camarilla_pivots(high, low, close):
    """
    Calculate Camarilla pivot points for given high, low, close prices
    """
    # Standard Camarilla levels
    pp = (high + low + close) / 3
    range_val = high - low
    
    r1 = close + (range_val * 1.1 / 12)
    r2 = close + (range_val * 1.1 / 6)
    r3 = close + (range_val * 1.1 / 4)
    r4 = close + (range_val * 1.1 / 2)
    
    s1 = close - (range_val * 1.1 / 12)
    s2 = close - (range_val * 1.1 / 6)
    s3 = close - (range_val * 1.1 / 4)
    s4 = close - (range_val * 1.1 / 2)
    
    # Additional levels as specified
    r5 = r4 + 1.168 * (r4 - r3)
    r6 = (high / low) * close if low != 0 else close
    s6 = close - (r6 - close)
    
    return {
        'PP': pp,
        'R1': r1, 'R2': r2, 'R3': r3, 'R4': r4, 'R5': r5, 'R6': r6,
        'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s1 - (s2 - s1),
        'S6': s6
    }

def get_aggregated_data(symbol, timeframe):
    """
    Get aggregated data for different timeframes
    """
    try:
        stock = yf.Ticker(symbol)
        
        if timeframe == 'daily':
            hist = stock.history(period='2mo')
            if len(hist) < 2:
                return None
            latest = hist.iloc[-1]
            prev_day = hist.iloc[-2]
            return {
                'high': prev_day['High'],
                'low': prev_day['Low'],
                'close': prev_day['Close'],
                'date': hist.index[-2].strftime('%Y-%m-%d')
            }
            
        elif timeframe == 'weekly':
            hist = stock.history(period='6mo')
            if len(hist) < 10:
                return None
            weekly = hist.resample('W-FRI').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
            
            if len(weekly) < 2:
                return None
                
            latest = weekly.iloc[-1]
            prev_week = weekly.iloc[-2]
            return {
                'high': prev_week['High'],
                'low': prev_week['Low'],
                'close': prev_week['Close'],
                'date': weekly.index[-2].strftime('%Y-%m-%d')
            }
            
        elif timeframe == 'monthly':
            hist = stock.history(period='18mo')
            if len(hist) < 30:
                return None
            monthly = hist.resample('M').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
            
            if len(monthly) < 2:
                return None
                
            latest = monthly.iloc[-1]
            prev_month = monthly.iloc[-2]
            return {
                'high': prev_month['High'],
                'low': prev_month['Low'],
                'close': prev_month['Close'],
                'date': monthly.index[-2].strftime('%Y-%m-%d')
            }
            
        elif timeframe == 'quarterly':
            hist = stock.history(period='2y')
            if len(hist) < 60:
                return None
            quarterly = hist.resample('Q').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
            
            if len(quarterly) < 2:
                return None
                
            latest = quarterly.iloc[-1]
            prev_quarter = quarterly.iloc[-2]
            return {
                'high': prev_quarter['High'],
                'low': prev_quarter['Low'],
                'close': prev_quarter['Close'],
                'date': quarterly.index[-2].strftime('%Y-%m-%d')
            }
            
    except Exception as e:
        print(f"Error fetching {timeframe} data for {symbol}: {str(e)}")
        return None

def analyze_stocks_timeframes(symbols, timeframes):
    """
    Analyze multiple stocks across multiple timeframes
    """
    results = []
    
    for symbol in symbols:
        print(f"\nAnalyzing {symbol}:")
        print("-" * 30)
        
        for timeframe in timeframes:
            data = get_aggregated_data(symbol, timeframe)
            if data is None:
                print(f"  {timeframe.capitalize()}: Insufficient data")
                continue
            
            pivots = calculate_camarilla_pivots(
                data['high'],
                data['low'],
                data['close']
            )
            
            # Get current price
            try:
                stock = yf.Ticker(symbol)
                current_hist = stock.history(period='1d')
                current_price = current_hist.iloc[-1]['Close'] if not current_hist.empty else data['close']
            except:
                current_price = data['close']
            
            result = {
                'Symbol': symbol,
                'Timeframe': timeframe.capitalize(),
                'Date': data['date'],
                'Current_Price': current_price,
                'Prev_High': data['high'],
                'Prev_Low': data['low'],
                'Prev_Close': data['close'],
                'PP': pivots['PP'],
                'R1': pivots['R1'],
                'R2': pivots['R2'],
                'R3': pivots['R3'],
                'R4': pivots['R4'],
                'R5': pivots['R5'],
                'R6': pivots['R6'],
                'S1': pivots['S1'],
                'S2': pivots['S2'],
                'S3': pivots['S3'],
                'S4': pivots['S4'],
                'S5': pivots['S5'],
                'S6': pivots['S6']
            }
            
            results.append(result)
            
            # Print key levels
            print(f"  {timeframe.capitalize()}: PP={pivots['PP']:.2f}, R1={pivots['R1']:.2f}, S1={pivots['S1']:.2f}")
            print(f"           R5={pivots['R5']:.2f}, R6={pivots['R6']:.2f}, S6={pivots['S6']:.2f}")
            
            time.sleep(0.5)  # Avoid rate limiting
    
    return results

def main():
    """
    Main function to demonstrate multi-timeframe Camarilla analysis
    """
    print("Multi-Timeframe Camarilla Pivot Analysis Demo")
    print("=" * 50)
    
    # Select representative stocks from different sectors
    stocks = [
        'AAPL',   # Technology
        'MSFT',   # Technology
        'JNJ',    # Healthcare
        'JPM',    # Financial
        'AMZN',   # Consumer Cyclical
        'PG',     # Consumer Defensive
        'XOM',    # Energy
        'CAT',    # Industrials
        'NEE',    # Utilities
        'AMT'     # Real Estate
    ]
    
    # Define timeframes (excluding HL1/HL2 as requested)
    timeframes = ['daily', 'weekly', 'monthly', 'quarterly']
    
    print(f"Analyzing {len(stocks)} stocks across {len(timeframes)} timeframes")
    print(f"Stocks: {', '.join(stocks)}")
    print(f"Timeframes: {', '.join([t.capitalize() for t in timeframes])}")
    
    # Run analysis
    results = analyze_stocks_timeframes(stocks, timeframes)
    
    # Save results
    if results:
        df = pd.DataFrame(results)
        df.to_csv('camarilla_multitimeframe_demo.csv', index=False)
        print(f"\nResults saved to camarilla_multitimeframe_demo.csv")
        print(f"Total analyses completed: {len(results)}")
        
        # Display results in a readable format
        print("\n" + "="*80)
        print("MULTI-TIMEFRAME CAMARILLA ANALYSIS RESULTS")
        print("="*80)
        
        for symbol in stocks:
            symbol_results = [r for r in results if r['Symbol'] == symbol]
            if symbol_results:
                print(f"\n{symbol}:")
                print("-" * 20)
                for result in symbol_results:
                    tf = result['Timeframe']
                    print(f"  {tf:>9}: PP={result['PP']:6.2f} | R1={result['R1']:6.2f} | S1={result['S1']:6.2f} | "
                          f"R5={result['R5']:6.2f} | R6={result['R6']:6.2f} | S6={result['S6']:6.2f}")
    
    return results

if __name__ == "__main__":
    results = main()