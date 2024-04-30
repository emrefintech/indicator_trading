
import ccxt
class OrderManagement():
    def __init__(self,client) -> None:
        if isinstance(client,ccxt.binance):
            self.connection = client

        else:
            raise ValueError("Only ccxt.binance variable is possible")


    def marketBuy(self,amount,symbol):
        self.connection.create_market_buy_order(symbol=symbol,amount=amount)

        
    def marketSell(self,amount,symbol):
        self.connection.create_market_sell_order(symbol=symbol,amount=amount)





        
