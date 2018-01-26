import requests, sys, selenium, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
import mysql.connector
from rutermextract import TermExtractor
import pymorphy2

def get_screened_page(from_station, to_station):
	url_params = {
	"domain": "https://metro.yandex.ru/",
	"from_station": from_station,
	"to_station": to_station
	}
	url = "{domain}spb?from={from_station}&to={to_station}&route=0".format(**url_params)
	DRIVER = 'chromedriver'
	driver = webdriver.Chrome(DRIVER)
	try:
		driver.get(url)
		driver.execute_script("document.body.style.zoom=0.8")
		time.sleep(3)
		name = str(from_station) + '-' + str(to_station) + '.png'
		screenshot = driver.save_screenshot(name)
		driver.quit()
	except:
		print("Request wasn't successful")
		sys.exit(0)
	screenshot = Image.open(name)
	screenshot = screenshot.crop((10,80,310,805))
	screenshot.save(name)
	pass

def stations_parser():
	cnx = mysql.connector.connect(
		user='ih813395_bot', 
		password='123123123bot',
		host='185.125.219.232',
		database='ih813395_bot_metro')
	cursor = cnx.cursor()
	DRIVER = 'chromedriver'
	driver = webdriver.Chrome(DRIVER)
	for i in range(67,68):
		url = 'https://metro.yandex.ru/spb?from={i}&to=1&route=0'.format(i = i)
		driver.get(url)
		time.sleep(2)
		metro_name = driver.find_element(By.CLASS_NAME, "route-details-block__terminal-station").text
		print(metro_name)
		term_extractor = TermExtractor()
		metro_normalized = ""
		for term in term_extractor(metro_name, strings=True):
			metro_normalized = term
		if len(metro_normalized) < 2:
			metro_normalized = metro_name.lower()
		print(metro_normalized)
		request = "insert into stations(number, name) values ({number},{name})".format(number = i, name = '"' + metro_normalized + '"')
		#print(request)
		cursor.execute(request)
		cnx.commit()
	pass

def text_request_definer(message):
	bugs_list = [
	'маршрут', 
	'метро', 
	'станция', 
	'проложи', 
	'на'
	]
	message = message.split()
	text = [word for word in message if word not in bugs_list]
	from_station = []
	to_station = []
	for word in text:
		if word == 'от':
			flag_from = True
			flag_to = False
		elif word == 'до':
			flag_to = True
			flag_from = False
		else:
			if flag_from:
				from_station.append(word)
			elif flag_to:
				to_station.append(word)
	morph = pymorphy2.MorphAnalyzer()
	from_normalized = [morph.parse(word)[0].normal_form for word in from_station]
	to_normalized = [morph.parse(word)[0].normal_form for word in to_station]
	
	return from_normalized, to_normalized

# get_screened_page(67,6)
#stations_parser()
print(text_request_definer('проложи маршрут на метро от академической до технологического института'))
