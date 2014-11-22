import file_reader
import nltk
from nltk.tag.stanford import NERTagger
from nltk.tag.stanford import POSTagger

def spanish_pos(text):
	""" Parts of speech tagger for Spanish """

	text = text.encode('utf8')

	st = POSTagger('/Users/Lena/src/context/stanford-ner-2014-10-26/edu/stanford/nlp/models/pos-tagger/spanish/spanish.tagger', 
				'/usr/share/stanford-postagger/stanford-postagger.jar', 'utf8')

	pos_tagged = st.tag(text.split())

	return pos_tagged  


def spanish_ner(text):
	""" Moves the list of words through the NER tagger"""

	text = text.encode('utf8')


	st = NERTagger('/Users/Lena/src/context/stanford-ner-2014-10-26/edu/stanford/nlp/models/ner/spanish.ancora.distsim.s512.crf.ser.gz',
                '/Users/Lena/src/context/stanford-ner-2014-10-26/stanford-postagger.jar', 'utf8')  #NOT WORKING

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

	print organizations, locations, people
	return organizations, locations, people



def main():
	""" Tests """
	text = file_reader.read_file('spanish_sample.txt')
	#tokens = german_tokenize(text)
	#print tokens
	#print postprocess(spanish_ner(text))
	print spanish_pos(text)
	

	
if __name__ == "__main__":
    main()