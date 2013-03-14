#!/usr/bin/python3.2
import glob
import os
import optparse
import urllib3
import socks 
import socket
#from bs4 import BeautifulSoup
#from BSXPath import BSXPathEvaluator,XPathResult
from lxml import etree
import json
import urllib
import re
from collections import OrderedDict
import http.client
from urllib.parse import urlparse
import httplib2
from time import sleep

parser = optparse.OptionParser()
fdomains100 = open('domains100.txt', 'r')

#DICTIONARY OR MAPPING OF ALL THE TOP 100 URLS
domains100=OrderedDict()


for domain in fdomains100.readlines():
    match = re.search('http\:\\/\/(?:www\.)?(.+)\/?', domain)
    domains100[match.group(1)]=1

def func_avg_length(text):
    return len(text)


def func_frowning(text):
    if len(re.findall('\:\( | \:-\(', text)) > 0:
        return 1
    else:
        return 0

def func_hashtags(text):
    if len(re.findall('\#', text)) > 0:
        return 1
    else:
        return 0

# RETURNS (1,URL) IF THE url IS IN TOP100 DOMAINS
def func_top100(url):
    t = urlparse(url)
    try:
        conn = http.client.HTTPConnection(t.netloc)
        conn.request("GET", t.path)
        fullurl=conn.getresponse().getheader("Location")
        match = re.search('https?\:\\/\/(?:www\.)?(.+)\/?', fullurl)
        if match and match.group(1) in domains100:
            return [1, match.group(1)]
        else:
            return [0, match.group(1)]
    except:
        return [0,1]

# RETURNS MENTION OF USER TWEET HAS 
def func_users(tweet):
    # regex : space or start of string then @ then alphanumeric
    mentions = re.findall('(\A | \s)@(\w+)',tweet)
    return mentions
    # if(len(mentions)>0):
    #     return 1
    # else:
    #     return 0

#RETURN 1 IF AUTH_DESC IS THERE **not clean right now
def func_has_author_desc(text):
    if len(text) > 1:
        # print ("has_author_desc:", text)
        return 1
    else:
        return 0

# RETURNS 1 IF THE TWEET HAS BEEN RETWEETED ATLEAST ONCE
def func_retweet(rc):
    retweet_count=int(rc)   
    if(retweet_count >0):
        return 1
    else :
        return 0



# SETTING PROXY TO CONNECT VIA YAHOO SOCKS PROXY
# curl -v  --socks socks.yahoo.com:1080 "http://generic19.timesense.ac4.yahoo.com:5810/?query=news&count=1"
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "socks.yahoo.com", 1080) 
socket.socket = socks.socksocket
socks.wrapmodule(httplib2)

h = httplib2.Http()
r,json_string = h.request("http://generic17.timesense.ac4.yahoo.com:4080/timesense/v3/en-us/topbuzzing")
json_data = json.loads(json_string.decode("utf-8"))


topic_list=[]
# GLOBAL MAPPING TWEET_ID TO CORRESPONDING BUZZING TOPIC
tweet_topic={}
topic_stats={}

for topic in json_data["topics"]:
    topic_list.append(topic["title"])
    print (topic["title"])
g = httplib2.Http()

# ALL THE BUZZING TOPICS IN THIS LIST
for topic_title in topic_list:
# FETCHING ALL THE TWEETS RELATED TO THE 'TOPIC_TITLE'
    query_url="http://generic19.timesense.ac4.yahoo.com:5810/?query="+urllib.parse.quote_plus(topic_title)
    # query_url="http://generic19.timesense.ac4.yahoo.com:5810/?query=news"
    print (query_url)
    xml=""
    try:
        r,xml1=g.request(query_url)
        xml = bytes.decode(xml1)
    except:
        print("Skipping the topic --skip->",topic_title)
        continue
    f = open("generic19.xml", 'w+')
    f.write(xml)
    f.close()

# THIS DOCUMENTS HAS ALL TWEETS RELATED TO BUZZ 'TOPIC_TITLE'
    document=etree.parse("generic19.xml")


	# Parsing the xml to get the tweet objects in 'nodes'
    nodes = document.xpath("//result/group/child::node()")
# Mapping from tweet_id to tweet attributes 'topic_title'
    tweet_attribs = {}
    tweet_count=0

