#!flask/bin/python
from socket import gethostname
from application import app
if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(debug=True)
