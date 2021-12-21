from app import db

class arrangement(db.Model):
    id_arrangement=db.Column(db.Integer,primary_key=True)
    start_date=db.Column(db.DateTime(),nullable=False)
    end_date=db.Column(db.DateTime(),nullable=False)
    description=db.Column(db.String(),nullable=False)
    destination=db.Column(db.String(),nullable=False)
    capacity=db.Column(db.Integer(),nullable=False)
    price=db.Column(db.Integer(),nullable=False)

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


class Users(db.Model):
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
