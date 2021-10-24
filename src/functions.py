from request import *
import random
from flask import jsonify
from bson import json_util


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
