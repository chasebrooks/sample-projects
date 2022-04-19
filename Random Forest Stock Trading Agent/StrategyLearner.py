""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  
import random  		 
from marketsimcode import compute_portvals 	   		   	 		  		  		    	 		 		   		 		  		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
import util as ut  	
import marketsimcode as simple
from BagLearner import BagLearner as learner
from ManualStrategy import ManualStrategy
from indicators import get_rsi, create_bollinger_bands, calc_bbp, calc_momentum  		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # constructor  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0, window=7, return_threshold=0.05, bags = 25):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		   	 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		   	 		  		  		    	 		 		   		 		  
        self.commission = commission  
        self.learner = learner()
        self.holdings = 0	  	  
        self.window = window
        self.return_threshold = max(return_threshold, impact)
        self.bags = bags
  	  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 12, 31),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=100000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        # add your code to do learning here
        self.price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=False)
        self.price_data = self.price_data[symbol]
        self.price_data = self.price_data.dropna()


        # Get Discretized Indicators
        self.get_discrete_indicators(symbol=symbol, sd=sd, ed=ed)
        
        # number of trading days
        num_trading_days = len(self.df_indicators)

        X_train=[]
        Y_train=[]        

        for i in range(self.window + 1, num_trading_days-self.window):
            momentum = self.df_indicators.momentum.values[i]
            rsi = self.df_indicators.rsi.values[i]
            bbp = self.df_indicators.bbp.values[i]
            X_train.append([momentum, rsi, bbp])
            period_ret = (self.price_data.iloc[i + self.window]  - self.price_data.iloc[i]) / self.price_data.iloc[i]
            if period_ret > self.return_threshold:
                Y_train.append(1)
            elif period_ret < -self.return_threshold:
                Y_train.append(-1)
            else:
                Y_train.append(0)

        X_train=np.array(X_train)
        Y_train=np.array(Y_train)

        self.learner.add_evidence(X_train, Y_train)
        
            		  		    	 		 		   		 	   	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=100000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        # add your code to do learning here
        self.price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=False)
        self.price_data = self.price_data.dropna()


        # Create empty df with trades
        self.trades = self.price_data.copy()
        self.trades[:] = 0.0

        # Get Discretized Indicators
        self.get_discrete_indicators(symbol=symbol, sd=sd, ed=ed)

        X_test = []
        # number of trading days
        num_trading_days = len(self.df_indicators)
        for i in range(self.window + 1, num_trading_days-self.window):
            momentum = self.df_indicators.momentum.values[i]
            rsi = self.df_indicators.rsi.values[i]
            bbp = self.df_indicators.bbp.values[i]
            X_test.append([momentum, rsi, bbp])

        X_test = np.array(X_test)
        
        out = self.learner.query(X_test)

        holdings = 0
        for idx, trade in enumerate(out):
            if trade > 0:
                self.trades.iloc[idx] = 1000 - holdings
                holdings = 1000
            elif trade < 0:
                self.trades.iloc[idx] = -1000 - holdings
                holdings = -1000
            
        return self.trades  	

    def get_discrete_indicators(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):

        price_data = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=False)
        price_data = price_data.dropna()
        price_data = price_data[symbol]


        # Compute rolling mean & standard deviation
        rolling_mean = price_data.rolling(window=20).mean()
        rolling_std = price_data.rolling(window=20).std()

        # Get High/Low Data
        high = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=False, colname='High')
        high = high[symbol]
        high.fillna(method='ffill', inplace=True)
        high.fillna(method='bfill', inplace=True)

        low = ut.get_data([symbol], pd.date_range(sd, ed), addSPY=False, colname='Low')
        low = low[symbol]
        low.fillna(method='ffill', inplace=True)
        low.fillna(method='bfill', inplace=True)	

        # Calculate Indicators
        momentum = calc_momentum(price_data)
        rsi = get_rsi(price_data)
        upper, lower = create_bollinger_bands(rolling_mean, rolling_std)
        bbp = calc_bbp(price_data, upper, lower)	

        # discretize_D = pd.cut(D, 10, labels=False, include_lowest=True)
        discretize_momentum = pd.cut(momentum, 10, labels=False, include_lowest=True)
        discretize_rsi = pd.cut(rsi, 10, labels=False, include_lowest=True)
        discretize_bbp = pd.cut(bbp, 10, labels=False, include_lowest=True)

        df_indicators = pd.concat([discretize_momentum, discretize_rsi, discretize_bbp	], axis=1)
        df_indicators.columns = ['momentum', 'rsi', 'bbp']
        df_indicators.dropna(inplace=True)

        self.df_indicators = df_indicators

        # only keep price data for days where indicators can be created
        self.price_data = self.price_data[self.price_data.index.isin(self.df_indicators.index.to_series())]


    def author(self):
        return 'DBrooks43'

def calc_performance(port_val):
    daily_ret = port_val.div(port_val.shift(1)) - 1
    daily_ret = daily_ret.iloc[1:]

    adr = daily_ret.mean()
    sddr = daily_ret.std()
    cr = (port_val[-1] / port_val[0]) - 1


    return cr, adr, sddr   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    # print("One does not simply think up a strategy")  
    symbol="AAPL"
    np.random.seed(903034113) 
    commission = 0.0
    impact = 0.0	
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009, 12, 31)

    manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
    benchmark_trades = manual.Benchmark()
    benchmark_holdings, benchmark_portval = compute_portvals(benchmark_trades, symbol=symbol, commission=commission, impact=impact)    
    
    learner = StrategyLearner(verbose=True, commission=commission, impact=impact, bags = 25, window=8, return_threshold=0.05)
    learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    trades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    trades = trades[symbol]
    
    holdings, learner_portval = compute_portvals(trades, symbol=symbol, commission=commission, impact=impact)
    benchmark_cr, benchmark_adr, benchmark_std = calc_performance(benchmark_portval)
    
    benchmark_cr, benchmark_adr, benchmark_std = calc_performance(benchmark_portval)
    learner_cr, learner_adr, learner_std = calc_performance(learner_portval)


    

