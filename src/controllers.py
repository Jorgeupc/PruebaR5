import asyncio
from app import app
from request import *
from functions import *
from flask import jsonify, request, Response, session
from datetime import timedelta
from bson import json_util


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

@app.route("/books")
async def get_json():
    if session.get('api_key') == 'Registrado':
        books = await get_find()
        response = json_util.dumps(books)
        return Response(response, mimetype="application/json")
    return not_session()

@app.route('/books/<isbn>', methods=['DELETE'])
async def delete_book(isbn):
    if session.get('api_key') == 'Registrado':
        resp = await delete_monogo_book(isbn)
        if resp > 0: 
            response = jsonify({'message': 'Book ' + isbn + ' Deleted Successfully'})
            response.status_code = 200
            return response
        response = jsonify({'message': 'Isbn book not found in database'})
        response.status_code = 404
        return response
    return not_session()

@app.route("/resgister")
def register():
    session['api_key'] = 'Registrado'
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=600)
    response = jsonify({'message': 'welcome, you are allowed to use the app'})
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

