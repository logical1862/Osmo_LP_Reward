import cryptofunctions as crypto
import requests
import json
import matplotlib.pyplot as plt




# set all class data as empty lists
daily_token = list()#daily
total = list()#total of daily rewards
current_price = list()# current trade price 
gain = list()# total at current price
name = list()# tokens rewarded in osmo wallet
hist_price = list()
apr = list()


# get user input data

api_key = input('CoinMarketCap API key?: \n')
wallet = input('OSMO wallet address?: \n')

# get user results
url_token_list = f'https://api-osmosis-chain.imperator.co/lp/v1/rewards/token/{wallet}'
token_list_response = requests.get(url= url_token_list)
tokens = json.loads(token_list_response.content)

print(f'Coins rewarded from LP: {tokens}')

#initialize class (users wallet info)
osmo_data = crypto.Osmo_data()
for i in tokens:
    #print(i, '\n\n')
   
    all_data = crypto.token_data(i=i, wallet=wallet, api_key=api_key)
    
    # get name
    name = all_data[0]
    
    # get daily
    daily_list = (all_data[1][:]) 
    daily_len = len(all_data[1][:])
    
    for i in daily_list:
      daily_token.append(i['amount'])
    daily_token.reverse()

    # get gain
    gain = all_data[2]

    # get currently listed trade price
    current_price = all_data[3]

    # get total coin rewarded
    total = all_data[4]

    # each tokens(i) data added to relevant class list
    osmo_data.make_lists(daily_token, total, gain, current_price, name)

    daily_token = []


crypto.osmo_plot(osmo_data=osmo_data)

plt.show()