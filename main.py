import matplotlib.pyplot as plt
import datetime as dt
import webbrowser
import itertools
import requests
import csv


POLYGON_API_KEY: str = "<polygon.io-api-key>"
ALPHA_API_KEY: str = "<alpha-vantage-api-key>"

# names of csv files containing ticker data
FILE1: str = "digital_currency.csv"
FILE2: str = "physical_currency.csv"


with open(FILE1) as f1, open(FILE2) as f2:
    digital = csv.reader(f1)
    physical = csv.reader(f2)

    # skip digital rows using next()
    next(digital); next(physical)

    # mapping available currency names to their codes
    NAME_TO_CODE = {}
    for row in itertools.chain(digital, physical):
        code, name = row
        NAME_TO_CODE[name.casefold()] = code


def stock_data_plot(y_label, volumes, low, high):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

    ax1.plot(low, color="red", linewidth=2, label="Low")
    ax1.plot(high, color="green", linewidth=2, label="High")
    ax2.plot(volumes, color="blue", linewidth=2, label="Volumes")

    for ax in (ax1, ax2):
        ax.axhline(y=0, color="black", linewidth=3)
        ax.axvline(x=0, color="black", linewidth=3)
        ax.plot(0, 0, color="black", linewidth=3, marker="o")
        ax.set_xlabel("Time Range")
        ax.grid(True)

    lowest, highest, max_vol = min(low), max(high), max(volumes)

    ax1.axhline(lowest, color="red", linewidth=1, linestyle="--", label="Lowest Price")
    ax1.axvline(low.index(lowest), color="red", linewidth=1, linestyle="--")

    ax1.axhline(highest, color="green", linewidth=1, linestyle="--", label="Highest Price")
    ax1.axvline(high.index(highest), color="green", linewidth=1, linestyle="--")

    ax2.axhline(max_vol, color="blue", linewidth=1, linestyle="--", label="Maximum Volume")
    ax2.axvline(volumes.index(max_vol), color="blue", linewidth=1, linestyle="--")

    ax1.set_ylabel(y_label)
    ax2.set_ylabel("Number of shares traded")
    ax1.legend()
    ax2.legend()
    plt.show()


def crypto_data_plot1(y_label, volumes, low, high, opening, closing):
    fig = plt.figure()
    ax1, ax2, ax3 = plt.subplot(211), plt.subplot(223), plt.subplot(224)

    ax1.plot(volumes, color="blue", linewidth=2, label="Volumes")

    ax2.plot(low, color="red", linewidth=2, label="Low")
    ax2.plot(high, color="green", linewidth=2, label="High")

    ax3.plot(opening, color="yellow", linewidth=2, label="Opening")
    ax3.plot(closing, color="orange", linewidth=2, label="Closing")

    for ax in (ax1, ax2, ax3):
        ax.axhline(y=0, color="black", linewidth=3)
        ax.axvline(x=0, color="black", linewidth=3)
        ax.plot(0, 0, color="black", linewidth=3, marker="o")
        ax.set_xlabel("Time Range")
        ax.set_ylabel(y_label)
        ax.grid(True)

    lowest, highest, max_vol = min(low), max(high), max(volumes)

    ax1.axhline(max_vol, color="blue", linewidth=1, linestyle="--", label="Maximum Volume")
    ax1.axvline(volumes.index(max_vol), color="blue", linewidth=1, linestyle="--")

    ax2.axhline(lowest, color="red", linewidth=1, linestyle="--", label="Lowest Price")
    ax2.axvline(low.index(lowest), color="red", linewidth=1, linestyle="--")

    ax2.axhline(highest, color="green", linewidth=1, linestyle="--", label="Highest Price")
    ax2.axvline(high.index(highest), color="green", linewidth=1, linestyle="--")

    ax1.set_ylabel("Number of shares traded")
    for ax in (ax1, ax2, ax3):
        ax.legend()
    plt.show()


