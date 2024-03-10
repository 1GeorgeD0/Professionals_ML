from flask import Flask, render_template, url_for, request as req
import requests
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import spacy
from nltk.corpus import stopwords
from gensim.models.phrases import Phrases
from textblob import TextBlob
from sklearn.preprocessing import LabelEncoder
import pickle
import joblib
import os


app = Flask(__name__)
basepath = os.path.abspath(".")


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    url = req.form['url']
    print("url is :"+  url)
    posts = []
    urls_posts = get_all_posts_links(url + "/blog/")
    print("urls_posts :" + str(urls_posts))
    profile_company = get_profile_info(url + "/profile/")
    print("parsing.......")
    for url in urls_posts:
        post = get_company_post_info(url)
        post.update(profile_company)
        posts.append(post)
    print("parsing DONE!")
    df = pd.DataFrame(posts)
    print("DF DONE!")

    print("PREPARE BEGIN.......")
    df['word_count'] = df['text_post'].apply(lambda x: len(str(x).split()))
    df['unique_word_count'] = df['text_post'].apply(lambda x: len(set(str(x).split())))
    stopwords_list = set(stopwords.words('russian'))  # Update with appropriate language
    df['stopword_count'] = df['text_post'].apply(
        lambda x: len([word for word in str(x).lower().split() if word in stopwords_list]))

    df['text_clear'] = df['text_post'].apply(remove_special_chars)
    df['text_clear'] = df['text_clear'].apply(remove_stopwords)
    df['text_clear'] = df['text_clear'].apply(lemmatize)

    df['tokens'] = df['text_clear'].apply(tokenize_russian_text)

    # Преобразуем объект WordList в список предложений
    sentences = list(df['text_clear'])

    # Создаем модели биграмм и триграмм с помощью функции Phrases из библиотеки Gensim
    # min_count и threshold - параметры, которые контролируют, как часто должна встречаться фраза в тексте, чтобы быть рассмотренной как биграмма или триграмма
    bigram = Phrases(sentences, min_count=5, threshold=100)
    trigram = Phrases(bigram[sentences], min_count=5, threshold=100)

    # Применяем модели к предложениям
    for idx in range(len(sentences)):
        for token in bigram[sentences[idx]]:
            if '_' in token:
                # Токен - биграмма, добавляем в предложение
                sentences[idx].append(token)
        for token in trigram[bigram[sentences[idx]]]:
            if '_' in token:
                # Токен - триграмма, добавляем в предложение
                sentences[idx].append(token)
    # Обновить столбец text_post предварительно обработанным текстом
    df['text_bigram_trigram'] = sentences

    df['sentiment_polarity'] = df['text_post'].apply(get_sentiment)
    print("PREPARE END.......")

    df = df[['name_post', 'reading_time_post', 'views_count_post',
             'tags_post', 'name_company', 'rating_company',
             'word_count',
             'unique_word_count', 'stopword_count', 'text_clear', 'tokens',
             'text_bigram_trigram', 'sentiment_polarity']]


    # Export the encoder to a file
    # with open('encoder.pkl', 'wb') as f:
    #     pickle.dump(le, f)
    #Загрузка модели обучения

    print("LOAD encoder .......")
    url_enc = url_for('static', filename='encoder.pkl')
    with open(basepath + url_enc, 'rb') as f:
        # Load the object from the file
        le = pickle.load(f)

    for col in df.columns:
        df[col] = le.fit_transform(df[col])

    print("Encoding  DONE!  .......")

    print(df.head())
    url_model = url_for('static', filename='model.pkl')
    model = joblib.load(basepath + url_model)
    predictions = model.predict(df)

    print(predictions)
    predicted_class = le.inverse_transform([predictions])
    print(predicted_class)
    return predicted_class

def get_pages_links(url:str, lists:list = [])->list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        lists.append(url)
        next_page_link = "https://habr.com" + soup.find('a', id='pagination-next-page')["href"]
        get_pages_links(next_page_link, lists)
    except:
        pass
    return lists

