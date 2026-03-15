import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def get_sector_stocks():
    """
    Define top sectors and their representative stocks
    In a real implementation, you would fetch actual sector constituents
    For now, we'll use some representative large-cap stocks from major sectors
    """
    # Major sectors with representative stocks (top 100 stocks across sectors)
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

def fetch_stock_data(symbol, period='1mo'):
    """
    Fetch historical data for a given stock symbol
    """
    try:
        stock = yf.Ticker(symbol)
        # Get daily data for the last month
        hist = stock.history(period=period)
        if hist.empty:
            print(f"No data found for {symbol}")
            return None
        return hist
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def calculate_camarilla_for_stock(symbol):
    """
    Calculate Camarilla pivots for a stock using recent data
    """
    hist = fetch_stock_data(symbol, period='1mo')
    if hist is None or len(hist) < 2:
        return None
    
    # Use the most recent complete day's data
    latest = hist.iloc[-1]
    prev_day = hist.iloc[-2] if len(hist) >= 2 else latest
    
    # Calculate pivots based on previous day's OHLC
    pivots = calculate_camarilla_pivots(
        prev_day['High'],
        prev_day['Low'],
        prev_day['Close']
    )
    
    return {
        'symbol': symbol,
        'date': hist.index[-1].strftime('%Y-%m-%d'),
        'close': latest['Close'],
        'prev_high': prev_day['High'],
        'prev_low': prev_day['Low'],
        'prev_close': prev_day['Close'],
        'pivots': pivots
    }

def main():
    """
    Main function to run the Camarilla strategy on top stocks
    """
    print("Starting Camarilla Pivot Strategy Analysis...")
    print("=" * 50)
    
    # Get list of stocks to analyze
    stocks = get_sector_stocks()
    print(f"Analyzing {len(stocks)} stocks across sectors...")
    
    results = []
    
    # Process each stock
    for i, symbol in enumerate(stocks, 1):
        print(f"Processing {symbol} ({i}/{len(stocks)})...")
        result = calculate_camarilla_for_stock(symbol)
        if result:
            results.append(result)
            # Print some key info
            pivots = result['pivots']
            print(f"  Close: ${result['close']:.2f}")
            print(f"  Pivot Points - PP: {pivots['PP']:.2f}, R1: {pivots['R1']:.2f}, S1: {pivots['S1']:.2f}")
            print(f"  Extended - R5: {pivots['R5']:.2f}, R6: {pivots['R6']:.2f}, S6: {pivots['S6']:.2f}")
        else:
            print(f"  Failed to get data for {symbol}")
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.1)
    
    # Save results to CSV
    if results:
        df_results = []
        for result in results:
            row = {
                'Symbol': result['symbol'],
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
        df.to_csv('camarilla_results.csv', index=False)
        print(f"\nResults saved to camarilla_results.csv")
        print(f"Successfully analyzed {len(results)} stocks")
        
        # Show top 5 results
        print("\nTop 5 Results:")
        print(df[['Symbol', 'Close', 'PP', 'R1', 'S1', 'R5', 'R6', 'S6']].head())
    
    return results

if __name__ == "__main__":
    results = main()