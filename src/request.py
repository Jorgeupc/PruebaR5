from app import mongo
from functions import generate_query_google
import requests
from bson import json_util


async def consultDB(filters, value):
    value = value.replace("+", " ")
    resp = mongo.db.books.find({filters:  {'$regex': value}}, {'_id': 0})
    response = json_util.dumps(resp)
    return response

async def consultGoogle(filters, value):
    resp = requests.get(generate_query_google(filters, value))
    return resp.json()

async def get_find():
    books = mongo.db.books.find({}, {'_id': 0})
    return books

async def insert_book(resp):
    books = mongo.db.books.insert_one(resp)
    print(books)
    return books

async def check_book(isbn):
    check = mongo.db.books.find({'isbn': isbn}, {'_id': 0})
    response = json_util.dumps(check)
    return response

async def delete_monogo_book(isbn):
    result = mongo.db.books.delete_one({'isbn': isbn})
    return result.deleted_count