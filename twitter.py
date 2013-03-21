import json
import oauth2 as oauth
import pprint


def get_uid(tweet, format):
	if(format=="yahoo"):
		return tweet['rtds_tweet']['user_id']
	else:
		return tweet['user']['id']

def get_tweetid(tweet, format):
	if(format=="yahoo"):
		return tweet['rtds_tweet']['id']
	else:
		return tweet['id']

# Make call to twitter API version to get all followers of user with uid
def get_followers(uid,type,version,client):

	cursor = '-1'
	limit_remaining = 4
	followers =[]
	count = 0

	# Loop to get all the pages of response
	while(limit_remaining > 3 and cursor!='0'):
		count +=1	
		if (count==3):
			break
		api_call = "https://api.twitter.com/"+str(version)+"/followers/ids.json?cursor="+cursor+"&user_id="+str(uid)
		if(type==1):
			api_call = "https://api.twitter.com/"+str(version)+"/followers/ids.json?cursor="+cursor+"&screen_name="+str(uid)
		
		
		response, data = client.request(api_call)
		data_json = json.loads(data)
	
		if(response['status']=='200'):
			followers = followers + data_json['ids']
			cursor = data_json['next_cursor_str']
		else:
			break
		
		if(version==1):
			limit_remaining = int(response['x-ratelimit-remaining'])
		else:
			limit_remaining = int(response['x-rate-limit-remaining'])

	entry = {
			 "author" : uid,
			 "followers" : followers,
			 "response"	 : response
			 }	
	return entry


# Batch request to Twitter API version to get details of all users in uids
def get_user_details_batch(uids,type,version,client):

	api_call = "https://api.twitter.com/"+str(version)+"/users/lookup.json?user_id="+str(uids)
	if(type==1):
		api_call = "https://api.twitter.com/"+str(version)+"/users/lookup.json?screen_name="+str(uids)

	response, data = client.request(api_call)
	return [response,data]



# Request to Twitter API get details of one user

def get_user_details(uids,type,version,client):
	
	api_call = "https://api.twitter.com/"+str(version)+"/users/show.json?user_id="+str(uid)
	if(type==1):
		api_call = "https://api.twitter.com/"+str(version)+"/users/show.json?screen_name="+str(uid)
	
	response, data = client.request(api_call)
	return [response,data]