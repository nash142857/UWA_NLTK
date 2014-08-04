import json
import os
data = json.loads(open("d3_final.json","r").read())
dir = "./friend"
node_st = {}
for file in os.listdir(dir):
	if os.path.isdir(file):
		pass
	else:
		f = open(os.path.join(dir, file), "r")
		tdata = json.loads(f.read())
		for key in tdata:
			for to in tdata[key]:
				node_st[to[0]] = to[1] + " " + to[2]
		f.close()

l = len(data["node"])
for i in range(l):
	data["node"][i].append(node_st[data["node"][i][0]])

f = open("d3_final2.json","w")
f.write(json.dumps(data))
f.close()