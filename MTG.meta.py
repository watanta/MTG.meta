# coding: utf-8
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, SelectMultipleField, BooleanField, FormField, FieldList
from wtforms.validators import DataRequired


app = Flask(__name__) #インスタンス生成
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mtga'
app.secret_key = 'hogehoge'
mongo = PyMongo(app)

@app.route("/")
def hello():
  return "Hello World!"


def get_decks(offset=0, per_page=9, query=None):
    search_word = session['freeword']

    return mongo.db.decks.find(query).skip(offset).limit(per_page)


def get_query():
    # 現在のsessionからqueryを作る
    query = {'red': session['red'], 'white': session['white'], 'green': session['green'],
             'blue': session['blue'], 'black': session['black'],
             'deckname': {'$regex': session['freeword']}}
    return query


def get_deck_image(deck):
    # deckのmainのカードに対応した画像urlをcardsから取ってくる
    card_name = list(deck['main'])[0]
    card = mongo.db.cards.find_one({'name': card_name})
    img_url = card['image_url']
    return img_url


def get_decks_image(decks):
    # 複数のdeckにそれぞれimg_urlを取ってくる
    img_urls = []
    for deck in decks:
        img_url = get_deck_image(deck)
        img_urls.append(img_url)
    return img_urls









class Deckform(FlaskForm):
    freeword = StringField('freeword')
    red = BooleanField('R', default=False)
    white = BooleanField('W', default=False)
    green = BooleanField('G', default=False)
    blue = BooleanField('U', default=False)
    black = BooleanField('B', default=False)
    submit = SubmitField('Submit')


@app.route("/decklist", methods=['GET', 'POST'])
def decklist():
    form = Deckform()
    if form.validate_on_submit():
        session['freeword'] = form.freeword.data
        session['red'] = form.red.data
        session['white'] = form.white.data
        session['green'] = form.green.data
        session['blue'] = form.blue.data
        session['black'] = form.black.data

        page, per_page, offset = get_page_args(page_parameter='page',
                                               per_page_parameter='per_page')

        query = get_query()

        total = mongo.db.decks.find(query).count()
        pagination_decks = get_decks(offset=offset, per_page=per_page, query=query)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap4')

        return render_template('decklist.html',
                               decks=pagination_decks,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               form=form,
                               total=total,
                               )

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    query = get_query()

    total = mongo.db.decks.find(query).count()
    pagination_decks = get_decks(offset=offset, per_page=per_page, query=query)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('decklist.html',
                           decks=pagination_decks,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           form=form,
                           total=total
                           )


@app.route('/form', methods=['GET','POST'])
def form():
    form = Deckform()
    if form.validate_on_submit():
        session['freeword'] = form.freeword.data
        session['red'] = form.red.data
        session['white'] = form.white.data
        session['green'] = form.green.data
        session['blue'] = form.blue.data
        session['black'] = form.black.data
        return redirect(url_for('thankyou'))

    return render_template('form.html', form=form)


@app.route('/thankyou', methods=['GET'])
def thankyou():
    return render_template('thankyou.html', session=session)


if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run(debug=True)

