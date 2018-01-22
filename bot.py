import telebot
import requests
from bs4 import BeatifulSoup

access_token = 335894434:AAF8cRoHH8syXSBzhJqeYrrwnaiBKDTnefY
bot = telebot.TeleBot(access_token)
@bot.message_handler(content_types=['text'])

def echo(message):
    bot.send_message(message.chat.id, message.text)

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

def get_shedule(page, day = '1'):
	day += 'day'
	soup = BeatifulSoup(page,'html5lib')
	shedule = soup.find('table', attrs = {"id" = day})
	time_list = shedule.find_all('td', attrs = {"class" = "time"})
	time_list = [time.span.text for time in time_list]
	room_list = shedule.find_all('td', attrs = {"class" = "room"})
    room_list = [room.span.text for room in room_list]
    lessons_list = shedule.find_all('td', attrs = {"class" = "lesson"})
    lessons_list = [lesson.span.text for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson if info]) for lesson in lessons_list]
    return time_list, room_list, lessons_list

if __name__ == '__main__':
    bot.polling(none_stop=True)