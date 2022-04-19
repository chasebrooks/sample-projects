import datetime as dt                                                                                                               
from experiment1 import Experiment1
from experiment2 import Experiment2
from ManualStrategy import ManualStrategy
from marketsimcode import compute_portvals 
import matplotlib.pyplot as plt   
import numpy as np


def main(symbol='JPM', commission = 9.95, impact = 0.005):

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
    plt.savefig('manual_in_sample.png')
    plt.clf()

    #### Calculate portfolio metrics for manual vs benchmark in sample
    manual_cr, manual_adr, manual_std = calc_performance(manual_portval)
    benchmark_cr, benchmark_adr, benchmark_std = calc_performance(benchmark_portval)
    with open("p8_outputs.txt", "a") as f:
        f.write('Manual: In Sample Results\n')
        f.write("Benchmark - cr: {0}, adr: {1}, std: {2}\n".format(benchmark_cr, benchmark_adr, benchmark_std))
        f.write("Manual Strategy - cr: {0}, adr: {1}, std: {2}\n\n".format(manual_cr, manual_adr, manual_std))

    ## Manual out of sample 1/1/2010 - 12/31/2011
    sd=dt.datetime(2010, 1, 1)
    ed=dt.datetime(2011, 12, 31)
    manual = ManualStrategy(symbol=symbol, sd=sd, ed=ed)
    manual_trades = manual.TestPolicy()
    manual_holdings, manual_portval = compute_portvals(manual_trades, symbol=symbol, commission=commission, impact=impact)
    cr, std, ar = calc_performance(manual_portval)
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
    plt.savefig('manual_out_sample.png')
    plt.clf()

    #### Calculate portfolio metrics for manual vs benchmark out of sample
    manual_cr, manual_adr, manual_std = calc_performance(manual_portval)
    benchmark_cr, benchmark_adr, benchmark_std = calc_performance(benchmark_portval)
    with open("p8_outputs.txt", "a") as f:
        f.write('Manual: Out of Sample Results\n')
        f.write("Benchmark - cr: {0}, adr: {1}, std: {2}\n".format(benchmark_cr, benchmark_adr, benchmark_std))
        f.write("Manual Strategy - cr: {0}, adr: {1}, std: {2}\n\n".format(manual_cr, manual_adr, manual_std))

   
    ## Experiment 1:
    Experiment1()

    ## Experiment 2:
    Experiment2()
    


def calc_performance(port_val):
    daily_ret = port_val.div(port_val.shift(1)) - 1
    daily_ret = daily_ret.iloc[1:]

    adr = daily_ret.mean()
    sddr = daily_ret.std()
    cr = (port_val[-1] / port_val[0]) - 1


    return cr, adr, sddr

def author():
    return 'DBrooks43'


if __name__ == "__main__":
    # plot Manual
    main()
