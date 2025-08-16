import requests
import pandas as pd
import backtesting_simulator
import json


APIKEY = "8RUS0YURXTPQQYEM"     # Alpha Vantage API Key (Solomon)
K = 2                           # K: number of standard deviations away from MA

def main():
    #################################################################################  
    ###################### Retrieve financial data from API #########################
    #################################################################################  

    # Get Ticker, Initial Capital & Time
    ticker = input("Ticker: ")
    time_length = int(input("Length of time (days): "))
    amount = int(input("Initial Amount: "))
    risk_free_rate = int(input("Risk-Free Rate (Annual): "))

    # Get closing price
    stock_info = api_call_stock(ticker)
    # Get 20-day moving average (MA) for Bollinger Band calculation
    moving_avg_20 = api_call_technical("EMA", ticker, "20")
    # Get RSI (Relative Strength Indicator) for momentum (overselling/overbuying)
    rsi = api_call_technical("RSI", ticker, "14")
    # Get 200-day & 50-day moving average (MA) for long term trend calculation (golden/death cross)
    moving_avg_200 = api_call_technical("EMA", ticker, "200")
    moving_avg_50 = api_call_technical("EMA", ticker, "50")
    
    # print(json.dumps(stock_info, indent=2))
    # print(json.dumps(rsi, indent=2))
    # print(json.dumps(moving_avg_20, indent=2))
    # print(json.dumps(moving_avg_200, indent=2))
    # print(json.dumps(moving_avg_50, indent=2))

    #################################################################################   
    ###################### Convert JSON to DataFrames ###############################
    #################################################################################  

    # Financial data cleaning & preprocessing
    df_stock_current = get_stock_past_n_days(stock_info, time_length)
    list_stock_std_dev = calc_std_dev(stock_info, 20) # std dev shld be same time period as MA
    df_ema_20 = convert_technical_json_to_dataframe("EMA", moving_avg_20, time_length)
    
    df_rsi_14 = convert_technical_json_to_dataframe("RSI", rsi, time_length)
    df_ema_200 = convert_technical_json_to_dataframe("EMA", moving_avg_200, time_length)
    df_ema_50 = convert_technical_json_to_dataframe("EMA", moving_avg_50, time_length)
    
    # print(list_stock_std_dev)
    # print(df_stock_current)
    # print(df_ema_20)
    # print(df_ema_200)
    # print(df_ema_50)

    #################################################################################   
    ########### Calculate technicals, generate signals and backtest #################
    #################################################################################
    
    # Calculate Bollinger Bands
    list_bollinger_bands = calc_bollinger_bands(list_stock_std_dev, df_ema_20)
    # Calculate RSI
    list_rsi = calc_rsi(df_rsi_14)
    # print(list_bollinger_bands)
    # print(list_rsi)
        
    # Generate buy/sell/hold signal
    trade_signals = trade_engine(df_stock_current, df_ema_20, list_bollinger_bands, list_rsi, df_ema_200, df_ema_50)

    # Simulate trades using backtester
    simulation = backtesting_simulator.simulate(df_stock_current, trade_signals, amount, risk_free_rate)
    
    # #################################################################################   
    # ###################### Display Metrics & Data ###################################
    # #################################################################################

    status = backtesting_simulator.display(simulation, ticker)
    if status != "Success":
        print("Failed")
    print(status)


def trade_engine(stock_close, ema_20, bollinger_bands, rsi, ema_200, ema_50):
    signal = []
    idx = 0
    for date, price in stock_close.iterrows():
        current_price = price["Close"]
        
        limits = bollinger_bands[idx]
        upper = limits["upper"]
        lower = limits["lower"]

        current_rsi = rsi[idx]

        ema_200_list = ema_200["EMA"].tolist()
        ema_50_list = ema_50["EMA"].tolist()
        ema_20_list = ema_20["EMA"].tolist()
        curr_ema_200 = ema_200_list[idx]
        curr_ema_50 = ema_50_list[idx]
        curr_ema_20 = ema_20_list[idx]

        # Entry rules
        if current_price < lower and current_rsi < 30 and curr_ema_50 > curr_ema_200:
            signal.append({date: "Enter Long"})
            idx += 1
            continue    
        
        if current_price > upper and current_rsi > 70 and curr_ema_50 < curr_ema_200:
            signal.append({date: "Enter Short"})
            idx += 1
            continue

        # Exit
        if current_price >= curr_ema_20:
            signal.append({date: "Exit Long"})
            idx += 1
            continue

        if current_price <= curr_ema_20:
            signal.append({date: "Exit Short"})
            idx += 1
            continue

        signal.append({date: "Hold"})
        idx += 1

    return signal


def api_call_stock(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={APIKEY}"
    r = requests.get(url)
    if r.status_code != 200:
        print("API call failed with status code:", r.status_code)
    return r.json()

def api_call_technical(indicator, ticker, period):
    url = f"https://www.alphavantage.co/query?function={indicator}&symbol={ticker}&interval=daily&time_period={period}&series_type=close&apikey={APIKEY}"
    r = requests.get(url)
    if r.status_code != 200:
        print("API call failed with status code:", r.status_code)
    return r.json()

def convert_technical_json_to_dataframe(indicator, json, days):
    df = pd.DataFrame.from_dict(json[f"Technical Analysis: {indicator}"], orient="index")
    df = df.sort_index() # sorted in ascending (oldest date first)
    df = df.astype(float)  # Convert all values to float
    df = df.tail(days) # 252 is 1 trading year
    return df

def get_stock_past_n_days(json, days):
    df = pd.DataFrame.from_dict(json["Time Series (Daily)"], orient="index")
    df = df.sort_index() # sorted in ascending (oldest date first)
    df = df[["4. close"]].astype(float).rename(columns={"4. close" : "Close"})
    df = df.tail(days) # 252 is 1 trading year
    return df

def calc_std_dev(json, days):
    std_dev = []

    df = pd.DataFrame.from_dict(json["Time Series (Daily)"], orient="index")
    df = df.sort_index() # sorted in ascending (oldest date first)
    df = df[["4. close"]].astype(float).rename(columns={"4. close" : "Close"})

    # Handle NaN: forward fill, then backward fill if first value is NaN
    df["Close"] = df["Close"].ffill().bfill()

    base_df = df.copy()

    for day in range(days):
        temp_df = base_df.tail(days + 20 - day)
        df_oldest_n_days = temp_df.tail(-1 * days)
        std_dev_curr = df_oldest_n_days["Close"].std(ddof=1)
        std_dev.append(std_dev_curr)
    
    return std_dev

def calc_rsi(rsi_df):
    rsi = []
    for rsi_daily in rsi_df["RSI"]:
        rsi.append(rsi_daily)

    return rsi

def calc_bollinger_bands(std_dev_list, ema_20_df):
    bollinger_bands = []
    for i, ema_curr in enumerate(ema_20_df["EMA"]):
        # print(ema_curr, type(ema_curr))
        # print(std_dev_list[i], type(std_dev_list[i]))
        std_dev_curr = std_dev_list[i]
        upper_limit = ema_curr + std_dev_curr
        lower_limit = ema_curr - std_dev_curr
        bollinger_bands.append({"upper": upper_limit, "lower": lower_limit})

    return bollinger_bands


if __name__ == "__main__":
    main()