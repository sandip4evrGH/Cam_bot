import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def get_sector_stocks():
    """
    Define top sectors and their representative stocks
    """
    sector_stocks = {
        'Technology': ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'AVGO', 'ORCL', 'CRM', 'ADBE', 'INTC'],
        'Healthcare': ['JNJ', 'UNH', 'LLY', 'PFE', 'ABT', 'TMO', 'DHR', 'BMY', 'AMGN', 'GILD'],
        'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'BLK', 'SCHW', 'CB'],
        'Consumer Cyclical': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'GM'],
        'Consumer Defensive': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CL', 'PM', 'MO', 'KMB', 'GIS'],
        'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'KMI', 'VLO', 'PSX', 'MPC', 'OXY'],
        'Industrials': ['HON', 'UPS', 'RTX', 'CAT', 'DE', 'GE', 'MMM', 'LMT', 'UBER', 'FDX'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL', 'WEC', 'ETR', 'AWK'],
        'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'O', 'DLR', 'WY', 'CBRE', 'SPG'],
        'Basic Materials': ['LIN', 'APD', 'ECL', 'SHW', 'FCX', 'NEM', 'DD', 'PPG', 'IFF', 'ALB'],
        'Communication Services': ['GOOGL', 'META', 'NFLX', 'DIS', 'CMCSA', 'VZ', 'T', 'CHTR', 'TMUS', 'ATVI']
    }
    
    # Flatten the list and remove duplicates
    all_stocks = []
    for stocks in sector_stocks.values():
        all_stocks.extend(stocks)
    
    # Remove duplicates while preserving order
    unique_stocks = list(dict.fromkeys(all_stocks))
    
    # Return top 100 stocks
    return unique_stocks[:100]

