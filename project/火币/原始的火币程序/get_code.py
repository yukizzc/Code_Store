import requests
import pandas as pd
import json 
#原始网页文件,获取所有品种信息
url = r'https://api.btcgateway.pro/api/v1/contract_contract_info'
url2 = r'https://api.btcgateway.pro/swap-api/v1/swap_contract_info'
url3 = r'https://api.btcgateway.pro/linear-swap-api/v1/swap_contract_info'

def get_df(url):
    r = requests.get(url)
    html = r.text
    temp = json.loads(html)
    df = pd.DataFrame(temp['data'])
    print(df)

if __name__ == "__main__":
    get_df(url2)