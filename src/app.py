from flask import Flask

app = Flask(__name__)

PORT = 3000
HOST = '0.0.0.0'

@app.route("/")
def startService():
    return 'Hello World'

if __name__ == '__main__':
    print('Server running on port %s'%(PORT))
    app.run(host=HOST, port=PORT,debug=True)


