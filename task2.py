import requests
from bs4 import BeautifulSoup
#import pprint
from datetime import datetime
#import urllib.parse
import tweepy
import matplotlib.pyplot as plt
import csv
import json


def predict(stra):
	auth = tweepy.OAuthHandler('Ct665pfqVroHRHgW3ma241QkS', 'bJxtEwOA2UKgoL7M14p12CwHpiCCnjykOquzF4aCHQuKMPFUdG')
	auth.set_access_token('1249374914894675969-nEKHHZyNIQVYJ2xvdgT0SLURs9rlgW', 'yJgVGbHT1WlEOCy8qvHXeovGJpdqJKG1bdNaB8fQAywQ8')
	api = tweepy.API(auth)
	tweets = api.search(stra)
	tweet_id = []
	with open('tweet_id.txt', 'r') as id_file:
		for x in id_file:
			data = x[:-1]
			tweet_id.append(data)
    

	tot_rt=[]
	

	for x in tweets:
		post_id = (x.id)
		#tweet = api.get_status(post_id)
		print(post_id)
		if post_id not in tweet_id:
			tweet_id.append(post_id)


	with open('tweet_id.txt', 'w') as id_file:
		for x in tweet_id:
			id_file.write('%s\n' % x)


	for x in tweet_id:
		tweet = api.get_status(x)
		if tweet.retweet_count not in tot_rt:
			tot_rt.append(tweet.retweet_count) 
		else:
			tot_rt.append(0)
	#print(tweet_id)
	#print(tot_rt)
	total_retweets = 0
	for x in tot_rt:
		total_retweets += x
	return total_retweets


def garbage_removal(lst):
	clean_text=''
	for x in lst:
		if x.upper() not in prepositions:
			clean_text +=(f' {x}')
	return clean_text			
		

def news_list(links):
	nl = []
	for idx,item in enumerate(mega_links):
		title = item.getText()
		nl.append({'title':title})
	return nl


start_time = datetime.now()
print(start_time)
res = requests.get('https://www.ndtv.com/top-stories/page-1')
res2 = requests.get('https://www.ndtv.com/top-stories/page-2')
soup = BeautifulSoup(res.text,'html.parser')
soup2 = BeautifulSoup(res2.text,'html.parser')
links1 = soup.select('.nstory_header') 
links2 = soup2.select('.nstory_header') 
mega_links = links1+links2
prepositions = ['A','AS','AN','THE','IN','TO','OF','AND','BUT','SO','\WITH','AT','FROM','INTO','DURING','INCLUDING','UNTIL','AGAINST','AMONG','THROUGHOUT','DESPITE','TOWARDS','UPON'	,'CONCERNING','TO','IN','FOR','ON','BY','ABOUT','LIKE','THROUGH','OVER','BEFORE','BETWEEN','AFTER','SINCE','WITHOUT','UNDER','WITHIN'	,'ALONG'	,'FOLLOWING'	,'ACROSS'	,'BEHIND'	,'BEYOND'	,'PLUS'	,'EXCEPT'	,'BUT'	,'UP'	,'OUT','AROUND'	,'DOWN'	,'OFF','ABOVE'	,'NEAR']
head_lines = news_list(mega_links)
'''
#for  multiple head lines
for item in head_lines:
	x = item.get("title")
	y = x.split()
	z = garbage_removal(y)
	val = predict(z)
'''
#for a single headline
test_string1 = 'Wear Masks Or Pay Rs 5,000 Fine, Says Ahmedabad Civic Body'  #Static News Headlines
y1=test_string1.split()
#z = urllib.parse.quote(garbage_removal(y1))
z=garbage_removal(y1)
print(z)
val = predict(z)
with open('test.txt',mode='a') as my_file:
	text = my_file.write(f'\n{start_time} , {val}')
x = []
y = []
with open('test.txt') as csvfile:
	plots = csv.reader(csvfile,delimiter=',')
	for row in plots:
		x.append(row[0])
		y.append(int(row[1]))
ref_length = len(x)
a = []
b = []
with open('reference.txt',mode='r') as csvfile:
	ref_plot = csv.reader(csvfile,delimiter=',')
	for row in ref_plot:
		a.append(row[0])
		b.append(int(row[1]))
a=a[:ref_length]
b=b[:ref_length]

plt.plot(x,y,'b',marker='o')
plt.xticks(rotation=45)
plt.xlabel('Time')
plt.ylabel('Retweets')
plt.title('Prediction of Virality')
plt.plot(x,b,'r')
percentage = (y[-1]/b[-1])*100
print(f'Probability of Virality = {percentage}%')
plt.show()

