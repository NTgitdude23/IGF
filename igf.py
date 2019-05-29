#!/usr/bin/python3

from colorama import Fore, Back, Style
from shodan import Shodan
from urllib.request import urlopen
from fake_useragent import UserAgent
from urllib.parse import urljoin
from builtwith import builtwith
import socket, time, os, dns.resolver, sys, urllib, urllib.request
import shodan
import requests, io, sys
import ipaddress
import whois
import http.client
import ftplib
import ssl
import re
import json

#####################################################################
#                                                                   #
# IGF - Information Gathering Framework v1.4 by c0deninja           #
#                                                                   #
# pip3 install -r requirements.txt                                  #
#                                                                   # 
#####################################################################

banner = """


 ██▓     ▄████      █████▒
▓██▒    ██▒ ▀█▒   ▓██   ▒ 
▒██▒   ▒██░▄▄▄░   ▒████ ░ 
░██░   ░▓█  ██▓   ░▓█▒  ░ 
░██░   ░▒▓███▀▒   ░▒█░    
░▓      ░▒   ▒     ▒ ░    
 ▒ ░     ░   ░     ░      
 ▒ ░   ░ ░   ░     ░ ░   v1.4
 ░           ░                                        

"""

def findbackup():
	try:
		site = input("Enter Site: ")
		wordlist = input("Enter Wordlist: ")
		print("\n")
		ua = UserAgent()
		header = {'User-Agent':str(ua.chrome)}
		try:
			f = open(wordlist, 'r')	
			backupfiles = f.readlines()
		except IOError:
			print (Fore.RED + "File not found")
			webinfo()
		
		for backuplist in backupfiles:
			backuplist = backuplist.strip()
			links = site + "/" + backuplist
			response = requests.get(links, headers=header)
			if response.status_code == 200:
				print (Fore.GREEN + "Found: {}".format(links))
			elif response.status_code == 429:
				print (Fore.RED + "Too many requests")
				webinfo()
			elif response.status_code == 400:
				print (Fore.RED + "Bad Request")
				webinfo()
			elif response.status_code == 403:
				print (Fore.RED + "Forbidden")
				webinfo()
			elif response.status_code == 500:
				print (Fore.RED + "Internal server error")	
				webinfo()
	except requests.exceptions.MissingSchema:
		print (Fore.RED + "Please use: http://site.com")


def techdiscovery():
	try:
		site = input("Enter Website: ")
		print("\n")
		info = builtwith(site)
		for framework, tech in info.items():
			print (Fore.GREEN + framework, ":", tech)
	except UnicodeDecodeError:
		pass

def spider():
	site = input("Enter site: ")
	print("\n")
	ua = UserAgent()
	header = {'User-Agent':str(ua.chrome)}	
	try:
		response = requests.get(site, headers=header)
		if response.status_code == 200:
			content = response.content
			links = re.findall('(?:href=")(.*?)"', content.decode('utf-8'))
			for link in links:
				link = urljoin(site, link)
				print (Fore.GREEN + link)
		elif response.status_code == 429:
			print (Fore.RED + "Too many requests")
		elif response.status_code == 400:
			print (Fore.RED + "Bad Request")
		elif response.status_code == 403:
			print (Fore.RED + "Forbidden")
		elif response.status_code == 500:
			print (Fore.RED + "Internal server error")	
	except requests.exceptions.ConnectionError:
		print (Fore.RED + "Connection Error")
	except requests.exceptions.MissingSchema:
		print (Fore.RED + "Please use: http://site.com")	


