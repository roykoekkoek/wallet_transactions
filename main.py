import os
import pandas as pd
import requests as rq
import json

BASE_URL = os.environ["BASE_URL"]
TOKEN = os.environ["TOKEN"]

def get_accounts(token: str):
    r = rq.get(BASE_URL+"/v1/api/accounts?limit=100", headers={"Authorization":"Bearer "+token}).json()
    print(json.dumps(r))
    with open('data/accounts.json', 'w', encoding='utf-8') as f:
        json.dump(r, f)

def get_transactions(token: str):
    r = rq.get(BASE_URL+"/v1/api/records?limit=200&recordDate=gte.2016-01-01", headers={"Authorization":"Bearer "+token}).json()
    print(json.dumps(r))
    with open('data/records.json', 'w', encoding='utf-8') as f:
        json.dump(r, f)

def main():
    get_transactions(token=TOKEN)

if __name__ == "__main__":
    main()
