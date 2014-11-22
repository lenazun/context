import file_reader
import nltk
from nltk.tag.stanford import NERTagger


# def german_tokenize(text):
# 	"""turns text into a list of tokens"""

# 	tokens = nltk.word_tokenize(text)

# 	return tokens


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



def main():
	""" Tests """
	text = file_reader.read_file('german_sample.txt')
	#tokens = german_tokenize(text)
	#print tokens
	print postprocess(german_ner(text))
	

	
if __name__ == "__main__":
    main()