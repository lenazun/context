import geopy
from geopy.geocoders import Nominatim

#MEMECACHE
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def geocode(place_list):

	#set a geocoder
	geolocator = Nominatim()

	#reformat the placelist to work ask keys for memcache and google maps
	place_list = [i.encode('utf8') for i in place_list ]
	keylist = [i.replace(" ", "_") for i in place_list]

	keyplace = dict(zip(keylist, place_list))

	for key, value in keyplace.iteritems():

		exists = mc.get(key)

		if exists:
			print "I exist"
			keyplace[key] = mc.get(key)			

		else:
			print "I don't exist yet"
			name = value
			loc = geolocator.geocode(value)
			lat = loc.latitude
			lon = loc.longitude

			itemdict = {}
			itemdict = {'name': name, 'lat': lat, 'lon': lon}

			keyplace[key] = itemdict
			mc.set(key, itemdict)


	return keyplace


def main():
	""" Tests """

	place_list = [u'New Orleans', u'Iowa', u'Colorado', u'North Carolina', u'Asheville', u'New York', u'Costa Rica']
	print geocode(place_list)
	
if __name__ == "__main__":
    main()