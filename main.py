import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Устанавливаем токен и создаем экземпляр бота
TOKEN = 'xxx'
bot = telegram.Bot(token=TOKEN)


# Функция-обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,\
                             text="Приветствую! Я - бот ServerGuider, который поможет вам рассчитать стоимость затрат на обслуживание серверного  оборудования!")


# Функция-обработчик текстовых сообщений
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Создаем объект Updater и привязываем функции-обработчики к командам и сообщениям
updater = Updater(bot.token)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
#dispatcher.add_handler(MessageHandler(filters.text, echo))

# Запускаем бота
updater.start_polling()
updater.idle()
