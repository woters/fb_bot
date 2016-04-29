import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import Response
from flask import request
import requests


app = Flask(__name__)
TOCKEN = ""


def respond_FB(sender_id, text):
    json_data = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    params = {
        "access_token": TOCKEN
    }
    r = requests.post('https://graph.facebook.com/v2.6/me/messages', json=json_data, params=params)
    print(r, r.status_code, r.text)



@app.route('/')
def hello_world():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return 'Hello World!'

@app.route('/webhook', methods=['GET', 'POST'])
def fb_webhook():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == 'token':
            return Response(request.args.get('hub.challenge'))
        else:
            return Response('Wrong validation token')
    else:
        if request.method == "POST":
            event = request.get_json()
            #event = request.values
            print("ff")
            print(event)
            resp = Response(status=200, mimetype='application/json')
            respond_FB(your_id, "Hi! to you!")
            return resp



if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
