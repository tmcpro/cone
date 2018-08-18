import flask
app = flask.Flask(__name__)

authcode = ''

@app.route('/')
def root():
    redirect = 'http://127.0.0.1:5000/auth'
    client_id = 'cc2f96ed55c54755ac591e5e790146d8'
    return flask.redirect('https://api-sandbox.capitalone.com/oauth2/authorize?redirect_uri=%s&scope=read_rewards_account_info&client_id=%s&response_type=code'
        % (redirect, client_id))

@app.route('/auth')
def auth():
    authcode = flask.request.args.get('code', '')
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
