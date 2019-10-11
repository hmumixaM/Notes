from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return 'index page'


@app.route('/<path:url>')
def name(url):
    return render_template('hello.html', name=url)


@app.route('/about')
def about():
    return 'About the program'


@app.route('/404')
def error404():
    return '404'


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login')
def loginpage():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


if __name__ == '__main__':
    app.run()