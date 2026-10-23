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

def get_all_transactions(token: str):
    params = {"limit": 200, "recordDate": "gte.2018-01-01"}
    headers = {"Authorization":"Bearer "+token}
    transactions = []

    while True:
        r = rq.get(BASE_URL+"/v1/api/records", headers=headers, params=params)
        r.raise_for_status()
        data = r.json()

        transactions.extend(data.get("records", []))

        next_offset = data.get("nextOffset")
        if next_offset is None:
            break
        params["offset"] = next_offset
        print(next_offset)


    #Parsing transactions
    parsed_transactions = []
    for t in transactions:
        parsed_transactions.append(
            {
                "id": t.get("id"),
                "note": t.get("note"),
                "recordDate": t.get("recordDate"),
                "amount": (t.get("amount") or {}).get("value"),
                "category": (t.get("category") or {}).get("name"),
                "categoryGroup": ((t.get("category") or {}).get("group") or {}).get("name"),
                "accountId": t.get("accountId"),
                "accountName": t.get("accountName"),
            }
        )

    return parsed_transactions


def main():
    transactions = get_all_transactions(token=TOKEN)
    df = pd.DataFrame(transactions)
    print(df)
    df.to_csv("data/transactions.csv")

if __name__ == "__main__":
    main()
