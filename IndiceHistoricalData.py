from lxml.etree import fromstring
import pandas as pd
import calendar, requests
from indices.indices import *
from indices.commodities import *

# set https header parameters
headers = {
	'User-Agent': 'Mozilla/5.0', #required 
	'referer': "https://www.investing.com",
	'host' : 'www.investing.com',
	'X-Requested-With' : 'XMLHttpRequest'
}

class IndiceHistoricalData():	
	
	def __init__(self, API_url):
		self.API_url = API_url

	#set https header for request
	def setHeaders(self, headers):
		self.headers = headers 
	
	#set indice data (indices.py) 
	def setFormData(self, data):
		self.data = data 

	#prices frequency, possible values: Monthly, Weekly, Daily		
	def updateFrequency(self, frequency):
		self.data['frequency'] = frequency	 

	#desired time period from/to
	def updateStartingEndingDate(self, startingDate, endingDate):
		self.data['st_date'] = startingDate	 
		self.data['end_date'] = endingDate	 

	#possible values: 'DESC', 'ASC'
	def setSortOreder(self, sorting_order):
		self.data['sort_ord'] = sorting_order	 

	#making the post request
	def downloadData(self):
		self.response = requests.post(self.API_url, data=self.data, headers=self.headers).content
		#parse tables with pandas - [0] probably there is only one html table in response
		self.observations = pd.read_html(self.response)[0]
		return self.observations

	#print retrieved data
	def printData(self):
		print(self.observations)

	#print retrieved data
	def saveDataCSV(self):
		self.observations.to_csv(self.data['name']+'.csv', sep='\t', encoding='utf-8')


def go(name, begin_date, end_date, freq):
    assert type(name) == str, '*name* must be string type!'
    # set https header parameters
    headers = {
    	'User-Agent': 'Mozilla/5.0', #required 
    	'referer': "https://www.investing.com",
    	'host' : 'www.investing.com',
    	'X-Requested-With' : 'XMLHttpRequest'
    }
    #first set Headers and FormData	
    ihd = IndiceHistoricalData('https://uk.investing.com/instruments/HistoricalDataAjax')
    ihd.setHeaders(headers)
    ihd.setFormData(eval(name))
    
    #second set Variables
    ihd.updateFrequency(freq)
    ihd.updateStartingEndingDate(begin_date, end_date)
    ihd.setSortOreder('ASC')
    df = ihd.downloadData()
    return df


