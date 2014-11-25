from operator import itemgetter

import file_reader
import nltk
from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import POSTagger


def german_pos(text):
	""" Parts of speech tagger for Spanish """
	
	text = text.encode('utf8')

	st = POSTagger('/Users/Lena/src/context/stanford-postagger/models/german-fast.tagger', 
				'/Users/Lena/src/context/stanford-postagger/stanford-postagger.jar', 'utf8')

	pos_tagged = st.tag(text.split())

	return pos_tagged  


def german_nouns(pos_tagged):
	""" Creates a list of nouns only ordered by their number of appearances in the text"""

	nouns_dict = {}

	for wordpair in pos_tagged[0]:
		if wordpair[1] in ('NN', 'NNS') and len(wordpair[0]) > 2:
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

	exclude = postprocess(german_ner(text))

	singlelist = [[x for x in i] for i in exclude]

	
	cleanlist = set(allnouns).difference(singlelist[0])
	cleanlist = list(cleanlist)

	return cleanlist[:20]


def german_ner(text):
	""" Moves the list of words through the NER tagger"""

	text = text.encode('utf8')  
	#print text
	#print text.split()


	st = NERTagger('/Users/Lena/src/context/stanford-ner-2014-10-26/classifiers/german/dewac_175m_600.crf.ser.gz',
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
			if 'I-PER' in wordpair:
				PERSON.append(wordpair[0])
			elif 'I-LOC' in wordpair:
				LOCATION.append(wordpair[0])
			elif 'I-ORG' in wordpair:
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

	return organizations, locations, people

def ner(text):
	return postprocess(german_ner(text))

def pos(text):
	return exclude_entities(german_nouns(german_pos(text)), text)



def main():
	""" Tests """
	text = file_reader.read_file('german_sample.txt')
	#tokens = german_tokenize(text)
	#print tokens
	#print postprocess(german_ner(text))
	print exclude_entities(german_nouns(german_pos(text)), text)

	
if __name__ == "__main__":
    main()