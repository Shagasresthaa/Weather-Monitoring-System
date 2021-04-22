from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    mac_id = db.Column(db.String(17), unique=True)

    def __init__(self, id, status, mac_id):
        self.id = id
        self.status = status
        self.mac_id = mac_id


class nodeList(db.Model):
    __tablename__ = 'nodelist'
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(50))
    mac_id = db.Column(db.String(17), unique=True)

    def __init__(self, id, loc, mac_id):
        self.id = id
        self.loc = loc
        self.mac_id = mac_id


class WeatherNodeData(db.Model):
    __tablename__ = "weathernodedata"
    rqid = db.Column(db.String(32), primary_key=True)
    id = db.Column(db.Integer)
    loc = db.Column(db.String(50))
    dtime = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    pres = db.Column(db.Float)
    humd = db.Column(db.Float)
    uvid = db.Column(db.Float)

    def __init__(self, rqid, id, loc, dtime, temp, pres, humd, uvid):
        self.rqid = rqid
        self.id = id
        self.loc = loc
        self.dtime = dtime
        self.temp = temp
        self.pres = pres
        self.humd = humd
        self.uvid = uvid


class adminAccessTable(db.Model):
    __tablename__ = "adminDashTable"
    id = db.Column(db.String(32), primary_key=True)
    nm = db.Column(db.String(100), unique=True)
    uemail = db.Column(db.String(100), unique=True)
    passwd = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __init__(self, id, nm, uemail, passwd, admin):
        self.id = id
        self.nm = nm
        self.uemail = uemail
        self.passwd = passwd
        self.admin = admin


class requestHist(db.Model):
    __tablename__ = "requestHistTable"
    rqid = db.Column(db.String(32), primary_key=True)
    id = db.Column(db.Integer)
    dtime = db.Column(db.DateTime)
    mac_id = db.Column(db.String(17))

    def __init__(self, reqid, id, dtime, mac_id):
        self.rqid = reqid
        self.id = id
        self.dtime = dtime
        self.mac_id = mac_id
