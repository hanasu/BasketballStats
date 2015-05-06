import re
import sys
import os
import urllib2
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class Gamelogs():

	def __init__(self):

		#the base bage that has all boxscore links
		self.teamPageSoup = BeautifulSoup(urllib2.urlopen('http://www.sports-reference.com/cbb/schools/' + school + '/2015-gamelogs.html'))
		#use regex to only find links with score data		
		self.statusPageLinks = self.teamPageSoup.findAll(href=re.compile("boxscores"));
	
def getlinks(school):
	gamelogs = Gamelogs()
	#remove extraneous links
	gamelogs.statusPageLinks = gamelogs.statusPageLinks[2:]	
	#remove duplicate links	
	gamelogs.statusPageLinks = set(gamelogs.statusPageLinks) 
	#create the list that will hold each school's seasonlong boxscores
	boxlinks = list()
	for s in gamelogs.statusPageLinks:		
		#make the list element a string so it can be sliced
		string = str(s)
		#remove extra HTML link formatting
		string = string[24:]
		string = string[:-16]
		#create the full list of games per school
		boxlinks.insert(0, 'http://www.sports-reference.com/cbb/boxscores/' + string)
	scoredata(boxlinks, school)		

def scoredata(links, school):	
	outputDirectory = '/home/hanasu/Desktop/NCAABBallData/' + school
	#check if school directory exists, if not make it
	if not (os.path.exists(outputDirectory)): 
		os.makedirs(outputDirectory)
	#for each link in the school's season	
	for filename in links:
		gameSoup = BeautifulSoup(urllib2.urlopen(filename))
		#remove extra link formatting to get just filename alone
		localfile = filename[38+len(school):]
		#create a list that will hold the box score data only	
		output = gameSoup.findAll(class_="sortable")
		localfile = os.path.join(outputDirectory, localfile)
		fo = open(localfile, "w")
		fo.write(str(output))
		outputSoup = BeautifulSoup(str(output))
		test = open("/home/hanasu/Desktop/textonly.txt", "w")
		line = outputSoup.findAll(text = True)
		line = line[60:]
		for l in line:
			if not l.isspace():
				test.write(str(l) + ',')
		print "outputted"
	
if __name__ == '__main__':
	#for each school as a commandline argument	
	for arg in sys.argv[1:]:
		school = arg	
		getlinks(school)