def checksite():
	try:
		site = input("Enter Website: ")
		print ("\n")
		ua = UserAgent()
		header = {'User-Agent':str(ua.chrome)}		
		response = requests.get(site, headers=header)
		if response.status_code == 200:
			print (Fore.GREEN + "Site: {} is up!".format(site))
			webinfo()
		elif response.status_code == 400:
			print (Fore.RED + "Bad Request")
		elif response.status_code == 404:
			print (Fore.RED + "Not Found")
		elif response.status_code == 403:
			print (Fore.RED + "Forbidden")
		elif response.status_code == 405:
			print (Fore.RED + "Method not allowed")
		elif response.status_code == 404:
			print (Fore.RED + "Not Found")
		elif response.status_code == 423:
			print (Fore.RED + "LOCKED")
		elif response.status_code == 429:
			print (Fore.RED + "Too many requests")
		elif response.status_code == 499:
			print (Fore.RED + "Client closed request")
		elif response.status_code == 500:
			print (Fore.RED + "Server error")
		elif response.status_code == 501:
			print (Fore.RED + "Not implemented")
		elif response.status_code == 502:
			print (Fore.RED + "Bad Gateway")
		elif response.status_code == 503:
			print (Fore.RED + "Service Unavailable")
		elif response.status_code == 511:
			print (Fore.RED + "Network Authentication Required")
		elif response.status_code == 599:
			print (Fore.RED + "Network Connect Timeout Error")
	except requests.exceptions.MissingSchema:
		print (Fore.GREEN + "Please use: http://site.com")	
	except requests.exceptions.ConnectionError:
		print (Fore.RED + "name or service not known")
	
	

def shodansearch():
	# shodan script by Sir809
	ask = input("Do you have a Shodan API key?: ").lower()

	if ask == "yes":
		pass
	else:
		start()

	apikey = input("Enter API key: ")
	try:
		api = Shodan(apikey)
		url = input("Ip:> ")
		print("\n")
		h = api.host(url)
	except shodan.exception.APIError:
		print (Fore.RED + "Invalid API key!")
		start()
	print(Fore.GREEN + '''
        IP: {}
        Country: {}
        City: {}
        ISP: {}
        Org: {}
        Ports: {}
        OS: {}
    
        '''.format(h['ip_str'],h['country_name'],h['city'],h['isp'],h['org'],h['ports'],h['os']))


def shellfinder():
	site = input("Enter Website: ")
	wordlist = input("Enter Wordlist: ")
	print("\n")
	try:
		f = open(wordlist, 'r')
		shells = f.readlines()
	except IOError:
		print (Fore.RED + "FIle not found!")
		webinfo()
	
	try:
		for shelllist in shells:
			shelllist = shelllist.strip()
			links = site + "/" + shelllist
			response = requests.get(links)
			if response.status_code == 200:
				print(Fore.GREEN + "Found: {}".format(links))
			elif response.status_code == 429:
				print (Fore.RED + "Too many requests")
				webinfo()
			elif response.status_code == 400:
				print (Fore.RED + "Bad Request")
				webinfo()
			elif response.status_code == 403:
				print (Fore.RED + "Forbidden")
				webinfo()
			elif response.status_code == 500:
				print (Fore.RED + "Internal server error")	
				webinfo()
	except requests.exceptions.MissingSchema:
		print (Fore.GREEN + "Please use: http://site.com")
			

def finduploads():
	upload = ["upload", "uploads", "upload.php", "up", "uploads.php",
	"blog/uploads", "blog/upload.php", "blog/uploads.php"]
	try:
		site = input("Enter site: ")
		print ("\n")
		for fileupload in upload:
			fileupload = fileupload.strip()
			uploadlinks = site + "/" + fileupload
			response = requests.get(uploadlinks)
			if response.status_code == 200:
				print (Fore.GREEN + "Found: {}".format(uploadlinks))
			elif response.status_code == 429:
				print (Fore.RED + "Too many requests")
				webinfo()
			elif response.status_code == 400:
				print (Fore.RED + "Bad Request")
				webinfo()
			elif response.status_code == 403:
				print (Fore.RED + "Forbidden")
				webinfo()
			elif response.status_code == 500:
				print (Fore.RED + "Internal server error")	
				webinfo()
	except requests.exceptions.MissingSchema:
		print ("Please use: http://wwww.site.com")

def geolocation():
	# IP Geolocation by Sir809
	try:
		ip = input("IP:> ")
		print('\n')
		url = ("https://ipinfo.io/{}/json".format(ip))
		v =  urllib.request.urlopen(url)
		j = json.loads(v.read())
		for dato in j:
			print(dato + ": " +j[dato])
	except urllib.error.HTTPError:
		print (Fore.RED + "NOT FOUND!")

