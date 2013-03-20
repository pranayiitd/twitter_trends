import json,pprint
import twitter
import oauth2 as oauth
import time

def collect_yahoo():
	file1 = "../resource/twitter.30421.log"
	f1 = open(file1,"r")

	line = f1.readline()
	while  line:
		break
		entry = json.loads(line)
		pprint.pprint(entry)
		# print line
		break



def collect_followers( version, app):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']


	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)


	fcount = open("../resource/followers_dump.txt","r")
	start_from = len(fcount.readlines())
	fcount.close()

	fdump = open("../resource/followers_dump.txt","a")

	file2 = "../resource/5feb.sample.txt"
	f2 = open(file2,"r")
	line=""
	
	for i in range(start_from):
		line = f2.readline()
		line = f2.readline()
		
	
	line = f2.readline()
	print "starting from the line number :",start_from
	count =1
	while line:
		print "The request number : ",count
		count+=1 
		tweet = json.loads(line)
		uid = twitter.get_uid(tweet)
		author_details = twitter.get_author_details(tweet)
		
		#Getting followers from twitter
		entry = twitter.get_followers(uid,0,version,client)
		

		
		
		if(version==1):
			limit = int(entry['response']['x-ratelimit-remaining'])
		else:
			limit = int(entry['response']['x-rate-limit-remaining'])

		print "limit x-ratelimit-remaining: ",limit

		if(limit<3):
			print "limit reached\n"
			break

		# Dumping into the file if limit is not reached ,hence response is not empty
		fdump.write(json.dumps(entry)+"\n")	
		#new line for the format
		line = f2.readline()
		line = f2.readline()

	fdump.close()
	f2.close()
	ret = 0
	if(limit >=3):
		ret =1
		print "The Job completed to process file "+file2
	return [ret, limit]


def collect_users_details(version,app):

	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']

	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)


	udump = open("../resource/users_details_dump.txt","w")
	fdump = open("../resource/followers_dump.txt","r")
	line = fdump.readline()
	
	while line:
		entry = json.loads(line)
		# print entry['followers']
		response,data = twitter.get_user_details_batch(entry['followers'],0,version,client)
		pprint.pprint(response)
		pprint.pprint(json.loads(data))

		# pprint.pprint(json.loads(data)[1])
		# print data
		udump.write(json.dumps(response)+"\n")
		udump.write(json.dumps(json.loads(data))+"\n")
		break
		line = fdump.readline()


def testing():
	udump = open("../resource/users_details_dump.txt","r")
	line = udump.readline()
	line = udump.readline()
	while line:
		# line = line[2:(len(line)-3)]
		# print line[0:100]
		resp = json.loads(line)
		pprint.pprint(resp)
		print len(resp)
		break

def start_collection():
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

	
	# print pprint.pprint(set_app[0])
	# print pprint.pprint(set_app[1])
	# print pprint.pprint(set_app[2])
	# print pprint.pprint(set_app[3])
	# collect_users_details(1,app[0])
	i =0
	v =1

	# collect_users_details(v,set_app[i])
	# return
	time_elapsed =0
	while(True):
		print "trying version,app number \n",v,i
		ret, limit = collect_followers(v,set_app[i])
		# ret, limit = collect_users_details(v,set_app[i])
		# The job is completed
		if ret==1:
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
					print "going to sleep now for 15 mins"
					time.sleep(15*60)
					time_elapsed +=15
					i=0
					if(time_elapsed>=60):
						v=1
						time_elapsed=0
					
					# break

testing()
# collect_users_details()
# collect_followers(1.1)
# time.sleep(15*60)
# start_collepythoction()