def get_profile_info(profile_url) -> dict:
    data = {}
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = soup.findAll("a", class_="tm-company-profile__categories-text")
    category_list = []
    for category in categories:
        category_list.append(category.get_text())
    if soup.find("a", class_="tm-company-card__name") != None:
        data = {
            "name_company": soup.find("a", class_="tm-company-card__name").get_text(),
            "rating_company": soup.find("span", class_="tm-votes-lever__score-counter").get_text(),
            "desc_company": soup.find("div", class_="tm-company-card__description").get_text(),
            "category_list_company": category_list,
            "about_company": soup.find("span", class_="tm-company-profile__content").get_text()
        }
    return data


def get_company_post_info(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = {}
    tags_post = []
    tags = soup.findAll("a", class_="tm-article-snippet__hubs-item-link")
    for tag in tags:
        tags_post.append(tag.get_text())

    labels_post = []
    labels = soup.findAll("div", class_="tm-article-snippet__label")
    for label in labels:
        labels_post.append(label.get_text())
    tag = soup.find("span", class_="tm-article-complexity__label")
    if tag is not None:
        difficulty_post = tag.get_text()
    else:
        difficulty_post = "No label found"
    reading_time = soup.find("span", class_="tm-article-reading-time__label")
    if reading_time is not None:
        reading_time_post = re.findall(r'\d+', reading_time.get_text())[0]
    else:
        reading_time_post = "N/A"

    views_count = soup.find("span", class_="tm-icon-counter__value")
    if views_count is not None:
        views_count_post = re.findall(r'\d+\.\d+|\d+', views_count.get_text())[0]
    else:
        views_count_post = "N/A"
    data = {
        # "name_company": soup.find("a", class_ = "tm-company-card__name").get_text(),
        "name_post": soup.find("h1", class_="tm-title tm-title_h1").get_text(),
        "difficulty_post": difficulty_post,
        "reading_time_post": reading_time_post,
        "views_count_post": views_count_post,
        "tags_post": tags_post,
        "text_post": soup.find("div", class_="tm-article-body").get_text()

    }
    return data

def get_all_posts_links(company_url):
    pages_links = get_pages_links(company_url)
    linkes = []
    for link in pages_links:
        linkes.append(get_posts_links_by_page_url(link))
    flat_list = [item for sublist in linkes for item in sublist]
    return list(set(flat_list))


def get_posts_links_by_page_url(page_url: str)-> list:
    posts_links = []
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for post_link in soup.find_all('a', class_='tm-title__link'):
        link = "https://habr.com" + post_link["href"]
        posts_links.append(link)
    return posts_links

#Удалены все лишние символы, кроме букв из текстов публикаций
def remove_special_chars(text):
    """
    Remove special characters and digits from text.
    """
    return re.sub(r'[^а-яА-Я\s]', '', text)

#Удалены все стоп-слова в тектах публикаций
def remove_stopwords(text):
    """
    Remove stop words from text.
    """
    stop_words = stopwords.words('russian')
    return ' '.join([word for word in text.split() if word not in stop_words])

# Выполнена лемматизация текстов публикаций
def lemmatize(text):
    """
    Lemmatize text using pymorphy2.
    """
    morph = MorphAnalyzer()
    return ' '.join([morph.parse(word)[0].normal_form for word in text.split()])
def tokenize_russian_text(text):
    tokens = nltk.word_tokenize(text, language='russian')
    return tokens
nlp = spacy.load("ru_core_news_sm")
# Define a function to perform part-of-speech tagging and highlight significant parts of speech
def highlight_pos(text):
    doc = nlp(text)
    highlighted_text = ""
    for token in doc:
        if token.pos_ in ["NOUN", "VERB"]:  # Define the significant parts of speech
            highlighted_text += f"{token.text} "  # Add HTML tags for highlighting
    return highlighted_text

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return sentiment

if __name__ == '__main__':
    app.run()
