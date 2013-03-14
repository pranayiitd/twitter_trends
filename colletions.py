import json,pprint
import twitter

file1 = "../resource/twitter.30421.log"


# f1 = open(file1,"w")
# entry = twitter.get_followers("swamy39",1)
# f1.write(json.dumps(entry))
# f1.close()



f1 = open(file1,"r")

#print "yahoo tweets\n\n"
line = f1.readline()
while  line:
	break
	entry = json.loads(line)
	pprint.pprint(entry)
	# print line
	break


#print "Raw tweets\n\n"
fdump = open("../resource/followers_dump.txt","w")
file2 = "../resource/5feb.sample.txt"
f2 = open(file2,"r")
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
	limit = entry['response']['x-ratelimit-remaining']
	
	# print uid
	# print author_details
	# print entry['followers']
	# print entry['response']
	# print line
	if(limit<3):
		break
	line = f2.readline()
	line = f2.readline()

fdump.close()
f2.close()

# print "number of followers",len(entry['followers'])
# print "response",entry['response']['date']
