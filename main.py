import urllib.request
import json
import math
import sys
import os

try:
	from bs4 import BeautifulSoup
except:
	print("This program needs BeautifulSoup4 to run. Enter your password to install it.")
	os.system('sudo pip install BeautifulSoup4')
	from bs4 import BeautifulSoup

try:
	movname = input('What movie do you want to watch?: ')
	if len(movname.split(' ')) > 1:
		movname = "%20".join(movname.split(' '))
	movpage = BeautifulSoup(urllib.request.urlopen('http://google.com/movies?q='+movname).read(),"html.parser")
	homeaddr = input("Please enter address of current location (eg 1234 Blah Way): ")
	rawtheaters = movpage.find_all("div", {"class":"theater"})
	rawaddrs = []
	for theater in rawtheaters:
		tempsoup = BeautifulSoup(str(theater),"html.parser")
		temp2soup = BeautifulSoup(str(tempsoup.find("div")),"html.parser")
		rawaddrs.append(temp2soup.find("div", {"class" : "address"}).text)
	dist = []
	for addr in rawaddrs:
		resp = urllib.request.urlopen('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+ "+".join(homeaddr.split(' ')) +'&destinations='+"+".join(addr.split(' '))+'&mode=driving&language=en&key=AIzaSyBLKYTC9RFRs8AieO_Ue1TrRUyLOAff9-M').read()
		str_resp = resp.decode('utf-8')
		dist.append(json.loads(str_resp)['rows'][0]['elements'][0]['duration']['value']/60)

	print("Theater closest to you: " +BeautifulSoup(str(rawtheaters[rawaddrs.index(str(rawaddrs[round(min(dist))]))]),"html.parser").find_all("div")[0].find_all("div")[0].find_all("div")[0].text+ ". This is located at "+str(rawaddrs[round(min(dist))])+". It will take you "+json.loads(str_resp)['rows'][0]['elements'][0]['duration']['text']+" to get there.")
	print("Showtimes at "+BeautifulSoup(str(rawtheaters[rawaddrs.index(str(rawaddrs[round(min(dist))]))]),"html.parser").find_all("div")[0].find_all("div")[0].find_all("div")[0].text+": ")
	timesoup = BeautifulSoup(str(rawtheaters[rawaddrs.index(str(rawaddrs[round(min(dist))]))]),"html.parser").find_all("div")[0]
	print(timesoup.find_all("div")[3].text)
except:
	print("One of the inputs was incorrect. Please re-run the program and try again.")
	sys.exit(1)
