# coding=UTF-8

#classify me or other fair
from function import *
import math
class prp:
	def __init__(self):
		pass
	def train(self,sample, label):
		self.has_hash = [0,0]
		self.has_at = [0,0]
		self.has_http = [0,0]
		self.has_enjoy = [0,0]
		index = ([i for i  in range(len(sample)) if label[i] == 'Y'],[i for i  in range(len(sample)) if label[i] == 'N'])
		self.len = [len(index[0]), len(index[1])]
		self.dictionary = [{}, {}]
		self.word_num = [0,0]
		for i in range(0,2):
			for idx in index[i]:
				#judge 
				if sample[idx].find("@") != -1:
					self.has_at[i] += 1
				
				#judge http
				if sample[idx].find("http:") != -1:
					self.has_http[i] += 1
				
				#judge hash
				if sample[idx].find("#") != -1:
					self.has_hash[i] += 1
				
				#judge face
				for idx2 in range(len(sample[idx])):
					if ((ord(sample[idx][idx2]) >> 4) == 15):
						val = getvalue(sample[idx][idx2:idx2 + 4])
						if(val >= 0xf09f9880 and val <= 0xf09f998f):
							self.has_enjoy[i] += 1
							break
			#naive bayes for pure words
			for idx in index[i]:
				arr_str = erase(sample[idx]).split(' ')
				for string in arr_str:
					if(string.startswith("@") or string.startswith("#") or string.startswith("http:")):
						continue
					else:
						self.word_num[i] += 1
						self.dictionary[i][string.lower()] = self.dictionary[i].get(string.lower(), 0) + 1

	def validate(self, sample, label):
		length = len(sample)
		res = [0,0,0,0]
		for idx in range(0,length):
			x1 = 0
			x2 = 0
			if label[idx] == 'Y':
				x1 = 1
			if self.test(sample[idx]) == 'Y':
				x2 = 1
			res[(x1 << 1) + x2] += 1

		precision = 1.0 * res[3] / (res[3] + res[1])
		recall = 1.0 * res[3] / (res[3] + res[2])
		ac = 1.0 * (res[3] + res[0]) / (res[0] + res[1] + res[2] + res[3])
		
		print "accurate percent: %.2f" % ac
		print "precision percent: %.2f" % precision
		print "recall percent: %.2f" % recall
		print "f-measure percent: %.2f" % (2.0 * precision * recall / (precision + recall))

	def test(self, string):	
		possibility = [math.log(1.0 * self.len[0] / (self.len[0] + self.len[1])), math.log(1.0 * self.len[1] / (self.len[0] + self.len[1]))]
		has_hash = False
		has_at = False
		has_http = False
		has_enjoy = False
		has_at =  (string.find("@") != -1)
		has_hash = (string.find("#") != -1)
		has_http = (string.find("http:") != -1)	
	
		for idx2 in range(len(string)):
			if ((ord(string[idx2]) >> 4) == 15):
				val = getvalue(string[idx2:idx2 + 4])
				if(val >= 0xf09f9880 and val <= 0xf09f998f):
					has_enjoy = True
					break
	
		for i in range(0,2):
			
			if has_hash:
				possibility[i] += math.log(1.0 * (self.has_hash[i] + 1) / (self.len[i] + 2))
			else:
				possibility[i] += math.log(1 - 1.0 * (self.has_hash[i] + 1) / (self.len[i] + 2))
			
			if has_at:
				possibility[i] += math.log(1.0 * (self.has_at[i] + 1) / (self.len[i] + 2))
			else:
				possibility[i] += math.log(1 - 1.0 * (self.has_at[i] + 1) / (self.len[i] + 2))
			
			if has_http:
				possibility[i] += math.log(1.0 * (self.has_http[i] + 1) / (self.len[i] + 2))
			else:
				possibility[i] += math.log(1 - 1.0 * (self.has_http[i] + 1) / (self.len[i] + 2))
			
			if has_enjoy:
				possibility[i] += math.log(1.0 * (self.has_enjoy[i] + 1) / (self.len[i] + 2))
			else:
				possibility[i] += math.log(1 - 1.0 * (self.has_enjoy[i] + 1) / (self.len[i] + 2))
			
			arr_str = erase(string).split(' ')
			len_dic = len(self.dictionary[i])
			
			for substr in arr_str:
				substr = substr.lower()
				possibility[i] += math.log(1.0 * (self.dictionary[i].get(substr, 0) + 1) / (self.word_num[i] + len_dic))
		return [possibility[0], possibility[1]]



