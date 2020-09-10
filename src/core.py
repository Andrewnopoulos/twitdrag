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
			print ("  ~~~~~~~~~~~~~~~")
			print (self.tweets[tweet]['text'])

	def printRecentTweets(self, numberToPrint=None):
		if numberToPrint is not None and numberToPrint < len(self.tweets):
			tweetsToPrint = list(self.tweets)[-1 * numberToPrint:]
		else:
			tweetsToPrint = self.tweets

		self._printTweetList(tweetsToPrint)


	def printNewTweetsSince(self, lastTweetId):
		if lastTweetId is None or lastTweetId not in self.tweets:
			print("Warning: tweet not found in database")
			return

		tweetList = list(self.tweets)
		recentIndex = tweetList.index(lastTweetId)

		if recentIndex+1 >= len(tweetList):
			print("no new tweets")
			return

		tweetsToPrint = tweetList[recentIndex+1:]

		self._printTweetList(tweetsToPrint)

	def populate(self):
		tweetList = getTweetList(self.username)

		self.tweets = OrderedDict(sorted(tweetList.items(), key=lambda t: t[0]))

	def update(self):
		if len(self.tweets) is not 0:
			lastItem = list(self.tweets)[-1]

		jsonResponse = getJsonDataFromUser(self.username)
		allNewTweets = None

		if jsonResponse:
			allNewTweets = getTweetsFromHtml(jsonResponse['items_html'])

		min_tweet = None

		while True:
			if allNewTweets is None or lastItem in allNewTweets:
				break

			if min_tweet is None:
				min_tweet = list(allNewTweets)[0]

			max_tweet = list(allNewTweets)[-1]

			if min_tweet is not max_tweet:
				if 'min_position' in jsonResponse:
					max_position = jsonResponse['min_position']
				else:
					max_position = "TWEET-%s-%s" % (max_tweet, min_tweet)

				rawJson = getJsonDataFromUser(self.username, max_position)
				nextTweetBatch = None
				if rawJson:
					nextTweetBatch = getTweetsFromHtml(rawJson['items_html'])

				if nextTweetBatch is None:
					break

				allNewTweets.update(nextTweetBatch)

			else:
				break

		self.tweets.update(allNewTweets)
		self.tweets = OrderedDict(sorted(self.tweets.items(), key=lambda t: t[0]))