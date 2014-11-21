import os
import json

from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug import secure_filename

import file_reader
import text_processing
import german_processing
import wikipedia_linker
import geocoding


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = frozenset(['txt'])

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567' #Fake key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_file_allowed(filename):
	"""Is this file allowed?"""

	return '.' in filename and \
	filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')
def index():

	session['target_lang'] = "es"
	return render_template("upload.html")



@app.route('/upload_file', methods=['POST'])
def upload_file():
	""" Uploads files or converts URLs into simple text files """
	print session

	#sets the source language
	session['source_lang'] = request.form.get('sourcelang')

	#saves an uploaded text file to the uploads folder
	if request.files['filename']:
		file_ = request.files['filename']
		if file_ and is_file_allowed(file_.filename):
			filename = secure_filename(file_.filename)
			file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			session['filename'] = filename
			session['filepath'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			
			return redirect(url_for('editor'))
		else:
			flash ("Make sure you're uploading a %s file" % [i for i in ALLOWED_EXTENSIONS])
			return render_template("upload.html")

	#grabs a URL and saves it as a temporary file in the uploads folder
	elif request.form.get("url"):
		url = request.form.get('url')
		newfile = file_reader.read_url_all(url)

		session['filename'] = 'temp'
		session['filepath'] = newfile
		
		return redirect(url_for('editor'))

	else:
		flash ("Enter a source file or URL")
		return render_template("upload.html")


@app.route('/editor', methods=["GET", "POST"])
def editor():
	""" Shows the main editor template"""

	filepath = session['filepath']
	target_lang = session['target_lang']


	return render_template("editor.html", 
		target_lang=target_lang,
		path= filepath)


@app.route('/set_target_lang', methods=["GET"])
def set_target_language():
	"""Changes the target language"""

	target_lang = request.args.get("target_lang")
	session['target_lang'] = target_lang

	return redirect(url_for('editor'))


@app.route('/named_entities')
def get_entities():
	"""Loads all entity names into a JSON for highlighting"""

	text = file_reader.read_file(session['filepath'])
	fullset = text_processing.single_set(text)
	return json.dumps(fullset)

# @app.route('/geocodes')
# def get_geocodes():

# 	text = file_reader.read_file(session['filepath'])
# 	organizations, locations, people = text_processing.ner_tagger(text)
# 	geocodes = geocoding.geocode(locations)
# 	return json.dumps(geocodes)


@app.route('/get_places', methods=["POST"])
def get_places():
	"""Extracts entities from text and returns lists and links to wikipedia"""

	text = file_reader.read_file(session['filepath'])
	target_lang = session['target_lang']
	source_lang = session['source_lang']

	#Checks the type of entity that is being requested
	ent = request.form['ent']

	#Uses the NER tagger to get entities
	if source_lang == 'de':
		organizations, locations, people = german_processing.postprocess(german_processing.german_ner(text))
	else:
		organizations, locations, people = text_processing.ner_tagger(text)
	
	if ent == "places":

		if locations: 
			loclist = wikipedia_linker.get_entity_info(locations, target_lang, source_lang)
			downfile = file_reader.write_csv_file(loclist)
			geocodes = geocoding.geocode(locations)
			return render_template("places.html", locations = loclist, geocodes = json.dumps(geocodes), downfile=downfile)
		else: 
			return render_template("places.html")

	elif ent == "organizations":

		if organizations:
			orglist = wikipedia_linker.get_entity_info(organizations, target_lang, source_lang)
			downfile = file_reader.write_csv_file(orglist)
			return render_template("orgs.html", organizations = orglist, downfile=downfile)
		else:
			return render_template("orgs.html")

	elif ent == "people":

		if people:
			peoplelist = wikipedia_linker.get_entity_info(people, target_lang, source_lang)
			downfile = file_reader.write_csv_file(peoplelist)
			return render_template("people.html", people = peoplelist, downfile=downfile)
		else:
			return render_template("people.html")

	elif ent == "nouns":
			nouns = text_processing.nouns_only(text_processing.make_word_dict(text_processing.preprocess(text)))
			if nouns: 	
				nounlist = wikipedia_linker.get_entity_info(nouns, target_lang, source_lang)
				downfile = file_reader.write_csv_file(nounlist)
				return render_template("other.html", nouns = nounlist, downfile=downfile)
			else:
				return render_template("other.html")






if __name__ == "__main__":
    app.run(debug = True)