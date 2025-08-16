import pandas as pd
import numpy as np
from project import calc_bollinger_bands, calc_rsi, trade_engine

dates = [
        "2025-08-04", "2025-08-05", "2025-08-06", "2025-08-07", "2025-08-08",
        "2025-08-11", "2025-08-12", "2025-08-13", "2025-08-14", "2025-08-15"
    ]

def main():
    test_calc_bollinger_bands()
    test_calc_rsi()
    test_trade_engine()

def test_calc_bollinger_bands():
    # Data provided
    std_list = [1.23, 1.45, 1.67, 1.89, 2.01, 2.22, 2.43, 2.64, 2.85, 3.06]
    ema_values = [
        207.5836, 207.3916, 207.6118, 208.0889, 208.9124,
        209.6287, 210.4139, 211.3126, 212.1544, 212.9166
    ]

    # Create DataFrame
    df = pd.DataFrame(ema_values, index=pd.to_datetime(dates), columns=["EMA"])
    # print(df)
    # print(std_list)
    
    # Perform actual correct calculations
    test_bb = []
    for i, ema_curr in enumerate(df["EMA"]):
        std_dev_curr = std_list[i]
        upper_limit = ema_curr + std_dev_curr
        lower_limit = ema_curr - std_dev_curr
        test_bb.append({"upper": upper_limit, "lower": lower_limit})
    # print(test_bb)

    # Test calculate bollinger band function
    actl_bb = calc_bollinger_bands(std_list, df)
    # print(actl_bb)
    assert actl_bb == test_bb


def test_calc_rsi():
    sample_rsi = [55.2, 52.8, 57.1, 60.3, 63.5, 59.7, 62.1, 65.4, 67.8, 70.2]
    df = pd.DataFrame(sample_rsi, index=pd.to_datetime(dates), columns=['RSI'])
    # print(df)

    rsi = []
    for rsi_daily in df["RSI"]:
        rsi.append(rsi_daily)
    # print(rsi)

    assert calc_rsi(df) == rsi


def test_trade_engine():
    # Prepare test data

    # Mock 10 closing price
    np.random.seed(42)  # for reproducibility
    base_price = 155
    price_changes = np.random.normal(loc=0, scale=1, size=10)  # small daily changes
    closing_prices = (base_price + np.cumsum(price_changes)).round(2)
    closing_prices_list = closing_prices.tolist()
    df_stock_close = pd.DataFrame(closing_prices_list, index=pd.to_datetime(dates), columns=["Close"])

    # Mock 10 std dev, 20-days ema, bollinger bands
    std_list = [1.23, 1.45, 1.67, 1.89, 2.01, 2.22, 2.43, 2.64, 2.85, 3.06]
    ema_values_20 = [
        207.5836, 207.3916, 207.6118, 208.0889, 208.9124,
        209.6287, 210.4139, 211.3126, 212.1544, 212.9166
    ]
    df_ema_20 = pd.DataFrame(ema_values_20, index=pd.to_datetime(dates), columns=["EMA"])
    list_bb = calc_bollinger_bands(std_list, df_ema_20)

    # Mock 10 RSI values
    sample_rsi = [55.2, 52.8, 57.1, 60.3, 63.5, 59.7, 62.1, 65.4, 67.8, 70.2]

    # Mock 10 200-days & 50-days EMA data
    ema_values_50 = [155.87, 156.18, 155.81, 156.61, 156.91, 157.68, 157.42, 157.22, 157.91, 158.99]
    ema_values_200 = [155.08, 155.23, 155.43, 155.41, 155.62, 155.71, 155.79, 155.94, 156.05, 156.27]
    df_ema_50 = pd.DataFrame(ema_values_50, index=pd.to_datetime(dates), columns=["EMA"])
    df_ema_200 = pd.DataFrame(ema_values_200, index=pd.to_datetime(dates), columns=["EMA"])
    
    # Calculate trade engine signals
    test_signal = []
    idx = 0
    for date, price in df_stock_close.iterrows():
        current_price = price["Close"]
        
        limits = list_bb[idx]
        upper = limits["upper"]
        lower = limits["lower"]

        current_rsi = sample_rsi[idx]

        ema_200_list = df_ema_200["EMA"].tolist()
        ema_50_list = df_ema_50["EMA"].tolist()
        ema_20_list = df_ema_20["EMA"].tolist()
        curr_ema_200 = ema_200_list[idx]
        curr_ema_50 = ema_50_list[idx]
        curr_ema_20 = ema_20_list[idx]

        # Entry rules
        if current_price < lower and current_rsi < 30 and curr_ema_50 > curr_ema_200:
            test_signal.append({date: "Enter Long"})
            idx += 1
            continue    
        
        if current_price > upper and current_rsi > 70 and curr_ema_50 < curr_ema_200:
            test_signal.append({date: "Enter Short"})
            idx += 1
            continue

        # Exit
        if current_price >= curr_ema_20:
            test_signal.append({date: "Exit Long"})
            idx += 1
            continue

        if current_price <= curr_ema_20:
            test_signal.append({date: "Exit Short"})
            idx += 1
            continue

        test_signal.append({date: "Hold"})
        idx += 1


    # Test trade engine function
    actl_signals = trade_engine(df_stock_close, df_ema_20, list_bb, sample_rsi, df_ema_200, df_ema_50)
    # print(actl_signals)
    assert actl_signals == test_signal


if __name__ == "__main__":
    main()