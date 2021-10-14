from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap





app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    print("user function is called!!!!!!!!!!!")
    return render_template('user.html', name=None)



if __name__ == '__main__':
    app.run(debug=True)
