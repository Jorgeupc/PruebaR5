import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
API_KEY =  os.environ.get('API_KEY', None)
PORT =  os.environ.get('PORT', None)
HOST =  os.environ.get('HOST', None)

from controllers import *

if __name__ == '__main__':
    print('Server running on port %s' % (PORT))
    app.run(host=HOST, port=PORT)