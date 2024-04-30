import ccxt


api_key=""
secret_key=""


def connection():
    binance = ccxt.binance({
        "apiKey" : api_key,
        "secret": secret_key,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })
    
    binance.set_sandbox_mode(True)
    
    return binance

