import urllib2
import re
import sys
from urllib2 import Request
from bs4 import BeautifulSoup

class Gamelogs():

	def __init__(self):

		self.teamPageSoup = BeautifulSoup(urllib2.urlopen('http://www.sports-reference.com/cbb/schools/' + school + '/2015-gamelogs.html'))
		self.statusPageLinks = self.teamPageSoup.findAll(href=re.compile("boxscores"));

def printLinks(school):
	gamelogs = Gamelogs()
	fo = open(school + '.txt',"w")
	fo.write('\n'.join(str(l) for l in gamelogs.statusPageLinks))
	fo.close

if __name__ == '__main__':
	for arg in sys.argv[1:]:
		school = arg	
		printLinks(school)
	
