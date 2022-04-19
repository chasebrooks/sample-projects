""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
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
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Chase Brooks (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: DBrooks43 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903034113 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
def compute_portvals(  		  	   		   	 		  		  		    	 		 		   		 		  
    orders,  
    symbol='JPM',		  	   		   	 		  		  		    	 		 		   		 		  
    start_val=100000,  		  	   		   	 		  		  		    	 		 		   		 		  
    commission=9.95,  		  	   		   	 		  		  		    	 		 		   		 		  
    impact=0.005,  		  	   		   	 		  		  		    	 		 		   		 		  
):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # Import Order Data
    orders = orders.sort_index()
    start_date = orders.index.min()
    end_date = orders.index.max()

    # Import Price Data
    price_data = get_data([symbol], pd.date_range(start_date, end_date), addSPY=False)
    price_data['Cash'] = 1.0
    price_data.fillna(method='ffill', inplace=True)
    price_data.fillna(method='bfill', inplace=True)

    trades = price_data.copy()
    trades[:] = 0
    trades['Cash'] = 0

    # cash = start_val
    
    for date, order in orders.items():
        shares = order
		
        trades.loc[date] += shares

        # update cash impact
        price = price_data.loc[date, symbol]
        if shares != 0:
        	trades.loc[date, 'Cash'] -= ((shares * price) + commission + (abs(shares) * price * impact))
        # else:
    
    holdings = trades.copy()
    holdings[:] = 0

    # update first day holdings values because doesn't follow same pattern as rest of dataframe
    holdings.loc[start_date, 'Cash'] = start_val
    holdings.iloc[0, :] += trades.iloc[0, :]
    
    for day in range(1, len(trades)):
        holdings.iloc[day, :] += holdings.iloc[day-1, :] + trades.iloc[day, :]

    syms_value = pd.DataFrame(holdings.values * price_data.values , index=price_data.index, columns= price_data.columns)
    portvals = syms_value.sum(axis=1)
    normed_portvals = portvals.div(portvals.iloc[0])

    return holdings, normed_portvals


def author():
    return 'DBrooks43'
  	 		  		  		    	 		 		   		 		  	   		   	 		  		  		    	 		 		   		 		   		   	 		  		  		    	 		 		   		 		  
  		 	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  	

    test_data = [['2011-12-27', 900], ['2011-12-28', 0.0] ]

    test_df = pd.DataFrame(test_data, columns=['Date', 'Shares'])	  
    test_df = test_df.set_index('Date')	 

    compute_portvals(test_df)