def reversednslookup():
	ip = input("Enter IP: ")
	print("\n")
	try:
		reversedns = socket.gethostbyaddr(str(ip))
		print(reversedns[0])
	except socket.error:
		print (Fore.RED + "Error")

def wordpresscheck():
	wp = ['wordpress', 'wp-content', 'wp-login', 'wp-login.php', 'wp-admin', 'wp', 'wp-config',
	'wp-config.php', 'wp-mail.php', 'wp-load.php', 'wp-settings.php', 'wp-includes', 'wp-activate.php',
	'wp-cron.php', 'wp-signup.php', 'wp-config-sample.php']

	site = input("Enter website: ")
	print ("\n")
	
	for wpress in wp:
		wpress = wpress.strip()
		wplinks = site + "/" + wpress
		response = requests.get(wplinks)
		if response.status_code == 200:
			print (Fore.GREEN + "Wordpress directory has been found! {}".format(wplinks))
		elif response.status_code == 429:
			print (Fore.RED + "Too many requests")
			webinfo()
		elif response.status_code == 400:
			print (Fore.RED + "Bad Request")
			webinfo()
		elif response.status_code == 403:
			print (Fore.RED + "Forbidden")
			webinfo()
		elif response.status_code == 500:
			print (Fore.RED + "Internal server error")	
			webinfo()

def cloudflarebypass():
	domains = ['mail', 'ftp', 'cpanel', 'webmail]
	try:
		site = input("Enter Website: ")
		print ("\n")
		try:
			ip = socket.gethostbyname(str(site))
		except socket.error:
			pass
		for subdomain in domains:
			subdomains = subdomain.strip()
			subsite = subdomains + site
			try:
				subip = socket.gethostbyname(subsite)
				if subip is not ip:
					print (Fore.GREEN + "Cloudflare has been bypassed!")
					print (Fore.GREEN + "The real IP is {}".format(subip))
					time.sleep(1)
					webinfo()
				else:
					print ("Could not retrieve the real IP.")
			except socket.error:
				pass
	except requests.exceptions.MissingSchema:
		print ("Please use: caca.com")

def adminpanelfind():
	adminlist = ['admin', 'cpanel', 'phpmyadmin', 'login', 'login.php', 'wp-admin', 'cp', 'master', 'adm', 'member', 'control', 'webmaster', 
'myadmin', 'admin_cp', 'admin_site', 'administratorlogin/', 'adm/', 'admin/account.php', 'admin/index.php', 'admin/login.php', 'admin/admin.php',
'admin/account.php', 'admin_area/admin.php', 'admin_area/login.php', 'siteadmin/login.php', 'siteadmin/index.php', 'siteadmin/login.html',
'admin/account.html', 'admin/index.html', 'admin/login.html', 'admin/admin.html']
	try:
		site = input("Enter Website: ")
		print ("\n")
		ua = UserAgent()
		header = {'User-Agent':str(ua.chrome)}
		for admin in adminlist:
			admin = admin.strip()
			link = site + "/" + admin
			response = requests.get(link, headers=header)
			if response.status_code == 200:
				print ("Found {}".format(link))
			elif response.status_code == 400:
				print("{} Not Found".format(link))
			elif response.status_code == 429:
				print ("Too many requests")
			elif response.status_code == 400:
				print ("Bad Request")
			elif response.status_code == 403:
				print ("Forbidden")
			elif response.status_code == 500:
				print ("Internal server error")	
	except requests.exceptions.MissingSchema:
		print (Fore.RED + "Please use http:// or https://")

def smtpenum():
	wordlist = input("Wordlist: ")
	host = input("Host: ")
	port = input("Port: ")

	try:
		f = open(wordlist, 'rb')
		smtplist = f.readlines()
	except IOError:
		print(Fore.RED + "Could not find the file!")
	
	print ("********************")
	print ("Host: " + host)
	print ("Port: " + port)
	print ("Wordlist: " + wordlist)
	print ("Size: " + str(len(smtplist)))
	print ("********************")
	print ("\n")
		
	print ("Verifying Users, Please wait..." + "\n")
		
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, int(port)))	
	except socket.error:
		print (Fore.RED + "Could not connect to host")
	except TimeoutError:
		print (Fore.RED + "Connection timed out")
	except ValueError:
		print (Fore.RED + "Value Error")
		
	try:
		for users in smtplist:
			userlist = users.strip()
			s.sendall(b"VRFY " + userlist + b"\r\n")
			response = s.recv(1024)
			
			if re.match(b"250", response):
				print ("Found User: " + str(userlist))
			elif re.match(b"550", response):
				print ("{} NOT found".format(str(userlist)))
	except ConnectionResetError:
		print ("Connection reset by peer")
	f.close()		
	s.close()

