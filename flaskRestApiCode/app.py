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
#   @Title  Weather Data Management API Code
#   @author Shaga Sresthaa
#############################################

from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models import (nodeList, Stats, WeatherNodeData)
import json

MODE = True
CREATE_DB = False

app = Flask(__name__)
api = Api(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


class createNode(Resource):
    def get(self, id, loc):
        data = nodeList(id, loc)
        db.session.add(data)
        db.session.commit()
        return {"status_code": "200", "action_status": "successful"}


class postData(Resource):
    def get(self, id, loc, dtime, temp, pres, humd, alti, uvid):
        data = WeatherNodeData(id, loc, dtime, temp, pres, humd, alti, uvid)
        db.session.add(data)
        db.session.commit()
        return {"status_code": "200", "action_status": "successful"}


class postStatus(Resource):
    def get(self, id, status):
        data = Stats(id, status)
        db.session.add(data)
        db.session.commit()
        return{"status_code": "200", "dev_id": id, "dev_status": status, "post_Status": "Successful"}


class getStatus(Resource):
    def get(self):
        data = db.session.query(Stats.id, Stats.status).all()
        return {"status_code": "200", "device_statuses": data}


class listApiData(Resource):
    def get(self):
        return{"status_code": "200", "API_Version": "1.0.0", "author": "Shaga Sresthaa", "License": "GPL v3.0"}


api.add_resource(listApiData, "/apiInfo")
api.add_resource(getStatus, "/getStatus")
api.add_resource(postStatus, "/postStatus/<int:id>/<string:status>")
api.add_resource(createNode, "/createNode/<int:id>/<string:status>")
api.add_resource(
    postData, "/postData/<int:id>/<string:loc>/<string:dtime>/<float:temp>/<float:pres>/<float:humd>/<float:alti>/<float:uvid>")

if __name__ == '__main__':
    app.run(debug=MODE)
