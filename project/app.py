from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask import Flask, render_template, session, redirect, url_for, flash
import pandas as pd
import json




# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[DataRequired()])
#     email = EmailField('What is your UofT Email Address', validators=[DataRequired(), Email()])
#     select = SelectField("Please select", choices=[1,2,3])
#     submit = SubmitField('Submit')

df = pd.read_pickle('project/resources/df_processed.pickle').set_index("Code")



app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    arr = [1,2,3]
    if request.method == 'POST':
        return results(request.form)
    return render_template('search.html', arr=arr)


def results(form):
    print(form.to_dict())
    arr = [1,2,3]
    table = df.loc[:, ["Course", "Division"]][:2]
    table = table.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False)
    return render_template('results.html', arr=arr, tables=[table])

@app.route('/course/<code>')
def course(code):
    course = None 
    if code in df.index:
        course = json.loads(df.loc[code].to_json())

    return render_template('course.html', course=course, code=code)

@app.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):
    print(f"Add comment of {code} is called!")
    return redirect(url_for("course", code=code))



@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return render_template('user.html', name=None)



# {
#     {
#         coursecode: ,
#         name: ,
#     },
#     {
#         coursecode: ,
#         name: ,
#     }
# }


if __name__ == '__main__':
    app.run(debug=True)
