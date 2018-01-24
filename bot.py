import telebot, sys, random
import requests
from package import vk
from bs4 import BeautifulSoup

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

def send_schedule(message):
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page)

    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')

def find_longest_word(message):
	longest_word = 'lol'
	max_len = 0
	for word in message.split():
		if len(word) > max_len:
			max_len = len(word)
			longest_word = word
	return longest_word

#### Getting messages from some chat and creating a bot #####
access_token = '335894434:AAF8cRoHH8syXSBzhJqeYrrwnaiBKDTnefY'
bot = telebot.TeleBot(access_token)
profile = 101909873	# mal 175747053 # ler 101909873 rya 86124924
messages = vk.messages_aggregator(profile)
#[messages.append(item) for item in vk.messages_aggregator(175747053)]
##############################################################

@bot.message_handler(content_types=["text"])
def stupid(message):
	bot.send_message(message.chat.id,'Хозяин отключил меня, потому что я слишком много знаю.')
	pass

def define_request_type(message,messages = messages):
	try:
		print(message.text)
		message.text = message.text.lower() 
		answers = [{'num': num, 'text': mes['body'].lower(), 'from_id': mes['from_id'] } for num, mes in enumerate(messages)]
		founded_requests = []
		founded_answers = []
		possible_answers = []
		key_word = find_longest_word(message.text)
		for req in answers:
			chat_key_word = find_longest_word(req['text'])
			if chat_key_word in message.text.split():
				founded_requests.append(req)
			elif message.text == req['text']:
				founded_requests.append(req)
				#print("req",req)
		for req in founded_requests:
			num = req['num']
			from_id = req['from_id']
			#print('found', req)
			for i in range(num -1,-1,-1):
				#print(i, answers[i])
				if answers[i]['from_id'] != from_id:
					founded_answers.append(answers[i]['text'])
					break
		bot.send_message(message.chat.id, founded_answers[random.randint(0, len(founded_answers) - 1)])			
	except:
		unknow_answers = ['Черт. Я потекла', 'Слава солнцеликому!!1!1!', 'не пойму тебя', 'хмммм', 'рот закрой!!)','хочу на мооооре', 'фух']
		bot.send_message(message.chat.id, unknow_answers[random.randint(0, 6)])	
if __name__ == '__main__':
    bot.polling(none_stop=True)