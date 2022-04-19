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

def Experiment1(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):
    # in sample comparison

    commission = 9.95
    impact = 0.005

    manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
    manual_trades = manual.TestPolicy()
    manual_holdings, manual_portval = compute_portvals(manual_trades, symbol=symbol, commission=commission, impact=impact)
    benchmark_trades = manual.Benchmark()
    benchmark_holdings, benchmark_portval = compute_portvals(benchmark_trades, symbol=symbol, commission=commission, impact=impact)    

    learner = StrategyLearner(commission=commission, impact=impact,bags=25, window=7, return_threshold=0.05)
    learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31))
    learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed)
    learner_trades = learner_trades[symbol]
    learner_holdings, learner_portval = compute_portvals(learner_trades, symbol=symbol, commission=commission, impact=impact)

    benchmark_cr, benchmark_adr, benchmark_std = calc_performance(benchmark_portval)
    manual_cr, manual_adr, manual_std= calc_performance(manual_portval)
    learner_cr, learner_adr, learner_std = calc_performance(learner_portval)
    
    with open("p8_outputs.txt", "a") as f:
        f.write('Experiment 1: In Sample Results\n')
        f.write("Benchmark - cr: {0}, adr: {1}, std: {2}\n".format(benchmark_cr, benchmark_adr, benchmark_std))
        f.write("Manual Strategy- cr: {0}, adr: {1}, std: {2}\n".format(manual_cr, manual_adr, manual_std))
        f.write("Learner - cr: {0}, adr: {1}, std: {2}\n".format(learner_cr, learner_adr, learner_std))

    manual_portval.plot(label='manual', color='r')
    benchmark_portval.plot(label='benchmark', color='g')
    learner_portval.plot(label='learner')
    plt.title('{} returns 1/1/2008-12/31/2009'.format(symbol))
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.savefig('experiment1.png')
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
    Experiment1(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))