from flask import Flask, url_for

app = Flask(__name__)


@app.route('/<path:url>')
def name(url):
    return 'Url: {}'.format(url)


@app.route('/about')
def about():
    return 'About the program'


@app.route('/404')
def error404():
    return '404'


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


if __name__ == '__main__':
    app.debug = True
    app.run()
