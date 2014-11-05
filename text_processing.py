

import file_reader
import nltk, re, pprint
import ner

####  loads custom stopwords
stopwords = [w.strip() for w in open('stopwords.txt').read().split('\n') if w != '']


###Quick and dirty text preprocessing: tokenization, tagging##

def preprocess(text):

	text = text.decode('utf8').encode('ascii', 'replace')
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences] 
	tagged = [nltk.pos_tag(sent) for sent in sentences]


	all_tagged_words = []
	for i in tagged:
		for wordpair in i:
			all_tagged_words.append(wordpair)

	#returns a list of tuples (word, pos)
	return all_tagged_words

def make_dict(all_tagged_words):	

	#makes a dictionary out of the whole word list
	main_dict = dict(all_tagged_words)
	return main_dict

#### NER tagger ####

def NERtagger(text):

	tagger = ner.SocketNER(host='localhost', port=8080)
	entitites = tagger.get_entities(text)

	return entitites

####  Most common POS

def most_common_pos(tagged_words):

	tag_fd = nltk.FreqDist(tag for (word, tag) in tagged_words)
	return tag_fd.most_common()


def main():

	text = file_reader.read_file('sample.txt')
	prepro = preprocess(text)
	#print most_common_pos(prepro)
	#ner = NERtagger(text)
	dictionary = make_dict(prepro)
	print len(dictionary.keys())

	
if __name__ == "__main__":
    main()
