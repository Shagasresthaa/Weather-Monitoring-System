'''
Weather Monitoring System using cost effective Weather nodes
Copyright (C) 2020  Shaga Sresthaa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>

The full text of the GNU General Public License version 3 can be found in the
source code root directory as COPYING.txt.

The full text of the GNU General Public License version 3 can be found in the
source code root directory as COPYING.txt.
'''

#############################################
#   @Title  Admin Dashboard Code
#   @author Shaga Sresthaa
#############################################

from flask import Flask, redirect, url_for, render_template, request, session, flash
import requests as rq
import pandas as pd
import json
import csv
from datetime import timedelta

MODE = True

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.permanent_session_lifetime = timedelta(minutes=5)

murl = "https://weather-main17.herokuapp.com/"

# App Methods


def getWeatherData(nodeId):
    surl = murl + "getWtData/" + nodeId
    data = rq.get(surl)
    dt = data.json()
    findt = json.dumps(dt["data"], indent=4)
    dt1 = json.loads(findt)
    filePath = "static/data_files/" + str(nodeId) + ".csv"
    csvfile = open(filePath, 'w', newline='')

    with csvfile:
        header = ['date_time', 'humd', 'id',
                  'location', 'pres', 'temp', 'uvindex']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for i in dt1:
            writer.writerow(i)

    df = pd.read_csv(filePath)
    findata = df[["date_time", "temp", "pres", "humd", "uvindex"]]
    temp = findata.to_dict('records')
    columnNames = findata.columns.values
    return temp, columnNames


def getNodesList():
    url = murl + "getNodes"
    data = rq.get(url)
    nodeData = data.json()
    nodeListStr = json.dumps(nodeData["nodes"], indent=4)
    nodeList = json.loads(nodeListStr)
    return nodeList


def getNodesCount():
    url = murl + "getNodes"
    data = rq.get(url)
    nodeData = data.json()
    nodeListStr = json.dumps(nodeData["nodes"], indent=4)
    nodeList = json.loads(nodeListStr)
    findt1 = json.dumps(nodeData["total_nodes"], indent=4)
    dt11 = json.loads(findt1)
    nodeCount = int(dt11)
    return nodeCount


def checkAuth(mailid, mpasswd):
    url = murl + "authUser/" + mailid + "/" + mpasswd
    dt = rq.get(url)
    rsp = dt.json()
    return rsp[0]['data']['accept_login_request']


def userRegistration(name, email, password):
    url = murl + "regUser/" + name + "/" + email + "/" + password
    dt = rq.get(url)
    rsp = dt.json()
    result = int(rsp['status_code'])
    print(rsp['status_code'])
    return result

# App Routing


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['memail']
        passwd = request.form['mpasswd']
        if(checkAuth(email, passwd)):
            session.permanent = True
            session["user"] = email
            return redirect(url_for("home"))

    else:
        if "user" in session:
            return redirect(url_for("home"))

        return render_template("index.html")


@app.route('/home')
def home():
    if "user" in session:
        user = session["user"]

        ncount = getNodesCount()

        return render_template("main.html", nodesCount=ncount)
    else:
        return render_template("index.html")


@app.route('/logout')
def logoutUser():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def registerUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['memail']
        passwd = request.form['mpasswd']
        res = userRegistration(name, email, passwd)
        print(res)
        if(res == 201):
            flash("Successfully Registered")
            return render_template("index.html")
        else:
            flash("Registration failed. Please try again")
            redirect(url_for("registerUser"))

    else:
        if "user" in session:
            return redirect(url_for("home"))

    return render_template("register.html")


@app.route('/home/nodeDataTables', methods=['GET', 'POST'])
def dataTables():
    if request.method == "POST":
        nodeSelVal = request.form.get('nodeId')
        nds = getNodesList()
        rcords, cols = getWeatherData(nodeSelVal)
        return render_template("datatables.html", nodeList=nds, records=rcords, colnames=cols)

    else:
        if "user" in session:
            user = session["user"]
            nds = getNodesList()
            return render_template("datatables.html", nodeList=nds)
        else:
            return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=MODE, port=8009, threaded=True)
