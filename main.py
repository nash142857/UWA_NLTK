# coding=UTF-8
# test git
import nltk, re, pprint
import csv
from collections import defaultdict
from urllib import urlopen
from divide import guess
from classify import classifier

if __name__ == '__main__':
	posts = []
	tags = []
	label = []
	reader = csv.reader(open("twitter.csv"))
	for line in reader:
		posts.append(line[1])
		label.append(line[2])
	classfy = classifier()
	classfy.train(posts, label)
	#yo no hablo espanol but some people parler francais tre bien und das ist eindeutig sehr gut
	classfy.validate(posts, label)
	guess().deal('おはよう,今天天气不错.',4)