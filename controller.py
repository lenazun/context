import os

from flask import Flask, render_template, redirect, request, flash, session, url_for
from werkzeug import secure_filename

import file_reader
import text_processing
import wikipedia_linker


UPLOAD_FOLDER = 'static/uploads'
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

	session['target_lang'] = "en"
	return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():
	""" Uploads files or converts URLs into simple text files """
	print session

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

	target_lang = request.args.get("target_lang")
	session['target_lang'] = target_lang

	return redirect(url_for('editor'))



@app.route('/get_places', methods=["POST"])
def get_places():

	text = file_reader.read_file(session['filepath'])
	target_lang = session['target_lang']
	#Checks the type of entity that is being requested
	ent = request.form['ent']

	#Uses the NER tagger to get entities
	organizations, locations, people = text_processing.ner_tagger(text)
	
	if ent == "places":

		loclist = wikipedia_linker.get_entity_info(locations, target_lang)
		return render_template("places.html", locations = loclist)

	elif ent == "organizations":

		orglist = wikipedia_linker.get_entity_info(organizations, target_lang)
		return render_template("orgs.html", organizations = orglist)

	elif ent == "people":

		peoplelist = wikipedia_linker.get_entity_info(people, target_lang)
		return render_template("people.html", people = peoplelist)

	elif ent == "nouns":

		nouns = text_processing.nouns_only(text_processing.make_word_dict(text_processing.preprocess(text)))
		nounlist = wikipedia_linker.get_entity_info(nouns, target_lang)
		return render_template("other.html", nouns = nounlist)






if __name__ == "__main__":
    app.run(debug = True)