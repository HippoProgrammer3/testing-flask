from flask import Flask, redirect

import requests

app = Flask(__name__)

guild_id = 0 # should be set to the correct id for prod use
api_key = 0
item_id = 0 # should be set to the id of the item

current_price = 100 

@app.route('/') # index with login page
def index():
    return '<h1>This site is under construction</h1>'

@app.route('/auth_redirect') # index redirects to this page for OAuth login
def auth_redirect():
    return redirect('https://google.com',code=302) # this should redirect to the OAuth2 application for sign in

@app.route('/profile') # OAuth redirects to this page after login
def profile():
    global api_key, guild_id, current_price

    # get the user id from the api then display profile
    user_id = 0

    # get the user balance then display valid buttons from the unbelievaboat api
    url = f"https://unbelievaboat.com/api/v1/guilds/{guild_id}/users/{user_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }

    response = requests.get(url, headers=headers)

    user_bal = response.json()['cash']

    return '<h1>Logged in</h1>'

@app.route('/profile/buy') # profile sends GET requests with JSON to this address after buy button clicked
def buy():
    global api_key,guild_id,current_price,item_id
    user_id = requests.json()['user_id']
    amount = requests.json()['amount']

    # check the user has enough money
    url = f"https://unbelievaboat.com/api/v1/guilds/{guild_id}/users/{user_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"{api_key}"
    }

    response = requests.get(url, headers=headers)

    user_bal = response.json()['cash']

    if user_bal > amount * current_price:
        url = f"https://unbelievaboat.com/api/v1/guilds/{guild_id}/users/{user_id}"
        payload = {
            "cash": f"{amount * current_price}",
            "reason": "BenjaminCoin purchase - webapp"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"{api_key}"
        }

        response = requests.patch(url, json=payload, headers=headers)

        url = f"https://unbelievaboat.com/api/v1/guilds/{guild_id}/users/{user_id}/inventory"

        payload = {
            "item_id": f{item_id},
            "quantity": amount
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"{api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)




