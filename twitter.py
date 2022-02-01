from requests_oauthlib import OAuth1Session
import json

def post(content):
	params = {"status": content}
	post_url = "https://api.twitter.com/1.1/statuses/update.json"
	twitter = OAuth1Session(
		"OgpyWtcR0RFjDYvC5ZHpetqCh",
		"Ar97tCJaxkLoFUud8NHJzFMjgaHAxjIkJPCLXHJKQFcXMpujYF",
		"1117095329847844865-hC3KcIinUWRl2R9l3oXUp6RYL9p86F",
		"UoUF4L7RbyEJox9t2JhS8jkmLhRNid08j39t6I1Y4Rxhc",
	)
	response = twitter.post(post_url, params=params)
	results = json.loads(response.text)

	return results