import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
API_KEY = os.getenv('API_KEY')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

from controllers import *

if __name__ == '__main__':
    print('Server running on port %s' % (PORT))
    app.run(host=HOST, port=PORT)