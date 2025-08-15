import requests
import json


APIKEY = "8RUS0YURXTPQQYEM"


def main():
    # Alpha Vantage API Key (Solomon)

    # Get Ticker, Initial Capital & Time
    ticker = input("Ticker: ")
    amount = int(input("Initial Amount: "))
    time_length = int(input("Length of time (days): "))

    stock_info = api_call(ticker)
    print(json.dumps(stock_info, indent=2))


def api_call(ticker):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={APIKEY}"
    r = requests.get(url)
    return r.json()


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()