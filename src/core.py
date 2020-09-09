import urllib.request
from urllib.parse import urlencode, urlunparse
from bs4 import BeautifulSoup
import ssl
import json


def getJsonDataFromUser(userAccount):
	fromItem = '(from:{})'.format(userAccount)

	params = {
		'f': 'tweets',
		'q': fromItem
	}

	url_tuple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
	url = urlunparse(url_tuple)

	headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	gcontext = ssl.SSLContext()
	r = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(r, context=gcontext)

	return json.loads(response.read())


def parseHtml(htmlinput):
	tweetDict = {}

	soup = BeautifulSoup(htmlinput, "html.parser")
	for tweetData in soup.find_all("li", class_='js-stream-item'):
		if 'data-item-id' not in tweetData.attrs:
			continue

		tweetDict[tweetData['data-item-id']] = {
			'timestamp' : None,
			'text' : None,
		}

		tweetText = tweetData.find('p', class_="tweet-text")
		if tweetText:
			tweetDict[tweetData['data-item-id']]['text'] = tweetText.get_text()

		timestamp = tweetData.find('span', class_='_timestamp')
		if timestamp:
			tweetDict[tweetData['data-item-id']]['timestamp'] = timestamp['data-time']

	for tweet in tweetDict:
		# print (tweet)
		print (tweetDict[tweet]['text'])
		print ("__________________________________________________________")