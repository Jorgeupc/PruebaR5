import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'r0AZS4u6NB')
API_KEY =  os.environ.get('API_KEY', 'AIzaSyAD61SNg8KIVn4oyjJlNARva6BrIq056oo')
PORT =  os.environ.get('PORT', 3000)
HOST =  os.environ.get('HOST', '0.0.0.0')

from controllers import *

if __name__ == '__main__':
    print('Server running on port %s' % (PORT))
    app.run(host=HOST, port=PORT)