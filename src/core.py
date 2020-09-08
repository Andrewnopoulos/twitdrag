import requests

def getJsonDataFromUser(userAccount):
	# baseUrl = 'https://twitter.com/i/search/timeline?f=realtime&q=(from%3Acodeandbeard)&src=typed_query&f=live'
	baseUrl = 'https://twitter.com/i/search/timeline?'
	fromItem = '(from:{})'.format(userAccount)
	parameters = {'f': 'realtime', 'last_note_ts': '85', 'q': fromItem, 'src': 'typd', 'f': 'live'}
	url = baseUrl
	for key in parameters:
		url += key + '=' + parameters[key] + '&'
	url = url[:-1]
	headers = {'user-agent': 'Chrome/51.0.2704.103'}
	r = requests.get(url, headers=headers)
	# print r.url
	return r.json()

# TODO: data-time
# HTMLParser