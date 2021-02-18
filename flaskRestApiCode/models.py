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
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(50))
    dtime = db.Column(db.DateTime)
    temp = db.Column(db.Float)
    pres = db.Column(db.Float)
    humd = db.Column(db.Float)
    alti = db.Column(db.Float)
    uvid = db.Column(db.Float)

    def __init__(self, id, loc, dtime, temp, pres, humd, alti, uvid):
        self.id = id
        self.loc = loc
        self.dtime = dtime
        self.temp = temp
        self.pres = pres
        self.humd = humd
        self.alti = alti
        self.uvid = uvid
