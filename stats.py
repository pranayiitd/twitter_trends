import json
import sys
import os

paths = {	"filtered_tweets" :"../tweets_dump",
			"sampled_tweets" :"../sample_dump/2013-03-29",
			"graph" : "../graph/2013-03-29",
			"users_db"   : "../graph/users_db.txt",

			"sampling_log" : "../graph/sampling_log.txt",
			"authors_log" :"../graph/authors_log.txt",
			"followers_log" : "../graph/followers_log.txt",
			"profiles_log" : "../graph/profiles_log.txt",
			
			}


def count_followers():
	f = open(paths["graph"]+"/followers.txt","r")
	line = f.readline()
	followers_count =0
	followers =[]
	while line:
		entry = json.loads(line)
		followers = followers+entry['followers']
		# count = len(set(entry['followers']))
		# followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
	return len(set(followers))


def count_users():
	f = open(paths["paths"]+"/profiles.txt","r")
	line = f.readline()
	users_count =0
	users =[]
	while line:
		entry = json.loads(line)
		users = users+json.loads(entry['users'])
		# count = len(set(entry['followers']))
		# followers_count+=count
		# print len(entry['followers'])
		line =f.readline()
	return ((users[0]))

def count_uids():
	f = open("../resource/uids_dump.txt","r")
	line = f.readline()
	count =0
	users=[]
	while line:
		entry = json.loads(line)
		print len(entry)
		break

def count_trending_tweets():
	files = os.listdir("../india/tweets")
	count =0
	for i in range(len(files)):
		f = open("../india/tweets/"+files[i],"r")
		line = f.readline()
		while line:
			entry = json.loads(line)
			tweets = json.loads(entry['tweets'])
			count = count+len(tweets['statuses'])
			# break
			line = f.readline()
		# break
	return count

cmd = sys.argv[1]

if(cmd=="u"):
	print "Number of profiles collected ",count_users()
elif (cmd=="f"):
	print "Number of followers ids ",count_followers()
elif (cmd=="ua"):
	print count_uids()
elif (cmd=="tt"):	
	print count_trending_tweets()
