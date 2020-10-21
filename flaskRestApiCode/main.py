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
'''

#############################################
#   @Title  Weather Data Management API Code
#   @author Shaga Sresthaa
#############################################

from flask import Flask
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/weather.db'
db = SQLAlchemy(app)

class NodeListAndStatus(db.Model):
    id = db.Column('id',db.Integer, primary_key=True)
    status = db.Column('status',db.String(30), nullable = False)

    def __repr__(self):
        return f"wstat(id={id},status={status})"

db.create_all()

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(HelloWorld,"/helloworld")

if __name__ == '__main__':
    app.run(debug=True)    