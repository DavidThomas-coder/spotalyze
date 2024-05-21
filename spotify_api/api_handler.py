import requests
import json
from datetime import date

def access_token():
    tokenUri = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    tokenRequestBody = {
        'grant_type': 'client_credentials',
        'client_id': '<your_client_id>',
        'client_secret': '<your_client_secret>'
    }
    response = requests.post(url=tokenUri, headers=header, data=tokenRequestBody)
    access_token = response.json()['access_token']
    return access_token
