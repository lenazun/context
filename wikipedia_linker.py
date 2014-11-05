
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

	if '-1' in json['query']['pages']:
		return "NA"

	elif 'langlinks' in json['query']['pages'][wiki_id]:

		lang_dict = json['query']['pages'][wiki_id]['langlinks'][0]
		langcode = lang_dict['lang']
		equivalent = lang_dict['*']

		return wiki_id, title, langcode, equivalent

	else:
		return False
	 

def get_entity_info(namelist, target_lang):
	
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



if __name__ == "__main__":
    main()