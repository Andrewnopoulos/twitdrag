import urllib.request
from urllib.parse import urlencode, urlunparse
from bs4 import BeautifulSoup
import ssl
import json
from collections import OrderedDict

def getJsonDataFromUser(userAccount, max_position=None):
	fromItem = '(from:{})'.format(userAccount)

	params = {
		'f': 'tweets',
		'q': fromItem
	}

	if max_position:
		params['max_position'] = max_position

	url_tuple = ('https', 'twitter.com', '/i/search/timeline', '', urlencode(params), '')
	url = urlunparse(url_tuple)

	headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	gcontext = ssl.SSLContext()
	r = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(r, context=gcontext)

	return json.loads(response.read())


def getTweetsFromHtml(htmlinput):
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

	return tweetDict

def getTweetList(userAccount, max_position=None):

	rawJson = getJsonDataFromUser(userAccount, max_position)

	tweetList = None
	if rawJson:
		tweetList = getTweetsFromHtml(rawJson['items_html'])

	return tweetList

class TweetDragger:

	def __init__(self, username):
		self.username = username
		self.tweets = {}

	def _printTweetList(self, tweetList):
		for tweet in tweetList:
			print()
			print (self.tweets[tweet]['text'])
		print()

	def getLatestTweet(self):
		if self.tweets is not None and len(self.tweets) > 0:
			return list(self.tweets)[-1]

		return None

	def printRecentTweets(self, numberToPrint=None):
		if numberToPrint is not None and numberToPrint < len(self.tweets):
			tweetsToPrint = list(self.tweets)[-1 * numberToPrint:]
		else:
			tweetsToPrint = self.tweets

		self._printTweetList(tweetsToPrint)


	def printNewTweetsSince(self, lastTweetId):
		if len(self.tweets) == 0:
			return

		if lastTweetId is None or lastTweetId not in self.tweets:
			self._printTweetList(self.tweets)

		tweetList = list(self.tweets)
		recentIndex = tweetList.index(lastTweetId)

		if recentIndex+1 >= len(tweetList):
			print("\tno new tweets")
			print()
			return

		tweetsToPrint = tweetList[recentIndex+1:]

		self._printTweetList(tweetsToPrint)

	def populate(self):
		tweetList = getTweetList(self.username)

		self.tweets = OrderedDict(sorted(tweetList.items(), key=lambda t: t[0]))

	def update(self):
		lastItem = None
		if len(self.tweets) is not 0:
			lastItem = list(self.tweets)[-1]

		jsonResponse = getJsonDataFromUser(self.username)
		tweets = None

		allNewTweets = {}

		if jsonResponse:
			tweets = getTweetsFromHtml(jsonResponse['items_html'])
			for tweet in tweets:
				allNewTweets[tweet] = tweets[tweet]

		while True:
			if len(tweets) == 0 or lastItem in tweets:
				break

			min_tweet = list(tweets)[0]
			max_tweet = list(tweets)[-1]

			if 'min_position' in jsonResponse:
				max_position = jsonResponse['min_position']
			else:
				max_position = "TWEET-%s-%s" % (max_tweet, min_tweet)

			jsonResponse = getJsonDataFromUser(self.username, max_position)

			tweets = getTweetsFromHtml(jsonResponse['items_html'])

			for tweet in tweets:
				allNewTweets[tweet] = tweets[tweet]

		self.tweets.update(allNewTweets)
		self.tweets = OrderedDict(sorted(self.tweets.items(), key=lambda t: t[0]))