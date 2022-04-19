import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import random  		 
from marketsimcode import compute_portvals 	   		   	 		  		  		    	 		 		   		 		  		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
import util as ut  	
import marketsimcode as simple
from indicators import get_rsi, create_bollinger_bands, calc_bbp, calc_momentum  		   	 		  		  		    	 		 		   		 		  
import numpy as np	   	 		  		  		    	 		 		   		 		  
from StrategyLearner import StrategyLearner



def test_params():
    bags = [5,10,15,20,25,30]
    windows = [5,6,7,8,9,10,11,12,13,14]
    thresholds = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    in_sample_candidates1 = []
    in_sample_candidates2 = []
    in_sample_candidates3 = []
    in_sample_candidates4 = []

    for i in windows:
        for j in thresholds:
            for k in bags:

                symbol="SINE_FAST_NOISE"
                commission = 9.95
                impact = 0.005	
                
                #iteration 1
                learner = StrategyLearner(commission=commission, impact=impact, bags = k, window = i, return_threshold = j)
                learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
                trades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
                holdings, vals = compute_portvals(trades, symbol=symbol, commission=commission, impact=impact)
                last1 = vals.iloc[-1]
                if last1 >= 3.0:
                    print('test 1: window: {0}, thresh:{1}, bags{2}, last1:{3}'.format(i,j,k,last1))
                    in_sample_candidates1.append((i, j, k))

    for i, j, k in in_sample_candidates1:
        symbol="AAPL"
        commission = 9.95
        impact = 0.005	
        
        #iteration 1
        learner = StrategyLearner(commission=commission, impact=impact, bags = k, window = i, return_threshold = j)
        learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        trades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        holdings, vals = compute_portvals(trades, symbol=symbol, commission=commission, impact=impact)
        last1 = vals.iloc[-1]
        if last1 >= 0.0:
            print('test 2: window: {0}, thresh:{1}, bags{2}, last1:{3}'.format(i,j,k,last1))
            in_sample_candidates2.append((i, j, k))

    for i, j, k in in_sample_candidates2:
        symbol="ML4T-220"
        commission = 9.95
        impact = 0.005	
        
        #iteration 1
        learner = StrategyLearner(commission=commission, impact=impact, bags = k, window = i, return_threshold = j)
        learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        trades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        holdings, vals = compute_portvals(trades, symbol=symbol, commission=commission, impact=impact)
        last1 = vals.iloc[-1]
        if last1 >= 0.0:
            print('test 3: window: {0}, thresh:{1}, bags{2}, last1:{3}'.format(i,j,k,last1))
            in_sample_candidates3.append((i, j, k))

    for i, j, k in in_sample_candidates3:
        symbol="UNH"
        commission = 9.95
        impact = 0.005	
        
        #iteration 1
        learner = StrategyLearner(commission=commission, impact=impact, bags = k, window = i, return_threshold = j)
        learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        trades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
        holdings, vals = compute_portvals(trades, symbol=symbol, commission=commission, impact=impact)
        last1 = vals.iloc[-1]
        if last1 >= 1.2:
            print('test 4: window: {0}, thresh:{1}, bags{2}, last1:{3}'.format(i,j,k,last1))
            in_sample_candidates4.append((i, j, k))


