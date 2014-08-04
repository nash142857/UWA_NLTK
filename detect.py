# coding=UTF-8
import urllib2

url = "http://translate.google.cn/#auto/zh-CN/你好"
browser='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
req = urllib2.Request(url + "hello")
req.add_header('User-Agent',browser)
req.add_header('cookie','datr=tg3xUvMHgxmVUFmrvOvMav2V; lu=ggkjSEPkvp_FvPos5_qQTpCA; c_user=100005519621836; fr=0mfTzkh1QDIJ5CF0Q.AWVtdmDMHuwPFLKdnlxgiKlRoIE.BTo4cs.Sz.FPF.AWVkg5pf; xs=214%3AFdIzX1Z8GTWQOA%3A2%3A1405421403%3A20772; csm=2; s=Aa6sLrwh5pTlBxK6.BTxQdb; act=1406532421662%2F12; p=-2; presence=EM406532641EuserFA21B05519621836A2EstateFDutF1406532641418Et2F_5b_5dEuct2F1406528739BElm2FnullEtrFA2loadA2EtwF3400421388EatF1406532638156Esb2F0CEchFDp_5f1B05519621836F0CC; wd=1440x454')
res = urllib2.urlopen(req).read()
f = open("1.html", "w")
f.write(res)
f.close()
