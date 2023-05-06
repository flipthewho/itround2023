import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Устанавливаем токен и создаем экземпляр бота
TOKEN = 'цацу'
bot = telegram.Bot(token=TOKEN)

# Создаем пустой массив для сохранения введенных пользователем данных
user_inputs = []


# Функция-обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Привет! Я бот, который поможет вам с оценкой стоимости затрат на содержание сервера. Напишите мне семь (7) сообщений, в которых будут указаны:\n1. Вендор\n2. Модель\n3. Год выпуска\n4. Срок аренды в месяцах\n5. Цена электричества за киловатт (примерно 4₽)\n6. Цена услуг провайдера (примерно 5000₽ в месяц)\n7. Стоимость аренды серверного помещения с охлаждением (примерно 20`000₽)')


# Функция-обработчик текстовых сообщений
def process_input(update, context):
    # Получаем текст сообщения от пользователя
    user_text = update.message.text
    # Добавляем текст введенный пользователем в массив
    user_inputs.append(user_text)
    # Если пользователь ввел уже 7 значений, обрабатываем данные и возвращаем результат
    if len(user_inputs) == 7:


        arenda_electrich = (int(user_inputs[6]) + int(user_inputs[5])) * int(user_inputs[3])
        #result = arenda_electrich +
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Содержание такого оборудования обойдется вам в : {result}₽')


# Создаем объект Updater и привязываем функции-обработчики к командам и сообщениям
updater = Updater(bot.token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, process_input))

# Запускаем бота
updater.start_polling()
updater.idle()
