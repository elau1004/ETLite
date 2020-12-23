import requests

#API_KEY = "OSxE5kQ2OgqGdUTlofGR1Aa07rrPjffca1hZPPGuxQyjVgel3FCrPKdhL0NY"    # Fake secret.
#STOCK_URL = f"https://api.worldtradingdata.com/api/v1/stock?api_token={API_KEY}"
#response = requests.get( url=STOCK_URL ,params={ "symbol" : "IBM" })

'''
There are several API endpoints to choose from:

(eod)End-of-Day Data: Get daily stock market data.
(intraday)Intraday Data: Get intraday and real-time market data.
(tickers)Tickers: Get information about stock ticker symbols.
(exchanges)Exchanges: Get infotmation about all supported exchanges.
(currencies)Currencies: Get information about all supported currencies.
(timezones)Timezones: Get information about all supported timezones.
'''
'''
API_KEY = "6dd4778d309dc5018782adbf17dea9ce"    # Fake secret.
STOCK_URL = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}"

response = requests.get( url=STOCK_URL ,params={ "symbol" : "IBM" })
print( response.text )

'''
params = {
  'access_key'  : '6dd4778d309dc5018782adbf17dea9ce' ,
  'symbols'     :   'aapl'
}

#good url version 1
#api_result = requests.get('http://api.marketstack.com/v1/tickers/aapl/eod', params)
#api_result = requests.get('http://api.marketstack.com/v1/eod', params)
api_result = requests.get('http://api.marketstack.com/v1/eod/latest', params)

print(api_result.text)
api_response = api_result.json()

print(api_response)

#write to a file
work_path = 'C:\\CaliforniaSciTechUniversity\\ETLITE\\Output\\'
with open(work_path + 'stock_output.txt','w') as fd:
    fd.write(api_result.text)

#write to a json file

import json

with open(work_path + 'data_json.txt', 'w') as outfile:
    json.dump(api_response, outfile, indent=2)

'''
for stock_data in api_response['data']:
    print(u'Ticker %s has a day high of  %s on %s' % (
      stock_data['symbol']
      stock_data['high']
      stock_data['date']
    ))ate']
))
'''