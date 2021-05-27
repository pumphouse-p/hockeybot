"""
Defines constant variables.
"""
import requests

BASEURL = "https://statsapi.web.nhl.com/api/v1"

def get(endpoint):
    url = '{}/{}'.format(BASEURL, endpoint)
    response = requests.get(url)
    return response.json()