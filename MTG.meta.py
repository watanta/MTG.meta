# coding: utf-8
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__) #インスタンス生成
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mtga'
mongo = PyMongo(app)



@app.route("/")
def hello():
  return "Hello World!"


@app.route("/decklist")
def decklist():
    decks = []
    decks = mongo.db.decks.find()

    return render_template('decklist.html', decks=decks)

if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run()