def calculate_camarilla_pivots(high, low, close):
    """
    Calculate Camarilla pivot points for given high, low, close prices
    
    Formula:
    PP = (High + Low + Close) / 3
    R1 = Close + ((High - Low) * 1.1 / 12)
    R2 = Close + ((High - Low) * 1.1 / 6)
    R3 = Close + ((High - Low) * 1.1 / 4)
    R4 = Close + ((High - Low) * 1.1 / 2)
    S1 = Close - ((High - Low) * 1.1 / 12)
    S2 = Close - ((High - Low) * 1.1 / 6)
    S3 = Close - ((High - Low) * 1.1 / 4)
    S4 = Close - ((High - Low) * 1.1 / 2)
    
    Additional levels as mentioned:
    R5 = R4 + 1.168 * (R4 - R3)
    R6 = (PP_high / PP_low) * PP_close  # Using previous period's values
    S6 = PP_close - (R6 - PP_close)
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
    # For R6 and S6, we'll use the same period's values as approximation
    # In practice, you'd use previous period's high/low/close
    r6 = (high / low) * close if low != 0 else close
    s6 = close - (r6 - close)
    
    return {
        'PP': pp,
        'R1': r1, 'R2': r2, 'R3': r3, 'R4': r4, 'R5': r5, 'R6': r6,
        'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s1 - (s2 - s1),  # S5 following pattern
        'S6': s6
    }

def get_timeframe_data(symbol, timeframe):
    """
    Get aggregated data for different timeframes
    """
    try:
        stock = yf.Ticker(symbol)
        
        if timeframe == 'daily':
            # Get last 2 months of daily data to ensure we have enough for calculation
            hist = stock.history(period='2mo')
            if len(hist) < 2:
                return None
            # Use most recent completed day
            latest = hist.iloc[-1]
            prev_day = hist.iloc[-2]
            return {
                'high': prev_day['High'],
                'low': prev_day['Low'],
                'close': prev_day['Close'],
                'date': hist.index[-2].strftime('%Y-%m-%d')  # Previous day's date
            }
            
        elif timeframe == 'weekly':
            # Get last 6 months of weekly data
            hist = stock.history(period='6mo')
            if len(hist) < 5:  # Need at least a week
                return None
            # Resample to weekly (Friday close)
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
                'date': weekly.index[-2].strftime('%Y-%m-%d')  # Previous week's end date
            }
            
        elif timeframe == 'monthly':
            # Get last 18 months of monthly data
            hist = stock.history(period='18mo')
            if len(hist) < 30:  # Need at least a month
                return None
            # Resample to monthly (month end)
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
                'date': monthly.index[-2].strftime('%Y-%m-%d')  # Previous month's end date
            }
            
        elif timeframe == 'quarterly':
            # Get last 2 years of quarterly data
            hist = stock.history(period='2y')
            if len(hist) < 60:  # Need at least a quarter
                return None
            # Resample to quarterly (quarter end)
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
                'date': quarterly.index[-2].strftime('%Y-%m-%d')  # Previous quarter's end date
            }
            
    except Exception as e:
        print(f"Error fetching {timeframe} data for {symbol}: {str(e)}")
        return None

def calculate_camarilla_for_timeframe(symbol, timeframe):
    """
    Calculate Camarilla pivots for a stock using specified timeframe
    """
    data = get_timeframe_data(symbol, timeframe)
    if data is None:
        return None
    
    # Calculate pivots based on previous period's OHLC
    pivots = calculate_camarilla_pivots(
        data['high'],
        data['low'],
        data['close']
    )
    
    # Get current price (most recent close)
    try:
        stock = yf.Ticker(symbol)
        current_hist = stock.history(period='1d')
        current_price = current_hist.iloc[-1]['Close'] if not current_hist.empty else data['close']
    except:
        current_price = data['close']
    
    return {
        'symbol': symbol,
        'timeframe': timeframe,
        'date': data['date'],
        'close': current_price,
        'prev_high': data['high'],
        'prev_low': data['low'],
        'prev_close': data['close'],
        'pivots': pivots
    }

def main():
    """
    Main function to run the Camarilla strategy on multiple timeframes
    """
    print("Starting Multi-Timeframe Camarilla Pivot Strategy Analysis...")
    print("=" * 60)
    
    # Get list of stocks to analyze
    stocks = get_sector_stocks()
    print(f"Analyzing {len(stocks)} stocks across sectors...")
    
    # Define timeframes to analyze
    timeframes = ['daily', 'weekly', 'monthly', 'quarterly']
    print(f"Timeframes: {', '.join(timeframes)}")
    
    all_results = []
    
    # Process each timeframe
    for timeframe in timeframes:
        print(f"\nProcessing {timeframe.upper()} timeframe...")
        print("-" * 40)
        
        timeframe_results = []
        
        # Process each stock for this timeframe
        for i, symbol in enumerate(stocks, 1):
            if i % 20 == 0:  # Progress update every 20 stocks
                print(f"  Processing {symbol} ({i}/{len(stocks)})...")
            
            result = calculate_camarilla_for_timeframe(symbol, timeframe)
            if result:
                timeframe_results.append(result)
        
        print(f"  Completed {timeframe.upper()}: {len(timeframe_results)} stocks processed")
        all_results.extend(timeframe_results)
        
        # Add delay between timeframes to avoid rate limiting
        time.sleep(1)
    
    # Save results to CSV
    if all_results:
        df_results = []
        for result in all_results:
            row = {
                'Symbol': result['symbol'],
                'Timeframe': result['timeframe'].capitalize(),
                'Date': result['date'],
                'Close': result['close'],
                'Prev_High': result['prev_high'],
                'Prev_Low': result['prev_low'],
                'Prev_Close': result['prev_close'],
                'PP': result['pivots']['PP'],
                'R1': result['pivots']['R1'],
                'R2': result['pivots']['R2'],
                'R3': result['pivots']['R3'],
                'R4': result['pivots']['R4'],
                'R5': result['pivots']['R5'],
                'R6': result['pivots']['R6'],
                'S1': result['pivots']['S1'],
                'S2': result['pivots']['S2'],
                'S3': result['pivots']['S3'],
                'S4': result['pivots']['S4'],
                'S5': result['pivots']['S5'],
                'S6': result['pivots']['S6']
            }
            df_results.append(row)
        
        df = pd.DataFrame(df_results)
        df.to_csv('camarilla_multitimeframe_results.csv', index=False)
        print(f"\nResults saved to camarilla_multitimeframe_results.csv")
        print(f"Successfully analyzed {len(all_results)} stock-timeframe combinations")
        
        # Show summary by timeframe
        summary = df.groupby('Timeframe').size().reset_index(name='Count')
        print("\nAnalysis Summary by Timeframe:")
        print(summary)
        
        # Show sample results
        print(f"\nSample Results (first 5 rows):")
        print(df[['Symbol', 'Timeframe', 'Close', 'PP', 'R1', 'S1', 'R5', 'R6', 'S6']].head())
    
    return all_results

if __name__ == "__main__":
    results = main()