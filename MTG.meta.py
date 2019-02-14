# coding: utf-8
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter, get_page_args


app = Flask(__name__) #インスタンス生成
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mtga'
mongo = PyMongo(app)
bootstrap = Bootstrap(app)




@app.route("/")
def hello():
  return "Hello World!"

def get_decks(offset=0, per_page=10):
    return mongo.db.decks.find().skip(offset).limit(per_page)

@app.route("/decklist", methods=['GET'])
def decklist():

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total = mongo.db.decks.count()
    pagination_decks = get_decks(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('decklist.html',
                           decks=pagination_decks,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )




if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run(debug=True)