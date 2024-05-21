import requests
import json
from datetime import date

def access_token():
    tokenUri = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    tokenRequestBody = {
        'grant_type': 'client_credentials',
        'client_id': '7f2bda3ce59b4026a3907cf750f21ee8',
        'client_secret': '506ff237590941348bc7e98b51924c44'
    }
    response = requests.post(url=tokenUri, headers=header, data=tokenRequestBody)
    access_token = response.json()['access_token']
    return access_token
