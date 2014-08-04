# coding=UTF-8
import os
import json
import urllib
import urllib2
from urllib import quote
from HTMLParser import HTMLParser
import sys
import Queue
import threading
reload(sys)
sys.setdefaultencoding("utf-8")
link = []
node_st =  set()
node = []
dir = "./friend"
cnt = 0
class my_parse(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.datas = []
		self.judge = 0
	def handle_starttag(self, tag, attrs):
		self.judge = 0
		for name,value in attrs:
			if name == "class" and value.find("userContent") != -1:
				self.judge = 1
	def handle_data(self,data):
		if self.judge:
			self.datas.append(data.encode("UTF-8"))

parser = my_parse()
class Geturl(threading.Thread):
	def __init__(self, q, o_q):
		self.q = q
		self.o_q = o_q
		threading.Thread.__init__(self)
	def run(self):
		while True:
			id = self.q.get()
			person = json.loads(urllib.urlopen("http://graph.facebook.com/" + str(id)).read());
			if "link" not in person:
				pass
			else:
				self.o_q.put(person["link"])
			self.q.task_done()

class Gettext(threading.Thread):
	def __init__(self, q, o_q):
		threading.Thread.__init__(self)
		self.q = q
		self.o_q = o_q

	def run(self):
		while True:
			mainpage = self.q.get()
			req = urllib2.Request(mainpage)
			browser='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
 			req.add_header('User-Agent',browser)
 			req.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
 			req.add_header('cookie','datr=tg3xUvMHgxmVUFmrvOvMav2V; lu=ggkjSEPkvp_FvPos5_qQTpCA; c_user=100005519621836; fr=0mfTzkh1QDIJ5CF0Q.AWVtdmDMHuwPFLKdnlxgiKlRoIE.BTo4cs.Sz.FPF.AWVkg5pf; xs=214%3AFdIzX1Z8GTWQOA%3A2%3A1405421403%3A20772; csm=2; s=Aa6sLrwh5pTlBxK6.BTxQdb; act=1406532421662%2F12; p=-2; presence=EM406532641EuserFA21B05519621836A2EstateFDutF1406532641418Et2F_5b_5dEuct2F1406528739BElm2FnullEtrFA2loadA2EtwF3400421388EatF1406532638156Esb2F0CEchFDp_5f1B05519621836F0CC; wd=1440x454')
 			res = urllib2.urlopen(req).read()
 			res = res.replace('<!--',' ')
 			res = res.replace('-->',' ')
 			res = res.decode("UTF-8")
			parser.feed(res)
			self.o_q.put('.'.join(parser.datas))
			self.q.task_done()


class Getlan(threading.Thread):
	def __init__(self, q):
		threading.Thread.__init__(self)
		self.q = q

	def run(self):
		global cnt
		while True:
			text = self.q.get()
			url = "https://www.googleapis.com/language/translate/v2/detect?key=AIzaSyAxvvshHkJ56rp7zKia5D-OGmndaiAhfKY&q=" + quote(text)
			language = json.loads(urllib.urlopen(url).read())["data"]["detections"][0][0]["language"]
			node.append((id,language))
			print cnt, language
			cnt = cnt + 1

for file in os.listdir(dir):
	if os.path.isdir(file):
		pass
	else:
		f = open(os.path.join(dir, file), "r")
		data = json.loads(f.read())
		for key in data:
			node_st.add(key)
			for to in data[key]:
				node_st.add(to[0])
				link.append({
						"source": key,
						"target": to[0],
						"weight": 1
					});

		f.close()


q1 = Queue.Queue()
q2 = Queue.Queue()
q3 = Queue.Queue()

def main():
	for i in range(5):
		t = Geturl(q1, q2)
		t.setDaemon(True)
		t.start()
	for id in node_st:
		q1.put(id)
	for i in range(5):
		t = Gettext(q2, q3)
		t.setDaemon(True)
		t.start()
	for i in range(5):
		t = Getlan(q3)
		t.setDaemon(True)
		t.start()
	q1.join()
	q2.join()
	q3.join()


main()
data["node"] = node
f = open("d3_" + l + "_" + "r" + ".json","w")
f.write(json.dumps(data))
f.close()