def filedownload():
	try:
		site = input("URL of the file: ")
		filename = input("Save file as: ")
		
		headers={'User-Agent': 'Mozilla/5.0'}
		req = requests.get(site, headers)
		
		with open(filename, 'wb') as download:
			download.write(req.content)
			print ("File {} has been downloaded".format(filename))
	except requests.exceptions.MissingSchema:
		print ("Please use: http://site.com")

def serviceban():
	host = input("IP: ")
	port = input("Port: ")
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, int(port)))
		data = s.recv(1024)
		print (data.strip())
		s.close()
	except socket.error:
		print ("Could not connect to host")

def anonftp():
	host = input("FTP server: ")
	print ("\n")
	try:
		ftp = ftplib.FTP(host)
		ftp.login('anonymous', 'anonymous')
		print (str(host) + "\033[0;0m Anonymous FTP logon successful")
		time.sleep(2)
		ftp.quit()
	except Exception as e:
		print (str(host) + Fore.RED + " Anonymous FTP logon failed.")


def subrute():
	host = input("Enter Website: ")
	wordlist = input("Enter Sub Domain list: ")
	ua = UserAgent()
	header = {'User-Agent':str(ua.chrome)}
	try:
		with open(wordlist, 'r') as f:
			sublist = f.readlines()
			sublist = list(map(lambda s: s.rstrip("\n"),sublist))
	except IOError:
		print (Fore.RED + "File not found")
	try:
		for lines in sublist:
			time.sleep(1.5)
			check = requests.get("https://" + lines + "." + host, headers=header).status_code
			if check == 200:
				print (Fore.GREEN + "Found: " + lines + "." + host)
	except requests.exceptions.ConnectionError:
		print (Fore.RED + "Connection Refused by Host")
	except UnboundLocalError:
		pass


def getoptions():
	try:
		host = input("Enter website: ")
		print ("\n")
		conn = http.client.HTTPConnection(host)
		conn.connect()
		conn.request('OPTIONS', '/')
		response = conn.getresponse()
		check = response.getheader('allow')
		print (Fore.GREEN + "[OPTIONS]")
		print (response.getheader('allow'))
		if check is None:
			print ("OPTIONS is not available for listing.")
			conn.close()
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")
		time.sleep(2)
	except http.client.InvalidURL:
		print (Fore.RED + "Please use: site.com or www.site.com")

def gethead():
	try:
		host = input("Enter Website: ")
		print ("\n")
		resp = requests.head(host)
		print (resp.headers)
		time.sleep(2)
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")
	except requests.exceptions.MissingSchema:
		print (Fore.RED + "Please use http or https://site.com")

def whoistool():
	try:
		host = input("Enter website: ")
		w = whois.whois(host)
		print (w)
		time.sleep(2)
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")

def getrobot():
	try:
		site = input("Enter Website: ")
		print ("\n")
		getreq = urlopen(site + "/" + "robots.txt", data=None)
		data = io.TextIOWrapper(getreq, encoding='utf-8')
		print (Fore.GREEN + data.read())
		time.sleep(2)
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")
	except urllib.error.URLError:
		print (Fore.RED + "Name or service not known")
	except ValueError:
		print(Fore.RED + "Unknown URL type, please use: http://site.com")


