# Camarilla Pivot Strategy Analysis

## Overview
This project implements the Camarilla pivot point strategy to analyze stock data from Yahoo Finance. The Camarilla formula is a set of support and resistance levels used by traders to identify potential turning points in the market.

## What We Accomplished
1. **Data Collection**: Fetched historical daily data for 100 stocks across 11 major sectors using Yahoo Finance
2. **Camarilla Calculation**: Implemented the Camarilla pivot point formulas including:
   - Standard levels: PP, R1-R4, S1-S4
   - Extended levels: R5, R6, S5, S6 as specified in the requirements
3. **Analysis**: Calculated pivot points for each stock based on previous day's OHLC data
4. **Results**: Saved all results to a CSV file for further analysis

## Camarilla Formulas Used

### Standard Camarilla Levels:
- **PP (Pivot Point)** = (High + Low + Close) / 3
- **R1** = Close + ((High - Low) × 1.1 / 12)
- **R2** = Close + ((High - Low) × 1.1 / 6)
- **R3** = Close + ((High - Low) × 1.1 / 4)
- **R4** = Close + ((High - Low) × 1.1 / 2)
- **S1** = Close - ((High - Low) × 1.1 / 12)
- **S2** = Close - ((High - Low) × 1.1 / 6)
- **S3** = Close - ((High - Low) × 1.1 / 4)
- **S4** = Close - ((High - Low) × 1.1 / 2)

### Extended Levels (as requested):
- **R5** = R4 + 1.168 × (R4 - R3)
- **R6** = (Previous High / Previous Low) × Previous Close
- **S6** = Previous Close - (R6 - Previous Close)
- **S5** = S1 - (S2 - S1) [following the same pattern as R5]

## Files Generated
- `camarilla_strategy.py`: Main Python script implementing the strategy
- `camarilla_results.csv`: CSV file containing all calculated pivot points for 100 stocks
- `requirements.txt`: Python dependencies (yfinance, pandas, numpy)
- `README.md`: This documentation file

## Key Insights from Results
The analysis shows pivot point levels for major stocks including:
- **Technology**: AAPL, MSFT, NVDA, GOOGL, META
- **Healthcare**: JNJ, UNH, LLY, PFE
- **Financial**: JPM, BAC, WFC, GS
- And 8 other sectors

Each stock shows:
- Current closing price
- Pivot Point (PP) - the main equilibrium level
- Resistance levels (R1-R6) - potential upward barriers
- Support levels (S1-S6) - potential downward barriers

## How to Use This Analysis
1. **Intraday Trading**: Traders watch for price action around these levels
2. **Breakout Trading**: Moves beyond R4 or S4 often indicate strong momentum
3. **Reversal Trading**: Price approaching R3/S3 or R4/S4 may signal exhaustion
4. **Stop Loss Placement**: Orders can be placed just beyond support/resistance levels

## Next Steps
To build upon this foundation, we could:
1. Add real-time scanning for breakouts/breakdowns
2. Implement backtesting to validate strategy effectiveness
3. Add volume confirmation filters
4. Create alert systems for when prices approach key levels
5. Integrate with brokerage APIs for automated trading

## Dependencies
- Python 3.12+
- yfinance (for Yahoo Finance data)
- pandas (for data manipulation)
- numpy (for numerical calculations)

Install with: `pip install -r requirements.txt` (in virtual environment)

## Disclaimer
This analysis is for educational purposes only. Past performance does not guarantee future results. Always conduct your own research and consider consulting with a financial advisor before making investment decisions.