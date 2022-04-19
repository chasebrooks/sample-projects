To run all required outputs for report:
- PYTHONPATH=../:. python testproject.py 


To run Manual Strategy:
manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
manual_trades = manual.TestPolicy()
manual_holdings, manual_portval = compute_portvals(manual_trades, symbol=symbol, commission=commission, impact=impact)
    
To run Benchmark:
benchmark_trades = manual.Benchmark()
benchmark_holdings, benchmark_portval = compute_portvals(benchmark_trades, symbol=symbol, commission=commission, impact=impact)    

To run strategy learner:
learner = StrategyLearner(commission=commission, impact=impact,bags=25, window=7, return_threshold=0.05)
learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31))
learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed)
learner_trades = learner_trades[symbol]
learner_holdings, learner_portval = compute_portvals(learner_trades, symbol=symbol, commission=commission, impact=impact)


testproject.py: code for orchestrating all required outputs.
- PYTHONPATH=../:. python testproject.py 
- generates required outputs for manual strategy, experiment 1, and experiment 2 for the report

indicators.py: contains code to calculate and plot the following technical indicators: 
- Bollinger Bands (and Bollinger Band Percentage)
- Relative Strength Index (RSI)
- Momentum

experiment1.py: contains code to run experiment 1 where in sample performance compared between benchmark buy
and hold, manual strategy, and decision tree learner for 1/1/2008-12/31/2009
- PYTHONPATH=../:. python experiment1.py 

experiment2.py: contains code to run experiment 2 where in sample performance compared for 
decision tree learner with various impact levels for 1/1/2008-12/31/2009
- PYTHONPATH=../:. python experiment2.py 

StrategyLearner.py: contains code to train Bag learner of random forests
- Default Params: impact=0.0, commission=0.0, window=7, return_threshold=0.05, bags = 25
- PYTHONPATH=../:. python StrategyLearner.py 

ManualStrategy.py: contains code to run manual strategy based on technical indicators
- Default Params: symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000
- PYTHONPATH=../:. python ManualStrategy.py 

marketsimcode.py: contains code to backtest portfolio values of trades
- Default Params: symbol='JPM',	start_val=100000, commission=9.95, impact=0.005

BagLearner.py: contains code to train bag learner strategy

RTLearner.py: contains code to invoke a random forests learner

