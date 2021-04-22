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

from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models import (nodeList, Stats, WeatherNodeData,
                    adminAccessTable, requestHist)
from models import db as db1
import json
import datetime as dt
import uuid
from random import randint
from flask_cors import CORS, cross_origin

MODE = False
CREATE_DB = False

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

if(CREATE_DB):
    with app.app_context():
        db1.create_all()


class postData(Resource):
    def get(self, rqid, mac_id, id, loc, dtime, temp, pres, humd, uvid):
        isValidRequest = checkReq(rqid, mac_id, id)
        tm = str(dtime)
        datetimeSplit = tm.split("+")
        findtime = datetimeSplit[0] + " " + datetimeSplit[1]
        if(isValidRequest):
            data = WeatherNodeData(rqid, id, loc, findtime,
                                   temp, pres, humd, uvid)
            dt = {'request_id': rqid, 'mac_id': mac_id, 'node_id': id, 'location': loc, 'date_and_time': findtime,
                  'recorded_temperature': temp, 'recorded_presure': pres, 'recorded_humidity': humd, 'recorded_uv_index': uvid}
            db.session.add(data)
            db.session.commit()
            return jsonify({"status_code": 201, "action_status": "successful", "data": dt})

        else:
            return jsonify({"status_code": 403, "action_status": "Invalid Request"})


class postStatus(Resource):
    def get(self, id, status, mac_id):
        data = Stats(id, status, mac_id)
        db.session.add(data)
        db.session.commit()
        return jsonify({"status_code": 201, "dev_id": id, "dev_status": status, "dev_mac_id": mac_id, "post_Status": "Successful"})


class getStatus(Resource):
    def get(self, nid):
        data = db.session.query(Stats.id, Stats.status).filter_by(id=nid)

        for lst in data:
            resp = {"status_code": 200, "node_id": nid,
                    "node_status": lst.status}

        return resp


class listApiData(Resource):
    def get(self):
        return jsonify({"status_code": "200", "API_Version": "1.3.0", "Author": "Shaga Sresthaa", "License": "GPL v3.0"})


class sendWeatherData(Resource):
    def get(self, nid):
        data = db.session.query(
            WeatherNodeData.id, WeatherNodeData.loc, WeatherNodeData.dtime, WeatherNodeData.temp, WeatherNodeData.pres, WeatherNodeData.humd, WeatherNodeData.uvid).filter_by(id=nid).order_by(WeatherNodeData.dtime)
        list1 = []
        for lst in data:

            txt = {'id': str(lst.id), 'date_time': str(lst.dtime), 'location': str(lst.loc), 'temp': str(
                lst.temp), 'pres': str(lst.pres), 'humd': str(lst.humd), 'uvindex': str(lst.uvid)}

            list1.append(txt)

        response = jsonify({"status_code": 200, "data": list1})
        return response


def idGenerator():
    rid = uuid.uuid4().hex
    return rid


def checkDuplicate(rndId):
    data = db.session.query(requestHist.rqid).filter_by(rqid=rndId).count()

    if(data == 0):
        return False
    else:
        return True


def checkNodeRequestValidity(nid, mac_id):
    data = db.session.query(nodeList.id, nodeList.mac_id).filter_by(id=nid)

    isValid = False

    for lst in data:

        if(lst.id == nid and lst.mac_id == mac_id):
            isValid = True
        else:
            isValid = False

    return isValid


def sendReqId():
    reqd = idGenerator()

    while(checkDuplicate(reqd)):
        reqd = idGenerator()

    return reqd


def checkReq(rqid, macAddr, nid):
    data = db.session.query(
        requestHist.rqid, requestHist.mac_id, requestHist.id).filter_by(rqid=rqid)
    for lst in data:
        if(lst.rqid == rqid and lst.mac_id == macAddr and lst.id == nid):
            return True

        else:
            return False


def checkDuplicateId(nid):
    data = db.session.query(nodeList.id).filter_by(id=nid).count()
    if(data == 0):
        return False
    else:
        return True


def idGenForNode():
    nid = randint(1000000, 9999999)
    return nid


def nidGenerator():
    nid = idGenForNode()
    while(checkDuplicateId(nid)):
        nid = idGenForNode()

    return nid


def checkNodeCreation(nid, mc_id):
    data = db.session.query(nodeList.id, nodeList.mac_id).filter_by(id=nid)

    for lst in data:
        if(lst.id == nid and lst.mac_id == mc_id):
            return True
        else:
            return False


