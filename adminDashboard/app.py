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

from flask import Flask, redirect, url_for, render_template, request, session
import requests as rq
import json
from datetime import timedelta

MODE = True

app = Flask(__name__)
# app.config.from_pyfile('config.py')
app.secret_key = "dzXNPaFQAA17prfcCVZd"
app.permanent_session_lifetime = timedelta(minutes=5)

# App Routing

murl = "https://weather-main17.herokuapp.com/"
dbgurl = "http://127.0.0.1:5000/"


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['memail']
        passwd = request.form['mpasswd']
        if(checkAuth(email, passwd)):
            session.permanent = True
            session["user"] = email
            return redirect(url_for("user"))

    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("index.html")


@app.route('/home')
def user():
    if "user" in session:
        user = session["user"]
        return render_template("main.html")
    else:
        return render_template("index.html")


@app.route('/logout')
def logoutUser():
    session.pop("user", None)
    return render_template("index.html")


def checkAuth(mailid, mpasswd):
    url = dbgurl + "authUser/" + mailid + "/" + mpasswd
    dt = rq.get(url)
    rsp = dt.json()
    return rsp[0]['data']['accept_login_request']


if __name__ == "__main__":
    app.run(debug=MODE, port=8009)
