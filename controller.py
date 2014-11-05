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

@app.route("/")
def index():
    return render_template("upload.html")


@app.route('/upload_file', methods=['POST'])
def upload_file():

	targetlang = request.form.get("targetlang")
	file = request.files['filename']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		session['filename'] = filename
		session['filepath'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		session['targetlang'] = targetlang
		
		return redirect(url_for('basic_process'))
	else:
		flash ("Make sure you're uploading a txt file")
		return render_template("upload.html")


@app.route("/basic_process")
def basic_process():
	filepath = session['filepath']
	targetlang = session['targetlang']
	text = file_reader.read_file(filepath)
	simplecount = len(text)

	return render_template("basic_process.html", simple=simplecount)



if __name__ == "__main__":
    app.run(debug = True)