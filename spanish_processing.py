from operator import itemgetter

import file_reader
import nltk
from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import POSTagger

def spanish_pos(text):
	""" Parts of speech tagger for Spanish """
	
	text = text.encode('utf8')

	st = POSTagger('/Users/Lena/src/context/stanford-postagger/models/spanish-distsim.tagger', 
				'/Users/Lena/src/context/stanford-postagger/stanford-postagger.jar', 'utf8')

	pos_tagged = st.tag(text.split())

	return pos_tagged  


def spanish_nouns(pos_tagged):
	""" Creates a list of nouns only ordered by their number of appearances in the text"""

	nouns_dict = {}

	for wordpair in pos_tagged[0]:
		if wordpair[1] in ('np00000', 'nc0s000') and len(wordpair[0]) > 2:
			nouns_dict[wordpair] = nouns_dict.get(wordpair, 0) + 1


	nouns_list = [(key[0], value) for key, value in nouns_dict.items()]

	#Alpha sort
	nouns_list.sort()
	#Sorts by number of appearances
	sorted_nouns = sorted(nouns_list, key=itemgetter(1), reverse = True)

	allnouns = [word[0] for word in sorted_nouns]

	return allnouns


def exclude_entities(allnouns, text):
	""" exclude nouns already identified as entities """

	exclude = postprocess(spanish_ner(text))

	singlelist = [[x for x in i] for i in exclude]

	
	cleanlist = set(allnouns).difference(singlelist[0])
	cleanlist = list(cleanlist)

	return cleanlist[:20]



def spanish_ner(text):
	""" Moves the list of words through the NER tagger"""

	text = text.encode('utf8')


	st = NERTagger('/Users/Lena/src/context/stanford-ner-2014-10-26/edu/stanford/nlp/models/ner/spanish.ancora.distsim.s512.crf.ser.gz',
                '/Users/Lena/src/context/stanford-ner-2014-10-26/stanford-ner.jar', 'utf8') 

	tagged = st.tag(text.split())

	return tagged  


def postprocess(tagged):
	""" Takes the output of the NER tagger and returns it as dictionaries"""

	entities = {}

	PERSON = []
	LOCATION = []
	ORGANIZATION = []

	for sentence in tagged:
		for wordpair in sentence:
			if 'PERS' in wordpair:
				PERSON.append(wordpair[0])
			elif 'LUG' in wordpair:
				LOCATION.append(wordpair[0])
			elif 'ORG' in wordpair:
				ORGANIZATION.append(wordpair[0])

	entities['PERSON'] = PERSON
	entities['LOCATION'] = LOCATION
	entities['ORGANIZATION'] = ORGANIZATION


	if 'ORGANIZATION' in entities:
		organizations = set(entities['ORGANIZATION'])
	else:
		organizations = None

	if 'LOCATION' in entities:
		locations = set(entities['LOCATION'])
	else:
		locations = None

	if 'PERSON' in entities:
		people = set(entities['PERSON'])
	else:
		people = None

	#print organizations, locations, people
	return organizations, locations, people


def ner(text):
	return postprocess(spanish_ner(text))

def pos(text):
	return exclude_entities(spanish_nouns(spanish_pos(text)), text)



def main():
	""" Tests """
	text = file_reader.read_file('spanish_sample.txt')

	#print spanish_pos(text)
	
	print spanish_ner(text)
	

	
if __name__ == "__main__":
    main()