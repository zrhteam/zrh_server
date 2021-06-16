from sqlalchemy.dialects.mysql import BIT

from ops import db

class FinalTag(db.Model):
    __tablename__ = 'final_tag'

    id = db.Column(db.BigInteger, primary_key=True, server_default=db.FetchedValue())
    code = db.Column(db.String(255, 'utf8_bin'), info='项目编码')
    name = db.Column(db.String(255, 'utf8_bin'), info='项目名称')
    feature = db.Column(db.String(255, 'utf8_bin'), info='项目特征')
    plan_start_time = db.Column(db.DateTime, info='预计开始时间')
    plan_end_time = db.Column(db.DateTime, info='预计结束时间')
    check_hide_tag = db.Column(db.String(100))
    project_tag = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    project_hide_tag = db.Column(db.String(100))
    region_tag = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    region_hide_tag = db.Column(db.String(100))
    headquarter_tag = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    headquarter_hide_tag = db.Column(db.String(100))
    remark = db.Column(db.String(100))