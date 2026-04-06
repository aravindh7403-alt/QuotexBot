import MetaTrader5 as mt5

# Connect to MT5 terminal
if not mt5.initialize():
    print("MT5 initialize failed")
else:
    print("MT5 initialized successfully")
    mt5.shutdown()
