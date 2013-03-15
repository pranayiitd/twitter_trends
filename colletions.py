import json,pprint
import twitter

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



def collect_followers():
	file2 = "../resource/5feb.sample.txt"
	f2 = open(file2,"r")

	fdump = open("../resource/followers_dump.txt","a")
	
	line = f2.readline()
	count =1
	while line:
		print "The request number : ",count
		count+=1 
		tweet = json.loads(line)
		uid = twitter.get_uid(tweet)
		author_details = twitter.get_author_details(tweet)
		entry = twitter.get_followers(uid,0)
		fdump.write(json.dumps(entry)+"\n")
		limit = int(entry['response']['x-ratelimit-remaining'])
		if(limit<3):
			print "limit reached\n"
			break
		#new line for the format
		line = f2.readline()
		line = f2.readline()

	fdump.close()
	f2.close()

def collect_users_details():
	udump = open("../resource/users_details_dump.txt","w")
	fdump = open("../resource/followers_dump.txt","r")
	line = fdump.readline()
	while line:
		entry = json.loads(line)
		# print entry['followers']
		response,data = twitter.get_user_details_batch(entry['followers'],0)
		pprint.pprint(response)
		pprint.pprint(json.loads(data)[1])
		# print data
		udump.write(json.dumps(response)+"\n")
		udump.write(json.dumps(data)+"\n")
		break


def testing():
	udump = open("../resource/users_details_dump.txt","r")
	line = udump.readline()
	line = udump.readline()
	while line:
		# print line
		# print line['content-length']
		# line = line.replace("\n","")
		resp = json.loads(line)
		
		pprint.pprint(resp)
		print len(resp)
		break

# testing()
# collect_users_details()
collect_followers()