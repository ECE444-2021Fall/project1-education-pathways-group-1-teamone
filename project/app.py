from os import pardir
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
import hashlib




#selections 
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
selections = {
    "Divisions":divisions,
    "Departments":departments,
    "Campus":campus,
    "Level":level
}



#app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcde'
CORS(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
bootstrap = Bootstrap(app)

#AWS API
headers = {
        "Content-Type": "application/json" 
}
    
api_urls = {
    "courseSearch":"https://8h7ianjw7a.execute-api.us-east-1.amazonaws.com/default/courseSearch",
    "discussionTable":"https://smpwfjd6r5.execute-api.us-east-1.amazonaws.com/default/discussionTable",
    "userTable":"https://kxa7awvtc4.execute-api.us-east-1.amazonaws.com/default/userTable"
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
    res = requests.get(url=api_urls["courseSearch"], headers=headers, data=json.dumps(params))

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


    #---------Get course information----------        
    params = {
        "from": 0,
        "numResults": 20,
        "queryString": code, 
        "filters": {
        }
    }
    res = requests.get(url=api_urls["courseSearch"], headers=headers, data=json.dumps(params))
    course = json.loads(res.text)[code]["data"]  
    del course["CourseID"]
    del course["Level"]
    course = dict(sorted(course.items(), key=sorter))
    if not session.get('user_authenticated'):
        return render_template('course.html', course=course, code=code)
    
    username = session.get('name')
    paths = get_paths(username)
    #---------Get course comments----------
    params = {
            "action": "GetComments",
            "courseID": code
    }
    r = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
    comments = sorted(json.loads(r.text), key=lambda x:int(x['NumLikes']), reverse=True)
    
    #---------Get paths----------
    paths = get_paths(username)
    return render_template('course.html', course=course, comments=comments, code=code, paths=paths, username=username)

@app.route('/course/<code>/add_comment/<username>', methods=['POST'])
def add_comment(code, username):
    form = request.form    
    params = {
        "action": "AddComment",
        "courseID": code,
        "User": username,
        "DateTime": datetime.now().strftime("%m/%d/%Y %H:%M"),
        "Message": form.get("message")
    }
    if form.get('anonymous') is not None:
        params['User'] = 'Anonymous'
    res = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("course", code=code))

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if not session.get('user_authenticated'):
        return render_template('enroll.html', username=None)
    return render_template('enroll.html', paths=get_paths(session['name']), username=session['name'])

def get_paths(username):    
    params = {
        "action": "GetUser",
        "Username": username
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    paths = res.json()['EnrolmentPaths']
    return paths

@app.route('/enroll/add_course/<course_name>/<code>/<username>', methods=['POST'])
def add_course(course_name, code, username):  
    form = request.form    
    params = {
        "action": "AddCourse",
        "Username": username,
        "pathName": form.get("path_choice"),
        "course":{
            "Code":code,
            "Name":course_name,
            "Semester":form.get("term_choice")
            
        }
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    if res.status_code!=200:
        flash(res.text)
        return res.text
    return redirect(url_for("enroll"))

@app.route('/enroll/remove_course', methods=['POST'])
def remove_course():      
    params = request.get_json()
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return res.text

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('username'):   
        session.pop('username')
    if session.get('user_authenticated'):   
        session.pop('user_authenticated')
    if session.get('user_info'):   
        session.pop('user_info')
    return redirect(url_for("index"))

@app.route('/enroll/add_path/<username>', methods=['POST'])
def add_path(username):   
    params = {
        "action": "AddPath",
        "Username": username,
        "pathName": request.form.get("path"),
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("enroll"))

@app.route('/enroll/delete_path/<username>', methods=['POST'])
def delete_path(username):  
    params = {
        "action": "DeletePath",
        "Username": username,
        "pathName": request.form.get("path_choice"),
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("enroll"))

@app.route('/upgrade_vote', methods=['GET', 'POST'])
def upgrade_vote():
    params = request.get_json()
    res = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
    return res.text
    

@app.route('/user', methods=['GET', 'POST'])
def user():
    if session.get('user_authenticated') == True:
        return render_template('user.html', name=session['username'])
    else:
        form = LogInForm()
        flash('Please login to access User Tab.')
        return redirect(url_for('login', des='user'))

#Log In Code
class LogInForm(Form):
    username = StringField('Username', validators=[DataRequired('Please provide a valid username.')])    
    password = PasswordField('Password', [validators.DataRequired('Please provide a valid password.')])
    remember_me = BooleanField('Remember Me')
    # submit = SubmitField('Submit')

#Register Code
class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired('Please provide a valid username.')])
    name = StringField('Full Name', validators=[DataRequired('Please provide a valid name.')])    
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    userType = SelectField(u'User Type', choices=[('STUDENT', 'Student'), ('PROFESSOR', 'Professor'), ('ADMIN', 'Course Admin')])
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
            params = {
                "action": "AddUser",
                "Username": str(form.username.data),
                "Email": str(form.email.data),
                "Password": encodePassword(form.password.data),
                "Type": str(form.userType.data)
            }
            res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
            if res.status_code!=200:
                flash("Please provide valid information")
            flash('Thanks for registering. Please sign In.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

def encodePassword(password):
    encoded = password.encode()
    return hashlib.sha256(encoded).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login(des = None):
    if (session.get('user_authenticated')):
        return redirect(url_for('index'))
    password = None
    form = LogInForm()
    if request.method == 'POST' and form.validate_on_submit():
        #---------Get User Authenticated----------        
        params = {
            "action": "Login",
            "Username": str(form.username.data),
            "Password": encodePassword(str(form.password.data))
        }
        res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
        if res.status_code!=200:
            flash("Incorrect username and/or password")
        else:
            #---------Get User Information----------   
            params = {
                "action": "GetUser",
                "Username": str(form.username.data),
            }
            res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
            if res.status_code!=200:
                flash("Please refer to your email to activate your account")
            user_info = json.loads(res.text) 
            session['username'] = form.username.data
            session['user_authenticated'] = True
            session['user_info'] = user_info
            if des:
                return redirect(url_for(des))
            else:
                return redirect(url_for('index'))
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
