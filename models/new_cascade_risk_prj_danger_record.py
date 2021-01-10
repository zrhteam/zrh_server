from ops import db


class NewCascadeRiskPrjDangerRecord(db.Model):
    __tablename__ = 'new_cascade_risk_prj_danger_record'

    project_code = db.Column(db.String(255, 'utf8_bin'), info='项目编码')
    project_name = db.Column(db.String(255, 'utf8_bin'), info='项目名称')
    project_tag = db.Column(db.String(255))
    region_tag = db.Column(db.String(255))
    headquarter_tag = db.Column(db.String(255))
    profession_tag = db.Column(db.String(255))
    major_name = db.Column(db.String(255, 'utf8_bin'), info='专业名称')
    system_name = db.Column(db.String(20, 'utf8_bin'), info='系统名称')
    note = db.Column(db.String(255, 'utf8_bin'), info='隐患描述')
    danger_number = db.Column(db.Integer, info='隐患数量')
    risk_level = db.Column(db.String(1, 'utf8_bin'), info='风险等级 1:低风险 2:中风险 3:高风险')
    state = db.Column(db.String(1, 'utf8_bin'), info='状态 1：待整改，2：整改中，3：复查中，4：复查不合格，5：合格已完成')
    create_time = db.Column(db.DateTime, info='创建时间')
    images_file_id = db.Column(db.String(100, 'utf8_bin'), info='隐患图片文件id,多个逗号隔开')
    stage = db.Column(db.String(32, 'utf8_bin'), info='致因阶段 0:设计 1:运营 2:施工 3:装修')
    area = db.Column(db.String(32, 'utf8_bin'), info='分布区域')
    lng = db.Column(db.Float(10), info='经度')
    lat = db.Column(db.Float(10), info='维度')
    plan_start_time = db.Column(db.DateTime, info='预计开始时间')
    plan_end_time = db.Column(db.DateTime, info='预计结束时间')
    id = db.Column(db.Integer, primary_key=True)