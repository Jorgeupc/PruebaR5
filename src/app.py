import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'r0AZS4u6NB'
API_KEY =  'AIzaSyAD61SNg8KIVn4oyjJlNARva6BrIq056oo'
PORT =  3000
HOST =  '0.0.0.0'

from controllers import *

if __name__ == '__main__':
    print('Server running on port %s' % (PORT))
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)