import requests
from requests import Request
import pandas as pd

# ftx request using signatures
def make_request(self, request, ts):
        s = requests.Session()
        prepared = request.prepare()
        ts = int(time.time() * 1000)
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        signature = hmac.new(self.api_secret.encode(), signature_payload, 'sha256').hexdigest()

        prepared.headers['FTX-KEY'] = self.api_key
        prepared.headers['FTX-SIGN'] = signature
        prepared.headers['FTX-TS'] = str(ts)

        response = s.send(prepared)
        return response.json()

# Using queries
def query_data(self):
        query = """
        {
              pair (id: "0x3041cbd36888becc7bbcbc0045e3b1f144466f5f") {
                reserve0
                reserve1
                reserveUSD
              }
        }
            """

        r = requests.post(self.url, json={'query': query})
        data = json.loads(r.text)
        balance_usdc = float(data['data']['pair']['reserve0'])
        balance_usdt = float(data['data']['pair']['reserve1'])
        total_liquidity = float(data['data']['pair']['reserveUSD'])
        pool_info = {'total_liquidity': total_liquidity,
                     'balance_usdc': balance_usdc,
                     'balance_usdt': balance_usdt}
        return pool_info

# Using Request
def get_data_pair(self, pair):
        request = Request('GET', pair.url)
        s = requests.Session()
        prepared = request.prepare()
        response = s.send(prepared).json()
        pair.volume = round(float(response['payload']['volume']), 3)
        pair.bid = round(float(response['payload']['bid']), 3)
        pair.ask = round(float(response['payload']['ask']), 3)
        pair.spread_usd = pair.bid-pair.ask
        pair.spread_pcg = (pair.bid-pair.ask) / \
                                                  ((pair.bid+pair.ask)/2)