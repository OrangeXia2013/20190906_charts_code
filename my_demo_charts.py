# -*- coding: utf-8 -*-
"""
Created on Fri May 17 21:03:49 2019

@author: admin
"""

import os
import time

#import mpl_finance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from IndiceHistoricalData import go as crawler
# set plot format
plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.facecolor'] = '1.'
plt.rcParams["axes.axisbelow"] = False


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class my_demo( ):
    '''
    '''
    ###########################################################################
    def __init__(self):

        print('My demo charts class')
        
        # create data path
        self.data_path = os.getcwd() + '/data/'
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        
        # create charts path
        self.charts_path = os.getcwd() + '/charts/'
        if not os.path.exists(self.charts_path):
            os.mkdir(self.charts_path)
        
        # initialize attributes
        self.data = {}
        pass
    
    def load_data(self, name = 'ERUUSD'):
        ''' Function to load data
        '''
        try:
            # fetch data
            data1 = crawler(name, '01/01/2003', '01/01/2011', 'Daily')
            data2 = crawler(name, '01/01/2010', '10/21/2019', 'Daily')
            data  = pd.concat([data1, data2], axis = 0).drop_duplicates('Date').reset_index(drop = True)
            
            # clean data
            data['Date'] = pd.to_datetime(data['Date'])
            data = data[['Date','Price', 'Open', 'High', 'Low']]
            data.columns = ['date', 'close', 'open', 'high', 'low' ]
    
            # save data
            df = data.sort_values(by = 'date')
            df.set_index('date', drop = True, inplace = True)
            df.to_csv(self.data_path + '%s.csv'%name)
            
        except Exception as e:
            print(e)
            print('Load data from local files.')
            df = pd.read_csv(self.data_path + '%s.csv'%name, index_col = 0, parse_dates = True)
            
        try:
            self.data['raw'][name] = df.copy()
            
        except:
            self.data['raw'] = {}
            self.data['raw'][name] = df.copy()
            
        return
    
    
    ###########################################################################
    def my_plot_1(self):
        ''' Data processing and plot No.1
        '''
        self.load_data(name = 'ERUUSD')
        df = self.data['raw']['ERUUSD'].copy()
        
        #####################################
        # code the logics here
        #####################################
        
        fig = plt.figure(figsize = [15, 9])
        ax = fig.add_subplot(111)
        ax.plot(df['close'], label = 'Realized Spread Pft')
        plt.title('ERUUSD', fontsize = 20)
        
        ax.get_figure().savefig(self.charts_path + 'ERUUSD.png') # save figure
        
         # CLOSE FIGURE TO SAVE MEMORY, VERY IMPORTANT!
        plt.close(fig)
        pass
    
    ###########################################################################
    def run(self,):
        ''' Trigger a for-loop, run real-time trading program
        '''
        while True:
            
            print(datetime.now(), 'Starts working!')
            t = time.time()
            self.my_plot_1() # plot and save figure no.1
            t1 = time.time() - t
            print(t1)
            # sleep for 1 day, depends to updating frequency.
            print(datetime.now(), 'Sleeping for 1 day...')
            time.sleep( 24 * 60 * 60 )
        pass
    

if __name__ == '__main__':
    
    t = time.time()

    self = my_demo()
    
    self.run()
    
    print(time.time() - t, ' seconds elapsed...')