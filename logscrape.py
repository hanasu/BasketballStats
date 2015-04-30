import re
import sys
import os
import urllib2
from bs4 import BeautifulSoup

class Gamelogs():

	def __init__(self):

		#the base bage that has all boxscore links
		self.teamPageSoup = BeautifulSoup(urllib2.urlopen('http://www.sports-reference.com/cbb/schools/' + school + '/2015-gamelogs.html'))
		#use regex to only find links with score data		
		self.statusPageLinks = self.teamPageSoup.findAll(href=re.compile("boxscores"));

def scoredata(links, school):
	#for each link in the school's season	
	for filename in links:
		print filename
		gameSoup = BeautifulSoup(urllib2.urlopen(filename))
		#remove extra link formatting to get just filename alone
		filename = filename[38+len(school):]
		#create a list that will hold the box score data only	
		output = gameSoup.findAll(class_="sortable")
		outputDirectory = '/home/hanasu/Desktop/NCAABBallData/' + school
		#check if school directory exists, if not make it
		if not (os.path.exists(outputDirectory)): 
			os.makedirs(outputDirectory)
		#conjoin the path with the filename for all OS versions	
		filename = os.path.join(outputDirectory, filename)
		#open a local file with that filename to store the results
		fo = open(filename,"w")
		#write it line by line to the file that was just opened	
		for o in output:
			fo.write(str(o) + '\n')
		fo.close
	
def getlinks(school):
	gamelogs = Gamelogs()
	#remove extraneous links
	gamelogs.statusPageLinks = gamelogs.statusPageLinks[2:]
	#create the list that will hold each school's seasonlong boxscores
	boxlinks = list()
	for s in gamelogs.statusPageLinks:
		#make the list element a string so it can be sliced
		string = str(s)
		#remove extra link formatting
		string = string[9:]
		string = string[:-16]
		#create the full list of games per school
		boxlinks.insert(0, 'http://www.sports-reference.com' + string)
	scoredata(boxlinks, school)		

if __name__ == '__main__':
	#for each school as a commandline argument	
	for arg in sys.argv[1:]:
		school = arg	
		getlinks(school)
