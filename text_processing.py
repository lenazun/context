import file_reader

import nltk, re, pprint
import ner


# loads custom stopwords
stopwords = [w.strip() for w in open('stopwords.txt').read().split('\n') if w != '']


def preprocess(text):
	""" Quick and dirty text preprocessing, tokenization, tagging"""

	text = text.decode('utf8').encode('ascii', 'replace')
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences] 
	tagged = [nltk.pos_tag(sent) for sent in sentences]


	all_tagged_words = []
	[[all_tagged_words.append(wordpair) for wordpair in i] for i in tagged]

	#returns a list of tuples (word, pos)
	return all_tagged_words


def make_word_dict(all_tagged_words):
	""" Makes a dictionary out of the whole word list"""	

	main_dict = dict(all_tagged_words)
	return main_dict



def nouns_only(main_dict):
	""" Creates a dictionary of nouns only """

	nouns_dict = {key: value for key, value in main_dict.items() 
             if value in ('NN','NNS') and len(key) > 2 }

	return  list(nouns_dict.keys())


def ner_tagger(text):    
	""" Processes and tags text using the Stanford NER tagger"""

	tagger = ner.SocketNER(host='localhost', port=8080)

	entities = tagger.get_entities(text)

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


def single_set(text):
	""" Makes all entities a single list so they can be highlighted"""

	organizations, locations, people = ner_tagger(text)

	set1 = []

	[set1.append(i.encode('utf8')) for i in organizations]
	[set1.append(i.encode('utf8')) for i in locations]
	[set1.append(i.encode('utf8')) for i in people]

	return set1


def most_common_pos(tagged_words):
	""" Return the most common parts of speech in a list of tagged words"""

	tag_fd = nltk.FreqDist(tag for (word, tag) in tagged_words)
	return tag_fd.most_common()


def main():
	""" Tests """

	text = file_reader.read_file('sample.txt')
	#prepro = preprocess(text)
	#print prepro
	#print most_common_pos(prepro)
	ner = ner_tagger(text)
	print ner
	#dictionary = make_word_dict(prepro)
	#print nouns_only(dictionary)
	#print dictionary

	
if __name__ == "__main__":
    main()
