# coding=UTF-8

from urllib import urlopen
from urllib import urlencode
from urllib import quote
import urllib2
import json
import re
import base64
from nltk import word_tokenize
#some common function
def getvalue(str):
	ret = 0
	for cr in str:
		ret = ret * 256 + ord(cr)
	return ret

def index(str, list):
	for i in range(len(str)):
		if str[i] in list:
			return i
	return -1

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

def translate(str, src, des):
	url = "http://translate.google.cn/translate_a/t?client=t"
	url += "&text=" + quote(str)
	url += "&hl=zh-CN"
	url += "&sl=" + src
	url += "&tl=" + des
	url += "&ue=UTF-8&oe=UTF-8"
 	req = urllib2.Request(url)
 	browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
 	req.add_header('User-Agent',browser)
 	response = urllib2.urlopen(req)
 	html = response.read()
 	index1 = html.find("\"")
 	index2 = html[index1 + 1:].find("\"")  + index1 + 1
 	return html[index1 + 1:index2]

def loop_g(id, tid):
	id = str(id)
	tid = str(tid)
	url = "https://www.facebook.com/ajax/pagelet/generic.php/AllFriendsAppCollectionPagelet?data=%7B%22collection_token%22%3A%22" + id + "%3A2356318349%3A2%22%2C%22cursor%22%3A%22" + quote(base64.encodestring("0:not_structured:" + tid)[:-1]) + "%22%2C%22tab_key%22%3A%22friends%22%2C%22profile_id%22%3A" + id + "%2C%22overview%22%3Afalse%2C%22ftid%22%3Anull%2C%22order%22%3Anull%2C%22sk%22%3A%22friends%22%2C%22importer_state%22%3Anull%7D&__user=100005519621836&__a=1&__rev=1346601"
	req = urllib2.Request(url)
	browser='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
 	req.add_header('User-Agent',browser)
 	req.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
 	#cookie needed
 	req.add_header('cookie','datr=tg3xUvMHgxmVUFmrvOvMav2V; lu=ggkjSEPkvp_FvPos5_qQTpCA; c_user=100005519621836; fr=0mfTzkh1QDIJ5CF0Q.AWVtdmDMHuwPFLKdnlxgiKlRoIE.BTo4cs.Sz.FPF.AWVkg5pf; xs=214%3AFdIzX1Z8GTWQOA%3A2%3A1405421403%3A20772; csm=2; s=Aa6sLrwh5pTlBxK6.BTxQdb; act=1406532421662%2F12; p=-2; presence=EM406532641EuserFA21B05519621836A2EstateFDutF1406532641418Et2F_5b_5dEuct2F1406528739BElm2FnullEtrFA2loadA2EtwF3400421388EatF1406532638156Esb2F0CEchFDp_5f1B05519621836F0CC; wd=1440x454')
 	html = urllib2.urlopen(req).read()
 	idx = 0
	cnt = 0
	arr = []
	while True:
		idx = html.find("eng_tid")
		if idx == -1:
			break
		cnt += 1
		html = html[idx + 20:]
		fid = int(html[0:html.find("&")])
		tid = fid
		print fid
 		pr = get_person(fid)
 		if "id" in pr and "first_name" in pr and "last_name" in pr:
			print pr["id"], pr["first_name"], pr["last_name"]
		else:
			continue
 		arr.append((pr["id"], pr["first_name"], pr["last_name"]))
 	if cnt != 20:
 		return arr
 	else:
 		arr += loop_g(id, tid)
 		return arr

def root_g(id):
	req = urllib2.Request("https://www.facebook.com/profile.php?id=" + str(id) + "&sk=friends")
	browser='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
 	req.add_header('User-Agent',browser)
 	req.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
 	#cookie needed
 	req.add_header('cookie','datr=tg3xUvMHgxmVUFmrvOvMav2V; lu=ggkjSEPkvp_FvPos5_qQTpCA; c_user=100005519621836; fr=0mfTzkh1QDIJ5CF0Q.AWVtdmDMHuwPFLKdnlxgiKlRoIE.BTo4cs.Sz.FPF.AWVkg5pf; xs=214%3AFdIzX1Z8GTWQOA%3A2%3A1405421403%3A20772; csm=2; s=Aa6sLrwh5pTlBxK6.BTxQdb; act=1406532421662%2F12; p=-2; presence=EM406532641EuserFA21B05519621836A2EstateFDutF1406532641418Et2F_5b_5dEuct2F1406528739BElm2FnullEtrFA2loadA2EtwF3400421388EatF1406532638156Esb2F0CEchFDp_5f1B05519621836F0CC; wd=1440x454')
 	res = urllib2.urlopen(req).read()
 	p = re.compile(r"fsl fwb fcb.*?data-gt.*?</a>")
 	r1 = re.findall(p, res)
 	res = 0
 	arr = []
 	for string in r1:
 		idx = string.find("eng_tid")
 		string = string[idx + 20:]
 		id = int(string[0:string.find("&")])
 		pr = get_person(id)
 		if "id" in pr and "first_name" in pr and "last_name" in pr:
 			print pr["id"],pr["first_name"], pr["last_name"]
 		else:
 			continue
 		arr.append((pr["id"], pr["first_name"], pr["last_name"]))
 		res = pr["id"]
 	return (res, arr)

def g_f(id):
	id = str(id)
	print "#############################you are asking: " + id
	pr = get_person(id)
	tid, arr = root_g(id)
	arr += loop_g(id, tid)
	return arr


def get_person(id):
	person = json.loads(urlopen(url = "http://graph.facebook.com/" + str(id)).read())
	return person

def save(id):
	id = str(id)
	arr = g_f(id)
	data = {}
	data[id] = arr
	f = open("friend/" + id + ".txt", "w")
	f.write(json.dumps(data))
	f.close
	cnt = 0
	for idx in arr:
		cnt += 1
		if cnt < 40:
			continue
		data = {}
		data[idx[0]] = g_f(idx[0])
		f = open("friend/" + idx[0] + ".txt", "w")
		f.write(json.dumps(data))
		f.close

if __name__ == '__main__':
	id = 100005519621836
	print save(id)


