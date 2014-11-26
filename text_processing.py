from operator import itemgetter

import file_reader

import nltk, re, pprint
import ner


def preprocess(text):
	""" Quick and dirty text preprocessing, tokenization, tagging"""

	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences] 
	tagged = [nltk.pos_tag(sent) for sent in sentences]


	all_tagged_words = []
	[[all_tagged_words.append(wordpair) for wordpair in i] for i in tagged]

	#returns a list of tuples (word, pos)
	return all_tagged_words


def nouns_only(all_tagged_words):
	""" Creates a list of nouns only ordered by their number of appearances in the text"""

	nouns_dict = {}

	for wordpair in all_tagged_words:
		if wordpair[1] in ('NN','NNS') and len(wordpair[0]) > 2:
			nouns_dict[wordpair] = nouns_dict.get(wordpair, 0) + 1


	nouns_list = [(key[0], value) for key, value in nouns_dict.items()]

	#Alpha sort
	nouns_list.sort()
	#Sorts by number of appearances
	sorted_nouns = sorted(nouns_list, key=itemgetter(1), reverse = True)

	top20 = [word[0] for word in sorted_nouns[:20]]

	return top20



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
	#print nouns_only(prepro)
	#print dictionary

	
if __name__ == "__main__":
    main()
