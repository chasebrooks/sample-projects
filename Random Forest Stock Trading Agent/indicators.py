import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  
import os  		  	   	
import matplotlib.pyplot as plt	  
import matplotlib.dates as mdates
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  


def calc_momentum(prices, window=10):
    """
    momentum[t] = (price[t]/price[t-N]) - 1  
    """
    momentum = pd.Series(np.nan, index=prices.index)
    momentum.iloc[window:] = prices.iloc[window:] / prices.values[:-window] - 1
    return momentum

def create_bollinger_bands(rolling_mean, rolling_std, num_std=2):
    upper = rolling_mean + rolling_std * num_std
    lower = rolling_mean - rolling_std * num_std
    return upper, lower

def calc_bbp(price, upper, lower):
    return (price - lower) / (upper - lower)


def get_rsi(prices, window=14):
    delta_price = prices.diff()

    up = delta_price.clip(lower=0)
    down = -delta_price.clip(upper=0)

    ma_up = up.rolling(window = window).mean()
    ma_down = down.rolling(window = window).mean()

    rs = ma_up / ma_down
    rsi = 100 - (100/(1 + rs))

    return rsi


def author():
    return 'DBrooks43'

if __name__ == "__main__":

   print('indicators.py')