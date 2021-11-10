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
    # table = df.loc[:, ["Course","Name", "Division"]][:4]
    # table = table.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False)
    # print(form.to_dict())
    form=request.form
    url = "https://8h7ianjw7a.execute-api.us-east-1.amazonaws.com/default/courseSearch"
    headers = { "Content-Type": "application/json" }

    params = {
        "from": 0,
        "numResults": 20,
        "queryString": "", 
        "filters": {
            # "Division": [form["Division"]],
            # "Department": [form["Department"]],
            # "Campus":[form["Department"]],
            # "Level": [form["Level"]],
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
    print(search_results)
    APIret = {
        "ECE444": { 
                "score": 3,
                "data": {
                    "Prerequisites":["abc"],
                    "Campus": ["Scarborough"],
                    "Division":["UofT Scarborough"],
                    "Department":["CS"],
                    "CourseID":["ECE444"],
                    "Description":["This is a Test"],
                    "Level": ["4"],
                    "Term":["2021 Fall"],
                    "Name":["Software Engineering"]
                }
        },
        "ENGB29": { 
                "score": 3,
                "data": {
                    "Prerequisites":["abc"],
                    "Campus": ["Scarborough"],
                    "Division":["UofT Scarborough"],
                    "Department":["CS", "ECE"],
                    "CourseID":["ENGB29H3"],
                    "Description":["(Calendar Reference)	This course is structured around the principle of the structure-property relationship. This relationship refers to an understanding of the microstructure of a solid, that is, the nature of the bonds between atoms and the spatial arrangement of atoms, which permits the explanation of observed behaviour. Observed materials behaviour includes mechanical, electrical, magnetic, optical, and corrosive behaviour. Topics covered in this course include: structure of the atom, models of the atom, electronic configuration, the electromagnetic spectrum, band theory, atomic bonding, optical transparency of solids, magnetic properties, molecular bonding, hybridized orbitals, crystal systems, lattices and structures, crystallographic notation, imperfections in solids, reaction rates, activation energy, solid-state diffusion, materials thermodynamics, free energy, and phase equilibrium."],
                    "Level": ["4"],
                    "Term":["2021 Fall"],
                    "Name":["Software Engineering"]
                }
        }
    }
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
        # course = json.loads(df.loc[code].to_json())
        # comments =[
        #     {
        #         "user":"Tony",
        #         "message":"Hello, this is Tony!",
        #         "like": 1,
        #         "time":datetime.datetime(2020, 5, 5).strftime("%m/%d/%Y")
        #     },
        #     {
        #         "user":"Tony2",
        #         "message":"Hello, this is Tony2!",
        #         "like": 3,
        #         "time":datetime.datetime(2021, 4, 9).strftime("%m/%d/%Y")
        #     }
        # ]
        
        url = "https://smpwfjd6r5.execute-api.us-east-1.amazonaws.com/default/discussionTable"
        params1 = {
                "action": "GetComments",
                "courseID": code
        }

        r = requests.get(url, headers=headers, data=json.dumps(params1))
        comments = json.loads(r.text)
        comments.sort(key = lambda x:x['NumLikes'], reverse=True)

    return render_template('course.html', course=sorted_course, comments=comments, code=code, course_name=course_name)

@app.route('/course/<code>/enroll')
def enroll_course(code):
    print(f"Enroll {code} is called!")
    form = request.form
    #------------Make API Call---------------
    return redirect(url_for("course", code=code))


@app.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):
    print(f"Add comment of {code} is called!")
    
    form = request.form
    print(form.to_dict())
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
    print(res.status_code)
    # course = json.loads(res.text)[code]["data"]
    #------------Make API Call---------------
    return redirect(url_for("course", code=code))


@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        if request.form.get("add_new"):
    		# do something
            print("Add New")
        elif request.form.get("delete_current"):
			# do something else
            print("Delete Current")
        return redirect(url_for("enroll"))
    
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
    return render_template('user.html', name=None)





if __name__ == '__main__':
    app.run(debug=True)
