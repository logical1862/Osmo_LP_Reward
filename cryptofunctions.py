import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
from requests import session
import os




class Osmo_data:
    def __init__(self) -> None:
        self.daily = list()
        self.total = list()
        self.gain = list()
        self.currentprice = list()
        self.name = list()
        self.histprice = list()
        self.apr = list()


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


def osmo_hist_price_APR():
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
    return content



def osmo_plot(osmo_data: Osmo_data):


# set plot for rewards history
    a = 65
    b = 0
    num_tokens = len(osmo_data.name)
    plt.figure, axs1 =  plt.subplot_mosaic(
      '''
      AF
      BF
      CF
      DH
      EH
      ''',
      figsize=(20,8)      
    
    )

    for i in osmo_data.name:   
        #axs1[chr(a)].st   #style.use('seaborn-darkgrid')
        
        axs1[chr(a)].plot(osmo_data.daily[b])      
        axs1[chr(a)].set_title(i)
        axs1[chr(a)].set_xlabel('Days of rewards for each token')
        axs1[chr(a)].set_xlim([0, len(osmo_data.daily[b])])
        max_value = max(osmo_data.daily[b])
        max_value = max_value + (max_value * 0.5)
        axs1[chr(a)].set_ylim([0, max_value])
        a = a + 1
        b += 1
    
    plt.margins(y = 10, x= 10)

    osmo_hist = osmo_hist_price_APR()
    print()
       
    axs1[chr(a )].bar('time', 'volume', data=osmo_hist, color='blue', width=0.05, linewidth=0.005)      
    axs1[chr(a )].set_title('OSMO Volume(in millions')
    axs1[chr(a )].grid()


    axs1[chr(a + 2)].plot('time', 'close', data=osmo_hist, color='red') 
    axs1[chr(a + 2)].plot('time', 'open', data=osmo_hist, color='green')       
    axs1[chr(a + 2)].set_title('OSMO (green = open/ red = close')
    
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=.2, 
                    hspace=2)
    
    return



##   COSMOS ##



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


def token_data(i, wallet, api_key):
    i = str(i)
    name = i[11:len(i) - 2]
    print(f'checking {name}')
    
    url = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/historical/{wallet}/{name}'
    
    
    rewards_response = requests.get(url = url)
    try:
      #get total/price of rewards
      dict = json.loads(rewards_response.content)
      
      total = total_reward(dict)
      
      current_price = price(name = name, api_key = api_key)
      
    except:
      print('error within response')
      input()
      os.exit()

    gain = current_price * total

    print(f"Total {name} coin reward (from lp): {total}\nAt current price: {current_price}\ncurrent profit from lp rewards in {name}: {gain}\n")
    return [name, dict, gain, current_price, total]