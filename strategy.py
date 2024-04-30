import ta.trend as trend
import data
from connection import connection
import pandas as pd
import OrderManagement
import websocket
import time
import json

class EmaStrategy:
    def __init__(self) -> None:
        self.close = data.getdata()
        self.time = data.gettime()
        self.ema20 = trend.ema_indicator(self.close,20)
        self.ema50 = trend.ema_indicator(self.close,50)
        self.order = OrderManagement.OrderManagement(connection())
        self.symbol = "BTC/USDT"
        self.amount = 1000
        self.crypto_amount = 0
        self.in_position = "Nan"
        self.status = False
        self.ws = ""


    def run(self):
        self.is_candle_closed()
        if self.status:
            self.strategy()
            self.status=False
            self.run()

       
            
        

    def strategy(self):
        self.close = data.getdata()
        self.time = data.gettime()
        self.ema20 = trend.ema_indicator(self.close,20)
        self.ema50 = trend.ema_indicator(self.close,50)
        
        
        
        if self.ema20.iloc[-1] > self.ema50.iloc[-1] and self.ema20.iloc[-2] <= self.ema50.iloc[-2]:
            if self.in_position =="Nan":
                self.crypto_amount = self.amount/connection().fetch_ticker(self.symbol)["last"]
                self.order.marketBuy(symbol=self.symbol,amount=self.crypto_amount)
                self.in_position = "long"
                print("Successful long order")


            elif self.in_position == "short":
                self.update()
                print("Short order is closed")
                print("Balance is ",self.amount,"\n")

                        
                self.order.marketBuy(symbol=self.symbol,amount=self.crypto_amount)

                self.crypto_amount = self.amount/connection().fetch_ticker(self.symbol)["last"]
                self.order.marketBuy(symbol=self.symbol,amount=self.crypto_amount)

                self.in_position="long"
                print("Successful long order")

                
                
        elif self.ema20.iloc[-1] < self.ema50.iloc[-1] and self.ema20.iloc[-2] >= self.ema50.iloc[-2]:
            if self.in_position =="Nan":
                self.crypto_amount = self.amount/connection().fetch_ticker(self.symbol)["last"]
                self.order.marketSell(symbol=self.symbol,amount=self.crypto_amount)
                self.in_position = "short"
                print("Successful short order")


            elif self.in_position =="long":
                self.update()
                print("Long order is closed")
                print("Balance is ",self.amount,"\n")
                self.order.marketSell(symbol=self.symbol,amount=self.crypto_amount)

                self.crypto_amount = self.amount/connection().fetch_ticker(self.symbol)["last"]
                self.order.marketSell(symbol=self.symbol,amount=self.crypto_amount)

                self.in_position = "short"
                print("Successful short order")

                

            
        else:
            print("HODL")

    def is_candle_closed(self):
        url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        ws = websocket.WebSocketApp(url, on_message=self.on_message)
        ws.run_forever()
        return True
    
    def on_message(self,ws,message):
    
        data = json.loads(message)
        candle = data["k"]["x"]

        if candle:
            print(f"Is Closed? {candle}")
            self.status=True
            ws.close()
        else:
            time.sleep(1)

    
       
    def update(self):
            
        for i in connection().fetch_positions():
            if (i["info"]["symbol"]==self.symbol.replace("/","")):
                self.crypto_amount = abs(float(i["info"]["positionAmt"]))
                PNL = float(i["info"]["unRealizedProfit"])
                self.amount+=PNL


    def strategy_backtest(self):
        close = list()
        time = list()
        position = ""
        profit = 0
        df = pd.DataFrame({
            'time': self.time,
            'close': self.close,
            'ema20': self.ema20,
            'ema50': self.ema50
            })
        for i in range(len(df)):
            if df.iloc[i,2] > df.iloc[i,3] and df.iloc[i-1,2] <= df.iloc[i-1,3]:
                close.append(df.iloc[i,1])
                time.append(df.iloc[i,0])
                if position=="":
                    position = "long"
                
            
            elif df.iloc[i,2] < df.iloc[i,3] and df.iloc[i-1,2] >= df.iloc[i-1,3]:
                close.append(df.iloc[i,1])
                time.append(df.iloc[i,0])
                if position=="":
                    position = "short"

        
        for i in range(1, len(close)):
            print("Step:", i)
            print("Current Price:", close[i])
            print("Previous Price:", close[i - 1])
            
            
            if position=="long":
                print("Action: Buy")
                print("Open Long Position")
                position = 'short'
                entry_price = close[i - 1]
                print("Entry Price for Long Position:", entry_price)
                print("Profit from Closing Long Position:", close[i] - entry_price)
                profit += close[i] - entry_price

            
            
            elif position=="short":
                print("Action: Sell")
                print("Open Short Position")
                position = 'long'
                entry_price = close[i - 1]
                print("Entry Price for Short Position:", entry_price)
                print("Profit from Closing Short Position:", entry_price - close[i])
                profit += entry_price - close[i]

                    

            print("Current Position:", position)
            print("Current Profit:", profit)
            print("------------------------")



        print("Total Profit:", profit)
                
                
    
        


EmaStrategy().run()
        
            


        
