import json
from pprint import pprint
import twitter
import oauth2 as oauth
import time
from datetime import datetime
import sys


def make_query(trending_objects=None):
	# f = open("/Users/pranayag/mtp/india/topics/14,55,14,625021","r")
	# line = f.readline()
	# obj = json.loads(line)

	obj = json.loads(trending_objects)
	# pprint(obj)
	# pprint(obj[0]['trends'][0])
	
	qr = ""
	

	for i in range(len(obj[0]['trends'])):
		if(qr==""):
			qr = obj[0]['trends'][i]['query']
		else:
			qr = qr+" OR "+ obj[0]['trends'][i]['query']
	# print qr
	return qr
	

# GET THE CURRENT TRENDING TOPICS FROM TWITTER API
def get_trending_topics(version, app, dump_path):
	CONSUMER_KEY = app['c_key']
	CONSUMER_SECRET = app['c_sec']
	ACCESS_KEY = app['a_key']
	ACCESS_SECRET = app['a_sec']
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
	client = oauth.Client(consumer, access_token)
	
	flog= open(dump_path['trending_log'],"a")

	version =1.1
	india = 23424848
	entry_trends = twitter.get_trending_topics(india, version, client)	

	ret =0
	response = entry_trends['response']['status']
	
	time_stamp =""

	if(response!="200"):
		ret = -1
	else :
		time_stamp = str(datetime.now()).split(" ")[1]
		time_stamp = time_stamp.replace(":",",")
		time_stamp = time_stamp.replace(".",",")
		topics_dump = dump_path['trending_topics_loc']+"/"+time_stamp
		f= open(topics_dump,"w")
		f.write(json.dumps(entry_trends)+"\n")
		f.close()
		ret =1
	
	flog.write(topics_dump+"\t"+str(time_stamp)+"\t"+str(datetime.now())+"\t"+str(ret)+"\t"+str(india)+"\n")
	
	return [ret,entry_trends['trends'],time_stamp]
	

def get_trending_tweets(set_app, dump_path, query, time_stamp):

	result_type ="mixed"
	query = query+"&result_type="+result_type+"&count=100"
	version =1.1
	tweets_dump = dump_path['trending_tweets_loc']+"/"+time_stamp
	f = open(tweets_dump,"a")
	flog= open(dump_path['trending_log'],"a")


	start_time = datetime.now()	
	delta = (datetime.now()-start_time).total_seconds()
	i=0;ret =0;success_count=0
	
	print "Starting to collct tweets at time ", start_time
	
	while(delta <(5*60)):
		app = set_app[i]
		
		CONSUMER_KEY = app['c_key']
		CONSUMER_SECRET = app['c_sec']
		ACCESS_KEY = app['a_key']
		ACCESS_SECRET = app['a_sec']
		consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
		access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
		client = oauth.Client(consumer, access_token)
		
		entry_tweets = twitter.get_trending_tweets(query, version, client)	
		
		response = entry_tweets['response']['status']

		if(response!="200"):
			i=(i+1)%4
			print "Didn't get the tweets"
			ret = -1
			time.sleep(1)
			if(response=="420"):
				print "Too fast! Have calm!!"
				ret = -2
				time.sleep(5)
		else:
			success_count+=1
			print "Getting tweets!! :) success_count",success_count
			ret =1
			# print "Writing the tweets at ", dump_path['trending_tweets_loc']+"/"+time_stamp
			f.write(json.dumps(entry_tweets)+"\n")
		
		delta = (datetime.now()-start_time).total_seconds()
	
	flog.write(tweets_dump+"\t"+str(start_time)+"\t"+str(datetime.now())+"\t"+str(ret)+"\t"+str(success_count)+"\n")
	f.close()
	flog.close()

	return [ret, time_stamp]


# START SCHEDULING THE COLLECTION 
def start_scheduling(dump_path):

	fapp = open('twitter_app.txt',"r")
	lines = fapp.readlines()
	set_app =[]; i=0
	
	while (i+3)<(len(lines)):
		app = {}
		app['c_key'] = lines[i].replace("\n","")
		app['c_sec'] = lines[i+1].replace("\n","")
		app['a_key'] = lines[i+2].replace("\n","")
		app['a_sec'] = lines[i+3].replace("\n","")
		set_app.append(app)
		i+=5

	x =1;y=0
	
	fout = open("../india/out.txt","w")
	
	while(True):
		print "Trying to get topics using app num. %d \n" %x
		fout.write("Trying to get topics using app num. %d \n" %x)
		ret,topics,time_stamp = get_trending_topics(1.1, set_app[x], dump_path)
		# Didn't get the topics
		if(ret=="-1"):
			print "Didn't get the topics, Trying another app no. %d \n"%x+1
			fout.write("Didn't get the topics, Trying another app no. %d \n"%x+1)
			time.sleep(1)
			x+=1
			continue
		else:
			print "Getting tweets for topics\n"
			fout.write("Getting tweets for topics\n")
			query = make_query(topics)
			# Collect tweets for this query for 5 mins
			get_trending_tweets(set_app, dump_path, query, time_stamp)		

		break

	fout.close()


# GLOBAL VARIABLES

dump_path = {
			"trending_topics_loc" : "../india/topics",
			"trending_tweets_loc" : "../india/tweets",
			"trending_log" : "../india/trending.log"
			}

start_scheduling(dump_path)
# print make_query()	