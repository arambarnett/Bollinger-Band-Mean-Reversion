def initialize():
    storage.invested = False


def tick():
    # Enter if the price is less than two standard deviations away from the moving average;
    # exit if the price becomes greater than two standard deviations away from the moving average.

    # Get the standard deviation from the moving average
    std = data[info.primary_pair].std(40)

    # Construct the upper and lower Bollinger Bands
    ma = data[info.primary_pair].ma(40)
    upper = ma + (Decimal(2) * std)
    lower = ma - (Decimal(2) * std)

    price = data[info.primary_pair].close

    if price < lower and not storage.invested:
        # The price has dropped below the lower BB, so buy
        buy(info.primary_pair)
        storage.invested = True
    elif price > upper and storage.invested:
        # The price has risen above the upper BB, so sell
        sell(info.primary_pair)
        storage.invested = False

    plot('MA', ma, secondary=True)
    plot('Upper', upper, secondary=True)
    plot('Lower', lower, secondary=True)


def stop():
    # If we're holding BTC, clear our position.
    if storage.invested:
        sell(info.primary_pair) 
