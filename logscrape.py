import urllib2
import re
import sys
from urllib2 import Request
from bs4 import BeautifulSoup

class Gamelogs():

	def __init__(self):

		#the base bage that has all boxscore links
		self.teamPageSoup = BeautifulSoup(urllib2.urlopen('http://www.sports-reference.com/cbb/schools/' + school + '/2015-gamelogs.html'))
		#use regex to only find links with score data		
		self.statusPageLinks = self.teamPageSoup.findAll(href=re.compile("boxscores"));

def outputLinks(school):
	gamelogs = Gamelogs()
	#open a new file to store the output
	fo = open(school + '.txt',"w")
	for s in gamelogs.statusPageLinks:
		#make the list a string so it can be sliced
		string = str(s)
		#remove extra link formatting
		string = string[9:]
		string = string[:-16]
		#write output, restoring initial part of link		
		fo.write('http://www.sports-reference.com/cbb/schools/' + school + string + '\n')
	fo.close

if __name__ == '__main__':
	#for each school as a commandline argument	
	for arg in sys.argv[1:]:
		school = arg	
		outputLinks(school)
	
