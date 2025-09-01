#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    #session['page_views'] = int(session.get('page_views')) + 1 or 0
    session['page_views'] = int(session.get('page_views') or 0) + 1

    if session['page_views'] <= 3:
        article = Article.query.filter(Article.id==id).first()
        response = make_response(jsonify({
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': str(article.date),
            'user_id': article.user_id,
            'cookies': [{cookie: request.cookies[cookie]}
                for cookie in request.cookies],
        }), 200)
    else:
        response = make_response(
            {'message': 'Maximum pageview limit reached'},
            401
        )

    return response

if __name__ == '__main__':
    app.run(port=5555)
