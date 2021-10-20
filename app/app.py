from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask import Flask, render_template, session, redirect, url_for, flash
import pandas as pd




# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[DataRequired()])
#     email = EmailField('What is your UofT Email Address', validators=[DataRequired(), Email()])
#     select = SelectField("Please select", choices=[1,2,3])
#     submit = SubmitField('Submit')

df = pd.read_pickle('resources/df_processed.pickle')



app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    arr = [1,2,3]
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html', arr=arr)

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return render_template('user.html', name=None)



if __name__ == '__main__':
    app.run(debug=True)
