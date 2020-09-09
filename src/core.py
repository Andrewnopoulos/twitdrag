import urllib.request
from urllib.parse import urlencode, urlunparse
from html.parser import HTMLParser
import ssl
import json

class tweetHTMLParser(HTMLParser):
	def __init__(self, tweetDict):
		super().__init__()
		self.activeTweetId = -1
		self.tweetDict = tweetDict
		self.appendingText = False

	def handle_starttag(self, tag, attrs):
		if attrs:
			for attr in attrs:
				if attr[0] == 'data-tweet-id':
					self.activeTweetId = attr[1]
					self.tweetDict[self.activeTweetId] = {'timestamp': -1, 'text': ""}
				if attr[0] == 'data-time':
					self.tweetDict[self.activeTweetId]['timestamp'] = attr[1]

			if attrs[0][1] and 'js-tweet-text tweet-text' in attrs[0][1]:
				self.appendingText = True

	def handle_endtag(self, tag):
		if tag == 'p':
			if self.activeTweetId is not -1:
				self.activeTweetId = -1
				self.appendingText = False

	def handle_data(self, data):
		if self.appendingText and self.activeTweetId is not -1:
			if 'pic.twitter.com' in data:
				self.tweetDict[self.activeTweetId]['text'] += ' '
			self.tweetDict[self.activeTweetId]['text'] += data

def getJsonDataFromUser(userAccount):
	fromItem = '(from:{})'.format(userAccount)
	params = {
		'f': 'tweets',
		'q': fromItem
	}
	url_tuple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
	url = urlunparse(url_tuple)
	print(url)
	headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	gcontext = ssl.SSLContext()
	r = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(r, context=gcontext)
	# print(response.read())

	return json.loads(response.read())


def parseHtml(htmlinput):
	tweetDict = {}
	parser = tweetHTMLParser(tweetDict)
	parser.feed(htmlinput)
	# print (listOfTweets)
	for tweet in tweetDict:
		print (tweet)
		print (tweetDict[tweet])

# TODO: data-time
# HTMLParser