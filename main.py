import telegram, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai, re, requests
import xml.etree.ElementTree as ET

# Устанавливаем токен и создаем экземпляр бота
TOKEN = '6124725227:AAEbZBkGhBUNLMMTwkK9x0'
bot = telegram.Bot(token=TOKEN)
openai.api_key = "sk-n8TA3BHaeTRvcQB3pwkL1yB4cwzRKx"

# Создаем пустой массив для сохранения введенных пользователем данных
user_inputs = []
prevprice = ''
prevarend = ''

def get_price(product_name):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"What is the price of {product_name}?",
        max_tokens=50
    )
    price_str = response.choices[0].text.strip()
    return price_str


# Функция-обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Привет! Я бот, который поможет вам с оценкой стоимости затрат на содержание сервера. ')
    time.sleep(2)
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Напишите мне девять (9) сообщений, в которых будут указаны:\n1. Вендор\n2. Модель\n3. Год выпуска\n4. Срок аренды в месяцах\n5. Цена электричества за киловатт (примерно 4₽)\n6. Цена услуг провайдера (примерно 5000₽ в месяц)\n7. Стоимость аренды серверного помещения с охлаждением (примерно 20`000₽)\n8. Количество серверов\n9. Потребляемая блоком питания мощность(в Ваттах!!!)')


def process_input(update, context):
    # Получаем текст сообщения от пользователя
    user_text = update.message.text
    # Добавляем текст введенный пользователем в массив
    user_inputs.append(user_text)
    # Если пользователь ввел уже 7 значений, обрабатываем данные и возвращаем результат
    if len(user_inputs) == 3:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                                 text='Фиксируем')
    if len(user_inputs) == 9:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Готово! Сейчас вернемся с результатами. Hang out \U0001F60E')
        name = f'{user_inputs[0]} {user_inputs[1]} {user_inputs[2]}'
        data = [get_price(name).split()]
        price = []
        # бегаем по списку ищем цену в долларах
        for i in range(len(data)):
            for x in data[i]:
                if x[0] == '$':
                    x = re.sub("[^0-9]", "", x)
                    price.append(int(x))
        # чуток парсим цб
        usd_rate = float(
            ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
            .find("./Valute[CharCode='USD']/Value")
            .text.replace(',', '.')
        )
        # конвертируем в рубли
        finallyprice = int(usd_rate * (sum(price) / len(price)))
        # сервера - такие же компьютеры, и блоки питания по 0.5КВт, максимум 1кВт
        arendaAndOther = int(user_inputs[5]) + int(user_inputs[6]) + int(user_inputs[7]) + (
                (31 * 24 * int(user_inputs[8])) / 1000)
        result = (finallyprice * int(user_inputs[7])) + (arendaAndOther * int(user_inputs[3]))
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Содержание {name}, стоящего {finallyprice}₽ за штуку, обойдется вам в: {result}₽ вместе с покупкой сервера\nОбслуживание в месяц будет стоить {arendaAndOther}₽')
        user_inputs.clear()

# Создаем объект Updater и привязываем функции-обработчики к командам и сообщениям
updater = Updater(bot.token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, process_input))
# Запускаем бота
updater.start_polling()
updater.idle()
