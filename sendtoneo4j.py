import json
import urllib2
import os
root = "http://localhost:7474/db/data/transaction/commit"
nodelabel = "facebooknode"
node_st = {}
def sendq(sentence):
	req = urllib2.Request(root)
	data = {}
	data["statements"] = []
 	data["statements"].append({
 		"statement":sentence
 		});
 	req.add_header("Content-Type", "application/json")
	req.add_header("Accept","application/json; charset=UTF-8")
	res = urllib2.urlopen(req, json.dumps(data))
	print res.read()

def add_node(id,lang,name):
	lang = lang.replace('-','_')
	str = "create (e:_facebook:%s {id:'%s', name:'%s'})" % (lang, id, name)	
	print str
	sendq(str)

def add_edge(lid, rid, llabel, rlabel):
	llabel = llabel.replace('-','_')
	rlabel = rlabel.replace('-','_')
	str = "match (l:_facebook {id:'%s'}) match (r:_facebook {id:'%s'}) create (l) - [:friend] -> (r)" % (lid,rid)
	print str
	sendq(str)

def clear():
	str = "match (a) optional match (a)-[r]-() delete a, r"
	sendq(str)

clear()
data = json.loads(open("d3_final4.json","r").read())
for item in data["node"]:
	add_node(item[0], item[1], item[2])
	node_st[item[0]] = item[1]

for edge in data["link"]:
	add_edge(edge["source"], edge["target"], node_st[edge["source"]], node_st[edge["target"]])
'''
usage:

1.search relation: 

	match (a:_facebook) - [r] -> (b:facebook) return r

2.search node:

	match (a:_facebook) return a

3.triangle connection:

	match (a:_facebook) - [r1] -> (b:_facebook) match (b:_facebook) - [r2] -> (c:_facebook) match (c:_facebook) - [r3] -> (a:_facebook) return r1, r2, r3 limit 1000

4.find a person's relation: 

	match (a:_facebook {id:'100005519621836'}) - [r:friend] -> (b:_facebook) return r
	
'''

