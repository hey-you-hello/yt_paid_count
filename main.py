import requests
from io import StringIO
import json
import re

data = StringIO(requests.get("https://dieddayofbattlecatserver.vercel.app/output.json").text).readlines()
money = 0

def transform_money(txt):
    exchange_rates = {
        'NT$': 1.0,
        'MYR': 7.44038,
        'SGD': 22.0,
        '₹': 0.4,
        '£': 40.0,
        '¥': 0.25,
        '₱': 0.6,
		"HK$":4.2207,
		"A$":20.71
    }
    #每天
    if 'MYR' in txt or 'SGD' in txt:
        p=txt.split()
        c=p[0]
        amount_str=p[1].replace(',', '')
        try:
            amount=float(amount_str)
        except ValueError:
            print(f"失敗！！！: {txt}")
            return 0
        return amount * exchange_rates[c]
    
    #應該對？
    match=re.match(r'^(\D+?)\s*([\d,.]+)$', txt)
    if match:
        currency_s=match.group(1).strip()
        amount_s=match.group(2).replace(',', '')
        try:
            amount=float(amount_s)
        except ValueError:
            print(f"失敗: {txt}")
            return 0
        
        rate=exchange_rates.get(currency_s, 0)
        if rate == 0:
            print(f"未找到貨幣符號 '{currency_s}'der匯率")
            return 0
        return amount * rate
    else:
        print(f"格式錯誤: {txt}")
        return 0

n_paid=0
for n in data:
    if "paid" in n:
        n_paid+=1
        paid_data=json.loads(n)["paid"]
        money+=transform_money(paid_data)

print(f"總金額台幣: {money}")
print(f"付費條目數: {n_paid}")
