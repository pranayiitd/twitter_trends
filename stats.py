import json

def count_followers():
	f = open("../resource/followers_dump.txt","r")
	line = f.readline()
	followers_count =0
	while line:
		entry = json.loads(line)
		count = len(entry['followers'])
		followers_count+=count
		line =f.readline()
	return followers_count

print count_followers()	