def crypto_data_plot2(y_label, volumes, low, high, opening, closing, market_cap):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)

    volumes, opening, closing = volumes[::10], opening[::10], closing[::10]
    low, high, market_cap = low[::10], high[::10], market_cap[::10]

    ax1.plot(low, color="red", linewidth=2, label="Low")
    ax1.plot(high, color="green", linewidth=2, label="High")

    ax2.plot(opening, color="yellow", linewidth=2, label="Opening")
    ax2.plot(closing, color="orange", linewidth=2, label="Closing")

    ax3.plot(volumes, color="blue", linewidth=2, label="Volumes")
    ax4.plot(market_cap, color="purple", linewidth=2, label="Market Caps")

    for ax in (ax1, ax2, ax3, ax4):
        ax.axhline(y=0, color="black", linewidth=3)
        ax.axvline(x=0, color="black", linewidth=3)
        ax.plot(0, 0, color="black", linewidth=3, marker="o")
        ax.set_xlabel("Time Range")
        ax.set_ylabel(y_label)
        ax.grid(True)

    lowest, highest, max_vol, max_cap = min(low), max(high), max(volumes), max(market_cap)

    ax1.axhline(lowest, color="red", linewidth=1, linestyle="--", label="Lowest Price")
    ax1.axvline(low.index(lowest), color="red", linewidth=1, linestyle="--")

    ax1.axhline(highest, color="green", linewidth=1, linestyle="--", label="Highest Price")
    ax1.axvline(high.index(highest), color="green", linewidth=1, linestyle="--")

    ax3.axhline(max_vol, color="blue", linewidth=1, linestyle="--", label="Maximum Volume")
    ax3.axvline(volumes.index(max_vol), color="blue", linewidth=1, linestyle="--")

    ax4.axhline(max_cap, color="purple", linewidth=1, linestyle="--", label="Maximum Market Cap")
    ax4.axvline(market_cap.index(max_cap), color="purple", linewidth=1, linestyle="--")

    ax3.set_ylabel("Number of shares traded")
    for ax in (ax1, ax2, ax3, ax4):
        ax.legend()
    plt.show()


def stock_news():
    # Stock News
    STOCK_NAME = input("Enter US company name: ").lower()
    # number of news results to be displayed
    LIMIT = int(input("Enter the number of headlines you want: "))
    DATE = input("Enter date (YYYY-MM-DD): ")

    try:
        d = dt.datetime.strptime(DATE, "%Y-%m-%d")
        today = dt.datetime.today()
        if d > today:
            print(f"Today is {today.date()}! Enter a date before {today.date()}!")
            return
    except ValueError:
        print("\nInvalid Date format provided!")
        return

    URL_TICKER = f"https://api.polygon.io/v3/reference/tickers?search={STOCK_NAME}&active=true&apiKey={POLYGON_API_KEY}"
    try:
        ticker_data = requests.get(URL_TICKER).json()
        ticker = str(ticker_data["results"][0]["ticker"])

        url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&published_utc.gte={DATE}&limit={LIMIT}&apiKey={POLYGON_API_KEY}"

        results = requests.get(url).json()
        news_list = {}

        for i in range(LIMIT):
            try:
                news_list[results["results"][i]["description"]] = results["results"][i]["article_url"]
            except:
                pass

        if not news_list:
            print(f"\nThere were no mentions of {STOCK_NAME.upper()} in the News on {DATE}")
            return

        print(f"\nMentions of {STOCK_NAME.upper()} in Stock News on {d.date()}:")

        flag, opened = True, False
        for n, (news, url) in enumerate(news_list.items(), start=1):
            print(f"\n{n}. \nTitle:", news)
            print("Article URL:", url)
            if flag:
                print("\nInterested? Open this article on the internet! Enter 'SKIP' if you do not want to open any links.")
                choice = input("Enter 'YES' to open the news on the internet and 'NO' to skip: ").casefold()
            if not opened and choice == "yes":
                webbrowser.open(url)
                opened = True
            elif choice == "skip":
                flag = False

    except IndexError:
        print("Company not present in the database.")

    except Exception:
        print("Data retrieval unsuccessful at the moment!")


