# To run:
# $ export FLASK_APP='cone_server.py'
# $ python3 -m flask run
# 
# Then go to 127.0.0.1:5000 in your browser

import os
import flask

import flight_price

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/')
def root():
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('index'))
    else:
        redirect = 'http://127.0.0.1:5000/auth'
        client_id = 'cc2f96ed55c54755ac591e5e790146d8'
        return flask.redirect(
            'https://api-sandbox.capitalone.com/oauth2/authorize?redirect_uri=%s&scope=read_rewards_account_info&client_id=%s&response_type=code'
            % (redirect, client_id))

@app.route('/auth')
def auth():
    flask.session['user'] = flask.request.args.get('code', '')
    return flask.redirect(flask.url_for('index'))

@app.route('/index')
def index():
    return app.send_static_file('test_index.html')

@app.route('/test_index.css')
def index_css():
    return app.send_static_file('test_index.css')

@app.route('/TripCone.png')
def trip_cone_png():
    return app.send_static_file('TripCone.png')

@app.route('/search')
def search():
    from_city = flask.request.args.get('from', '')
    to_city = flask.request.args.get('to', '')
    price = flight_price.flight_price(from_city, to_city)
    return '/rewards'
    
@app.route('/rewards')
def rewards():
    return app.send_static_file('rewards_money_input.html')