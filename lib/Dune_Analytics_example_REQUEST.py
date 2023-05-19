import requests 
from requests import Request 
import pandas as pd 

API_KEY = 'YOUR_API_KEY'
url = 'https://api.dune.com/api/v1/query/589150/results?api_key='+ API_KEY
request = Request('GET', url) 
s = requests.Session() 
prepared = request.prepare() 
response = s.send(prepared).json() 

print(pd.DataFrame(response['result']['rows']))