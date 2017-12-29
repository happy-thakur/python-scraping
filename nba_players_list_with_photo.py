####################################################################################
# 			MY FIRST PROJECT TO SCRAP http://stats.nba.com/player/203518/		   #
####################################################################################
# ------------------ #
# By: SURYANSH SINGH #
# ------------------ #

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import time

class Player():
	def __init__(self):
		self.name = ""
		self.link = ""
		self.height = ""
		self.width = ""


#  THIS IS TO GET THE ALL PLAYERS LIST
def getPlayerList():
	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	url = "http://stats.nba.com/players/list/"

	driver.get(url)

	html_doc = driver.page_source

	# CREATING SOUP...
	soup = BeautifulSoup(html_doc, 'lxml')

	div = soup.find('div', class_ = "stats-player-list")

	player_list = []

	for a in div.find_all('a'):
		# print a.text
		# print a['href']
		newPlayer = Player()
		newPlayer.name = a.text
		newPlayer.link = a['href']
		player_list.append(newPlayer)

	for a in player_list:
		print a.name
		print a.link


	driver.quit()
	return player_list


# THIS IS TO GET THE DETAIL FROM THE LIST..
def get_all_player_detail(player_list):

	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	
	for p in player_list:
		if(len(p.link) > 0):
			url = "http://stats.nba.com"+p.link

			driver.get(url)

			html_doc = driver.page_source

			soup = BeautifulSoup(html_doc, "lxml")

			height = ""
			born = ""
			weight = ""


			h_div = soup.find("div", string = 'HT')

			for div in h_div.findNextSiblings():
				height += div.text

			w_div = soup.find("div", string = 'WT')


			for div in w_div.findNextSiblings():
				weight += div.text

			b_div = soup.find("div", string = "BORN")

			for div in b_div.findNextSiblings():
				born += div.text

			p.height = height
			p.born = born
			p.weight = weight
			print height
			print weight
			print born
		else:
			print p.link
			print p.name

	driver.quit()

	return player_list

# UNCOMMENT TO RUN FETCH THE LIST WITH HEIGHT WEIGHT AND DOB
# player_list = get_all_player_detail(getPlayerList())


# THIS IS TO GET THE IMAGE OF THE PLAYER..
def get_player_image(player_list):

	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	if not os.path.exists('player images'):
		os.makedirs('player images')

	for p in player_list:
		if(len(p.link) > 0):
			# player-summary__image-block
			url = "http://stats.nba.com"+p.link

			driver.get(url)

			time.sleep(2)

			soup = BeautifulSoup(driver.page_source, 'lxml')

			# print driver.page_source.encode("UTF-8")

			img_div = soup.find('div', class_ = 'player-summary__image-block')

			img = img_div.find("img")

			print img['src']

			f = open('player images\{0}.jpg'.format(p.name), 'wb')

			f.write(requests.get(img['src']).content)

			f.close()

	driver.quit()


get_player_image(getPlayerList())