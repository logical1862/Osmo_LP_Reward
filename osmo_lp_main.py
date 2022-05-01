import requests
import json
import os
import cryptofunctions as crypto




#get coinmarketcap api key to pass to price() params
api_key = input('CoinMarketCap API key?: \n')

#get coin name
wallet = input('OSMO wallet address?: \n')


url_token_list = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/token/{wallet}'

token_list_response = requests.get(url= url_token_list)
tokens = json.loads(token_list_response.content)

print(f'Coins rewarded from LP: {tokens}')

#get rewards


x_axis_list = list()#daily
total = list()#total
price = list()
gain = list()
name = list()


#initialize class containing all data lists
all_data = crypto.all_token_data(daily=x_axis_list, total=total, gain=gain, price= price, name= name)

for i in tokens:
   
    i = str(i)
    name = i[11:len(i) - 2]
    print(f'checking {name}')
    
    url = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/historical/{wallet}/{name}'
    
    
    rewards_response = requests.get(url = url)
    try:
      #get total/price of rewards
      dict = json.loads(rewards_response.content)
      total = crypto.total_reward(dict)
      price = crypto.price(name = name, api_key = api_key)

    except:
      print('error within response')

    gain = price * total

    print(f"Total {name} coin reward (from lp): {total}\nAt current price: {price}\ncurrent profit from lp rewards in {name}: {gain}\n")

    #######START OF GRAPH CODE

    chart_len = len(dict)
    
    x_axis_list = list()
    y_axis_list = list()

    
    #x axis is each reward per day
    for i in range(chart_len - 1):
      x_axis_list.append(dict[i]['amount'])

    x_axis_list.reverse()

  
    #each tokens(i) data added to relevant class list
    all_data.daily.append(x_axis_list)
    all_data.gain.append(gain)
    all_data.name.append(name)
    all_data.price.append(price)
    all_data.total.append(total)
    

crypto.osmo_reward_line_plot(all_data)











###possible dev        

#make file with data (possibly with a pandas Dataframe)
#    a = 0
#    cwd = os.getcwd()
#    fileType = '\\osmolist.txt'
#    cwd = cwd + fileType

#open and write file with contents of dict
#with open(cwd, 'w') as f:
    #

      #

      #f.write()
      #f.write('\n')
    #f.write(f"Total {name} coin reward (from lp): {total}\nAt current price: {price}\ncurrent profit from lp rewards in {name}: {gain}\n")