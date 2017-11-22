import telebot
import bss_sql
import logging

TOKEN = bss_sql.TOKEN
bot = telebot.TeleBot(TOKEN)

bls = u'\U00002605'
city = u'\U0001F3F0'
hot = u'\U0001F525'
globe = u'\U0001F30D'
money = u'\U00014FB0'
credit = u'\U0001F4B3'
red = u'\U0001F4CD'
pill = u'\U0001F48A'
warning = u'\U000026A0'
hand = u'\U0001F449'
rice = u'\U0001F35A'
times = u'\U000023F1'
ticket = u'\U0001F39F'
trava = u'\U00002618'
decor = '\n-------------------------'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, hot +
                     '<i>Моментальные покупки на </i>' +
                     '<b>-=VAGABUND24=-</b>' + decor +
                     '\n'+city+'Барнаул '+hand+' /barnaul' +
                     '\n'+city+'Бийск   '+hand+' /biysk',
                     parse_mode='HTML')


#---------------------------------#

@bot.message_handler(commands=['barnaul'])
def command_barnaul(message):
    items = bss_sql.in_brn()
    bot.send_message(message.chat.id, city + '<b>Барнаул:</b>' +
                     decor + items +
                     decor + '\n'+globe+'Список городов: '+hand+' /start',
                     parse_mode='HTML')


#---------------------------------#

@bot.message_handler(commands=['biysk'])
def command_biysk(message):
    bot.send_message(message.chat.id, city + '<b>Бийск:</b>' + decor +
                     '\n' + warning + ' <em>Товар закончился</em>' +
                     decor + '\n'+globe+'Список городов: '+hand+' /start',
                     parse_mode='HTML')


#---------------------------------#

@bot.message_handler(commands=['buy_1200'])
def command_buy_1200(message):
    promt = bss_sql.buy_brn_1200(message.chat.id)
    bot.send_message(message.chat.id, promt, parse_mode='HTML')
    bot.send_message('248333540', '<pre>Клиент: ' +
                     str(message.chat.first_name) +
                     '(chat_id: ' +
                     str(message.chat.id) + ')' +
                     ' - сделал заказ</pre>', parse_mode='HTML')


#---------------------------------#

@bot.message_handler(commands=['buy_2100'])
def command_buy_2100(message):
    promt = bss_sql.buy_brn_2100(message.chat.id)
    bot.send_message(message.chat.id, promt, parse_mode='HTML')
    bot.send_message('248333540', '<pre>Клиент: ' +
                     str(message.chat.first_name) +
                     '(chat_id: ' +
                     str(message.chat.id) + ')' +
                     ' - сделал заказ</pre>', parse_mode='HTML')


#---------------------------------#
@bot.message_handler(commands=['check_payment'])
def command_check_payment(message):
    check_pay = bss_sql.check_qiwi(message.chat.id)
    logging.info(len(check_pay))
    if len(check_pay) > 3:
        bot.send_message(message.chat.id, check_pay, parse_mode='HTML')

    elif len(check_pay) == 3:
        logging.info(check_pay)
        # admin_message = message.chat.username
        i = 0
        for item in check_pay:
            bot.send_message(message.chat.id, check_pay[i], parse_mode='HTML')
            i += 1

        bot.send_message(message.chat.id, 'Сделать <b>новый заказ</b> ' +
                         u'\U0001F6D2' +
                         hand + ' /start', parse_mode='HTML')
        bot.send_message('248333540', '<pre>Клиент: ' +
                         str(message.chat.first_name) +
                         '(chat_id: ' +
                         str(message.chat.id) + ')' +
                         ' - купил товар</pre>', parse_mode='HTML')
        bot.send_message('293832770', '<pre>Клиент: ' +
                         str(message.chat.first_name) +
                         '(chat_id: ' +
                         str(message.chat.id) + ')' +
                         ' - купил товар</pre>', parse_mode='HTML')


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id,
                     '\n'+bls+bls+bls+bls+bls+bls +
                     bls+bls+bls+bls +
                     '\n'+'   VAGABUND 24h  ' +
                     '\n'+bls+bls+bls+bls+bls+bls +
                     bls+bls+bls+bls +
                     '\n'+globe+'Список городов: '+hand+' /cities',
                     parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     '\n<b>VAGABUND 24h HELP</b>' + decor + '\n' + hand +
                     '1. Для того, чтобы <b>сделать</b>' +
                     ' <i>заказ</i> - перейдите ' +
                     'по --> /start, для выбора города.' + decor +
                     '\n' + hand + '2. <b>Сделайте</b> заказ ' +
                     'выбрав позицию товара' + decor +
                     '\n' + hand + '3. <b>Произведите оплату</b> по' +
                     ' указанным реквизитам.' + decor +
                     '\n' + hand + '4. <b>Проверьте статус</b>' +
                     ' оплаты своего <i>заказа</i>.' +
                     '<b> Таймер</b> ожидания оплаты заказа <b>15 мин</b>.' +
                     'После <b>истечения времени</b>' +
                     ' ваша бронь <i>анулируется</i> и ' +
                     'вы снова сможете <i>сделать заказ</i>' + decor,
                     parse_mode='HTML')

bot.polling()
