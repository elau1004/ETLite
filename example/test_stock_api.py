import requests

API_KEY = "OSxE5kQ2OgqGdUTlofGR1Aa07rrPjffca1hZPPGuxQyjVgel3FCrPKdhL0NY"    # Fake secret.
STOCK_URL = f"https://api.worldtradingdata.com/api/v1/stock?api_token={API_KEY}"

response = requests.get( url=STOCK_URL ,params={ "symbol" : "IBM" })
print( response.text )