def ipaddressresolv():
	try:
		print ("EX: site.com")
		host = input("Website: ") #Ex: use site.com format
		print ("\n")
		print (Fore.GREEN + "IPv4 Address: " + socket.gethostbyname(host))
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")
	time.sleep(2)

def ipv4tov6():
	try:
		ip = input("Enter IP Address: ")
		print ("\n")
		print (Fore.GREEN + ipaddress.IPv6Address('2002::' + ip).compressed)
		time.sleep(2)
	except ipaddress.AddressValueError:
		print (Fore.RED + "IP address not permitted sorry")


def grabthebanner():
	try:
		host = input("Enter Host: ")
		port = int(input("Enter Port: "))
		sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sck.connect((host, port))
		print ("STATUS: " + "host is up!" + "\n")
		print ("Grabbing the banner please wait!" + "\n")
		time.sleep(3)
		sck.send(b"HEAD / HTTP/1.0\r\n\r\n")
		data = sck.recv(1024)
		sck.close()
		print (data.strip())
		time.sleep(2)
	except socket.error:
		print (Fore.RED + "Host is not reachable")
	except ValueError:
		pass

def grabthebannerssl():
	host = input("Enter Host: ")
	port = int(input("Enter Port: "))
	try:
		sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssock = ssl.wrap_socket(sck)
		ssock.connect((host, port))
		print ("STATUS: " + "host is up!" + "\n")
		print ("Grabbing the banner please wait!" + "\n")
		time.sleep(3)
		ssock.send(b"HEAD / HTTP/1.0\r\n\r\n")
		data = ssock.recv(1024)
		ssock.close()
		print (data.strip())
		time.sleep(2)
	except socket.error:
		print (Fore.RED + "Host is not reachable")

def dirbrute():
	host = input("Enter Website: ")
	wordlist = input("Enter Wordlist: ")
	try:
		file = open(wordlist, 'r')
		print (Fore.GREEN + "Found: " + wordlist)
		file.close()
	except IOError:
		print (Fore.RED + "Couldn't find " + wordlist)
		pass
	
	ua = UserAgent()
	header = {'User-Agent':str(ua.chrome)}

	with open(wordlist, 'r') as f:
		dirblist = f.readlines()
	try:
		for lines in dirblist:
			dirlines = lines.strip()
			links = host + dirlines
			response = requests.get(links, headers=header)
			if response.status_code == 200:
				print ("Found: {}".format(links))
			elif response.status_code == 429:
				print (Fore.RED + "Too many requests")
				webinfo()
			elif response.status_code == 400:
				print (Fore.RED + "Bad Request")
				webinfo()
			elif response.status_code == 403:
				print (Fore.RED + "Forbidden")
				webinfo()
			elif response.status_code == 500:
				print (Fore.RED + "Internal server error")	
				webinfo()
			else: 
				print ("Not Found: {}".format(links))

	except requests.exceptions.MissingSchema:
		print (Fore.RED + "Please use: http or https://www.site.com/")
	except socket.gaierror:
		print (Fore.RED + "Name or service not known")

def dnslookup():
	try:
		host = input("Enter Host: ")
		print ("\n")
		info = dns.resolver.query(host, 'MX')
		for rdata in info:
			print (Fore.GREEN + "Host ", rdata.exchange, 'has preference', rdata.preference)
			time.sleep(2)
	except dns.resolver.NoAnswer:
		print (Fore.RED + "Please use: site.com")
	except dns.resolver.NXDOMAIN:
		print (Fore.RED + "Please use: site.com")

def portscanner():
	ip = input("Enter IP to scan: ")
	print ("\n")
	print ("Scanning IP: " + ip + " please wait..." + "\n")
	try:
		for port in range(1, 65535):
			sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			data = sck.connect_ex((ip, port))
			if data == 0:
				print (Fore.GREEN + "Port: " + str(port) + " " + "open")
			sck.close()
	except socket.error:
		print (Fore.RED + "Could not connect to host")
	except KeyboardInterrupt:
		print ("You pressed CTRL+C")
	except ipaddress.AddressValueError:
		print ("IP address not allowed")

