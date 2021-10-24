import asyncio
from datetime import timedelta
import requests
import random
from flask import Flask, jsonify, request, Response, session
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongodb/library'
app.config['SECRET_KEY'] = 'r0AZS4u6NB'


mongo = PyMongo(app)
API_KEY = 'AIzaSyAD61SNg8KIVn4oyjJlNARva6BrIq056oo'
PORT = 3000
HOST = '0.0.0.0'

async def get_find():
    books = mongo.db.books.find({}, {'_id': 0})
    return books


@app.route("/books")
async def get_json():
    if session.get('api_key') == 'Registrado':
        books = await get_find()
        response = json_util.dumps(books)
        return Response(response, mimetype="application/json")
    return not_session()


def generate_query_google(filters, value):
    ['isbn', 'title', 'authors', 'category', 'editor']
    if filters == 'isbn':
        query = f'q=isbn:{value}'
    elif filters == 'title':
        query = f'q=intitle:{value}'
    elif filters == 'authors':
        query = f'q=inauthor:{value}'
    elif filters == 'category':
        query = f'q=subject:{value}'
    else:
        query = f'q=inpublisher:{value}'

    base_url = f'https://www.googleapis.com/books/v1/volumes?{query}'

    print(base_url)
    return base_url

async def consultDB(filters, value):
    value = value.replace("+", " ")
    print(value)
    print('+++++++++++++++++++++++++++++++++++++++++')
    resp = mongo.db.books.find({filters:  {'$regex': value}}, {'_id': 0})
    response = json_util.dumps(resp)
    return response

async def consultGoogle(filters, value):
    resp = requests.get(generate_query_google(filters, value))
    return resp.json()


@app.route("/books/<filters>/<value>")
async def get_data(filters, value):
    if session.get('api_key') == 'Registrado':
        filtersValide = ['isbn', 'title', 'authors', 'category', 'editor']
        params = text_mutation(filters, value)
        if params['filters'] in filtersValide:
            print("getting the value of %s in the filters %s" %
                (params['value'], params['filters']))
            tasks = []
            tasks.append(asyncio.ensure_future(
                consultDB(params['filters'], params['value'])))
            tasks.append(asyncio.ensure_future(
                consultGoogle(params['filters'], params['value'])))
            response, response_google = await asyncio.gather(*tasks)
            datas = json_util.loads(response)
            if not response == '[]':
                for x in datas:
                    x['fuente'] = 'db interna'
                temp = json_util.dumps(datas)
                return Response(temp, mimetype="application/json")
            return book_no_exist(response_google)
        return not_found_filter(filters)
    return not_session()


def book_no_exist(data):
    if data['totalItems']>0:
        if data['totalItems']>10:
            idbook = random.randint(0, 9)
        else:
            idbook = random.randint(0, data['totalItems'])
        
        data_esp = data['items'][idbook]
        print(data_esp)
        resp = {
            "isbn": [isbn.get('identifier') for isbn in data_esp.get('volumeInfo').get('industryIdentifiers')],
            "title": data_esp.get('volumeInfo').get('title').lower(),
            "subtitle": data_esp.get('volumeInfo').get('subtitle',"Subtitle not found on google Books API"),
            "authors": [author.lower() for author in data_esp.get('volumeInfo').get('authors','')],
            "category": [category.lower() for category in data_esp.get('volumeInfo').get('categories','')],
            "publicationDate": data_esp.get('volumeInfo').get('publishedDate'),
            "editor":  data_esp.get('volumeInfo').get('publisher','').lower(),
            "description": data_esp.get('volumeInfo').get('description',''),
        }

        respta = mongo.db.books.find({'isbn': resp['isbn'][0]}, {'_id': 0})
        response = json_util.dumps(respta)
        print(response)
        if response == '[]':
            insert = mongo.db.books.insert_one(resp)
            if insert:
                resp['fuente'] = 'Google Books API'
                del resp['_id']
                response = jsonify(resp)
                response.status_code = 200
                return response
        message = {
            'message': 'internal error',
            'status': 500
        }
        response = jsonify(message)
        response.status_code = 500
        return response
    message = {
        'message': 'Not found data in Google Books API',
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    if session.get('api_key') == 'Registrado':
        mongo.db.books.delete_one({'isbn': isbn})
        response = jsonify({'message': 'Book ' + isbn + ' Deleted Successfully'})
        response.status_code = 200
        return response
    return not_session()


@app.route("/resgister")
def register():
    session['api_key'] = 'Registrado'
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=15*60)
    response = jsonify({'message': 'welcome, you are allowed to use the app for 15 minutes'})
    response.status_code = 200
    return response

@app.errorhandler(401)
def not_session(error=None):
    message = {
        'message': 'You are not allowed to use the app, go to /register',
        'status': 401
    }
    response = jsonify(message)
    response.status_code = 401
    return response

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


def text_mutation(filters, value):
    data = {}
    data['filters'] = filters.lower()
    if type(value) is str:
        data['value'] = value.lower();
    else:
        data['value'] = value;
    return data;


def not_found_filter(filters):
    message = {
        'message': 'Filter /%s not allowed ' % (filters),
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    print('Server running on port %s' % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