def stock_data():
    # Stock Data

    STOCK_NAME = input("Enter US company name: ")
    URL_TICKER = f"https://api.polygon.io/v3/reference/tickers?search={STOCK_NAME}&active=true&apiKey={POLYGON_API_KEY}"
    DATA_RANGE = input("Enter the time interval (Minute, Hour or Day): ").casefold()

    if DATA_RANGE not in {"minute", "hour", "day"}:
        print("Invalid Time Interval!")
        return

    DATE_FROM = input("Enter 'FROM' date (YYYY-MM-DD): ")
    DATE_TO = input("Enter 'TO' date (YYYY-MM-DD): ")

    try:
        d1 = dt.datetime.strptime(DATE_FROM, "%Y-%m-%d")
        d2 = dt.datetime.strptime(DATE_TO, "%Y-%m-%d")
        today = dt.datetime.today()
        if d1 > today or d2 > today:
            print(f"Today is {today.date()}! Enter a date before {today.date()}!")
            return
        ticker_data = requests.get(URL_TICKER).json()
        ticker = str(ticker_data["results"][0]["ticker"])
        STOCK_URL = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{DATA_RANGE}/{DATE_FROM}/{DATE_TO}?adjusted=true&limit=120&apiKey={POLYGON_API_KEY}"

        high, low, volumes = [], [], []
        stock_data = requests.get(STOCK_URL).json()

        results = stock_data["results"]
        opening, closing = results[0]["o"], results[0]["c"]

        for i in range(len(results)):
            high.append(results[i]["h"])
            low.append(results[i]["l"])
            volumes.append(results[i]["v"])

        FUNCTION = "CURRENCY_EXCHANGE_RATE"
        FROM = "USD"
        API_URL = f"https://www.alphavantage.co/query?function={FUNCTION}&from_currency={FROM}&to_currency={{}}&apikey={ALPHA_API_KEY}"

        currency_choice = input("Enter what currency you want the data in (ex: 'Indian Rupee' / 'INR'): ")
        try:
            TO = NAME_TO_CODE[currency_choice.title()]
        except KeyError:
            if currency_choice.upper() in NAME_TO_CODE.values():
                TO = currency_choice.upper()
            else:
                print("Invalid Currency Name/Code! Showing results in default currency (USD)")
                TO = "USD"

        if TO != "USD":
            response = requests.get(API_URL.format(code))
            data = response.json()
            ex_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

            opening *= ex_rate
            closing *= ex_rate
            for i in range(len(results)):
                high[i] *= ex_rate
                low[i] *= ex_rate
                volumes[i] *= ex_rate

        print(f"\nStock Bar Data for {STOCK_NAME.upper()} in {TO}: \n")
        print("Highest price:", max(high))
        print("Lowest Price:", min(low))
        print("Opening Price:", opening)
        print("Closing Price:", closing)
        print("Max traded Volume:", max(volumes))

        stock_data_plot(y_label=f"Price (in {TO})", volumes=volumes, low=low, high=high)

    except IndexError:
        print("Company not present in the database.")

    except ValueError:
        print("Invalid Date Format")

    except KeyError:
        print("The Market was closed in the given time period.")

    except Exception:
        print("Data retrieval unsuccessful at the moment!")


