import requests

response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
data = response.json()
# print(data["USDBRL"]["bid"])
taxa_dolar = float(data["USDBRL"]["bid"])
print(f"Taxa de dólar: R$ {taxa_dolar:.2f}")
