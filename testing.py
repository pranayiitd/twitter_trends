import json

d ={1:"a",2:"b"}
f = open("test.txt","w")
f.write(json.dumps(d))
f.write("\n")
f.close()

f = open("test.txt","r")
line = f.readline()
print line
line_json = json.loads(line)
print line_json["1"]

