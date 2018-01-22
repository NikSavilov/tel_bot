import telebot
import requests
from bs4 import BeautifulSoup

access_token = '335894434:BAF8cRoHH8syXSBzhJqeYrrwnaiBKDTnefY'
bot = telebot.TeleBot(access_token)

def get_page(group = 'M3100', week = ''):
    if week:	
        week = week + '/'
    url = 'http://www.ifmo.ru/ru/schedule/0/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        group = group,
        week = week,
        )
    response = requests.get(url)
    page = response.text
    return page

def get_schedule(page, day = '1'):
    day += 'day'
    soup = BeautifulSoup(page,"html5lib")
    shedule = soup.find('table', attrs = {"id": day})
    time_list = shedule.find_all('td', attrs = {"class": "time"})
    time_list = [time.span.text for time in time_list]
    room_list = shedule.find_all('td', attrs = {"class": "room"})
    room_list = [room.span.text for room in room_list]
    lessons_list = shedule.find_all('td', attrs = {"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson if info]) for lesson in lessons_list]
    return time_list, room_list, lessons_list

@bot.message_handler(commands=['monday'])
def get_monday(message):
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)

    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')

if __name__ == '__main__':
    bot.polling(none_stop=True)