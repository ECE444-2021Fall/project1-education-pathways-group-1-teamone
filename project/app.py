from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from flask import Flask, render_template, session, redirect, url_for, flash
import pandas as pd
import json
import requests
from datetime import datetime
from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField
from markupsafe import Markup


df = pd.read_pickle('project/resources/df_processed.pickle').set_index("Code")
divisions = sorted([
    t for t in set(df.Division.values)
])
departments = sorted([
    t for t in set(df.Department.values)
])
campus = sorted([
    t for t in set(df.Campus.values)
])
level = [
    str(t) for t in set(df['Course Level'].values)
]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcde'
CORS(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
bootstrap = Bootstrap(app)
selections = {
    "Divisions":divisions,
    "Departments":departments,
    "Campus":campus,
    "Level":level
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        return results()
    
    return render_template('search.html', form=request.form, selections=selections)


def results():
    form=request.form
    url = "https://8h7ianjw7a.execute-api.us-east-1.amazonaws.com/default/courseSearch"
    headers = { "Content-Type": "application/json" }
    params = {
        "from": 0,
        "numResults": 20,
        "queryString": "", 
        "filters": {
        }
    }
    if form["Code"]:
        params["queryString"] = form["Code"]
    else:
        params["queryString"] = form["Keyword"]
        for k in form:
            if k not in {"Keyword", "Code"}:
                ls = form.getlist(k)
                if len(ls) > 0:
                    params["filters"][k] = ls
    res = requests.get(url, headers=headers, data=json.dumps(params))

    search_results = json.loads(res.text)
    return render_template('results.html', form=form, selections=selections, search_results=search_results)

@app.route('/course/<code>')
def course(code):
    dic = {
        "Description":(0),
        "Department":(1),
        "Prerequisites":(2),
        "Division":(3),
        "Division":(4),
        "Term": (5),
    }
    def sorter(x):
        if x[0] in dic:
            return dic[x[0]]
        else:
            return (float('inf'))
    course = None 
    comments = None
    if code in df.index:
        url = "https://8h7ianjw7a.execute-api.us-east-1.amazonaws.com/default/courseSearch"
        headers = { "Content-Type": "application/json" }
        params = {
            "from": 0,
            "numResults": 20,
            "queryString": code, 
            "filters": {
            }
        }
        res = requests.get(url, headers=headers, data=json.dumps(params))
        course = json.loads(res.text)[code]["data"]
        course_name = course["Name"]
        del course["CourseID"]
        del course["Name"]
        del course["Level"]
        sorted_course = sorted(course.items(), key = sorter)  
        url = "https://smpwfjd6r5.execute-api.us-east-1.amazonaws.com/default/discussionTable"
        params1 = {
                "action": "GetComments",
                "courseID": code
        }
        r = requests.get(url, headers=headers, data=json.dumps(params1))
        comments = json.loads(r.text)
        comments.sort(key = lambda x:int(x['NumLikes']), reverse=True)
    return render_template('course.html', course=sorted_course, comments=comments, code=code, course_name=course_name)

@app.route('/course/<code>/enroll')
def enroll_course(code):
    form = request.form
    return redirect(url_for("course", code=code))


@app.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):
    form = request.form
    url = "https://smpwfjd6r5.execute-api.us-east-1.amazonaws.com/default/discussionTable"
    headers = { "Content-Type": "application/json" }
    params = {
        "action": "AddComment",
        "courseID": code,
        "User": "",
        "DateTime": datetime.datetime.now().strftime("%m/%d/%Y %H:%M"),
        "Message": form.get("message")
    }
    if form.get('anonymous') is not None:
        params['User'] = 'Anonymous'
    else:
        params['User'] = 'Anyone'
    res = requests.get(url, headers=headers, data=json.dumps(params))
    return redirect(url_for("course", code=code))


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        if request.form.get("add_new"):
            pass
        elif request.form.get("delete_current"):
            pass
        return redirect(url_for("enroll"))

    if session.get('user_authenticated') != True:
        flash('Please login to access Login Tab.')
        return redirect(url_for("login"))

    paths = {
        "path1":[
            {
                "Code":"ECE444",
                "Name":"Software Engineering",
                "Semester":"2021 Fall",
            },
            {
                "Code":"ECE444",
                "Name":"Software Engineering",
                "Semester":"2021 Fall",
            }
        ],
        
        "path2":[
            {
                "Code":"CSC384",
                "Name":"Intoduction to AI",
                "Semester":"2021 Fall",
            },
        ]
    }
    for i in range(5):
        paths["path1"].append({
                "Code":"CSC384",
                "Name":"Intoduction to AI",
                "Semester":"2021 Fall",
            })

    return render_template('enroll.html', paths=paths)

@app.route('/upgrade_vote', methods=['GET', 'POST'])
def upgrade_vote():
    url = "https://smpwfjd6r5.execute-api.us-east-1.amazonaws.com/default/discussionTable"
    headers = { "Content-Type": "application/json" }
    params = request.get_json()
    res = requests.get(url, headers=headers, data=json.dumps(params))
    return res.text
    

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    if session.get('user_authenticated') == True:
        return render_template('user.html', name=session['name'])
    else:
        form = LogInForm()
        flash('Please login to access User Tab.')
        return render_template('login.html', form=form)

#Log In Code
class LogInForm(Form):
    name = StringField('Username', validators=[DataRequired('Please provide a valid username.')])    
    password = PasswordField('Password', [validators.DataRequired('Please provide a strong password.')])
    remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Submit')

#Log In Code
class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired('Please provide a valid username.')])
    name = StringField('Full Name', validators=[DataRequired('Please provide a valid username.')])    
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    userType = SelectField(u'User Type', choices=[('student', 'Student'), ('professor', 'Professor'), ('admin', 'Course Admin'), ('developer', 'Application Develooper')])
    password = PasswordField('Password', [validators.DataRequired('Please provide a strong password.')])
    # password = PasswordField('Password', [InputRequired(), EqualTo(fieldname='passwordConfirm', message='Passwords must match')])
    passwordConfirm = PasswordField('Repeat Password')

    # submit = SubmitField('Submit')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if str(form.password.data) != str(form.passwordConfirm.data):
            flash('Passwords must match')
            # return redirect(url_for('register'))
        elif str(form.password.data).isalpha():
            flash('Please include numbers in your password.')
        elif str(form.password.data).isdigit():
            flash('Please include alphabets in your password.')
        elif str(form.password.data).isalnum():
            flash('Please include special characters in your password.')
        else:
            flash('Thanks for registering. Please sign In.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    name = None
    password = None
    form = LogInForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('password')
        if str(form.password.data).isalpha():
            flash('Please include numbers in your password.')
        elif str(form.password.data).isdigit():
            flash('Please include alphabets in your password.')
        elif str(form.password.data).isalnum():
            flash('Please include special characters in your password.')
        else:
            #Call API to Update the BackEnd
            session['name'] = form.name.data
            session['user_authenticated'] = True
       
        return redirect(url_for('login'))

    return render_template('login.html', form=form, name=session.get('name'), password=session.get('password'))
    # return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
