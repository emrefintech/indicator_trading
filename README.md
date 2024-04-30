Application that buys and sells ema 20/50 strategy on Binance test server

First of all, you need to enter your own API key and secret key in the connection file.

If you want to do this with a real account, enter the keys of your real account and delete the "binance.set_sandbox_mode(True)" code.

Currently, this code buys and sells in a 1-minute period. To change this, change the necessary codes in the data.py file and change the url in the is_candle_closed function in strategy.py.

Other variables depend on your preference.

Contact: X: @emre_fintech
