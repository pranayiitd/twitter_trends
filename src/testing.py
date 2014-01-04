import pprint,json
import oauth2 as oauth

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

app = set_app[0]

CONSUMER_KEY = app['c_key']
CONSUMER_SECRET = app['c_sec']
ACCESS_KEY = app['a_key']
ACCESS_SECRET = app['a_sec']
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

version =1.1
uids =[180891072]		
cursor= '-1'
for uid in uids:
	api_call = "https://api.twitter.com/"+str(version)+"/followers/ids.json?cursor="+cursor+"&user_id="+str(uid)
	print api_call,"\n\n"
	response, data = client.request(api_call)
	data_json = json.loads(data)
	pprint.pprint(data_json)
	pprint.pprint(response)