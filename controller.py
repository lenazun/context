from flask import Flask, render_template, redirect, request, flash, session, url_for
import file_reader
import text_processing
import wikipedia_linker
from werkzeug import secure_filename
import os


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567' #Fake key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():


	if request.files['filename']:
		file = request.files['filename']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			session['filename'] = filename
			session['filepath'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			
			return redirect(url_for('basic_process'))
		else:
			flash ("Make sure you're uploading a txt file")
			return render_template("upload.html")

	elif request.form.get("url"):
		url = request.form.get('url')
		file_reader.read_url_all(url)
		session['filename'] = 'newfile.txt'
		session['filepath'] = os.path.join(app.config['UPLOAD_FOLDER'], 'newfile.txt')
		
		return redirect(url_for('basic_process'))

	else:
		flash ("Enter a source file or URL")
		return render_template("upload.html")


@app.route('/basic_process')
def basic_process():
	filepath = session['filepath']

	text = file_reader.read_file(filepath)

	simplecount = len(text)

	return render_template("basic_process.html", simple=simplecount)



@app.route('/entities', methods=["GET"])
def entities():

	filepath = session['filepath']

	target_lang = request.args.get("target_lang")
	print target_lang


	text = file_reader.read_file(filepath)
	organizations, locations, people = text_processing.NERtagger(text)
	nouns = text_processing.nouns_only(text_processing.make_dict(text_processing.preprocess(text)))

	orglist = wikipedia_linker.get_entity_info(organizations, target_lang)
	loclist = wikipedia_linker.get_entity_info(locations, target_lang)
	peoplelist = wikipedia_linker.get_entity_info(people, target_lang)
	nounlist = wikipedia_linker.get_entity_info(nouns, target_lang)


	return render_template("entities.html", entities=entities, organizations=orglist, locations=loclist, people=peoplelist, nouns=nounlist, target_lang=target_lang)


if __name__ == "__main__":
    app.run(debug = True)