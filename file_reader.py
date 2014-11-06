import os 
import urllib
import tempfile
from bs4 import BeautifulSoup

import nltk

UPLOAD_FOLDER = './uploads'

def read_file(input_file):
	""" Open and read a text file """
	text = open(input_file, 'rU')
	raw = text.read()
	text = raw.decode('utf8').encode('ascii', 'replace')

	return text

 
def read_url(url):
	""" Open and read a URL """
	html = urllib.urlopen(url).read().decode('utf8')
	raw = BeautifulSoup(html)

	return raw


def clean_html(raw):
	""" Clean HTML tags returns only text"""

	for script in raw(["script", "style"]):
		script.extract()

	pretext = raw.get_text()

	#gets rid of blank lines and spaces
	lines = (line.strip() for line in pretext.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)

	return text


def write_file(text):
	""" Write a file with clean plain text in a temporary file """

	tempfile.tempdir = UPLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False)

	text = text.encode('ascii', 'replace').decode('utf8')

	with open(temp_file.name, 'w') as temp:
		temp.write(text)

	#returns the temporary file path
	return temp.name


def read_url_all(url):
		""" Write a file with clean URL input"""

		return write_file(clean_html(read_url(url)))

def main():
	""" Tests """
	
	#read_file('sample.txt')
	output = read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	print write_file(clean_html(output))

if __name__ == "__main__":
    main()