import json,pprint
import twitter
import oauth2 as oauth
import time
from datetime import datetime
import sys

def find_start(dest, source, typ):
	followers_dump = dest
	raw_tweet = source

	ff = open(dest,"r")
	flines = ff.readlines()
	last_id=""
	
	n =len(flines)
	for i in range(n):
		entry = json.loads(flines[n-i-1])
		# Last non-empty response in the destination dumping file
		if(len(entry[typ])!=0):
			if(typ=="users"):
				last_id = entry['user_id']
			elif(typ=="followers"):
				last_id = entry['tweet_id']
			break
	ff.close()

	# Fiding line number in the source file containing the last_tid
	fr = open(source,"r")
	line = fr.readline()
	count =0;start_line=0
	while line:
		count+=1
		entry = json.loads(line)
		_id =0
		if(typ=="followers"):
			_id = entry['rtds_tweet']['id']
		elif(typ=="users"):
			_id = entry[0]
		
		if(_id==last_id):
			start_line = count
			break
		line = fr.readline()
	
	fr.close()
	return start_line

# COLLECTS AUTHOR DETAILS FROM THE TWEET
def get_author_details(tweet, format, author_dump):
	# Will have to change as per yahoo format

	if(format=="yahoo"):
		time_zone =""
		
		if(tweet['rtds_tweet'].has_key('user_time_zone')):
			time_zone = tweet['rtds_tweet']['user_time_zone']
		
		author_details ={
				"user_id" : tweet['rtds_tweet']['user_id'],
				"user_created_at" : tweet['rtds_tweet']['user_created_at'],
				"user_followers_count" :tweet['rtds_tweet']['user_followers_count'],
				"user_friends_count"  :tweet['rtds_tweet']['user_friends_count'],
				"user_lang" : tweet['rtds_tweet']['user_lang'],
				"user_location" : tweet['rtds_tweet']	['user_location'], 
				"user_name" : tweet['rtds_tweet']['user_name'],
				"user_profile_image_url" :tweet['rtds_tweet']['user_profile_image_url'],
				"user_protected"  : tweet['rtds_tweet']['user_protected'] ,
				"user_screen_name" :tweet['rtds_tweet']['user_screen_name'],
				"user_statuses_count" :tweet['rtds_tweet']['user_statuses_count'],
				"user_time_zone" :time_zone,
				"user_utc_offset" :tweet['rtds_tweet']['user_utc_offset'],
				"user_verified"  :tweet['rtds_tweet']['user_verified'],
			}
		return author_details
		
	else:
		return tweet['user']

# COLLECTS THE FOLLOWERS OF THE AUTHOR 
def collect_followers(version, app, dump_path):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)

	raw_tweet = dump_path[0]
	followers_dump = dump_path[1]
	author_dump = dump_path[2]
	log_details = dump_path[4]
	
	fraw = open(raw_tweet,"r")
	flog = open(log_details,"a")
	fdump = open(followers_dump,"a")
	fauth = open(author_dump,"a")
	# ----------------------------------
	# Skipping the lines to start from right place.
	start_from = find_start(followers_dump, raw_tweet)
	line=""
	for i in range(start_from):
		line = fraw.readline()
	# ----------------------------------
	
	starttime = datetime.now() 
	endtime =""
	endtweet=""

	print "starting from the line number :",start_from
	count =1;limit =0;ret =0
	
	line = fraw.readline()
	while line:
		count+=1 
		tweet = json.loads(line)
		uid = twitter.get_uid(tweet,"yahoo")
		tid = twitter.get_tweetid(tweet,"yahoo")
		endtweet = tid
		author_details = get_author_details(tweet,"yahoo", author_dump)
		
		
		#GETTING FOLLOWERS FROM TWITTER by user_id
		entry = twitter.get_followers(uid,0,version,client)
		
		
		
		if(version==1):
			limit = int(entry['response']['x-ratelimit-remaining'])
		else:
			limit = int(entry['response']['x-rate-limit-remaining'])

		sys.stdout.write("\rlimit x-ratelimit-remaining: %d The request number : %d" %(limit,count))
		sys.stdout.flush()

		if(limit<3):
			endtime = datetime.now()
			ret =1
			print "limit reached\n"
			break

		# Dumping followers ids and author_details
		entry["tweet_id"] = tid
		fdump.write(json.dumps(entry)+"\n")	
		fauth.write(json.dumps(author_details)+"\n")
		
		#new line 
		line = fraw.readline()

	
	fraw.close()
	fdump.close()
	fauth.close()

	if(limit >=3):
		ret =2
		endtime = datetime.now()
	flog.write(raw_tweet+"\t"+str(starttime)+"\t"+str(endtime)+"\t"+str(endtweet)+"\t"+str(ret)+"\t"+str(count)+"\n")
	flog.close()
	return [ret, limit]

