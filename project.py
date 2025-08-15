import requests
import json
import pandas as pd

APIKEY = "8RUS0YURXTPQQYEM"


def main():
    # Alpha Vantage API Key (Solomon)

    # Get Ticker, Initial Capital & Time
    ticker = input("Ticker: ")
    amount = int(input("Initial Amount: "))
    time_length = int(input("Length of time (days): "))

    # API call to retrieve stock data
    stock_info = api_call(ticker)

    # Convert json of data to a pandas dataframe
    df = convert_json_to_dataframe(stock_info, time_length)
    print(df)

def api_call(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={APIKEY}"
    r = requests.get(url)
    return r.json()


def convert_json_to_dataframe(json, days):
    df = pd.DataFrame.from_dict(json["Time Series (Daily)"], orient="index")
    df = df.sort_index() # sorted in ascending (oldest date first)
    df = df[["4. close"]].astype(float).rename(columns={"4. close" : "Close"})
    df = df.tail(days) # 252 is 1 trading year
    return df


def function_n():
    ...



def function_n():
    ...



def function_n():
    ...


if __name__ == "__main__":
    main()