def checkUserCreation(usid, usemail, uspasswd):
    data = db.session.query(adminAccessTable.id,
                            adminAccessTable.uemail,
                            adminAccessTable.passwd,
                            adminAccessTable.admin).filter_by(id=usid)

    for lst in data:
        if(lst.id == usid and lst.uemail == usemail and lst.passwd == uspasswd):
            return True

    return False


class reqIdGen(Resource):
    def get(self, nid, mac_id):
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        isValid = checkNodeRequestValidity(nid, mac_id)

        if(isValid):
            requestId = sendReqId()
            data = requestHist(requestId, nid, now, mac_id)
            db.session.add(data)
            db.session.commit()
            response = jsonify({"status_code": 200, "dtime": str(
                now), "node_id": nid, "reqid": requestId})

        else:
            response = jsonify(
                {"status_code": 403, "status": "Invalid Request"})

        return response


def userIdGenerator():
    num = idGenerator()
    data = db.session.query(adminAccessTable.id).filter_by(id=num).count()
    if(data == 0):
        return num
    else:
        userIdGenerator()


def checkUserPresence(unames, mailid):
    mailcount = db.session.query(adminAccessTable.uemail).filter_by(
        uemail=mailid).count()
    namecount = db.session.query(adminAccessTable.uemail).filter_by(
        nm=unames).count()
    if(mailcount > 0 or namecount > 0):
        return False
    else:
        return True


class nodeIdGenerator(Resource):
    def get(self, loc, mac_id):

        nodeId = nidGenerator()

        data = nodeList(nodeId, loc, mac_id)
        db.session.add(data)
        db.session.commit()

        if(checkNodeCreation(nodeId, mac_id)):
            return jsonify({"status_code": 201, "node_reg_status": "node registered successfully", "assigned_node_id": nodeId})
        else:
            return jsonify({"status_code": 424, "node_reg_status": "node registration failed"})


class loginManager(Resource):
    def get(self, mail, passwd):
        data = db.session.query(adminAccessTable.uemail,
                                adminAccessTable.passwd,
                                adminAccessTable.nm,
                                adminAccessTable.admin).filter_by(uemail=mail)

        for lst in data:
            if(lst.uemail == mail and lst.passwd == passwd and lst.admin):
                return jsonify({"status_code": 200, "data": {"auth_status": "authenticated", "name": lst.nm, "admin_status": "True", "accept_login_request": True}}, 200)
            elif(lst.uemail == mail and lst.passwd == passwd and not lst.admin):
                return jsonify({"status_code": 200, "data": {"auth_status": "authenticated", "name": lst.nm, "admin_status": "False", "accept_login_request": True}}, 200)
            else:
                return jsonify({"status_code": 403, "data": {"auth_status": "not authenticated", "accept_login_request": False}}, 403)


class registerUser(Resource):
    def get(self, name, mail, passwd):
        uid = userIdGenerator()
        if(checkUserPresence(name, mail)):
            data = adminAccessTable(uid, name, mail, passwd, False)
            db.session.add(data)
            db.session.commit()
            if(checkUserCreation(uid, mail, passwd)):
                return jsonify({"status_code": 201, "user_reg_status": "user registered successfully", "assigned_user_id": uid})
            else:
                return jsonify({"status_code": 424, "user_reg_status": "user registration failed"})
        else:
            return jsonify({"status_code": 403, "user_reg_status": "user with same name or email already exists"})


class listAllNodes(Resource):
    def get(self):
        nodedata = db.session.query(nodeList).all()
        nodecount = db.session.query(nodeList.id).count()
        nodes = []

        for lst in nodedata:
            nodes.append(str(lst.id))

        return jsonify({"status_code": 201, "nodes": nodes, "total_nodes": str(nodecount)})


api.add_resource(listAllNodes, "/getNodes")
api.add_resource(
    registerUser, "/regUser/<string:name>/<string:mail>/<string:passwd>")
api.add_resource(loginManager, "/authUser/<string:mail>/<string:passwd>")
api.add_resource(nodeIdGenerator, "/nodeCreate/<string:loc>/<string:mac_id>")
api.add_resource(reqIdGen, "/getReqIdAuth/<int:nid>/<string:mac_id>")
api.add_resource(listApiData, "/apiInfo")
api.add_resource(sendWeatherData, "/getWtData/<int:nid>")
api.add_resource(getStatus, "/getStatus/<int:nid>")
api.add_resource(
    postStatus, "/postStatus/<int:id>/<string:status>/<string:mac_id>")
api.add_resource(
    postData, "/postData/<string:rqid>/<string:mac_id>/<int:id>/<string:loc>/<string:dtime>/<float:temp>/<float:pres>/<float:humd>/<float:uvid>")

if __name__ == '__main__':
    app.run(debug=MODE, threaded=True)
