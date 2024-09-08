# crypto-stocks

## About crypto-stocks

crypto-stocks is a project that uses [polygon.io](https://polygon.io/) and [Alpha Vantage](https://www.alphavantage.co/) APIs to fetch news and visualize stock and cryptocurrency data. It was developed in `March 2022` as a Project Assignment for the course **[CSE101: *Introduction to Programming*](http://techtree.iiitd.edu.in/viewDescription/filename?=CSE101)**.

## Features of the project

### Stock News

Access news of the most famous stocks of your choice, along with any news or article that references it. For each news displayed, a button to go directly to the article is given along with the headline.

### Stock Data

Gather and visualize stock data such as *Opening Prices*, *Closing Prices*, *Maximum Traded Volume*, and others, for a selected stock during a particular time period. 

### Cryptocurrency Data

Gather and visualize cryptocurrency data such as *Opening Value*, *Closing Value*, *Maximum Market Cap*, and others, for a selected crypto. The currency in which the data is displayed (default USD) can be convereted to any other, using the latest price rate.

## Use your own API Keys

To generate your own API keys to use the project, visit [polygon.io](https://polygon.io/) and [Alpha Vantage](https://www.alphavantage.co/). To use the generated keys, add the following lines to `main.py` as a header:

```python
POLYGON_API_KEY: str = <your-polygon.io-api-key>
ALPHA_API_KEY: str = <your-alpha-vantage-api-key>
```

## Run

To use, clone the repository on your device, navigate to the folder, and execute:
```
python3 main.py
```

## References

- [polygon.io (YouTube)](https://youtu.be/RLtEiDNKfkU)
- [Alpha Vantage (YouTube)](https://youtu.be/PytQROAncxg)
