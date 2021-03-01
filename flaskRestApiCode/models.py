from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))

    def __init__(self, id, status):
        self.id = id
        self.status = status


class nodeList(db.Model):
    __tablename__ = 'nodelist'
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(50))

    def __init__(self, id, loc):
        self.id = id
        self.loc = loc


class WeatherNodeData(db.Model):
    __tablename__ = "weathernodedata"
    rqid = db.Column(db.String(15), primary_key=True)
    id = db.Column(db.Integer)
    loc = db.Column(db.String(50))
    dtime = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    pres = db.Column(db.Float)
    humd = db.Column(db.Float)
    alti = db.Column(db.Float)
    uvid = db.Column(db.Float)

    def __init__(self, rqid, id, loc, dtime, temp, pres, humd, alti, uvid):
        self.rqid = rqid
        self.id = id
        self.loc = loc
        self.dtime = dtime
        self.temp = temp
        self.pres = pres
        self.humd = humd
        self.alti = alti
        self.uvid = uvid


class adminAccessTable(db.Model):
    __tablename__ = "adminDashTable"
    id = db.Column(db.Integer, primary_key=True)
    nm = db.Column(db.String(100))
    admStat = db.Column(db.Boolean)

    def __init__(self, id, nm, admStat):
        self.id = id
        self.nm = nm
        self.admStat = admStat


class requestHist(db.Model):
    __tablename__ = "requestHistTable"
    rqid = db.Column(db.String(15), primary_key=True)
    id = db.Column(db.Integer)
    dtime = db.Column(db.DateTime)

    def __init__(self, reqid, id, dtime):
        self.rqid = reqid
        self.id = id
        self.dtime = dtime
