# coding=UTF-8
from function import *
from nltk import word_tokenize
#personal or topic
#topic:
	#1.social or personal
	#2.opinion or non-opinion

class ptop:
	special_char = ['%', '&', 'etc']
	
	function_file = ["adposition.xls", "auvi_verb.xls", "conjunction.xls", "interjection.xls","pro_noun.xls","pro_setence.xls"]
	
	function_word = []
	
	#init function word
	for file in function_file:
		res = []
		f = open("function_word/" + file, 'r')
		fline = f.readlines()
		for word_line in fline:
			res += [word.lower() for word in word_line.split(',')]
		f.close()
		function_word += res

	syntactic_word = ['\'', ',','.',':',';','?','!']
	
	social_word_begin = ['@', '#', 'http://']

	def character_based(self,str):
		numofletter = 0.
		numofupper = 0.
		numofdigit = 0.
		numofspace = 0.
		numofspecial = 0.
		for idx, char in enumerate(str):
			if char.isdigit():
				numofdigit += 1
			elif char.isupper():
				numofupper += 1
				numofletter += 1
			elif char.islower():
				numofletter += 1
			elif char.isspace():
				numofspace += 1
			else:
				for string in ptop.special_char:
					if str[idx:].startswith(string):
						numofspecial += 1
						break

		l = len(str)
		[l, numofletter / l, numofupper / l, numofdigit / l, numofspace / l, numofspecial / l]

	def word_based(self,str):
		arr_word = word_tokenize(str)
		word_num = len(str.split(' '))
		word_length = 0.	
		short_wordnum = 0.
		for word in arr_word:
			word_length += len(word)
			if len(word) in range(1,4):
				short_wordnum += 1
		return [word_num, word_length / word_num, short_wordnum / word_num]


	def function_based(self,str):
		arr_word = word_tokenize(str)
		l = len(str.split(' '))
		res = [0.] * len(ptop.function_word)
		for word in arr_word:
			for word in ptop.function_word:
				res[function_word.index(word)] += 1

		return [val / l for val in res]

	def syntactic_based(self,str):
		res = [0.] * 10
		multiple = ['???', '!!!','...']
		l = len(str.split(' ')) # can't use word_tokenize length
		for idx, char in enumerate(str):
			if char in self.syntactic_word:
				res[syntactic_word.index(char)] += 1
			for i in range(0,3):
				str[idx:].startswith(multiple[i])			
				res[7 + i] += 1

		return [val / l for val in res]

	def social_based(self,str):
		l = len(str.split(' '))
		arr_word = word_tokenize(str)
		res = [0] * 4
		for word in arr_word:
			for i in range(len(social_word_begin)):
				if word.startswith(social_word_begin[i]):
					res[i] += 1

		for idx in range(len(str) - 4):
			if ((ord(str[idx]) >> 4) == 15):
				val = getvalue(sample[idx][idx2:idx2 + 4])
				if(val >= 0xf09f9880 and val <= 0xf09f998f):
					res[3] += 1

		return [val / l for val in res]

	def normalize(self,data):
		l = len(data)
		minval = [-1] * l
		maxval = [-1] * l
		dimen = len(data[0])
		for i in range(dimen):
			for j in range(l):
				if minval[i] == -1 or minval[i] > dimen[j][i]:
					minval[i] = dimen[j][i]
				if maxval[i] == -1 or maxval[i] < dimen[j][i]:
					maxval[i] = dimen[j][i]
		data = [[[(val - minval[idx]) / (maxval[idx] - minval[idx])] for idx,val in enumerate(vt)] for vt in data]
		self.maxval = maxval
		self.minval = minval
	def __init__(self):
		self.feature_extraction = [self.character_based, self.word_based,
		self.function_based, self.syntactic_based, self.social_based]

	def training(self, posts, label, select_feature):
		data = []
		target = []
		self.judger = svm.SVC(gamma=0.001, C=100.)
		self.select = select_feature
		for post in posts:
			feature = []
			for i in range(0,5):
				if (select_feature >> i) & 1:
					feature += self.feature_extraction[i](post)
			data.append(feature)
		self.normalize(data)
		self.judger.fit(data,target)
	def predict(self, str):
		feature = []
		for i in range(0,5):
			if (self.select >> i) & 1:
				feature += self.feature_extraction[i](str)
		feature = [(val - minval[idx]) / (maxval[idx] - minval[idx]) for idx, val in enumerate(feature)]
		print self.judger.predict(feature)


