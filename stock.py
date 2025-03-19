import yfinance as yf
import pandas as pd
import numpy as np
import talib
import json

# Function to fetch stock data and calculate indicators
def get_stock_signals(stock_list, period="5d", interval="5m"):
    results = {}
    
    for stock in stock_list:
        try:
            # Fetching data from Yahoo Finance
            ticker = yf.Ticker(stock + ".NS") # .NS for NSE stocks
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                results[stock] = "Data not available"
                continue
            
            # Calculate Indicators
            # 1. Simple Moving Average (SMA) - 50 period
            df['SMA50'] = talib.SMA(df['Close'], timeperiod=50)
            # 2. Simple Moving Average (SMA) - 200 period
            df['SMA200'] = talib.SMA(df['Close'], timeperiod=200)
            # 3. Relative Strength Index (RSI) - 14 period
            df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
            
            # Latest values
            latest_close = df['Close'].iloc[-1]
            latest_sma50 = df['SMA50'].iloc[-1]
            latest_sma200 = df['SMA200'].iloc[-1] if not np.isnan(df['SMA200'].iloc[-1]) else 0
            latest_rsi = df['RSI'].iloc[-1]
            
            # Buy Signal Logic
            # 1. Price > SMA50 (short-term bullish)
            # 2. SMA50 > SMA200 (long-term bullish trend)
            # 3. RSI between 30 and 70 (not overbought/oversold)
            buy_signal = (latest_close > latest_sma50) and \
                         (latest_sma50 > latest_sma200) and \
                         (30 < latest_rsi < 70)
            
            # Store result
            results[stock] =  {
                "Close": str(round(latest_close, 2)),
                "SMA50": str(round(latest_sma50, 2)),
                "SMA200": str(round(latest_sma200, 2)),
                "RSI": str(round(latest_rsi, 2)),
                "Buy": "Yes" if buy_signal else "No"
            }
            
        except Exception as e:
            results[stock] = f"Error: {str(e)}"
    
    return results

def main():
    myList=["RELIANCE", "HINDALCO"
           ,"BAJAJFINSV"
           ,"TITAN"
           ,"ONGC"
           ,"TATACONSUM"
           ,"ADANIENT"
           ,"TRENT"
           ,"BAJFINANCE"
           ,"BHARTIARTL"
           ,"KOTAKBANK"
           ,"CIPLA"
           ,"RELIANCE"
           ,"HEROMOTOCO"
           ,"NESTLEIND"
           ,"MARUTI"
           ,"NTPC"
           ,"BRITANNIA"
           ,"BAJAJ-AUTO"
           ,"ITC"
           ,"LT"
           ,"TCS"
           ,"INDUSINDBK"
           ,"COALINDIA"
           ,"WIPRO"
           ,"ULTRACEMCO"
           ,"TATASTEEL"
           ,"APOLLOHOSP"
           ,"HDFCLIFE"
           ,"SHRIRAMFIN"
           ,"BAJAJHIND" ]
    print(get_stock_signals(myList))

if __name__ == '__main__':
    main()