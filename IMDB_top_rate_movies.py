####################################################################################
#	MY FIRST PROJECT TO SCRAP IMDB WEBSITES TOP RATED MOVIES NAME AND POSTERS      #
####################################################################################
# http://www.imdb.com/chart/top?ref_=nv_mv_250_6 #
# ------------------ #
# By: SURYANSH SINGH #
# ------------------ #


from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

class Film():
	def __init__(self):
		self.title = ""
		self.rank = ""
		self.year = ""
		self.link = ""


def get_film_list():

	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	url = "http://www.imdb.com/chart/top?ref_=nv_mv_250_6"

	driver.get(url)

	# class="chart full-width"

	soup = BeautifulSoup(driver.page_source, "lxml")

	table = soup.find("table", class_ = "chart")

	all_td = table.find_all('td', class_ = "titleColumn")

	# print all_tr

	film_list = []

	for td in all_td:

		ref_link = td.find('a')['href']

		full_title = td.text.encode("UTF-8").strip().replace('\n', '').replace('      ', '')
		print full_title

		rank = full_title.split('.')[0]
		title = full_title.split('.')[1].split('(')[0]
		year = full_title.split('(')[1].split(')')[0]

		newFilm = Film()
		newFilm.title = title
		newFilm.rank = rank
		newFilm.year = year
		newFilm.link = ref_link

		film_list.append(newFilm)
	driver.quit()
	return film_list

# print table

# print driver.page_source.encode("UTF-8")


# for f in get_film_list():
# 	print "-----------------------"
# 	print f.rank
# 	print f.title
# 	print f.year
# 	print f.link
# 	print "-----------------------"


def get_poster_for_each_film(film_list):

	if not os.path.exists('film poster'):
		os.makedirs('film poster')
	
	for film in film_list[0:2]:

		url = "http://www.imdb.com"+film.link

		driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		poster_div = soup.find('div', class_ = 'poster')

		poster_link = poster_div.find('a')['href']

		# print poster_link


		# print poster_div
		# print driver.page_source.encode("UTF-8")

		# move to the link and then get the div with the class pswp__zoom-wrap -> find a and get image form second image..

		driver.get('http://www.imdb.com'+poster_link)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		img_div = soup.find_all("div", class_ = 'pswp__zoom-wrap')

		temp = 0;
		for div in img_div:
			temp = temp + 1
			img_src = div.find_all('img')[1]['src']
			f = open('film poster\{0}{1}.jpg'.format(film.title.encode("UTF-8").replace(':', ''), temp), 'wb')
			f.write(requests.get(img_src).content)
			print img_src

			f.close

	driver.quit()


get_poster_for_each_film(get_film_list())