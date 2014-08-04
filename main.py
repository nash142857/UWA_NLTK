# coding=UTF-8
import nltk, re, pprint
import csv
from collections import defaultdict
from urllib import urlopen
from divide import guess
from prp import prp
import sys
import json
import socket
from thread import *
from nltk import word_tokenize
from function import *
#global variable
classfy = classifier()
guesser = guess()
key = "ZXhpdA=="

def condeal(con):
	data = str(con.recv(1024).strip())
	print "receive data:",data
	print word_tokenize(data)
	if not data:
		return
	if data == key:
		return
	res = guesser.process(data)
	res.append(classfy.test(data))
	res = json.dumps(res,ensure_ascii=False)
	con.sendall(res)
	con.close()
	print "connection closed"

def init():
	posts = []
	tags = []
	label = []
	reader = csv.reader(open("twitter.csv"))
	for line in reader:
		posts.append(line[1])
		label.append(line[2])
	classfy.train(posts, label)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "wrong parameter size"
		print "usage: python main.py port"
		sys.exit()
	init()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "judge server has been created"
	s.bind(('', int(sys.argv[1])))
	print "judge server has been binded"
	s.listen(10)
	print "judge server is now listening"
	while True:
		con, addr = s.accept()
		print "connect with",addr[0],":",addr[1]
		start_new_thread(condeal, (con,))
	s.close()


