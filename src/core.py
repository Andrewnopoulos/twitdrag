import urllib.request
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
				if attr[0] == 'data-conversation-id' and tag == 'a':
					self.activeTweetId = attr[1]
				if attr[0] == 'data-time':
					self.tweetDict[self.activeTweetId] = {'timestamp': attr[1]}

			if attrs[0][1] and 'js-tweet-text tweet-text' in attrs[0][1]:
				self.appendingText = True

	def handle_endtag(self, tag):
		if tag == 'p':
			if self.activeTweetId is not -1 and self.tweetDict[self.activeTweetId]['text']:
				self.activeTweetId = -1
				self.appendingText = False

	def handle_data(self, data):
		if self.appendingText:
			if 'text' in self.tweetDict[self.activeTweetId]:
				if 'pic.twitter.com' in data:
					self.tweetDict[self.activeTweetId]['text'] += ' '
				self.tweetDict[self.activeTweetId]['text'] += data
			else:
				self.tweetDict[self.activeTweetId]['text'] = data

def getJsonDataFromUser(userAccount):
	# baseUrl = 'https://twitter.com/i/search/timeline?f=realtime&q=(from%3Acodeandbeard)&src=typed_query&f=live'
	baseUrl = 'https://twitter.com/i/search/timeline?'
	fromItem = '(from:{})'.format(userAccount)
	parameters = {'f': 'realtime', 'last_note_ts': '85', 'q': fromItem, 'src': 'typd', 'f': 'live'}
	url = baseUrl
	for key in parameters:
		url += key + '=' + parameters[key] + '&'
	url = url[:-1]
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