def miscellaneous():
	while True:
		print (Fore.RED + banner)
		
		print (Fore.RED + "[" + Fore.CYAN + "1" + Fore.RED + "]" + Fore.WHITE + " Port Scanner")
		print (Fore.RED + "[" + Fore.CYAN + "2" + Fore.RED + "]" + Fore.WHITE + " SMTP Enumeration")
		print (Fore.RED + "[" + Fore.CYAN + "3" + Fore.RED + "]" + Fore.WHITE + " Anonymous FTP")
		print (Fore.RED + "[" + Fore.CYAN + "4" + Fore.RED + "]" + Fore.WHITE + " Service Banner")
		print (Fore.RED + "[" + Fore.CYAN + "5" + Fore.RED + "]" + Fore.WHITE + " Download File")
		print (Fore.RED + "<" + Fore.CYAN +"--" + Fore.WHITE + " Back")
		print ("\n")

		misccolor = Fore.RED + "(" + Fore.CYAN + "Miscellaneous" + Fore.RED + ")"
		prompt = input(Fore.WHITE + "IGF~" + misccolor + Fore.WHITE + "# ")
		if prompt == "1":
			portscanner()
		if prompt == "2":
			smtpenum()
		if prompt == "3":
			anonftp()
		if prompt == "4":
			serviceban()
		if prompt == "5":
			filedownload()
		if prompt == "back":
			start()


def ipinformation():
	while True:
		print (Fore.RED + banner)
		
		print (Fore.RED + "[" + Fore.CYAN + "1" + Fore.RED + "]" + Fore.WHITE + " IPv4 to IPv6")
		print (Fore.RED + "[" + Fore.CYAN + "2" + Fore.RED + "]" + Fore.WHITE + " IP Geolocation")
		print (Fore.RED + "[" + Fore.CYAN + "3" + Fore.RED + "]" + Fore.WHITE + " Shodan IP info")
		print (Fore.RED + "<" + Fore.CYAN +"--" + Fore.WHITE + " Back")
		print ("\n")

		ipinfocolor = Fore.RED + "(" + Fore.CYAN + "IP Information" + Fore.RED + ")"
		prompt = input(Fore.WHITE + "IGF~" + ipinfocolor + Fore.WHITE + "# ")
		if prompt == "1":
			ipv4tov6()
		if prompt == "2":
			geolocation()
		if prompt == "3":
			shodansearch()
		if prompt == "back":
			start()
		

