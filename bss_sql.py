import MySQLdb
import requests
import json
import time
import logging


pill = u'\U0001F48A'
hand = u'\U0001F449'
warning = u'\U000026A0'
time_wait = u'\U000023F1'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TOKEN = '476931349:AAGecJeO0tZCabU8O5JEOgMYpjA00t27eWs'


def conn_sql():
    logging.info(time.strftime('%X') + ' --> Бот: Подключение к БД...')
    # print(time.strftime('%X') + ' --> Бот: Подключение к БД...')
    conn = MySQLdb.connect(host='f962794y.beget.tech',
                           database='f962794y_bss24',
                           user='f962794y_bss24',
                           password='bss24f962794$$$',
                           charset='utf8')
    logging.info(time.strftime('%X') + ' --> Бот: Подключение выполнено!')
    # print(time.strftime('%X') + ' --> Бот: Подключение выполнено!')
    return conn


#===================== LIST ITEMS IN TOWN ============================


def in_brn():
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT name, price, command FROM main WHERE \
      chat_id is NULL ORDER BY name")
    results = cur.fetchall()
    cur.close()
    conn.close()
    logging.info(time.strftime('%X') + ' --> Бот: Отключение от БД.')
    # print(time.strftime('%X') + ' --> Бот: Отключение от БД.')
    list_item = ''
    i = 0
    for item in results:
        list_item += '\n' + pill + '<b>' + results[i][0] +\
            '</b> - ' + results[i][1] + 'р.' + hand + results[i][2]
        i += 1

    if list_item == '':
        list_item = '\n' + u'\U000026A0' + ' <em>Товар закончился</em>'

    logging.info(list_item)
    return list_item


#===================== BUY 1 POSITION ===================================


def buy_brn_1200(chat_id):
    ticks = time.time()
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT unique_code, price FROM main WHERE \
            chat_id is NULL AND name = 'Амф 0.5г (город)' ORDER BY \
            unique_code ASC")
    results = cur.fetchall()
    cur.close()
    conn.close()
    promt = ''

    if len(results) == 0:
        promt = warning + '<i>Этот товар закончился</i>'

    elif (len(results) > 0 and rule_1(chat_id) == 'true'):
        conn = conn_sql()
        cur = conn.cursor()
        cur.execute("""UPDATE main SET chat_id = %s, time_begin = %s \
                    WHERE unique_code = '%s'""" %
                    (chat_id, ticks, results[0][0]))
        conn.commit()
        cur.close()
        conn.close()

        promt = u'\U0001F48A' + '<b>Амф 0.5г (город)</b>' +\
                '\n-----------------------\n' +\
                'Qiwi-кошелек: +79619938166\n' +\
                'Cумма к оплате: <b>' +\
                str(results[0][1]) + 'р.</b>\n' +\
                'Ваш комментарий к заказу: <b>' + str(results[0][0]) +\
                '</b>\n-----------------------\n' +\
                'Проверка оплаты: ' + hand + ' /check_payment'

    else:
        promt = u'\U0001F539' + '<b> У Вас уже имеются заказы.</b> ' +\
                '\nОплатите их, либо подождите\n' +\
                'истечения времени брони.\n' +\
                '--------------------------\n' +\
                '<b>Проверка оплаты:</b> ' + hand + ' /check_payment'

    return promt


#===================== BUY 2 POSITION ===================================


def buy_brn_2100(chat_id):
    ticks = time.time()
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT unique_code, price FROM main WHERE \
            chat_id is NULL AND name = 'Амф 1.0г (город)' ORDER BY \
            unique_code ASC")
    results = cur.fetchall()
    cur.close()
    conn.close()
    promt = ''

    if len(results) == 0:
        promt = warning + '<i>Этот товар закончился</i>'

    elif (len(results) > 0 and rule_1(chat_id) == 'true'):
        conn = conn_sql()
        cur = conn.cursor()
        cur.execute("""UPDATE main SET chat_id = %s, time_begin = %s \
                    WHERE unique_code = '%s'""" %
                    (chat_id, ticks, results[0][0]))
        conn.commit()
        cur.close()
        conn.close()

        promt = u'\U0001F48A' + '<b>Амф 1.0г (город)</b>' +\
                '\n-----------------------\n' +\
                'Qiwi-кошелек: +79619938166\n' +\
                'Cумма к оплате: <b>' +\
                str(results[0][1]) + 'р.</b>\n' +\
                'Ваш комментарий к заказу: <b>' + str(results[0][0]) +\
                '</b>\n-----------------------\n' +\
                'Проверка оплаты: ' + hand + ' /check_payment'

    else:
        promt = u'\U0001F539' + '<b> У Вас уже имеются заказы.</b> ' +\
                '\nОплатите их, либо подождите\n' +\
                'истечения времени брони.\n' +\
                '--------------------------\n' +\
                '<b>Проверка оплаты:</b> ' + hand + ' /check_payment'

    return promt


