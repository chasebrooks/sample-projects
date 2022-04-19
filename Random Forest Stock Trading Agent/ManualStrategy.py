import datetime as dt                                                                                                               
import os                                                                                                                                                                                                                            
import numpy as np                                                                                                                                                                                                                            
import pandas as pd                                                                                                               
from util import get_data, plot_data  
from marketsimcode import compute_portvals    
from indicators import get_rsi, create_bollinger_bands, calc_bbp, calc_momentum
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals 



class ManualStrategy():
    def __init__(self, symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
        self.symbol = symbol
        self.sd = sd
        self.ed = ed
        self.sv = sv 
    
    def TestPolicy(self):
        self.price_data = get_data([self.symbol], pd.date_range(self.sd, self.ed), addSPY=False)
        self.price_data = self.price_data[self.symbol]
        # self.price_data = self.price_data.dropna()

        self.price_data.fillna(method='ffill', inplace=True)
        self.price_data.fillna(method='bfill', inplace=True)

        # Compute rolling mean & standard deviation
        rolling_mean = self.price_data.rolling(window=20).mean()
        rolling_std = self.price_data.rolling(window=20).std()

        # Get High/Low Data
        high = get_data([self.symbol], pd.date_range(self.sd, self.ed), addSPY=False, colname='High')
        high = high[self.symbol]
        high.fillna(method='ffill', inplace=True)
        high.fillna(method='bfill', inplace=True)

        low = get_data([self.symbol], pd.date_range(self.sd, self.ed), addSPY=False, colname='Low')
        low = low[self.symbol]
        low.fillna(method='ffill', inplace=True)
        low.fillna(method='bfill', inplace=True)

        # Create empty df with trades
        trades = self.price_data.copy()
        trades[:] = 0


        # get indicators
        rsi = get_rsi(self.price_data)
        upper, lower = create_bollinger_bands(rolling_mean, rolling_std)
        bbp = calc_bbp(self.price_data, upper, lower)
        momentum = calc_momentum(self.price_data)

        # Attempt 1: Overbought/sold with mean reversion
        holdings = 0
        for index, row in trades.iteritems():
            if bbp.loc[index] <= 0.2 and momentum.loc[index] < 0 and rsi.loc[index] <=50 and holdings <= 0:
            # if rsi.loc[index] <= 40 and bbp.loc[index] <= 0.2 and D.loc[index] < 20 and holdings <= 0:
                trades.loc[index] = 1000 - holdings
                holdings = 1000
            elif bbp.loc[index] >= 0.8 and momentum.loc[index] > 0 and rsi.loc[index] > 50 and holdings > 0:
                trades.loc[index] = -1000 - holdings
                holdings = -1000

        return trades

    def Benchmark(self):
        """Benchmark: The performance of a portfolio starting with $100,000 cash, 
        investing in 1000 shares of the symbol in use on the first trading day,  
        and holding that position. Include transaction costs. 
        """
        price_data = get_data([self.symbol], pd.date_range(self.sd, self.ed), addSPY=False)
        price_data = price_data[self.symbol]
        price_data.fillna(method='ffill', inplace=True)
        price_data.fillna(method='bfill', inplace=True)
        trades = price_data.copy()
        trades[:] = 0
        trades[0] = 1000
        trades[-1] = -1000
        return trades   
    
    def author(self):
        return 'DBrooks43'


if __name__ == "__main__":
    symbol="JPM"
    commission = 0.0
    impact = 0.0
    
    np.random.seed(903034113) 

    ## Manual in sample 1/1/2008 - 12/31/2009
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009, 12, 31)
    manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
    manual_trades = manual.TestPolicy()
    manual_holdings, manual_portval = compute_portvals(manual_trades, symbol=symbol, commission=commission, impact=impact)
    short_dates = manual_trades.loc[manual_trades < 0].index
    long_dates = manual_trades.loc[manual_trades > 0].index

    benchmark_trades = manual.Benchmark()
    benchmark_holdings, benchmark_portval = compute_portvals(benchmark_trades, symbol=symbol, commission=commission, impact=impact)
    
    manual_portval.plot(label='manual', color='r')
    for short in short_dates:
        plt.axvline(x=short, color='k')
    for long in long_dates:
        plt.axvline(x=long, color='b')
    benchmark_portval.plot(label='benchmark', color='g')
    plt.legend()
    plt.title('Manual Strategy In Sample Results')
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.savefig('charts/manual_in_sample.png')
    plt.clf()

    ## Manual out of sample 1/1/2010 - 12/31/2011
    sd=dt.datetime(2010, 1, 1)
    ed=dt.datetime(2011, 12, 31)
    manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
    manual_trades = manual.TestPolicy()
    manual_holdings, manual_portval = compute_portvals(manual_trades, symbol=symbol, commission=commission, impact=impact)
    short_dates = manual_trades.loc[manual_trades < 0].index
    long_dates = manual_trades.loc[manual_trades > 0].index

    benchmark_trades = manual.Benchmark()
    benchmark_holdings, benchmark_portval = compute_portvals(benchmark_trades, symbol=symbol, commission=commission, impact=impact)

    manual_portval.plot(label='manual', color='r')
    for short in short_dates:
        plt.axvline(x=short, color='k')
    for long in long_dates:
        plt.axvline(x=long, color='b')
    benchmark_portval.plot(label='benchmark', color='g')
    plt.legend()
    plt.title('Manual Strategy Out of Sample Results')
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.savefig('charts/manual_out_sample.png')
    plt.clf()

