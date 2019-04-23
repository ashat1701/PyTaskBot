from flask import Flask, render_template

app = Flask(__name__)
def init():
    pass


@app.route('/login', methods=['GET, POST'])
def get_login_hook():
    pass


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def obr(name):
    return render_template(name)
