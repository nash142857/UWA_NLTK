# coding=UTF-8
from function import *

class ngram:
	bigram_word = set()
	def __init__(self, language, number):
		f = open(language + ".txt")
		pair = ' ' * number
		self.d = {}
		self.number = number
		for line in f:
			for letter in line.strip():
				pair = pair[1:-1] + pair[-1] + letter
				self.d.setdefault(pair, 0)
				self.d[pair] += 1
			arr_word = line.strip().split(' ')
			for i in range(0,len(arr_word) - 1):
				ngram.bigram_word.add("#".join(arr_word[i:i + 2]))
		self.length = 0
		for x in self.d.values():
			self.length += x * x
		self.length **= 0.5
		
	def eva(self, setence):
		pair = '   '
		d1 = self.d
		length1 = self.length
		d2 = {}
		pair = ' ' * self.number
		for letter in setence.strip():
			pair = pair[1:-1] + pair[-1] + letter
			d2.setdefault(pair, 0)
			d2[pair] += 1
		length2 = 0
		for x in d2.values():
			length2 += x * x
		length2 **= 0.5

		dot = 0
		for item in d1.keys():
			if item in d2:
				dot += d1[item] * d2[item]

		return float(dot) / (length1 * length2)

class guess:
	lan = ["English", "Danish", "French", "Finnish", "Swedish"]
	ng =  [[ngram(language, i) for language in lan] for i in range(1,6)]
	
	#prior given by the paper

	prior = [[0], [1,0], [1,2,0], [2,1,3,0], [2,3,1,4,0]]
	
	def eva(self, setence, n=None):
		maxscore = -1
		if n is not None:
			ran = range(n, n + 1)
		else:
			ran = range(0, 5)
		idx = -1
		for i in range(0,5):
			score = 0
			for j in ran:
				score += (j + 1) * guess.ng[j][i].eva(setence)
			if maxscore == -1 or score > maxscore:
				maxscore = score
				idx = i
		return idx

	def process(self, str):
		l = len(str)
		if l == 0:
			return {}	
		str = str.lower()
		if str[-1] not in [' ', '.', ',']:
			str += ' '
		last_i =  0
		i = 0
		res = []
		filter = ["http://", "@", "#"]
		stop_char = [(',', ' '), (',','.',' '), (',','.',' ')]
		while i < l:
			for idx2, fil in enumerate(filter):
				if str[i:].startswith(fil):
					res += self.deal(str[last_i:i], 4)
					idx = index(str[i:], stop_char[idx2])
					res.append((fil, str[i:i + idx]))
					i = i + idx
					last_i = i
			i += 1
		if last_i != l:
			res += self.deal(str[last_i:l], 4)
		return res
 
	def deal(self, str, n):
		res = []
		l = len(str)
		i = 0
		last_lan = None
		last_idx = 0
		while i < l:
			#space is common for all language
			if str[i] in [',','.',' ']:
				i = i + 1
				continue
			biggest = 128
			nxtlen = 0
			while ord(str[i]) & biggest:
				nxtlen = nxtlen + 1
				biggest >>= 1
			
			if nxtlen == 0:
				nxtlen = 1

			val = getvalue(str[i:i + nxtlen])
			#first judge language
			if nxtlen == 1:
				if val >= ord('0') and val <= ord('9'):
					lan = "Digit"
				else:
					lan = "latin"
			elif nxtlen == 2:
				if val > 0xc280 and val < 0xc9bf:
					lan = "latin"
				if val > 0xd880 and val < 0xdc80:
					lan = "Arabic"	
			elif nxtlen == 3:
				if val >= 0xE4B880 and val <= 0xe9bfbf:
					lan = "Chinese"
				elif val >= 0xe38080 and val <= 0xe383bf:
					lan = "Japanese"
				elif (val >= 0xe18480 and val <= 0xe187bf) or (val >= 0xe384b0 and val <= 0xe3868f) or (val >= 0xeab080 and val <= 0xed9eaf):
					lan = "Korean"
				else:
					lan = last_lan
			else:
				lan = "latin"

			if last_lan is not None and last_lan != lan:
				#the second step to judge latin
				if(last_lan == "latin"):
					res += self.en_deal(str[last_idx:i], n)
				else:
					res.append((last_lan, str[last_idx:i]))
				last_idx = i

			i += nxtlen
			last_lan = lan

		if last_lan == "latin":
			res += self.en_deal(str[last_idx:l], n)
		else:
			res.append((last_lan, str[last_idx:l]))

		return res
			

	def en_deal(self, setence, n):
		res = []
		arr_word = setence.strip().split(' ')
		idx = 0
		last_lan = -1
		length = len(arr_word)
		break_where = []
		last_divide = -1
		while idx + n <= length:
			lan = self.eva(' '.join(arr_word[idx:idx + n]))
			if last_lan != -1 and lan != last_lan:
				break_place = []
				for j in range(idx, idx + n - 1):
					if "#".join(arr_word[j:j + 2]) not in ngram.bigram_word:
						break_place.append(idx + n - 2 - j)
				break_pos = -1
				for j in guess.prior[n - 2]:
					if j in break_place:
						break_pos = j
						break
				if break_pos == -1:
					raise "no place to divide"
				break_where.append(idx + n - 2 - break_pos)
				idx = idx + n - 1 - break_pos
				res.append((guess.lan[last_lan], ' '.join(arr_word[last_divide + 1:idx])))
				last_divide = idx - 1
			else:
				idx = idx + 1
			last_lan = lan
		res.append((guess.lan[last_lan], ' '.join(arr_word[last_divide + 1:length])))
		return res

#unit testing

if __name__ == '__main__':
	print guess().process("hello world1234,古慎龙,http://www.baidu.com, got it")