def webinfo():
	while True:
		print (Fore.RED + banner)

		print (Fore.RED + "[" + Fore.CYAN + "1" + Fore.RED + "]" + Fore.WHITE + "  Banner Grabber")     
		print (Fore.RED + "[" + Fore.CYAN + "2" + Fore.RED + "]" + Fore.WHITE + "  Directory brute")     
		print (Fore.RED + "[" + Fore.CYAN + "3" + Fore.RED + "]" + Fore.WHITE + "  Sub domain brute")    
		print (Fore.RED + "[" + Fore.CYAN + "4" + Fore.RED + "]" + Fore.WHITE + "  Convert domain to IP") 
		print (Fore.RED + "[" + Fore.CYAN + "5" + Fore.RED + "]" + Fore.WHITE + "  Get robots.txt")       
		print (Fore.RED + "[" + Fore.CYAN + "6" + Fore.RED + "]" + Fore.WHITE + "  Whois lookup tool")    
		print (Fore.RED + "[" + Fore.CYAN + "7" + Fore.RED + "]" + Fore.WHITE + "  HTTP HEAD request")    
		print (Fore.RED + "[" + Fore.CYAN + "8" + Fore.RED + "]" + Fore.WHITE + "  HTTP OPTIONS")        
		print (Fore.RED + "[" + Fore.CYAN + "9" + Fore.RED + "]" + Fore.WHITE + "  DNS lookup")
		print (Fore.RED + "[" + Fore.CYAN + "10" + Fore.RED + "]" + Fore.WHITE + " Find Admin Panel")
		print (Fore.RED + "[" + Fore.CYAN + "11" + Fore.RED + "]" + Fore.WHITE + " Cloudflare Bypass")
		print (Fore.RED + "[" + Fore.CYAN + "12" + Fore.RED + "]" + Fore.WHITE + " Wordpress Dir Finder")
		print (Fore.RED + "[" + Fore.CYAN + "13" + Fore.RED + "]" + Fore.WHITE + " Reverse DNS Lookup")
		print (Fore.RED + "[" + Fore.CYAN + "14" + Fore.RED + "]" + Fore.WHITE + " Find upload path")
		print (Fore.RED + "[" + Fore.CYAN + "15" + Fore.RED + "]" + Fore.WHITE + " Find Shells")
		print (Fore.RED + "[" + Fore.CYAN + "16" + Fore.RED + "]" + Fore.WHITE + " Website Status")
		print (Fore.RED + "[" + Fore.CYAN + "17" + Fore.RED + "]" + Fore.WHITE + " Spider: Extract Links")
		print (Fore.RED + "[" + Fore.CYAN + "18" + Fore.RED + "]" + Fore.WHITE + " Technology Discovery")
		print (Fore.RED + "[" + Fore.CYAN + "19" + Fore.RED + "]" + Fore.WHITE + " Find Backup files")
		print (Fore.RED + "<" + Fore.CYAN +"--" + Fore.WHITE + " Back")


		print ("\n")
		
		webinfocolor = Fore.RED + "(" + Fore.CYAN + "Web Information" + Fore.RED + ")"
		prompt = input(Fore.WHITE + "IGF~" + webinfocolor + Fore.WHITE + "# ")
		if prompt == "1":
			ask = input("HTTP or HTTPS? ")
			if ask == "HTTPS":
				grabthebannerssl()
			else:
				grabthebanner()
		if prompt == "2":
			dirbrute()
		if prompt == "3":
			subrute()
		if prompt == "4":
			ipaddressresolv()
		if prompt == "5":
			getrobot()
		if prompt == "6":
			whoistool()
		if prompt == "7":
			gethead()
		if prompt == "8":
			getoptions()
		if prompt == "9":
			dnslookup()
		if prompt == "10":
			adminpanelfind()
		if prompt == "11":
			cloudflarebypass()
		if prompt == "12":
			wordpresscheck()
		if prompt == "13":
			reversednslookup()
		if prompt == "14":
			finduploads()
		if prompt == "15":
			shellfinder()
		if prompt == "16":
			checksite()
		if prompt == "17":
			spider()
		if prompt == "18":
			techdiscovery()
		if prompt == "19":
			findbackup()
		if prompt == "back":
			start()
		if prompt == "exit":
			exit()

def start():
	while True:
		print (Fore.RED + banner)
		print (Fore.RED + "\033[0;0mAuthor  : c0deninja".rjust(30, "="))
		print (Fore.RED + "\033[0;0mDiscord : gotr00t?".rjust(29, "=")+ "\n\n")

		print (Fore.RED + "[ " + Fore.CYAN + "IGF Menu" + Fore.RED + " ]" + "\n")

		print (Fore.RED + "[" + Fore.CYAN + "01" + Fore.RED + "] " + Fore.WHITE + "Website Information")
		print (Fore.RED + "[" + Fore.CYAN + "02" + Fore.RED + "] " + Fore.WHITE + "IP Information")
		print (Fore.RED + "[" + Fore.CYAN + "03" + Fore.RED + "] " + Fore.WHITE + "Miscellaneous")
		print (Fore.RED + "[" + Fore.CYAN + "X" + Fore.RED + "] " + Fore.WHITE +  " EXIT")

		print ("\n")
		prompt = input(Fore.WHITE + "IGF~#: ").lower()
		if prompt == "01":
			webinfo()
		if prompt == "02":
			ipinformation()
		if prompt == "03":
			miscellaneous()
		if "exit" or "x" in prompt.lower():
			sys.exit(0)

if __name__ == "__main__":
	start()
