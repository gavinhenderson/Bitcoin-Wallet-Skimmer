#+441784605378 twilio no

from twilio.rest import Client
import urllib2, sys
import bs4 as bs
from random import randint
import time as t

def sendParseText(scrapeNo):
	# Your Account SID from twilio.com/console
	account_sid = "AC216d8bb08152b6f544b391268d155e30"
	# Your Auth Token from twilio.com/console
	auth_token  = "98aad9f144f807da09bf6f59b04435a6"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to="+447414525394", 
	    from_="+441228830063",
	    body="Parsed "+ str(scrapeNo)+" amount of wallets")

def sendWalletID(page, wallet, pKey):
	# Your Account SID from twilio.com/console
	account_sid = "AC216d8bb08152b6f544b391268d155e30"
	# Your Auth Token from twilio.com/console
	auth_token  = "98aad9f144f807da09bf6f59b04435a6"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to="+447414525394", 
	    from_="+441228830063",
	    body="Something interesting happened on page: "+str(page)+ "\n at wallet: "+ str(wallet) + "\n with private key: " + str(pKey))

def sendError():
	# Your Account SID from twilio.com/console
	account_sid = "AC216d8bb08152b6f544b391268d155e30"
	# Your Auth Token from twilio.com/console
	auth_token  = "98aad9f144f807da09bf6f59b04435a6"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to="+447414525394", 
	    from_="+441228830063",
	    body="Error was thrown, waiting for a few mins")

pageNo = 1
def ScrapeDir():
	pageNo = randint(0,904625697166532776746648320380374280100293470930272690489102837043110636675)
	site= str('http://directory.io/'+str(pageNo))
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(site,headers=hdr)
	page = urllib2.urlopen(req)
	soup = bs.BeautifulSoup(page,'html.parser')

	key = []

	keys = soup.find('pre',class_='keys')
	for span in keys.find_all('span'):
		counter = 0
		for links in span.find_all('a'):
			counter = counter + 1
			if(counter==2):
				#key.append(links.contents[0])
				key.append((span['id'],links.contents[0]))

	return key
	
def ScrapeWallet((key,address)):
	site= str("https://blockchain.info/address/"+str(address))
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request(site,headers=hdr)
	page = urllib2.urlopen(req)
	soup = bs.BeautifulSoup(page,'html.parser')

	transactions = soup.find("td", {"id": "n_transactions"}).contents[0]
	#print site
	#print transactions

	if(int(transactions)!=0):
		sendWalletID(pageNo, address, key)
	
scrapeCount = 0
while(True):
	try:
		addresses = ScrapeDir()
		for pair in addresses:
			ScrapeWallet(pair)
			scrapeCount = scrapeCount + 1
			if(scrapeCount%1000000==0):
				sendParseText(scrapeCount)
		print "Page skimmed"
	except:
		sendError()
		t.sleep(60)