# COLLECTS THE USERS DETAILS FROM TWITER API AND DUMPS IN A FILE
def collect_users_details(version, app, dump_path):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)

	followers_dump = dump_path["followers_dump"]

	uids_dump = dump_path["uids_dump"]
	users_dump = dump_path["users_dump"]
	log_details = dump_path["log_dump"]
	
	
	fdump = open(uids_dump,"r")
	udump = open(users_dump,"a")
	flog  = open(log_details,"a")
	# ----------------------------------
	# Skipping the lines to start from right place.
	start_from = find_start(users_dump, uids_dump, "users")
	line=""
	for i in range(start_from):
		line = fdump.readline()
	# ----------------------------------
	
	starttime = datetime.now() 
	endtime =""
	
	enduid=""

	print "starting from the line number :",start_from
	count =1;limit =0;ret =0
	line = fdump.readline()
	
	while line:
		count+=1
		entry_followers = json.loads(line)
	
		uid = entry_followers[0]
		enduid = uid


		# GETTING USERS DETAILS FORM TWITTER API
		entry_users = twitter.get_user_details_batch(entry_followers, 0, version, client)
		# print len(entry_followers['followers'])
		#pprint.pprint(entry_users)
		if(entry_users['response']['status']!="200"):
			print "response is ",entry_users['response']['status']
			continue
		###############
		if(version==1):
			# pprint.pprint(entry_users['response'])
			limit = int(entry_users['response']['x-ratelimit-remaining'])
		else:
			limit = int(entry_users['response']['x-rate-limit-remaining'])

		sys.stdout.write("limit x-ratelimit-remaining: %d The request number : %d \n " %(limit,count))
		sys.stdout.flush()

		if(limit<3):
			endtime = datetime.now()
			ret =1
			print "limit reached\n"
			break

		# Dumping user_details
		entry_users["user_id"] = uid
		udump.write(json.dumps(entry_users)+"\n")	
		#new line 
		line = fdump.readline()
		
	
	fdump.close()
	udump.close()

	if(limit >=3):
		ret =2
		endtime = datetime.now()
	flog.write(uids_dump+"\t"+str(starttime)+"\t"+str(endtime)+"\t"+str(enduid)+"\t"+str(ret)+"\t"+str(count)+"\n")
	flog.close()
	return [ret, limit]


# START SCHEDULING THE COLLECTION 
def start_scheduling(dump_path):
	fapp = open('twitter_app.txt',"r")
	lines = fapp.readlines()
	set_app =[]
	
	i=0
	
	while (i+3)<(len(lines)):
		app = {}
		app['c_key'] = lines[i].replace("\n","")
		app['c_sec'] = lines[i+1].replace("\n","")
		app['a_key'] = lines[i+2].replace("\n","")
		app['a_sec'] = lines[i+3].replace("\n","")
		set_app.append(app)
		i+=5

	i =0;v =1;time_elapsed =0
	
	while(True):
		print "trying version ,app number \n",v,i
		# ret, limit = collect_followers(v,set_app[i],dump_path)
		ret, limit = collect_users_details(v,set_app[i],dump_path)
	#	break
		# ret, limit = collect_users_details(v,set_app[i])
		# The job is completed
		if ret==2:
			print "ret2\n"
			break
		# Try different app combination
		if(limit<3):
			if(i<3):
				i+=1
			else:
				if(v==1):
					v=1.1
					i=0
				else:
					print "going to sleep now for 15 mins from ",datetime.now()
					time.sleep(15*60)
					time_elapsed +=15
					i=0
					if(time_elapsed>=60):
						v=1
						time_elapsed=0
					
					# break

def testing():
	users_dump = "../resource/y_users_details_dump.txt"
	f = open(users_dump,"r")
	line = f.readline()
	entry = json.loads(line)
	print int(entry['response']['x-ratelimit-remaining'])
	pprint.pprint(entry['response']['x-ratelimit-remaining'])
	print len(json.loads(entry['users']))

	
	return

	rtds = open("../tweets_dump/sf03_twitter.8432.log_1363570500","r")
	line = rtds.readline()
	tweet = json.loads(line)
	tweet['rtds_tweet']["pranay"] ="is the boss"
	pprint.pprint(tweet['rtds_tweet'])
	line = rtds.readline()
	tweet = json.loads(line)
	tweet['rtds_tweet']["pranay"] ="is the boss"
	pprint.pprint(tweet['rtds_tweet'])


	return

	limit =1
	count =1
	
	while line :
		resp = json.loads(line)
		break
		pprint.pprint(resp)
		pprint.pprint(resp['rtds_tweet']['user_id'])
		# print len(resp)
		break

# raw_tweet  ="../resource/5feb.sample.txt"
raw_tweet  = "../tweets_dump/sf03_twitter.8432.log_1363570500"
followers_dump = "../resource/y_followers_dump.txt"
users_dump = "../resource/y_users_details_dump.txt"
authors_dump = "../resource/y_authors_details_dump.txt"
# log_dump = "../resource/y_log.txt"
log_dump = "../resource/y_log_users.txt"
uids_dump ="../resource/uids_dump.txt"

dump_path =[raw_tweet, followers_dump, authors_dump, users_dump, log_dump ] 

dump_path ={
			"raw_tweet" : raw_tweet,
			"followers_dump":followers_dump,
			"authors_dump" : authors_dump,
			"users_dump" : users_dump,
			"log_dump" : log_dump,
			"uids_dump": uids_dump	
}

# print find_start(followers_dump, raw_tweet,"followers")
# print find_start(users_dump, uids_dump, "users")
# testing()
start_scheduling(dump_path)
# collect_users_details(dump_path)
# collect_followers(v,)
# time.sleep(15*60)
# start_collepythoction()
