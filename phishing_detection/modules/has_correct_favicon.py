from bs4 import BeautifulSoup
import re
import requests
from urlparse import *

def has_correct_favicon(url, resp):
	status = 'U'
	mod = 'favicon'
	parse = urlparse(url)

	try:
		current_page = BeautifulSoup(resp.text,'lxml')
		if parse.netloc.find("www.") != -1:
			string = parse.netloc.replace("www.","")
		else:
			string = parse.netloc
		for rel in current_page.find_all('link'):
			if rel.get('href').find("favicon") != -1:
				if rel.get('href').find("http") != -1:
					answer = urlparse(rel.get('href')).netloc
					if(answer != string):
						status = "P"
						if(answer == ""):
							if urlparse(rel.get('href')).path.find("favicon.ico") != -1:
								status = "S"
								break
					if(answer == string):
						status = "S"
						break
				else:
					path = rel.get('href').split("/")
					for i in path:
						if bool(re.match('favicon(_)?(\d*).ico',i)):
							status = "S"
							break
					
	except requests.ConnectionError, e:
		status = "U"
	except requests.exceptions.Timeout:
		status = "U"

	return status, mod
