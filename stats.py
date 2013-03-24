import json
import sys
import os

def count_followers():
	f = open("../resource/y_users_details_dump.txt","r")
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

# print "The number of followers ids :",count_followers()	

def count_users():
	f = open("../resource/y_users_details_dump.txt","r")
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
	print count_users()
elif (cmd=="f"):
	print count_followers()
elif (cmd=="ua"):
	print count_uids()
elif (cmd=="tt"):	
	print count_trending_tweets()
