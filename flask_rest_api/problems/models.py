from .. import db

class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.Integer(), primary_key=True, nullable=False, autoincrement=True)  # defaults to auto inc
    question = db.Column(db.String(100), nullable=False)
    answer= db.Column(db.String(100), nullable=False)
    distraction1=db.Column(db.String(100))
    distraction2=db.Column(db.String(100))
    distraction3=db.Column(db.String(100))
    distraction4=db.Column(db.String(100))
    distraction5=db.Column(db.String(100))

    db.Index('qindex', question) #speed up filtering
