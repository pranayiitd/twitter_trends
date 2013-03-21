import json

def count_followers():
	f = open("../resource/y_followers_dump.txt","r")
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

print "The number of followers ids :",count_followers()	
