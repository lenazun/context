News Context Explorer
====================


About
---------------------

News Context Explorer (NCE) helps to find people, places and nouns referenced by news articles (or any other text, but it works better with News articles).  It was built thinking of translators and news readers in a second language. After uploading a text file or providing an article URL, NCE will find names, places, organizations and other relevant words with their links to Wikipedia, as well as images, maps and other contextual information in 10 languages.

### Features:

+ Uploads a txt file or processes a URL
+ Supports English, German and Spanish as input languages
+ Cleans HTML for text processing and display
+ Provides the user with an editor to work and download the source text html
+ Highlights found entities
+ Allows the user to explore entities in a target language (10 languages currently supported) and download the references to a CSV file
+ Geocodes found locations and marks them on a google map
+ Retrieves photos of found entities and displays them on a gallery


Requirements
---------------------

NCE requires:

+ Python 2.7.6 or later
+ Flask
+ Java (JRE) is required to run the Stanford NES and POS taggers
+ A Google API key for geocoding and map display
+ Memcache and memcached to store entities in cache

Python libraries listed in requirements.txt


Installing NCE
---------------------

+ Better to start with a virtual environment.  To install virtualenv:

	<code>$ sudo pip install virtualenv
	$ cd ~/code/myproject/
	$ virtualenv env</code>

	To activate the virtual environment:

	<code>$ source env/bin/activate</code>


+ Once you have a virtual environment Pip install the required libraries with requirements.txt

	<code>$ env/bin/pip install -r requirements.txt</code>

+ Most files, including the Stanford NER and POS taggers are included on this repo. Clone it in your project folder.

+ You need to add 2 keys:  
	- A Flask API key in controller.py
	- A Google API key in geocoding.py and templates/places.html

+ Run the English NER file in java as a server in port 8080

	<code>java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.muc.7class.distsim.crf.ser.gz -port 8080 -outputFormat inlineXML</code>

	The German and Spanish NER files are not running as a server, but they are noticeably  slower.  You can adapt the code to run either way.

+ Donwload and [install memcached](http://memcached.org/downloads) and run it.  If memcached is not running the app will still work but it will be slower and make more requests to the Wikipedia API.

+ If you want to add or remove target languages, just add or remove the item from the templates/editor.html dropdown menu, and add new languages to the lancodes dictionary in controller.py.  Wikipedia has articles in 128 locales!


Aknowledgments
---------------------

I used excellent code and examples from:

[Stanford NLP](http://nlp.stanford.edu).
[Wikipedia API](http://www.mediawiki.org/wiki/API:Main_page).
[jQuery Highlight plugin](http://bartaz.github.io/sandbox.js/jquery.highlight.html).
[Medium editor](https://github.com/daviferreira/medium-editor).
[Magnific Popup](http://dimsemenov.com/plugins/magnific-popup/).
[HTML sanitizer](http://chase-seibert.github.io/blog/2011/01/28/sanitize-html-with-beautiful-soup.html).
[Front page tutorial](http://www.williamghelfi.com/blog/2013/08/04/bootstrap-in-practice-a-landing-page/).


Screenshots
---------------------

![Front page](/static/img/cover_ss.jpg "Front page")

![Text processing](/static/img/inside_ss.jpg "Text processing")


Contact info
---------------------

This project was completed during Hackbright, a 10 week engineering fellowship for women.

If you want to know more about this project, find me on Twitter [@lenazun](https://twitter.com/lenazun)
