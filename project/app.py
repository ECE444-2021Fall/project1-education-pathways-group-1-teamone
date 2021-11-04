from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
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
year = [
    t for t in set(df['Course Level'].values)
]


app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
bootstrap = Bootstrap(app)
selections = {
    "Divisions":divisions,
    "Departments":departments,
    "Campus":campus,
    "Year":year
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    
    if request.method == 'POST':
        return results(request.form)
    
    return render_template('search.html', selections=selections)


def results(form):
    # table = df.loc[:, ["Course","Name", "Division"]][:4]
    # table = table.to_html(classes='data',index=False,na_rep='',render_links=True, escape=False)
    # print(form.to_dict())
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
            # "Level": [form["Year"]],
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
    print(params)
    res = requests.get(url, headers=headers, data=json.dumps(params))

    search_results = json.loads(res.text)
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

    return render_template('results.html', selections=selections, search_results = search_results)

@app.route('/course/<code>')
def course(code):
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
        print(res.status_code)
        print(res.text)
        course = json.loads(res.text)[code]["data"]
        # course = json.loads(df.loc[code].to_json())
        comments =[
            {
                "user":"Tony",
                "message":"Hello, this is Tony!",
                "like": 1,
                "time":datetime.datetime(2020, 5, 5).strftime("%m/%d/%Y")
            },
            {
                "user":"Tony2",
                "message":"Hello, this is Tony2!",
                "like": 3,
                "time":datetime.datetime(2021, 4, 9).strftime("%m/%d/%Y")
            }
        ]
    return render_template('course.html', course=course, comments=comments, code=code)

@app.route('/course/<code>/add_comment', methods=['POST'])
def add_comment(code):
    print(f"Add comment of {code} is called!")
    return redirect(url_for("course", code=code))


@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return render_template('user.html', name=None)


if __name__ == '__main__':
    app.run(debug=True)
