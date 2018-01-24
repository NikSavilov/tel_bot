import requests, sys, selenium, time, os
from selenium import webdriver
from PIL import Image

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
	screenshot = screenshot.crop((0,100,245,700))
	screenshot.save(name)
	pass


get_screened_page(67,6)

