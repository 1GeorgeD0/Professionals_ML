from flask import Flask, render_template,request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.externals import joblib
import fasttext
fasttext.FastText.eprint = lambda x: None

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods = ['POST'])
def predict():
	print("HELLP")
	clf = fasttext.load_model("OptimizedModel.model")

	if request.method == 'POST':
		comment = request.form['comment']
		data = [comment]
		vect = cv.transform(data).toarray()
		ml_prognoz = clf.predict(vect)

	return render_template('result.html', prognoz = ml_prognoz)


if __name__ == '__main__':
	app.run()
