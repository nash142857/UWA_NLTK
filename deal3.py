import json
import os
data = json.loads(open("d3_final2.json","r").read())
id = [arr[0] for arr in data["node"]]
node_st = {}
dir = "./friend"
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

for key in node_st:
	if key not in id:
		data["node"].append((key, "unable", node_st[key]))

f = open("d3_final3.json","w")
f.write(json.dumps(data))
f.close()
