import yfinance as yf
import pandas as pd
import numpy as np
import talib
import time

def get_stock_signals(stock_list, period="1d", interval="5m", profit_target=1.5, stop_loss=1.0):
    results = {}
    
    for stock in stock_list:
        try:
            ticker = yf.Ticker(stock + ".NS")
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                results[stock] = "Data not available"
                continue
            
            # Calculate Indicators
            df['SMA20'] = talib.SMA(df['Close'], timeperiod=20)
            df['SMA50'] = talib.SMA(df['Close'], timeperiod=50)
            df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
            
            # Latest values
            latest_close = df['Close'].iloc[-1]
            latest_sma20 = df['SMA20'].iloc[-1]
            latest_sma50 = df['SMA50'].iloc[-1]
            latest_rsi = df['RSI'].iloc[-1]
            
            # Buy Signal Logic
            buy_signal = (latest_close > latest_sma20) and \
                         (latest_sma20 > latest_sma50) and \
                         (30 < latest_rsi < 70)
            
            # Sell Signal Logic
            sell_signal = (latest_close < latest_sma20) or \
                          (latest_sma20 < latest_sma50) or \
                          (latest_rsi > 70 or latest_rsi < 30)
            
            # Action and Trade Details
            if buy_signal and not sell_signal:
                action = "Buy"
                entry_price = latest_close
                target_price = entry_price * (1 + profit_target / 100)  # Profit target %
                stop_loss_price = entry_price * (1 - stop_loss / 100)   # Stop loss %
                trailing_stop = stop_loss_price  # Initial trailing stop
            elif sell_signal and not buy_signal:
                action = "Sell"
                entry_price = latest_close
                target_price = None
                stop_loss_price = None
                trailing_stop = None
            else:
                action = "Hold"
                entry_price = latest_close
                target_price = None
                stop_loss_price = None
                trailing_stop = None
            
            # Trailing Stop Logic (only for Buy)
            if action == "Buy":
                max_price = df['Close'].iloc[-5:].max()  # Last 5 candles ka high
                if max_price > entry_price:
                    trailing_stop = max_price * (1 - stop_loss / 100)  # Adjust trailing stop
            
            results[stock] = {
                "Close": round(latest_close, 2),
                "SMA20": round(latest_sma20, 2),
                "SMA50": round(latest_sma50, 2),
                "RSI": round(latest_rsi, 2),
                "Action": action,
                "Entry": round(entry_price, 2) if entry_price else None,
                "Target": round(target_price, 2) if target_price else None,
                "StopLoss": round(stop_loss_price, 2) if stop_loss_price else None,
                "TrailingStop": round(trailing_stop, 2) if trailing_stop else None
            }
            
        except Exception as e:
            results[stock] = f"Error: {str(e)}"
    
    return results

def print_signals(signals):
    print("\nIntraday Trading Signals (as of now):")
    print("-" * 70)
    for stock, data in signals.items():
        if isinstance(data, dict):
            print(f"Stock: {stock}")
            print(f"Close: {data['Close']}, SMA20: {data['SMA20']}, SMA50: {data['SMA50']}, RSI: {data['RSI']}")
            print(f"Action: {data['Action']}")
            if data['Action'] in ["Buy", "Sell"]:
                print(f"Entry: {data['Entry']}")
            if data['Action'] == "Buy":
                print(f"Target: {data['Target']}, Stop Loss: {data['StopLoss']}, Trailing Stop: {data['TrailingStop']}")
            print("-" * 70)
        else:
            print(f"Stock: {stock} - {data}")
            print("-" * 70)

if __name__ == "__main__":
    my_file = open("list", "r") 
    data = my_file.read() 
    data_into_list = data.replace('\n', '').replace('"', '').split(",")
    # stocks = ["TATAMOTORS", "RELIANCE", "SBIN", "VODIDEA", "JSWSTEEL"]
    stocks = data_into_list
    # Custom Parameters
    profit_target = 1.5  # 1.5% profit target
    stop_loss = 1.0      # 1% stop loss
    
    # Real-Time Loop
    while True:
        signals = get_stock_signals(stocks, profit_target=profit_target, stop_loss=stop_loss)
        print_signals(signals)
        print(f"Last updated: {time.ctime()}")
        time.sleep(300)  # Refresh every 5 minutes (300 seconds)