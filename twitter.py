from requests_oauthlib import OAuth1Session
import json

def post(content):
	params = {"status": content}
	post_url = "https://api.twitter.com/1.1/statuses/update.json"
	twitter = OAuth1Session(
		"OAUTH INFO"
	)
	response = twitter.post(post_url, params=params)
	results = json.loads(response.text)

	return results