# Traversing all the tweets related to the buzzing topic from timesense
    print("-----------------------------------------------------")
    print("=======",topic_title,"=======")
    print("-----------------------------------------------------")
    for n in nodes:
        if len(n) > 10:
            d = etree.XPathEvaluator(n)
			# Getting all the fields of the tweet 'n'
            tweet_id = d("field[@name='tweet_id']/text()")[0]
            tweet_text = d("field[@name='tweet']/text()")[0]
            tweet_url = d("field[@name='url']/text()")[0]
            retweet_count = d("field[@name='retweet_count']/text()")[0]
            print (tweet_text)
#             Map the tweet_id to buzzing topic
            # print('------',topic_title,tweet_text,retweet_count,'------')
            tweet_topic[tweet_id]=[topic_title,func_retweet(retweet_count),tweet_text]

            tweet_attribs[tweet_id] = []
            tweet_attribs[tweet_id].append(func_avg_length(tweet_text))
            tweet_attribs[tweet_id].append(func_frowning(tweet_text))
            tweet_attribs[tweet_id].append(func_hashtags(tweet_text))
            tweet_attribs[tweet_id].append(func_top100(tweet_url))
            # tweet_attribs[tweet_id].append((1,1))
#            tweet_attribs[tweet_id].append(urls(tweet_url))
            tweet_attribs[tweet_id].append(func_users(tweet_text))
            tweet_attribs[tweet_id].append(func_has_author_desc(tweet_text))
            tweet_attribs[tweet_id].append(func_retweet(retweet_count))

            tweet_count+=1

    topic_stats[topic_title]=[]

    length_of_tweet=0
    frowns=0
    hashtags=0
    top100=0
    retweet=0
    # THE DISTINCT USERS MENTIONS IN URLS IN ALL TWEETS IN TOPIC CLUSTER
    distinct_users={}
    authors_desc=0
    distinct_urls={}

    if (tweet_count==0):
        tweet_count=1

    for tweetid in tweet_attribs.keys():
        length_of_tweet+= tweet_attribs[tweetid][0]
        frowns+= tweet_attribs[tweetid][1]
        hashtags+= tweet_attribs[tweetid][2]
        top100+= tweet_attribs[tweetid][3][0]
        for user in tweet_attribs[tweetid][4]:
            distinct_users[user[1]]=1
        authors_desc+=tweet_attribs[tweetid][5]
        retweet+=tweet_attribs[tweetid][6]
        distinct_urls[tweet_attribs[tweetid][3][1]]=1

#   MAPPING BUZZING TOPIC 'TOPIC_TITLE' TO STATS OF ALL RELATED TWEETS.
    topic_stats[topic_title].append(authors_desc*1.0/tweet_count)
    topic_stats[topic_title].append(len(distinct_urls.keys())*1.0/tweet_count)
    topic_stats[topic_title].append(len(distinct_users.keys())*1.0/tweet_count)
    topic_stats[topic_title].append(top100*1.0/tweet_count)
    topic_stats[topic_title].append(hashtags*1.0/tweet_count)
    topic_stats[topic_title].append(length_of_tweet*1.0/tweet_count)
    topic_stats[topic_title].append(frowns*1.0/tweet_count)
    topic_stats[topic_title].append(retweet*1.0/tweet_count)
    # break

#ALL TWEETS FOR SAME TOPIC WILL HAVE SAME STATS HENCE COMMENTING BELOW
#INSTEAD USING TOPIC_STATS TO TRAVERSE
fw = open('model_1_test.arff','w')
f_tweet = open('tweets.txt','w')

for tweet in tweet_topic:
    topic = tweet_topic[tweet][0]
    rc    = tweet_topic[tweet][1]
    tweet = tweet_topic[tweet][2]
    row = "?,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f \n"%(topic_stats[topic][0],topic_stats[topic][1],topic_stats[topic][2],topic_stats[topic][3],topic_stats[topic][4],topic_stats[topic][5],topic_stats[topic][6],rc)
    fw.write(row)
    f_tweet.write(tweet+topic+tweet+"\n")
    print(row)
    # print (topic_stats[tweet_topic[tweet]][0], topic_stats[tweet_topic[tweet]][1], topic_stats[tweet_topic[tweet]][2], topic_stats[tweet_topic[tweet]][3], topic_stats[tweet_topic[tweet]][4], topic_stats[tweet_topic[tweet]][5], topic_stats[tweet_topic[tweet]][6],tweet)

# print("<length>","<frowns>","<hashtags>","<top100>","<retweetCount>")

# for tweet in topic_stats.keys():
#     print (tweet)
#     print("%.2f \t %.2f \t %.2f \t %.2f \t %.2f" %(topic_stats[tweet][0],topic_stats[tweet][1],topic_stats[tweet][2],topic_stats[tweet][3],topic_stats[tweet][6]))
