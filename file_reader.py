import nltk
import os 
import urllib
from bs4 import BeautifulSoup

#######################################
### Open and read a local txt file ####
########################################

def read_file(input_file):
    text = open(input_file, 'rU')
    raw = text.read()
    #corpus = passage.split()

    return raw

###########################
### Open and read a URL ###
###########################
 
def read_url(url):
	html = urllib.urlopen(url).read().decode('utf8')
	raw = BeautifulSoup(html)

	return raw

#########################################
### Clean HTML tags returns only text ###
#########################################

def clean_html(raw):

	for script in raw(["script", "style"]):
		script.extract()

	pretext = raw.get_text()

	#gets rid of blank lines and spaces
	lines = (line.strip() for line in pretext.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)

	return text


def main():

	#read_file('sample.txt')
	output = read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	print clean_html(output)

if __name__ == "__main__":
    main()