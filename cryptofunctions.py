import matplotlib.pyplot as plt
import requests
import json



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




def daily_reward_line_plot(all_token_data: all_token_data):
    
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
