import json,pprint
import datetime
import pickle


print datetime.datetime.now()
followers_dump = "../resource/y_followers_dump.txt"
uids = "../resource/uids_dump.txt"

f = open(followers_dump,"r")
fu =open(uids,"w")

line = f.readline()
# f_set = set()
f_set =[]

while line:
	entry = json.loads(line)
	# f_set = f_set|set(entry['followers'])
	f_set = f_set + entry['followers']
	line = f.readline()

f_arr = list(set(f_set))
i=0
while(i <len(f_arr)):
	end = i+100
	if(end>len(f_arr)):
		end =len(f_arr)
	fu.write(json.dumps(f_arr[i:end])+"\n")
	i+=100

# print len(f_set)
print datetime.datetime.now()