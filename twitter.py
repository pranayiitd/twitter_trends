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

def get_followers(uid,type):
	CONSUMER_KEY = "YSXXstxTV3rJFRAmX9HyQ"
	CONSUMER_SECRET = "96ZZ8qoULMeptOiumnYYPcl2WmzVgPQdNlLeSkGG4yU"
	ACCESS_KEY = "121059967-SVLSt2qIwLQXPYAKVzZIHquQFHR2g3kkWFrGZeee"
	ACCESS_SECRET = "zUXxk8EI7tf4nJLtWqxrYbCQ83z0yTm83AYaXrLTyU"

	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)

	cursor = '-1'
	limit_remaining = 4
	followers =[]
	count = 0
	while(limit_remaining > 3 and cursor!='0'):
#		count +=1	
#		if (count==3):
#			break
		api_call = "https://api.twitter.com/1/followers/ids.json?cursor="+cursor+"&used_id="+str(uid)
		if(type==1):
			api_call = "https://api.twitter.com/1/followers/ids.json?cursor="+cursor+"&screen_name="+str(uid)
		response, data = client.request(api_call)
		data_json = json.loads(data)
		
#		print response
#		print data
		if(response['status']=='200'):
			followers = followers + data_json['ids']
			cursor = data_json['next_cursor_str']
		else:
			break
		limit_remaining = int(response['x-ratelimit-remaining'])

#		print limit_remaining
		
		#print followers

	entry = {
			 "author" : uid,
			 "followers" : followers,
			 "response"	 : response
			 }	

	
	return entry

def get_user_details(uid,type):
	CONSUMER_KEY = "YSXXstxTV3rJFRAmX9HyQ"
	CONSUMER_SECRET = "96ZZ8qoULMeptOiumnYYPcl2WmzVgPQdNlLeSkGG4yU"
	ACCESS_KEY = "121059967-SVLSt2qIwLQXPYAKVzZIHquQFHR2g3kkWFrGZeee"
	ACCESS_SECRET = "zUXxk8EI7tf4nJLtWqxrYbCQ83z0yTm83AYaXrLTyU"

	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)
	
	api_call = "https://api.twitter.com/1/users/show.json?user_id="+str(uid)
	if(type==1):
		api_call = "https://api.twitter.com/1/users/show.json?screen_name="+str(uid)
	
	response, data = client.request(api_call)
	data_json = json.loads(data)
	#print response
	#print data
	return [response,data]



