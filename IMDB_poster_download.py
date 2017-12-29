####################################################################################
#  				MY FIRST PROJECT TO SCRAP IMDB WEBSITES TOP POSTERS      		   #
####################################################################################
# http://www.imdb.com/gallery/rg1624939264?ref_=nv_ph_lp_2 #
# ------------------ #
# By: SURYANSH SINGH #
# ------------------ #



from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
import time

driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

for i in range(1, 12):
	
	url = "http://www.imdb.com/gallery/rg1624939264?page={0}&ref_=rgmi_mi_sm".format(i)

	time.sleep(2)
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'lxml')

	container_div = soup.find("div", class_ = 'media_index_thumb_list')

	# print container_div

	if not os.path.exists("img poster"):
		os.makedirs('img poster')

	for img_link in container_div.find_all('a'):
		img_src = img_link['href']
		img_title = img_link['title']
		driver.get('http://www.imdb.com'+img_src)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		img_div = soup.find_all("div", class_ = 'pswp__zoom-wrap')[1]

		img_src = img_div.find_all('img')[1]['src']
		f = open('img poster\{0}.jpg'.format(img_title.encode("UTF-8").replace(':', '')), 'wb')
		f.write(requests.get(img_src).content)

		f.close

driver.quit()
# print driver.page_source.encode('UTF-8')