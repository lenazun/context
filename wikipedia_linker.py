

import urllib
import urllib2
import simplejson


#MEMECACHE
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)



def get_wiki_data(title, target_lang, source_lang):
	""" Gets wiki language data from the wikipedia API """



	#creates a unique id for memcache
	title_with_lang = (title.replace(" ", "_") + "_" + target_lang).encode('utf8')

	#searches the wiki ID in memcache
	exists = mc.get(title_with_lang)

	if exists:
		print "I'm in your memcache"
		return mc.get(title_with_lang)

	else:
		print "BRB going to wikipedia to find this"

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
			print "."
			data = urllib.urlencode(values)  
			req = urllib2.Request(URL, data)
			response = urllib2.urlopen(req)
			json_file = response.read()            
			json_file = simplejson.loads(json_file)

			return json_file

		#get json lang file based on the values above
		lang_json = get_json(langvalues)

		#gets the wiki id from the json file
		wiki_id = str([key for key in lang_json['query']['pages'].keys()])
		wiki_id = wiki_id.strip("['']")

		#if the article doesn't exist in English, returns None
		if '-1' in lang_json['query']['pages']:
			return None

		else:
			#if the article has language links, extracts the equivalent titles
			if 'langlinks' in lang_json['query']['pages'][wiki_id]:

				lang_dict = lang_json['query']['pages'][wiki_id]['langlinks'][0]
				langcode = lang_dict['lang']
				equivalent = lang_dict['*']

			else:
				langcode = False
				equivalent = " "

			#if the image json contains an image, it sets it as thumbnail
			image_json = get_json(imagevalues)
			if 'thumbnail' in image_json['query']['pages'][wiki_id]:
				thumbnail = image_json['query']['pages'][wiki_id]['thumbnail']['source']

			else:
				thumbnail = False	

		#creates a dictionary for the item 
		item_dict = {}
		item_dict[wiki_id] = {'title': title, 'targetlang': langcode, 'targetwiki' : equivalent, 'thumbnail': thumbnail }
		
		#adds the item to memcache
		mc.set(title_with_lang, item_dict)

		return item_dict




def get_entity_info(namelist, target_lang, source_lang):
	""" Creates a dictionary with the individual entity dictionaries"""

	entity_dict = {}

	for i in namelist:
		data = get_wiki_data(i, target_lang, source_lang)

		if data:
			entity_dict.update(data)

	return  entity_dict




def main():
	#namelist = ["New York", "Barack Obama", "Earthquake", "President Obama", "North Carolina Board of Elections", "Amsterdam", "The Bible"]
	pass
	
if __name__ == "__main__":
    main()



