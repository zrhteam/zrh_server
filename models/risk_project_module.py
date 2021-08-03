from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.mysql import BIT
from ops import db



class RiskProjectModule(db.Model):
    __tablename__ = 'risk_project_module'
    __table_args__ = (
        db.Index('ep', 'module_code', 'project_code'),
    )

    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(32, 'utf8_bin'), info='组件序号/编码')
    module_name = db.Column(db.String(32, 'utf8_bin'), info='设备名称')
    project_code = db.Column(db.String(32, 'utf8_bin'), info='项目编码')
    unit = db.Column(db.String(32, 'utf8_bin'), info='单位')
    quantity = db.Column(db.BigInteger, info='工程量')
    check_quantity = db.Column(db.BigInteger, info='检测量')
    check_scale = db.Column(db.Numeric(18, 2), info='检测比例')
    mark = db.Column(db.String(100, 'utf8_bin'), info='备注')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1))
    version = db.Column(db.Integer, server_default=db.FetchedValue(), info='乐观锁')