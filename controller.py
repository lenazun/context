import os

from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug import secure_filename

import file_reader
import text_processing
import wikipedia_linker


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = frozenset(['txt'])

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567' #Fake key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_file_allowed(filename):
	"""Is this file allowed?

	    >>> allowed_file('foo.txt')
	    True

	    >>> allowed_file('foo.jpg')
	    False
	"""
	return '.' in filename and \
	filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():
	""" Uploads files or converts URLs into simple text files """

	#saves an uploaded text file to the uploads folder
	if request.files['filename']:
		file_ = request.files['filename']
		if file_ and is_file_allowed(file_.filename):
			filename = secure_filename(file_.filename)
			file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			session['filename'] = filename
			session['filepath'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			
			return redirect(url_for('basic_process'))
		else:
			flash ("Make sure you're uploading a %s file" % [i for i in ALLOWED_EXTENSIONS])
			return render_template("upload.html")

	#grabs a URL and saves it as a temporary file in the uploads folder
	elif request.form.get("url"):
		url = request.form.get('url')
		newfile = file_reader.read_url_all(url)

		session['filename'] = 'temp'
		session['filepath'] = newfile
		
		return redirect(url_for('basic_process'))

	else:
		flash ("Enter a source file or URL")
		return render_template("upload.html")


@app.route('/basic_process')
def basic_process():
	filepath = session['filepath']

	#reads the file into memory
	text = file_reader.read_file(filepath)

	#simple word count
	simplecount = len(text)

	return render_template("basic_process.html", simple=simplecount)



@app.route('/entities', methods=["GET"])
def entities():
	""" Gets entities from text and grabs wikipedia information"""

	filepath = session['filepath']
	target_lang = request.args.get("target_lang")

	#applies the NER tags to the text and extract nouns from tagged words
	text = file_reader.read_file(filepath)
	organizations, locations, people = text_processing.ner_tagger(text)
	nouns = text_processing.nouns_only(text_processing.make_word_dict(text_processing.preprocess(text)))

	#generates dictionaries for the entities and their wiki data
	orglist = wikipedia_linker.get_entity_info(organizations, target_lang)
	loclist = wikipedia_linker.get_entity_info(locations, target_lang)
	peoplelist = wikipedia_linker.get_entity_info(people, target_lang)
	nounlist = wikipedia_linker.get_entity_info(nouns, target_lang)


	return render_template("entities.html", 
		entities=entities, 
		organizations=orglist, 
		locations=loclist, 
		people=peoplelist, 
		nouns=nounlist, 
		target_lang=target_lang)


if __name__ == "__main__":
    app.run(debug = True)