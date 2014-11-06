
import json
import urllib
import urllib2
import simplejson
from pprint import pprint

URL = 'http://en.wikipedia.org/w/api.php'

def get_wiki_data(title, target_lang):
	""" Gets wiki language data from the wikipedia API """

	langvalues = {'action' : 'query',
			'prop' : 'langlinks',
			'lllang': target_lang,
			'titles' : title,
			'redirects': '',
			'format' : 'json'}

	data = urllib.urlencode(langvalues)
	req = urllib2.Request(URL, data)
	response = urllib2.urlopen(req)
	json_file = response.read()            
	json_file = simplejson.loads(json_file)

	#gets the wiki id from the json file
	wiki_id = str([key for key in json_file['query']['pages'].keys()])
	wiki_id = wiki_id.strip("['']")	

	#if the article doesn't exist in English, returns NA
	if '-1' in json_file['query']['pages']:
		return "NA"

	#if the article has language links, extracts the equivalent titles
	elif 'langlinks' in json_file['query']['pages'][wiki_id]:

		lang_dict = json_file['query']['pages'][wiki_id]['langlinks'][0]
		langcode = lang_dict['lang']
		equivalent = lang_dict['*']

		#gets the thumbnail
		thumbnail = get_wiki_thumbnail(title)

		return [wiki_id, title, langcode, equivalent, thumbnail]

	else:
		return False

def get_wiki_thumbnail(title):
	""" Gets wiki thumbnail from the wikipedia API"""

	imgvalues = {'action' : 'query',
	          'prop' : 'pageimages',
	          'titles' : title,
	          'redirects': '',
	          'format' : 'json', 
	          'pithumbsize': '100'}

	data = urllib.urlencode(imgvalues)
	req = urllib2.Request(URL, data)
	response = urllib2.urlopen(req)
	json_file = response.read()
	json_file = simplejson.loads(json_file)

	#gets the wiki id from the json file
	wiki_id = str([key for key in json_file['query']['pages'].keys()])
	wiki_id = wiki_id.strip("['']")	

	#if the article doesn't exist in English, returns NA
	if '-1' in json_file['query']['pages']:
		return "NA"

	#if the article has a thumbnail, extracts the URL
	elif 'thumbnail' in json_file['query']['pages'][wiki_id]:

		thumbnail = json_file['query']['pages'][wiki_id]['thumbnail']['source']

		return thumbnail

	else:
		return False
	 

def get_entity_info(namelist, target_lang):
	""" Creates a dictionary with all entities in a list and their data from wikipedia"""
	
	entity_dict = {}

	for i in namelist:
		entity_dict[i] = get_wiki_data(i, target_lang)

	#Removes the values where there's no original wikipedia article
	entity_dict = {key: value for key, value in entity_dict.items() 
             if value is not "NA"}

	return  entity_dict


def main():
	namelist = ["New York", "Barack Obama", "Earthquake", "President Obama", "North Carolina Board of Elections"]
	
	print get_entity_info(namelist, 'fr')

	# FIXME : learn about assert



if __name__ == "__main__":
    main()