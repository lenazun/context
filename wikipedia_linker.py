
import json
import urllib
import urllib2
import simplejson
from pprint import pprint



def get_wiki_data(title, target_lang):

	url = 'http://en.wikipedia.org/w/api.php'

	values = {'action' : 'query',
	          'prop' : 'langlinks',
	          'lllang': target_lang,
	          'titles' : title,
	          'redirects': '',
	          'format' : 'json'}

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()

	json = simplejson.loads(json)

	wiki_id = str([key for key in json['query']['pages'].keys()])
	wiki_id = wiki_id.strip("['']")	

	if 'langlinks' in json['query']['pages'][wiki_id]:
		lang_dict = json['query']['pages'][wiki_id]['langlinks'][0]

		langcode = lang_dict['lang']
		equivalent = lang_dict['*']

		return langcode, equivalent, wiki_id

	else:
		return False
	 

def main():
	namelist = ["New York", "Barack Obama", "Earthquake", "President Obama", "North Carolina Board of Elections"]
	
	for i in namelist:
		print get_wiki_data(i, "fr")



if __name__ == "__main__":
    main()