import json
import os
data = json.loads(open("d3_final3.json","r").read())
id = [arr[0] for arr in data["node"]]
node_st = {}
for edge in data["link"]:
	node_st.setdefault(edge["source"],0)
	node_st.setdefault(edge["target"],0)
	node_st[edge["source"]] += 1
	node_st[edge["target"]] += 1

value_st = {}
for idx in id:
	value_st[idx] = node_st[idx]
	for edge in data["link"]:	
		if idx == edge["source"]:
			value_st[idx] += node_st[edge["target"]]
		if idx == edge["target"]:
			value_st[idx] += node_st[edge["source"]]	

node = []
for item in data["node"]:
	if value_st[item[0]] >= 600:
		node.append(item)

print len(node)

data["node"] = node
id = [arr[0] for arr in data["node"]]
link = []
for edge in data["link"]:
	if edge["source"] not in id or edge["target"] not in id:
		pass
	else:
		link.append(edge)

data["link"] = link

f = open("d3_final4.json","w")
f.write(json.dumps(data))
f.close()