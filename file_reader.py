#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import os 
import urllib
import tempfile
import csv


from clean_html  import safe_html, plaintext 
# an open soure html sanitizer here http://chase-seibert.github.io/blog/2011/01/28/sanitize-html-with-beautiful-soup.html


UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER ='static/downloads'



#### FILE READING ######


def read_file(input_file):
	""" Open and read a cleaned up simpletext file """

	text = open(input_file)
	raw = text.read()
#	decoded = raw.decode('utf8').encode('ascii', 'replace')
	decoded = raw.decode('utf8')

	#moves this through the html cleaner
	text = plaintext(decoded)

	return text


def read_file_pretty(input_file):
	""" Open and read a text file and preserve spaces for display """

	text = open(input_file)
	raw = text.readlines()
	decoded = [line.decode('utf8') for line in raw]
	lines = [line.strip() for line in decoded if line.strip() != '']
	lines = [("<p>" + line + "</p>") for line in lines]
	lines.insert(0, '<meta charset="UTF-8">')

	return lines

 
def read_url(url):
	""" Open and read a URL and return plain text """
	html = urllib.urlopen(url).read().decode('utf8')
	text = plaintext(html)
	lines = text.splitlines()
	lines = [line for line in lines if line.strip() != '']
	lines = [line for line in lines if line.startswith('<') == False]
	lines = [line for line in lines if ('{') not in line]

	print lines
 
	text ='\n'.join(line for line in lines)

	return text


def read_url_all(url):
		""" Write a file with clean URL input"""

		return write_file(read_url(url))


##### FILE WRITING #########


def write_file(text):
	""" Write a file with clean plain text in a temporary file """

	tempfile.tempdir = UPLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')

	text = text.encode('utf8')

	with open(temp_file.name, 'w') as temp:
		temp.write(text)

	pathparts = (temp.name).split('/')
	path = "/".join(pathparts[5:])

	#returns the temporary file path
	return path



def write_csv_file(dictionary):
	
	wikiURL = 'http://en.wikipedia.org/wiki?curid='
	tempfile.tempdir = DOWNLOAD_FOLDER
	temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')

	with open(temp_file.name, 'wb') as temp:
		w = csv.writer(temp)
		w.writerow(['wiki_id', 'title', 'targetlang', 'equiv_title', 'wiki_url'])
		try:
			for key, value in dictionary.iteritems():
				try:
					w.writerow([(key).encode('utf8'), 
								(value['title']).encode('utf8'), 
								(value['targetlang']).encode('utf8'), 
								(value['targetwiki']).encode('utf8'),
								(wikiURL + key)])
				except Exception:
					pass
		except Exception:
			pass

	pathparts = (temp.name).split('/')
	path = "/".join(pathparts[5:])

	return path



def main():
	""" Tests """
	
	#output = read_url('http://www.sfchronicle.com/bayarea/article/Throngs-of-fans-already-packing-Civic-Center-5860820.php')
	#print read_file_pretty('sample.txt')
	#output = read_url('http://www.newyorker.com/culture/cultural-comment/pills-difficult-birth')
	#print read_url_all('http://www.theguardian.com/world/2014/nov/14/putin-russia-oil-price-collapse-sanctions-g20')
	read_url('http://internacional.elpais.com/internacional/2014/11/28/actualidad/1417195929_767998.html')
	#dictionary = {'3390': {'targetlang': 'fr', 'targetwiki': 'Bible', 'title': 'The Bible'}, '844': {'targetlang': 'fr', 'targetwiki': 'Amsterdam', 'title': 'Amsterdam'}, '10106': {'targetlang': 'fr', 'targetwiki': u'S\xe9isme', 'title': 'Earthquake'}, '8210131': {'targetlang': 'fr', 'targetwiki': u'\xc9tat de New York', 'title': 'New York'}, '534366': {'targetlang': 'fr', 'targetwiki': 'Barack Obama', 'title': 'Barack Obama'}}
	#write_csv_file(dictionary)


if __name__ == "__main__":
    main()