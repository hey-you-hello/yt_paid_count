import requests
from io import StringIO
import json
import re



data = StringIO(requests.get(f"https://dieddayofbattlecatserver.vercel.app/output.json").text).readlines()

money = 0

country = {
		'NT$': 0,
		'MYR': 0,
		'SGD': 0,
		'₹': 0,
		'£': 0,
		'¥': 0,
		'₱': 0,
		"HK$": 0,
		"A$": 0,
		"₩": 0,
		"$":0,
		"CA$":0,
		"€":0,
		"ARS":0,
		"₫":0,
	}
cn=country.copy()

def transform_money(txt):
	out=0

	exchange_rates = {
		'NT$': 1.0,
		'MYR': 7.44038,
		'SGD': 22.0,
		'₹': 0.4,
		'£': 40.0,
		'¥': 0.25,
		'₱': 0.6,
		"HK$": 4.2207,
		"A$": 20.71,
		"₩": 0.0236,
		"$":32.0,
		"CA$":22.8,
		"€":36.22,
		"ARS":0.0311,
		"₫":0.00129,
	}

	if 'MYR' in txt or 'SGD' in txt:
		p = txt.split()
		c = p[0]
		amount_str = p[1].replace(',', '')
		try:
			amount = float(amount_str)
		except ValueError:
			print(f"失敗！！！: {txt}")
			return 0
		out= amount * exchange_rates[c]
		country[c]+=out
		cn[c]+=1
		
		return out

	# 應該對？
	match = re.match(r'^(\D+?)\s*([\d,.]+)$', txt)
	if match:
		currency_s = match.group(1).strip()
		amount_s = match.group(2).replace(',', '')
		try:
			amount = float(amount_s)
		except ValueError:
			print(f"失敗: {txt}")
			return 0

		rate = exchange_rates.get(currency_s, 0)
		if rate == 0:
			print(f"未找到貨幣符號 '{currency_s}'der匯率")
			return 0
		out= amount * rate
		country[currency_s]+=out
		cn[currency_s]+=1
		return out
	else:
		print(f"格式錯誤: {txt}")
		return 0
pai330=[]
i=0
max_p = 0
max_p_data = None
n_paid = 0
moneys = 0
for n in data:
	if "paid" in n:
		
		if "330" in n:
			pai330.append(json.loads(n)["author"])
		
		
	
		n_paid += 1
		paid_data = json.loads(n)["paid"]
		money = transform_money(paid_data)
		
		
		if money > max_p:
			max_p = money
			max_p_data = n
		moneys += money
so=[]

for c in country:
	

	so.append((c,country[c]))
	
	
so.sort(key= lambda x:x[1])
so.reverse()



	

print(f"捐最多的人：{max_p_data}")
print(f"總金額台幣: {moneys}")
print(f"付費條目數: {n_paid}")
for n in so:
	

	print(f"捐款國家：{n[0]}金額：{n[1]:.2f},總宣捐款數：{cn[n[0]]} 平均：{n[1]/cn[n[0]]:.2f}")
