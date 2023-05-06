import openai, re, requests
import xml.etree.ElementTree as ET

# Установка ключа API OpenAI
openai.api_key = "nea"


# Функция для получения цены на товар
def get_price(product_name):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"What is the price of {product_name}?",
        max_tokens=50
    )
    price_str = response.choices[0].text.strip()
    return price_str


data = [get_price('iphone 12').split()]
# Пример использования функции
print(data)
for i in range(len(data)):
    for x in data[i]:
        if x[0] == '$':
            x = re.sub("[^0-9]", "", x)
            print(x)

usd_rate = float(
    ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
    .find("./Valute[CharCode='USD']/Value")
    .text.replace(',', '.')
)
print(usd_rate)
