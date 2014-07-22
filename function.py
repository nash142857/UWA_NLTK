#some common function
def getvalue(str):
	ret = 0
	for cr in str:
		ret = ret * 256 + ord(cr)
	return ret


def erase(string):
	res = ""
	length = len(string)
	idx = 0
	while idx < length:
		val = ord(string[idx])
		shift = 0
		bestval = 128
		while val & bestval:
			shift += 1
			bestval >>= 1
		if shift == 0:
			res += string[idx]
			shift = 1
		idx = idx + shift
	return res
