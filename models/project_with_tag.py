from ops import db


class PrjWithTag(db.Model):
    __tablename__ = 'prj_with_tag'

    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(100))
    province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    project_name = db.Column(db.String(255))
    project_character = db.Column(db.String(255))
    customer_name = db.Column(db.String(255))
    project_tag = db.Column(db.String(255))
    region_tag = db.Column(db.String(255))
    headquarter_tag = db.Column(db.String(255))
    profession_tag = db.Column(db.String(255))