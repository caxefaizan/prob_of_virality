from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pprint
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def count(ls):
	chrome_browser = webdriver.Chrome('./chromedriver')
	accumulator = 0
	
	for x in ls:
		x=x.replace(':','')
		x=x.replace('-','')
		x=x.replace('\'','')
		x=x.replace(',','')
		x=x.replace('\"','')
		chrome_browser.get('https://www.instagram.com/explore/tags/caxe/')
		try: 
			text_box = chrome_browser.find_element_by_class_name('TqC_a')
			text_box.click()
			input_search = WebDriverWait(chrome_browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@class,'XTCLo x3qfX')]")))
			input_search.click()
			#time.sleep(1)
			input_search.clear()
			input_search.send_keys(f"#{x}")
			#time.sleep(1)
		except:
			print('login required')
			chrome_browser.close()
		try:
			continue_link = WebDriverWait(chrome_browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "yCE8d  ")))
			continue_link.click()
			#time.sleep(5)
			user_posts = WebDriverWait(chrome_browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "g47SY ")))
			accumulator += int((user_posts.get_attribute('innerHTML')).replace(',',''))
		except:
			print("link broken")
	chrome_browser.close()
	return accumulator
	
res = requests.get('https://www.ndtv.com/top-stories/page-1')
res2 = requests.get('https://www.ndtv.com/top-stories/page-2')
soup = BeautifulSoup(res.text,'html.parser')
soup2 = BeautifulSoup(res2.text,'html.parser')
links1 = soup.select('.nstory_header') 
links2 = soup2.select('.nstory_header') 
mega_links = links1+links2

prepositions = ['A','AS','AN','THE','IN','TO','OF','AND','BUT','SO','\WITH','AT','FROM','INTO','DURING','INCLUDING','UNTIL','AGAINST','AMONG','THROUGHOUT','DESPITE','TOWARDS','UPON'	,'CONCERNING','TO','IN','FOR','ON','BY','ABOUT','LIKE','THROUGH','OVER','BEFORE','BETWEEN','AFTER','SINCE','WITHOUT','UNDER','WITHIN'	,'ALONG'	,'FOLLOWING'	,'ACROSS'	,'BEHIND'	,'BEYOND'	,'PLUS'	,'EXCEPT'	,'BUT'	,'UP'	,'OUT','AROUND'	,'DOWN'	,'OFF','ABOVE'	,'NEAR']


def calculate(lst):
	viral_factors=[]
	for x in lst:
		if x not in prepositions:
			viral_factors.append(x)
	return viral_factors			
		

def news_list(links):
	nl = []
	for idx,item in enumerate(mega_links):
		title = item.getText()
		nl.append({'title':title})
	return nl

head_lines = news_list(mega_links)


for item in head_lines:
	x = item.get("title")
	x = x.upper()
	y = x.split()
	z = calculate(y)
	factor = count(z)
	print(f'Probability of virality of the Headlines Titled: {x} is {factor/(10**3)}%')
