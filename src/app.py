from flask import Flask, make_response, jsonify, request, Response
from datetime import datetime
from flask_pymongo import PyMongo
from bson.json_util import loads
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://mongodb/library'

mongo = PyMongo(app)

PORT = 3000
HOST = '0.0.0.0'

@app.route("/books",methods={"POST"})
def create_book():
    isbn = request.json['isbn']
    title = request.json['title']
    subtitle = request.json['subtitle']
    authors = request.json['authors']
    category = request.json['category']
    publicationDate = request.json['publicationDate']
    editor = request.json['editor']
    description = request.json['description']

    if isbn and title:
        id = mongo.db.books.insert_one(
            {
        "isbn":isbn,
        "title":title.capitalize(),
        "subtitle":subtitle.capitalize(),
        "authors":[author.capitalize() for author in authors],
        "category":[categ.capitalize() for categ in category],
        "publicationDate":publicationDate,
        "editor":editor.capitalize(),
        "description":description.capitalize(),
    })
        response = jsonify({
            '_id': str(id),
        })
        response.status_code = 201
        return response
    else:
        return not_found()

@app.route("/books")
def get_json():
    books = mongo.db.books.find({},{'_id': 0})
    response = json_util.dumps(books)
    return Response(response, mimetype="application/json")

@app.route("/books/<filters>/<value>")
def get_data(filters, value):
    filtersValide = ['isbn','title','authors','category','editor']
    params = text_mutation(filters, value)
    if params['filters'] in filtersValide:
        print("getting the value of %s in the filters %s"%(params['value'],params['filters']))
        resp = mongo.db.books.find({params['filters']:  {'$regex': params['value']} },{'_id':0})
        response = json_util.dumps(resp)
        datas = json_util.loads(response)
        if not response == '[]':
            for x in datas:
                x['fuente']= 'db interna';
            temp= json_util.dumps(datas)
            return Response(temp, mimetype="application/json")
        return 'no existe el libro carnal'
    return not_found_filter(filters)

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    mongo.db.books.delete_one({'isbn': isbn})
    response = jsonify({'message': 'Book ' + isbn + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/resgister")
def register():
    return 'Bienvenido ya puedes usar nuestra api'

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

def text_mutation(filters,value):
    data = {}
    data['filters'] = filters.lower();
    if type(value) is str:
        data['value'] = value.capitalize();
    else:
        data['value'] = value;
    return data;

def not_found_filter(filters):
    message = {
        'message': 'Filter /%s not allowed '%(filters),
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    print('Server running on port %s'%(PORT))
    app.run(host=HOST, port=PORT,debug=True)