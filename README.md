# TwitDrag

TwitDrag is a Python3 application for monitoring twitter accounts.

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install BeautifulSoup for html parsing.

```bash
pip install beautifulsoup4
```

## Usage

view help:
```bash
python3 twitdrag -h
```

Print recent tweets from and continue to monitor a twitter account
```bash
python3 twitdrag nytimes
```

Output a json object containing tweets that have been monitored by TwitDrag so far
```bash
python3 twitdrag nytimes --dump
```

Wait 5 minutes between scrapes instead of the default 10
```bash
python3 twitdrag nytimes --timer=5
```

## Requirements
There were a number of requirements for this project:
- The program must output text from new tweets to stdout.
- The program must output the 5 most recent tweets right after execution, then it must check for new tweets (and display them) every 10 mins.
- The Twitter handle will be provided as a command line argument by the user starting the program
- Make sure to use scraping or APIs that do not require user authentication or a twitter developer account.
- Must not use open source libraries such as Twint, Tweepy to do the heavy lifting
### Assumptions
I've written this with the assumption that it's intended more as a monitoring system than a tweet history lookup. For this reason, the number of most recent tweets shown initially (specified in the requirements as 5) can only be increased to 20 without further development as that's the maximum size of the initial search query. More focus was thus placed on ensuring correctness in the subsequent scrapes, making sure that if more than 20 tweets are made in the 10 minutes between scrapes that they're all handled.

>Must not use open source libraries such as Twint, Tweepy to do the heavy lifting

I've assumed that this doesn't apply to a simple html parser, hence the inclusion of BeautifulSoup

>The program must output text from new tweets to stdout.

I assume that the only output the user requests is the text of the tweet, and so other details such as likes and retweets are ommitted from output and recording.

>The Twitter handle will be provided as a command line argument by the user starting the program

This sounds like a request that the CLI is written such that the user account can just be provided as a positional argument, instead of as an optional argument.
```bash
python3 twitdrag nytimes
```
as opposed to
```bash
python3 twitdrag --account=nytimes
```
However this is something I would clarify with the end user.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)