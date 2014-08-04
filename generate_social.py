import json
node = [("1","zh-CN"), ("2","en"), ("3", "zh-TW"),("4","en")]
link = [(1,2),(3,4),(2,3),(1,4)]

links = []
for a,b in link:
	links.append({
		"source":a,
		"target":b,
		"weight":1
	});

data = {
	"node":node,
	"link":links
}
f = open("../facebook/public/d3.json","w")
f.write(json.dumps(data))
f.close()