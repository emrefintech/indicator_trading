from connection import connection
import pandas as py

def getdata():
    binance = connection()

    data = binance.fetch_ohlcv("BTC/USDT","1m")

    close = []


    for i in data:
        close.append(i[4])
    return py.Series(close)

def gettime():
    binance = connection()

    data = binance.fetch_ohlcv("BTC/USDT","1m")

    time = []


    for i in data:
        time.append(i[0])
    return py.Series(time)
    