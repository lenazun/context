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
#	decoded = raw.decode('utf8').encode('ascii', 'replace')
	decoded = raw.decode('utf8')

	text = decoded

	return text

 
def read_url(url):
	""" Open and read a URL """
	html = urllib.urlopen(url).read().decode('utf8')
	#raw = BeautifulSoup(html)
	return html


def clean_html(raw):
	""" Clean HTML tags returns only text"""


	text = plaintext(raw)

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
	
	wikiURL = 'http://en.wikipedia.org/wiki?curid='
	tempfile.tempdir = DOWNLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

	with open(temp_file.name, 'wb') as temp:
		w = csv.writer(temp)
		w.writerow(['wiki_id', 'title', 'targetlang', 'equiv_title', 'wiki_url', 'wiki_image'])
		for key, value in dictionary.iteritems():
			w.writerow([(key).encode('utf8'), 
						(value['title']).encode('utf8'), 
						(value['targetlang']).encode('utf8'), 
						(value['targetwiki']).encode('utf8'),
						(wikiURL + key),
						(value['thumbnail'])])

	pathparts = (temp.name).split('/')
	path = "/".join(pathparts[5:])

	return path



def main():
	""" Tests """
	
	#print read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	print read_file('sample.txt')
	#output = read_url('http://www.newyorker.com/culture/cultural-comment/pills-difficult-birth')
	#print clean_html(output)
	#dictionary = {'3390': {'targetlang': 'fr', 'targetwiki': 'Bible', 'title': 'The Bible'}, '844': {'targetlang': 'fr', 'targetwiki': 'Amsterdam', 'title': 'Amsterdam'}, '10106': {'targetlang': 'fr', 'targetwiki': u'S\xe9isme', 'title': 'Earthquake'}, '8210131': {'targetlang': 'fr', 'targetwiki': u'\xc9tat de New York', 'title': 'New York'}, '534366': {'targetlang': 'fr', 'targetwiki': 'Barack Obama', 'title': 'Barack Obama'}}
	#write_csv_file(dictionary)

if __name__ == "__main__":
    main()