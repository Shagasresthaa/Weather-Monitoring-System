from flask import Flask
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/weather.db'
db = SQLAlchemy(app)

class NodeListAndStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f"wstat(id={id},status={status})"

db.create_all()

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(HelloWorld,"/helloworld")

if __name__ == '__main__':
    app.run(debug=True)    