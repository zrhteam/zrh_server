from ops import db
from sqlalchemy.dialects.mysql.types import BIT


class SysFile(db.Model):
    __tablename__ = 'sys_files'

    id = db.Column(db.BigInteger, primary_key=True)
    tags = db.Column(db.String(32, 'utf8_bin'), info='业务编码')
    directory = db.Column(db.String(255, 'utf8_bin'), info='储存路径')
    name = db.Column(db.String(255, 'utf8_bin'), info='文件名')
    type = db.Column(db.Integer, info='文件类型：1文档、2图片、3影音')
    suffix = db.Column(db.String(32, 'utf8_bin'), info='文件后缀')
    upload_host = db.Column(db.String(32, 'utf8_bin'))
    source_id = db.Column(db.BigInteger, info='来源')
    url = db.Column(db.String(255, 'utf8_bin'))
    size = db.Column(db.BigInteger, info='大小')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1))
    version = db.Column(db.Integer, server_default=db.FetchedValue(), info='乐观锁')
