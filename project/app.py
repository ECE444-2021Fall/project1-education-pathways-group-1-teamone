from os import pardir
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask import Flask, render_template, session, redirect, url_for, flash
import pandas as pd
import json
import datetime
import requests


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
    course = None 
    comments = None
    if code in df.index:
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
        
        #---------Get course comments----------
        params = {
                "action": "GetComments",
                "courseID": code
        }
        r = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
        comments = sorted(json.loads(r.text), key=lambda x:int(x['NumLikes']), reverse=True)
        
        #---------Get paths----------
        paths = get_paths()
    return render_template('course.html', course=course, comments=comments, code=code, paths=paths)

@app.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):
    form = request.form    
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
    res = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("course", code=code))

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    return render_template('enroll.html', paths=get_paths())

def get_paths():    
    params = {
        "action": "GetUser",
        "Username": "Tony"
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    paths = res.json()['EnrolmentPaths']
    return paths

@app.route('/enroll/add_course/<course_name>/<code>', methods=['POST'])
def add_course(course_name, code):  
    form = request.form    
    params = {
        "action": "AddCourse",
        "Username": "Tony",
        "pathName": form.get("path_choice"),
        "course":{
            "Code":code,
            "Name":course_name,
            "Semester":form.get("term_choice")
            
        }
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("enroll"))

@app.route('/enroll/remove_course', methods=['POST'])
def remove_course():      
    params = request.get_json()
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return res.text

@app.route('/enroll/add_path', methods=['POST'])
def add_path():   
    params = {
        "action": "AddPath",
        "Username": "Tony",
        "pathName": request.form.get("path"),
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("enroll"))

@app.route('/enroll/delete_path', methods=['POST'])
def delete_path():  
    params = {
        "action": "DeletePath",
        "Username": "Tony",
        "pathName": request.form.get("path_choice"),
    }
    res = requests.get(url=api_urls["userTable"], headers=headers, data=json.dumps(params))
    return redirect(url_for("enroll"))

@app.route('/upgrade_vote', methods=['GET', 'POST'])
def upgrade_vote():
    params = request.get_json()
    res = requests.get(url=api_urls["discussionTable"], headers=headers, data=json.dumps(params))
    return res.text
    




if __name__ == '__main__':
    app.run(debug=True)
