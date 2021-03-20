from ops import db


class UserGrantChart(db.Model):
    __tablename__ = 'user_grant_chart'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(100))
    title = db.Column(db.String(100))
    object1 = db.Column(db.String(10000))
    object2 = db.Column(db.String(10000))
    user_name = db.Column(db.String(200))

    def __init__(self, id, level, title, object1, object2, user_name):
        self.id = id
        self.level = level
        self.title = title
        self.object1 = object1
        self.object2 = object2
        self.user_name = user_name
