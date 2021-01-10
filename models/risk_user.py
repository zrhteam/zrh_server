from ops import db


class RiskUser(db.Model):
    __tablename__ = 'risk_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    user_grant = db.Column(db.String(25))
    headquarter_tag = db.Column(db.String(100))
    region_tag = db.Column(db.String(100))
    project_tag = db.Column(db.String(100))