def crypto():
    # Crypto Data

    ENDPT = "https://www.alphavantage.co/query"

    crypto_currency = input("Enter required crypto Currency Name/Code (ex: 'Bitcoin' / 'BTC'): ")
    try:
        crypto_symbol = NAME_TO_CODE[crypto_currency.casefold()]
    except KeyError:
        if crypto_currency.upper() in NAME_TO_CODE.values():
            crypto_symbol = crypto_currency.upper()
        else:
            print("Invalid Currency NAME/CODE Entered")
            return

    market = input("Enter what currency you want the data in (ex: 'United States Dollar' / 'USD'): ")
    try:
        market_symbol = NAME_TO_CODE[market.title()]
    except KeyError:
        if market.upper() in NAME_TO_CODE.values():
            market_symbol = market.upper()
        else:
            print("Invalid Currency NAME/CODE Entered")
            return

    frequency = input("Enter frequency (Intraday, Daily, Weekly or Monthly): ").casefold()

    selected = [
        "BTC", "LTC", "ETH", "BCH", "DOT", "DOGE", "ADA", "XLM", "BNB", "XMR", "SOL",
        "AVAX", "ALGO", "MATIC", "VET", "TRX", "ZEC", "XTZ", "DGB", "ZRX", "STORJ"
    ]

    if crypto_symbol not in selected:
        print(f"Sorry, Data not available for {crypto_symbol}")
        return

    if frequency == "intraday":
        func = "CRYPTO_INTRADAY"
        time = int(input("Enter time interval in minutes (1, 5, 15, 30 or 60): "))
        inter = f"{time}min"

        params = {
            "function": func, "symbol": crypto_symbol, "market": market_symbol,
            "interval": inter, "apikey": ALPHA_API_KEY
        }
        try:
            data = requests.get(ENDPT, params=params).json()
        except Exception:
            print("Data retrieval unsuccessful at the moment!")
            return

        open_, high, low, close, volumes = [], [], [], [], []
        d = data[f"Time Series crypto ({inter})"]

        for i in d:
            for j in d[i]:
                try:
                    value = float(d[i][j])
                except ValueError:
                    continue
                if j == "1. open":
                    open_.append(value)
                elif j == "2. high":
                    high.append(value)
                elif j == "3. low":
                    low.append(value)
                elif j == "4. close":
                    close.append(value)
                elif j == "5. volume":
                    volumes.append(value)

        print(f"\ncrypto Currency Data for {crypto_currency.upper()} in {market_symbol}: \n")
        print("Highest Value:", max(high))
        print("Lowest Value:", min(low))
        print("Opening Value:", open_[0])
        print("Closing Value:", close[-1])
        print("Max traded Volume:", max(volumes))

        crypto_data_plot1(
            y_label=f"Price (in {market_symbol})", volumes=volumes,
            low=low, high=high, opening=open_, closing=close
        )

    else:
        if frequency == "daily":
            func = "DIGITAL_CURRENCY_DAILY"
            dec = "Time Series (Digital Currency Daily)"

        elif frequency == "weekly":
            func = "DIGITAL_CURRENCY_WEEKLY"
            dec = "Time Series (Digital Currency Weekly)"

        elif frequency == "monthly":
            func = "DIGITAL_CURRENCY_MONTHLY"
            dec = "Time Series (Digital Currency Monthly)"

        else:
            print("INVALID Frequency entered! Please enter a valid frequency!")
            return

        p = {"function": func, "symbol": crypto_symbol, "market": market_symbol, "apikey": ALPHA_API_KEY}
        try:
            data = requests.get(ENDPT, params=p).json()
            d = data[dec]
        except Exception:
            print("Data retrieval unsuccessful at the moment!")
            return

        open_m, high_m, low_m, close_m, volume, market_cap = [], [], [], [], [], []

        for i in d:
            for j in d[i]:
                try:
                    value = float(d[i][j])
                except ValueError:
                    continue
                if j == f"1a. open ({market_symbol})":
                    open_m.append(value)
                elif j == f"2a. high ({market_symbol})":
                    high_m.append(value)
                elif j == f"3a. low ({market_symbol})":
                    low_m.append(value)
                elif j == f"4a. close ({market_symbol})":
                    close_m.append(value)
                elif j == "5. volume":
                    volume.append(value)
                elif j == "6. market cap (USD)":
                    market_cap.append(value)

        print(f"\ncrypto Currency Data for {crypto_currency.upper()} in {market_symbol}: \n")
        print("Highest Value at Market Price:", max(high_m))
        print("Lowest Value at Market Price:", min(low_m))
        print("Opening Value at Market Price:", open_m[0])
        print("Closing value at Market Price:", close_m[-1])
        print("Max traded Volume:", max(volume))
        print("Max Market Cap:", max(market_cap))

        crypto_data_plot2(
            y_label=f"Price (in {market_symbol})", market_cap=market_cap,
            volumes=volume, low=low_m, high=high_m, opening=open_m, closing=close_m,
        )


def main():
    """__main__ function"""

    print("\nWelcome to the APPLICATION")

    while True:
        print(f"\n{'=' * 80}\n")
        print("Type 'NEWS' to get News About Stocks")
        print("Type 'DATA' to get Latest Stock Data")
        print("Type 'CRYPTO' to get latest crypto currency data")
        print("Type 'EXIT' to exit the application")

        choice = input("\nEnter your choice: ").casefold()
        print(f"\n{'=' * 80}\n")

        if choice == "news":
            stock_news()
        elif choice == "data":
            stock_data()
        elif choice == "crypto":
            crypto()
        elif choice == "exit":
            print("EXITING...")
            break
        else:
            print("INVALID CHOICE! Enter again!")


if __name__ == "__main__":
    main()