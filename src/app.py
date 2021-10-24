import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
DB_NAME = str(os.environ.get('DB_NAME', '/library'));
DB_PORT = int(os.environ.get('DB_PORT', 27017));
app.config['MONGO_URI'] = str(os.environ.get('MONGO_URI', f'mongodb://db:{DB_PORT}{DB_NAME}'))

mongo = PyMongo(app)
app.config['SECRET_KEY'] = str(os.environ.get('DB_NAME', 'r0AZS4u6NB'))

from controllers import *

if __name__ == '__main__':
    port = int(os.environ.get('APP_PORT', 8080))
    host = str(os.environ.get('HOST', '0.0.0.0'))
    print('Server running on port %s' % (port))
    print(port,host)
    app.run(host = host, port = port)