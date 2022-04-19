import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  
from marketsimcode import compute_portvals	
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner

def Experiment2(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), commission = 0.0, impact = 0.0):
    # in sample comparison

    learner1 = StrategyLearner(commission=commission, impact=0.0,bags=25, window=15, return_threshold=0.05)
    learner1.add_evidence(symbol=symbol, sd=sd, ed=ed)
    learner1_trades = learner1.testPolicy(symbol=symbol, sd=sd, ed=ed)
    learner1_trades = learner1_trades[symbol]
    learner1_holdings, learner1_portval = compute_portvals(learner1_trades, symbol=symbol, commission=commission, impact=0.0)

    learner3 = StrategyLearner(commission=commission, impact=0.05,bags=25, window=15, return_threshold=0.05)
    learner3.add_evidence(symbol=symbol, sd=sd, ed=ed)
    learner3_trades = learner3.testPolicy(symbol=symbol, sd=sd, ed=ed)
    learner3_trades = learner3_trades[symbol]
    learner3_holdings, learner3_portval = compute_portvals(learner3_trades, symbol=symbol, commission=commission, impact=0.05)

    learner4 = StrategyLearner(commission=commission, impact=0.03,bags=25, window=15, return_threshold=0.05)
    learner4.add_evidence(symbol=symbol, sd=sd, ed=ed)
    learner4_trades = learner4.testPolicy(symbol=symbol, sd=sd, ed=ed)
    learner4_trades = learner4_trades[symbol]
    learner4_holdings, learner4_portval = compute_portvals(learner4_trades, symbol=symbol, commission=commission, impact=0.03)

    learner1_portval.plot(label='impact=0.0')
    learner4_portval.plot(label='impact=0.03')
    learner3_portval.plot(label='impact=0.05')
    plt.title('{} returns 1/1/2008-12/31/2009'.format(symbol))
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.savefig('experiment2.png')
    plt.clf()


    x = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    y = []
    for i in x:
        impact = i

        learner = StrategyLearner(commission=commission, impact=i,bags=25, window=15, return_threshold=0.05)
        learner.add_evidence(symbol=symbol, sd=sd, ed=ed)
        learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed)
        learner_trades = learner_trades[symbol]
        learner_holdings, learner_portval = compute_portvals(learner_trades, symbol=symbol, commission=commission, impact=i)
        y.append(len(learner_trades.loc[learner_trades != 0].index))
    plt.title('Number of Trades vs. Impact')
    plt.ylabel('Number of Trades')
    plt.xlabel('Impact')
    plt.plot(x, y)
    plt.savefig('trades_impact.png')
    plt.clf()




def calc_performance(port_val):
    daily_ret = port_val.div(port_val.shift(1)) - 1
    daily_ret = daily_ret.iloc[1:]

    adr = daily_ret.mean()
    sddr = daily_ret.std()
    cr = (port_val[-1] / port_val[0]) - 1


    return cr, adr, sddr

def author():
    return 'DBrooks43'
    

if __name__ == '__main__':
    np.random.seed(903034113) 
    Experiment2(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))