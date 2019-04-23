from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)


def init():
    app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/login', methods=['GET, POST'])
def get_login_hook():
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def obr(name):
    return render_template(name)

if __name__ == "__main__":
    init()
    app.run()