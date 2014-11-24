
import json
import urllib
import urllib2
import simplejson
from pprint import pprint


#MEMECACHE
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)



def get_wiki_data(title, target_lang, source_lang):
	""" Gets wiki language data from the wikipedia API """

	URL = 'http://' +  source_lang + '.wikipedia.org/w/api.php'

	langvalues = {'action' : 'query',
			'prop' : 'langlinks',
			'lllang': target_lang,
			'titles' : title.encode('utf8'),
			'redirects': '',
			'format' : 'json'}

	imagevalues = {'action' : 'query',
	          'prop' : 'pageimages',
	          'titles' : title.encode('utf8'),
	          'redirects': '',
	          'format' : 'json', 
	          'pithumbsize': '500'}

	def get_json(values):
		data = urllib.urlencode(values)  
		req = urllib2.Request(URL, data)
		response = urllib2.urlopen(req)
		json_file = response.read()            
		json_file = simplejson.loads(json_file)

		return json_file

	lang_json = get_json(langvalues)
	image_json = get_json(imagevalues)


	#gets the wiki id from the json file
	wiki_id = str([key for key in lang_json['query']['pages'].keys()])
	wiki_id = wiki_id.strip("['']")

	#creates a unique id for memcache
	id_with_lang = (wiki_id + "_" + target_lang).encode('utf8')

	#if the article doesn't exist in English, returns None
	if '-1' in lang_json['query']['pages']:
		return None

	else:
		#searches the wiki ID in memcache
		exists = mc.get(id_with_lang)

		if exists:
			print "I'm in your memcache"
			return mc.get(id_with_lang)

		else:
			#if the article has language links, extracts the equivalent titles
			if 'langlinks' in lang_json['query']['pages'][wiki_id]:

				lang_dict = lang_json['query']['pages'][wiki_id]['langlinks'][0]
				langcode = lang_dict['lang']
				equivalent = lang_dict['*']

				if 'thumbnail' in image_json['query']['pages'][wiki_id]:
					thumbnail = image_json['query']['pages'][wiki_id]['thumbnail']['source']
				else:
					thumbnail = False

				item_dict = {}
				item_dict[wiki_id] = {'title': title, 'targetlang': langcode, 'targetwiki' : equivalent, 'thumbnail': thumbnail }
				#adds it to memcache
				mc.set(id_with_lang, item_dict)

				print "BRB Im running to wikipedia to find this"
				return item_dict

			else:
				return False




def get_entity_info(namelist, target_lang, source_lang):
	""" Creates a dictionary with all entities in a list and their data from wikipedia"""

	entity_dict = {}

	for i in namelist:
		data = get_wiki_data(i, target_lang, source_lang)

		if data:
			entity_dict.update(data)

	return  entity_dict


# def twitter_search_query(entity_dict):
# 	"""Creates a twitter search query separated by spaces and OR """

# 	names = [key for key in entity_dict.keys()]
# 	words = [i.replace(' ', '%20') for i in names]
# 	query = "%20OR%20".join(words)

# 	return query



def main():
	namelist = ["New York", "Barack Obama", "Earthquake", "President Obama", "North Carolina Board of Elections", "Amsterdam", "The Bible"]
	#namelist = [u'Instituto', u'Sociales', u'Brasil', u'Bolsa', u'Data', u'Partido', u'Ipea', u'Pol\xedticas', u'Folha', u'Dilma', u'del', u'Familia', u'Gobierno', u'Popular', u'-LRB-', u'Estado', u'Rousseff']
	
	print get_entity_info(namelist, 'fr', 'es')

	# FIXME : learn about assert



if __name__ == "__main__":
    main()