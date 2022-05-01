import matplotlib.pyplot as plt
import requests
import json
import pandas as pd

from requests import session



class all_token_data:
    def __init__(self, daily, total, gain, price, name) -> None:
        self.daily = list(daily)
        self.total = list(total)
        self.gain = list(gain)
        self.price = list(price)
        self.name = list(name)





def price(name, api_key):
    url = R'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    params = {
      'symbol': name
    }

    headers = {
      'Accepts': 'application/json', 
      'X-CMC_PRO_API_KEY' : api_key
    }
    session = requests.Session()
    session.headers.update(headers)

    response1 = session.get(url = url, params= params)
    content = json.loads(response1.text)

    price = json.loads(response1.content)['data'][name]['quote']['USD']['price']
    return float(price)


def total_reward(dict):
    a = 0
    total = 0
    for i in dict:
        if (a == len(dict) - 1):
          break
        a = a + 1

        total = total + float(dict[a]['amount'])
    return total




def osmo_reward_line_plot(all_token_data: all_token_data):
    
    a = 0
    num_tokens = len(all_token_data.name)

    plt.figure, axs =  plt.subplots(num_tokens, sharex= True)
    
    for i in all_token_data.name:   
       
        axs[a].plot(all_token_data.daily[a])      
        axs[a].set_title(all_token_data.name[a])
        
        a = a + 1
    plt.margins(y = 5, x= 5)
    plt.figure.supylabel('Token rewarded per day')
    plt.figure.supxlabel('Days since start')
    plt.tight_layout()
    plt.show()


def cosmos_account(wallet):
  url = f'https://api.cosmoscan.net/account/{wallet}'

  headers = {
    'Accepts': 'application/json', 
  }

  session = requests.Session()
  session.headers.update(headers)

  response = session.get(url = url)
  content = json.loads(response.content)

  return content


def cosmos_history():
    url = R'https://api.cosmoscan.net/historical-state'

    session = requests.Session()
    response = session.get(url=url)
    content = json.loads(response.content)
    content = content['price_agg']
    
    history_df = pd.DataFrame.from_dict(content)
    history_df['time'] = pd.to_datetime(history_df['time'],unit='s')

    return history_df

def osmo_price_APR():
  url = f'https://api-osmosis.imperator.co/tokens/v2/historical/OSMO/chart?tf=60'
  headers = {
    'Accepts': 'application/json', 
  }
  session = requests.Session()
  session.headers.update(headers)

  response = session.get(url = url)
  content = json.loads(response.content)
  content = pd.DataFrame(content)
  
  content['time'] = pd.to_datetime(content['time'],unit='s')
  
  plt.figure, axs =  plt.subplots(2)
       
  axs[0].plot('time', 'volume', data=content, color='blue')      
  axs[0].set_title('OSMO Volume(in millions')

  axs[1].plot('time', 'close', data=content, color='red') 
  axs[1].plot('time', 'open', data=content, color='green')       
  axs[1].set_title('OSMO (green = open/ red = close')
  
  plt.tight_layout()
  
  plt.rcParams["figure.figsize"] = (10, 10)
  plt.show()
  
  return 