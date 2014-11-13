import os 
import urllib
import tempfile
import csv
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import nltk

from clean_html  import safe_html, plaintext 
# an open soure html sanitizer I found here http://chase-seibert.github.io/blog/2011/01/28/sanitize-html-with-beautiful-soup.html


UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER ='static/downloads'

def read_file(input_file):
	""" Open and read a text file """
	text = open(input_file)
	raw = text.read()
	decoded = raw.decode('utf8').encode('ascii', 'replace')

	text = decoded

	return text

 
def read_url(url):
	""" Open and read a URL """
	html = urllib.urlopen(url).read().decode('utf8')
	#raw = BeautifulSoup(html)
	return html


def clean_html(raw):
	""" Clean HTML tags returns only text"""


	text = safe_html(raw)

	# for script in raw(["script", "style"]):
	# 	script.extract()

	# pretext = raw.get_text()

	# #gets rid of blank lines and spaces
	# lines = (line.strip() for line in pretext.splitlines())
	# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# text = '\n'.join(chunk for chunk in chunks if chunk)

	return text


def write_file(text):
	""" Write a file with clean plain text in a temporary file """

	tempfile.tempdir = UPLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')

	text = text.encode('ascii', 'replace').decode('utf8')

	with open(temp_file.name, 'w') as temp:
		temp.write(text)

	pathparts = (temp.name).split('/')
	path = "/".join(pathparts[5:])

	#returns the temporary file path
	return path


def read_url_all(url):
		""" Write a file with clean URL input"""

		return write_file(clean_html(read_url(url)))

def write_csv_file(dictionary):
	
	tempfile.tempdir = DOWNLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False)

	with open(temp_file.name, 'wb') as temp:
		w = csv.writer(temp)
		w.writerow(['wiki_id', 'title', 'targetlang', 'equiv_title', 'thumbnail'])
		for key, value in dictionary.iteritems():
			w.writerow([i.encode('ascii', 'replace').decode('utf8') for i in value])
			
	return temp.name


def main():
	""" Tests """
	
	#print read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	#print read_file('sample.txt')
	#output = read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	#print clean_html(output)
	#dictionary = {'New York': ['8210131', 'New York', 'fr', u'\xc9tat de New York', 'http://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_New_York.svg/100px-Flag_of_New_York.svg.png'], 'Barack Obama': ['534366', 'Barack Obama', 'fr', 'Barack Obama', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/80px-President_Barack_Obama.jpg'], 'Earthquake': ['10106', 'Earthquake', 'fr', u'S\xe9isme', 'http://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Quake_epicenters_1963-98.png/100px-Quake_epicenters_1963-98.png'], 'President Obama': ['534366', 'President Obama', 'fr', 'Barack Obama', 'http://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/80px-President_Barack_Obama.jpg']}
	#write_csv_file(dictionary)

if __name__ == "__main__":
    main()