from sqlalchemy.dialects.postgresql import JSON
from flask import Flask, json,jsonify,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:marko@localhost/data_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)

class users(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    last_name=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(255),nullable=False)
    username=db.Column(db.String(255),nullable=False)
    password=db.Column(db.String(255),nullable=False)
    acc_type=db.Column(db.Integer,nullable=False)
    

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()