# #=========================== QIWI CHECK =================================

def check_qiwi(chat_id):
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT unique_code, price, komment, pic_url_1\
                FROM main WHERE chat_id = %s" % str(chat_id))
    row_values = cur.fetchall()
    cur.close()
    conn.close()

    if len(row_values) != 0:

        part_1 = row_values
        api_access_token = '4290cc16cccf361f6eb64b08ae8819a0'
        my_login = '+79619938166'
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + api_access_token
        parameters = {'rows': '10', 'operation': 'IN'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' +
                  my_login+'/payments', params=parameters)
        parsed_string = json.loads(h.text)

        # j = 0
        # for item in parsed_string:
        #     logging.info(str(parsed_string["data"][j]["comment"]) + '---' +
        #                  str(parsed_string["data"][j]["total"]["amount"]))
        #     j += 1

        if rule_2(parsed_string, part_1) == 'true':
                conn = conn_sql()
                cur = conn.cursor()
                logging.info(part_1[0][0])
                logging.info(chat_id)
                cur.execute("INSERT INTO `f962794y_bss24`.`trades` \
                             SELECT `f962794y_bss24`.`main`.* \
                             FROM `f962794y_bss24`.`main` \
                             WHERE `unique_code`='%s'" % str(part_1[0][0]))
                conn.commit()
                cur.execute("DELETE FROM main WHERE unique_code = '%s' AND \
                            chat_id = %s" % (str(part_1[0][0]), str(chat_id)))
                conn.commit()
                cur.close()
                conn.close()

                check_payed = (u'\U00002705' + 'Платеж выполнен!',
                               str(part_1[0][2]),
                               str(part_1[0][3]))

        elif (rule_3(chat_id) != '1' and
              rule_3(chat_id) != '2'):
                check_payed = (u'\U000023F1' + ' <b>Ожидание платежа...</b>' +
                               '\n--------------------------\n' +
                               'Детали оплаты: ' + u'\U0001F4B3' +
                               '\n--------------------------\n' +
                               'Qiwi-кошелек: <b>+79619938166</b>\n' +
                               'Cумма к оплате: ' +
                               str(part_1[0][1]) + 'р.\n' +
                               'Коментарий к платежу: ' + str(part_1[0][0]) +
                               '\n--------------------------\n' +
                               rule_3(chat_id))

        elif (rule_3(chat_id) == '2'):
                check_payed = (u'\U0001F538' +
                               'Время ожидания оплаты <b>истекло</b>.\n' +
                               'Сделайте <b>новый заказ</b> ' + u'\U0001F6D2' +
                               hand + ' /start')

    else:
        check_payed = ('Сделать <b>новый заказ</b> ' + u'\U0001F6D2' +
                       hand + ' /start')

    return check_payed


# #=========================== RULES 1 =================================


def rule_1(chat_id):
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM main WHERE chat_id =" + str(chat_id) + "")
    results = cur.fetchall()
    cur.close()
    conn.close()
    if len(results) == 0:
        return 'true'
    else:
        return 'false'


# #=========================== RULES 2 ================================


def rule_2(parsed_string, part_1):
    i = 0
    for item in parsed_string["data"]:
        if (str(parsed_string["data"][i]["comment"]) ==
                str(part_1[0][0]) and
                str(parsed_string["data"][i]["total"]["amount"]) >=
                str(part_1[0][1])):
            return 'true'
            break
        else:
            return 'false'

        i += 1


# #=========================== RULES 3 ================================


def rule_3(chat_id):
    promt = ('Сделать новый заказ --> /start')
    conn = conn_sql()
    cur = conn.cursor()
    cur.execute("SELECT time_begin, unique_code FROM main \
                          WHERE chat_id = '%s'" % str(chat_id))
    time_start = cur.fetchall()
    cur.close()
    conn.close()

    if len(time_start) != 0:
        time_remaning = round((900 -
                             (round(time.time()) - time_start[0][0]))/60)

        if time_remaning > 0:
            promt = ('<b>Проверка оплаты:</b> ' + hand + ' /check_payment\n' +
                     '--------------------------\n' +
                     u'\U000023F3' + ' <i>(Осталось: ' +
                     str(time_remaning) + ' мин)</i>')

        else:
            promt = '1'
            conn = conn_sql()
            cur = conn.cursor()
            cur.execute("""UPDATE main SET chat_id = NULL, \
                        time_begin = NULL \
                        WHERE unique_code = '%s'""" % time_start[0][1])
            conn.commit()
            cur.close()
            conn.close()

    else:
        promt = '2'

    return promt
