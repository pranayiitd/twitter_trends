import json
# import urllib3
import oauth2 as oauth
import pprint

def get_tweets():
	f= open('../resource/tweet.txt','r')
	tweet = json.loads(f.readline())
	return tweet

def get_uid(tweet):
	return tweet['user']['id']

def get_tweetid(tweet):
	return tweet['id']
	
def get_author_details(tweet):
	uid = tweet['user']['id']
	verified = tweet['user']['verified']
	followers_count = tweet['user']['followers_count']
	description = tweet['user']['description']
	name = tweet['user']['name']
	screen_name = tweet['user']['screen_name']
	created_at = tweet['user']['created_at']
	time_zone  = tweet['user']['time_zone']
	text = tweet['text']
	
	return tweet['user']

def get_followers(uid):
	CONSUMER_KEY = "YSXXstxTV3rJFRAmX9HyQ"
	CONSUMER_SECRET = "96ZZ8qoULMeptOiumnYYPcl2WmzVgPQdNlLeSkGG4yU"
	ACCESS_KEY = "121059967-SVLSt2qIwLQXPYAKVzZIHquQFHR2g3kkWFrGZeee"
	ACCESS_SECRET = "zUXxk8EI7tf4nJLtWqxrYbCQ83z0yTm83AYaXrLTyU"

	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)

	api_call = "https://api.twitter.com/1/followers/ids.json?cursor=-1&used_id="+str(uid)
	response, data = client.request(api_call)


	print 'response',response
	return [response,data]
	#pprint.pprint (data)	
	# return followers


#uid = getUserDetails(getTweets())	
#getFollowers(uid)