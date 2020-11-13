import decimal
from datetime import datetime
from uuid import UUID

from flask import Flask, make_response, json, jsonify, redirect, url_for, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, MetaData, Numeric, String
from sqlalchemy.dialects.mysql.types import BIT
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import *

import requests
import pymysql
import os
import pdb
from datetime import datetime

# import test

data = [
    {"id": 1, "username": "小明", "password": "123", "role": 0, "sex": 0, "telephone": "10086", "address": "北京市海淀区"},
    {"id": 2, "username": "李华", "password": "abc", "role": 1, "sex": 0, "telephone": "10010", "address": "广州市天河区"},
    {"id": 3, "username": "大白", "password": "666666", "role": 0, "sex": 1, "telephone": "10000", "address": "深圳市南山区"}
]

app = Flask(__name__,
            static_folder="./templates/vuetest/dist/dist",  # 设置静态文件夹目录
            template_folder="./templates/vuetest/dist"  # 设置vue编译输出目录dist文件夹，为Flask模板文件目录
            )

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示

# 生成秘钥
app.secret_key = os.urandom(24)

# #用于连接数据库的URI                  数据库类型   账号密码    ip     端口   数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://data2:zruih2ZRH@!@47.92.250.148/riskapply'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://liqian:password@10.20.36.64:3306/zrh_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 创建一个管理数据库对象,注意参数需要和app产生联系
db = SQLAlchemy(app)  # SQLAlchemy语言的映射关系


# 定义risk_module模型
# Remind: 如果是已有的表，一定要 1）变量名和列名相等；2）Column的属性要一致。
# TODO: 把列取表的写到同一个文件里面
class RiskModule(db.Model):
    # 表名
    __tablename__ = 'risk_module_converted'
    # ID
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    # 组件名称
    component_name = db.Column(db.TEXT)
    # 所属设备名称
    belonged_equipment = db.Column(db.TEXT)

    def __repr__(self):
        return "system_module id = {}, component_name = {}, belonged_equipment = {}".format(repr(self.id),
                                                                                            repr(self.component_name),
                                                                                            repr(
                                                                                                self.belonged_equipment)
                                                                                            )
        # return {"id": repr(self.id), "component_name": repr(self.component_name), "belonged_equipment": repr(self.belonged_equipment)}

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict


# class RiskProject(test.OutputMixin, db.Model):
#     __tablename__ = 'risk_project'
#
#     id = db.Column(db.BigInteger, primary_key=True)
#     code = Column(String(255, 'utf8_bin'), info='项目编码')
#     name = Column(String(255, 'utf8_bin'), info='项目名称')
#     ctr_code = Column(String(255, 'utf8_bin'), info='合同编码')
#     ctr_codes = Column(String(255, 'utf8_bin'), info='合同父级编码')
#     cust_code = Column(String(32, 'utf8_bin'), info='客户编码')
#     feature = Column(String(255, 'utf8_bin'), info='项目特征')
#     status = Column(String(1, 'utf8_bin'), info='项目状态 0:立项 1:首次会议 2:专业报告 3:末次会议 4:已归档')
#     pro_leader_code = Column(String(32, 'utf8_bin'), info='项目负责人/项目组长')
#     pro_leader_name = Column(String(40, 'utf8_bin'), info='项目组长名字')
#     province_code = Column(String(10, 'utf8_bin'), info='省编码')
#     province_name = Column(String(20, 'utf8_bin'), info='省名称')
#     city_code = Column(String(10, 'utf8_bin'), info='市编码')
#     city_name = Column(String(20, 'utf8_bin'), info='市名')
#     district_code = Column(String(10, 'utf8_bin'), info='区域编码')
#     district_name = Column(String(20, 'utf8_bin'), info='区域名')
#     address = Column(String(100, 'utf8_bin'), info='详细地址')
#     full_address = Column(String(255, 'utf8_bin'), info='完整地址')
#     lng = Column(Float(10), info='经度')
#     lat = Column(Float(10), info='维度')
#     leader_phone = Column(String(32, 'utf8_bin'), info='组长/负责人手机号')
#     plan_start_time = Column(DateTime, info='预计开始时间')
#     plan_end_time = Column(DateTime, info='预计结束时间')
#     type = Column(String(2, 'utf8_bin'), info='检查类型 1:A类检查 2:B类检查  3:C类检查 4:其他类')
#     frist_meetting_file_id = Column(String(255, 'utf8_bin'), info='首次会议文件id')
#     professional_report_file_ids = Column(String(255, 'utf8_bin'))
#     end_meeting_file_id = Column(String(255, 'utf8_bin'), info='末次文件id')
#     general_report_file_id = Column(String(255, 'utf8_bin'), info='综合报告')
#     check_unit = Column(String(32, 'utf8_bin'), info='检查单位')
#     amount = Column(Numeric(18, 2, asdecimal=False), info='项目金额')
#     note = Column(String(500, 'utf8_bin'), info='项目概况')
#     create_time = Column(DateTime, info='创建时间')
#     create_user = Column(BigInteger, info='创建人')
#     update_time = Column(DateTime)
#     update_user = Column(BigInteger, info='更新人')
#     del_ind = Column(BIT(1))
#     version = Column(Integer, server_default=FetchedValue(), info='乐观锁')
#     unit_key = Column(String(36, 'utf8_bin'), info='唯一标识，用于树形结构')
#
#     def to_dict(self, rel=None, backref=None, exclude=()):
#         if rel is None:
#             rel = self.RELATIONSHIPS_TO_DICT
#         res = {column.key: getattr(self, attr)
#                for attr, column in self.__mapper__.c.items()
#                if column.key not in exclude}
#         if rel:
#             for attr, relation in self.__mapper__.relationships.items():
#                 # Avoid recursive loop between to tables.
#                 if backref == relation.table:
#                     continue
#                 value = getattr(self, attr)
#                 if value is None:
#                     res[relation.key] = None
#                 elif isinstance(value.__class__, DeclarativeMeta):
#                     res[relation.key] = value.to_dict(backref=self.__table__)
#                 else:
#                     res[relation.key] = [i.to_dict(backref=self.__table__)
#                                          for i in value]
#         return res
#
#     def to_json(self, rel=None, exclude=None):
#         def extended_encoder(x):
#             if isinstance(x, datetime):
#                 return x.isoformat()
#             if isinstance(x, UUID):
#                 return str(x)
#         if rel is None:
#             rel = self.RELATIONSHIPS_TO_DICT
#         return json.dumps(self.to_dict(rel, exclude=exclude),
#                           default=extended_encoder)


class RiskProject(db.Model):
    __tablename__ = 'risk_project'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(255, 'utf8_bin'), info='项目编码')
    name = db.Column(db.String(255, 'utf8_bin'), info='项目名称')
    ctr_code = db.Column(db.String(255, 'utf8_bin'), info='合同编码')
    ctr_codes = db.Column(db.String(255, 'utf8_bin'), info='合同父级编码')
    cust_code = db.Column(db.String(32, 'utf8_bin'), info='客户编码')
    feature = db.Column(db.String(255, 'utf8_bin'), info='项目特征')
    status = db.Column(db.String(1, 'utf8_bin'), info='项目状态 0:立项 1:首次会议 2:专业报告 3:末次会议 4:已归档')
    pro_leader_code = db.Column(db.String(32, 'utf8_bin'), info='项目负责人/项目组长')
    pro_leader_name = db.Column(db.String(40, 'utf8_bin'), info='项目组长名字')
    province_code = db.Column(db.String(10, 'utf8_bin'), info='省编码')
    province_name = db.Column(db.String(20, 'utf8_bin'), info='省名称')
    city_code = db.Column(db.String(10, 'utf8_bin'), info='市编码')
    city_name = db.Column(db.String(20, 'utf8_bin'), info='市名')
    district_code = db.Column(db.String(10, 'utf8_bin'), info='区域编码')
    district_name = db.Column(db.String(20, 'utf8_bin'), info='区域名')
    address = db.Column(db.String(100, 'utf8_bin'), info='详细地址')
    full_address = db.Column(db.String(255, 'utf8_bin'), info='完整地址')
    lng = db.Column(db.Float(10), info='经度')
    lat = db.Column(db.Float(10), info='维度')
    leader_phone = db.Column(db.String(32, 'utf8_bin'), info='组长/负责人手机号')
    plan_start_time = db.Column(db.DateTime, info='预计开始时间')
    plan_end_time = db.Column(db.DateTime, info='预计结束时间')
    type = db.Column(db.String(2, 'utf8_bin'), info='检查类型 1:A类检查 2:B类检查  3:C类检查 4:其他类')
    frist_meetting_file_id = db.Column(db.String(255, 'utf8_bin'), info='首次会议文件id')
    professional_report_file_ids = db.Column(db.String(255, 'utf8_bin'))
    end_meeting_file_id = db.Column(db.String(255, 'utf8_bin'), info='末次文件id')
    general_report_file_id = db.Column(db.String(255, 'utf8_bin'), info='综合报告')
    check_unit = db.Column(db.String(32, 'utf8_bin'), info='检查单位')
    amount = db.Column(db.Numeric(18, 2), info='项目金额')
    note = db.Column(db.String(500, 'utf8_bin'), info='项目概况')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1))
    version = db.Column(db.Integer, server_default=db.FetchedValue(), info='乐观锁')
    unit_key = db.Column(db.String(36, 'utf8_bin'), info='唯一标识，用于树形结构')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict


class RiskPrjDangerRecord(db.Model):
    __tablename__ = 'risk_prj_danger_record'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32, 'utf8_bin'), nullable=False, unique=True, info='隐患编码')
    danger_library_code = db.Column(db.String(32, 'utf8_bin'), info='隐患库编码')
    project_code = db.Column(db.String(255, 'utf8_bin'), info='项目编码')
    project_name = db.Column(db.String(255, 'utf8_bin'), info='项目名称')
    danger_number = db.Column(db.Integer, info='隐患数量')
    major_code = db.Column(db.String(32, 'utf8_bin'), info='专业编码')
    major_name = db.Column(db.String(255, 'utf8_bin'), info='专业名称')
    system_code = db.Column(db.String(32, 'utf8_bin'), info='系统编码')
    major_sort = db.Column(db.String(255, 'utf8_bin'), info='专业排序')
    system_name = db.Column(db.String(20, 'utf8_bin'), info='系统名称')
    system_sort = db.Column(db.String(255, 'utf8_bin'), info='系统排序')
    equipment_code = db.Column(db.String(32, 'utf8_bin'), info='设备编码')
    equipment_name = db.Column(db.String(20, 'utf8_bin'), info='设备名称')
    module_code = db.Column(db.String(32, 'utf8_bin'), info='组件编码')
    module_name = db.Column(db.String(20, 'utf8_bin'), info='组件名称')
    note = db.Column(db.String(255, 'utf8_bin'), info='隐患描述')
    position = db.Column(db.String(255, 'utf8_bin'), info='隐患地点/位置')
    risk_level = db.Column(db.String(1, 'utf8_bin'), info='风险等级 1:低风险 2:中风险 3:高风险')
    area = db.Column(db.String(32, 'utf8_bin'), info='分布区域')
    stage = db.Column(db.String(32, 'utf8_bin'), info='致因阶段 0:设计 1:运营 2:施工 3:装修')
    images_file_id = db.Column(db.String(100, 'utf8_bin'), info='隐患图片文件id,多个逗号隔开')
    write_person = db.Column(db.String(32, 'utf8_bin'), info='录入人')
    write_person_name = db.Column(db.String(32, 'utf8_bin'), info='录入人姓名')
    state = db.Column(db.String(1, 'utf8_bin'), info='状态 1：待整改，2：整改中，3：复查中，4：复查不合格，5：合格已完成')
    frequency = db.Column(db.Integer, info='出现频率')
    voice_time = db.Column(db.Integer, info='录音长度（秒）')
    voice_file_id = db.Column(db.String(100, 'utf8_bin'), info='语音文件id')
    confirm_file_id = db.Column(db.BigInteger, info='手写确认图片')
    confirm_person = db.Column(db.String(32, 'utf8_bin'), info='确认人')
    confirm_person_tel = db.Column(db.String(20, 'utf8_bin'), info='手写确认人电话')
    mark = db.Column(db.String(100, 'utf8_bin'), info='备注')
    upload_time = db.Column(db.DateTime, info='上传时间')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1))
    version = db.Column(db.Integer, server_default=db.FetchedValue(), info='乐观锁')
    appflag = db.Column(db.String(32, 'utf8_bin'), info='appflag')
    rule_code = db.Column(db.String(100, 'utf8_bin'), info='法规编号')
    rule_name = db.Column(db.String(1024, 'utf8_bin'), info='法规名称')
    rule_standard = db.Column(db.String(255, 'utf8_bin'), info='法规标准')
    clause = db.Column(db.String(100, 'utf8_bin'), info='相关条款')
    clause_contact = db.Column(db.String(1024, 'utf8_bin'), info='条款内容')
    rectify_advise = db.Column(db.String(1024, 'utf8_bin'), info='整改建议')
    dangerNote = db.Column(db.String(1024, 'utf8_bin'), info='隐患库的隐患描述')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


# overview页面地图部分
# @app.route('/api/overview', methods=['POST'])
# def overview():
#     error = None
#     # DEBUG
#     res = db.session.query(RiskProject).limit(1).all()
#     print(res)
#     ret = []
#     for x in res:
#         ret.append(x.to_json())
#     print(ret)
#     return json.dumps(ret)


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


# overview页面根据项目名称查询
@app.route('/api/overview_prjname', methods=['POST'])
def overview_prjname():
    print("In function overview_getLocation")
    # res = db.session.query(RiskProject.id, RiskProject.code, RiskProject.lng, RiskProject.lat).all()
    res = db.session.query(RiskProject).all()
    result = []
    for risk_prj in RiskProject:
        result.append(risk_prj.to_json())
    print("res")
    print(res)
    # return jsonify(json_list=res)
    return json.dumps(result)
    # ...........................
    # actual func..
    # error = None
    # res = db.session.query(RiskProject).limit(1).all()
    # print(res)
    # ret = []
    # for x in res:
    #     ret.append(x.to_json())
    # print(ret)
    # return json.dumps(ret)
    # ...........................
    # if request.method == 'POST' and request.form.get("project_name"):
    #     datax = request.form.get("project_name")
    #     print(datax)
    #     return jsonify({'msg': '没问题'})
    # return jsonify({'msg': '出错了'})


#  overview页面地图部分
#
#  FunctionName: getLocation
#  Purpose:      初始化时得到每个项目的经纬度
#  Parameter:    null
#  Return:       包含经纬度的json
@app.route('/api/overview', methods=['POST'])
def overview_get_location():
    print("In function overview_get_location")
    start_t = datetime.now()
    result = RiskProject.query.limit(100).all()
    actual_data = {}
    cnt = 0
    print(len(result))
    for item in result:
        if str(item.code) not in actual_data.keys():
            print("handle..." + str(cnt))
            cnt += 1
            tmp_data = {'id': item.id, "longitude": item.lng, "latitude": item.lat, "risk_level": {1: 0, 2: 0, 3: 0}}
            risk_result = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            for ele in risk_result:
                # print(ele.risk_level)
                if ele.risk_level == "1":
                    tmp_data["risk_level"][1] += 1
                elif ele.risk_level == "2":
                    tmp_data["risk_level"][2] += 1
                elif ele.risk_level == "3":
                    tmp_data["risk_level"][3] += 1
                else:
                    print("Unexpected result")
            actual_data[str(item.code)] = tmp_data
    print("Returned data: ")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    # return jsonify(json_list=res)
    return jsonify(actual_data)


#  overview页面地图部分
#
#  FunctionName: getPrjPie
#  Purpose:      展示每个项目各风险等级对应的数量
#  Parameter:    所有项目code
#  Return:       风险等级及其对应数量
@app.route('/api/overview_pie', methods=['POST'])
def overview_get_prj_pie():
    prj_code = request.form.get("project_code")
    print(prj_code)
    print("In function overview_get_prj_pie")

    result = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == str(prj_code)).all()
    print(result)
    actual_data = {1: 0, 2: 0, 3: 0}
    for item in result:
        print(item.risk_level)
        if item.risk_level == "1":
            actual_data[1] += 1
        elif item.risk_level == "2":
            actual_data[2] += 1
        elif item.risk_level == "3":
            actual_data[3] += 1
        else:
            print("Unexpected value!")
            # Entry.query.filter_by(uuid=uuid).first_or_404()
    print("Returned data: ")
    print(actual_data)
    # print("res")
    # print(res)
    return jsonify(actual_data)


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitIndexData
# Purpose: 初始化页面显示不同专业（消防、电梯、电气、燃气）的危险指数
# Parameter: null
# Return: 包含消防、电梯、电气、燃气危险指数的json文件
#
# 初始化页面需要数据：消防危险指数、电梯危险指数、电气危险指数、燃气危险指数
@app.route('/api/land_ehs_screen_top_left', methods=['POST'])
def ehs_get_init_index_data():
    print("In function ehs_get_init_index_data")
    # result = RiskPrjDangerRecord.query.all()
    # total_index = 0
    # for item in result:
    #     total_index += item.danger
    return None


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRectification
# Purpose: 初始化页面显示总部整改率
# Parameter: null
# Return: 包含总部整改率数据的json文件
@app.route('/api/land_ehs_screen_rectification', methods=['POST'])
def ehs_get_init_rectification():
    print("In function ehs_get_init_rectification")
    result_total = RiskPrjDangerRecord.query.all()
    result_ok = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.state == 1).all()
    total = len(result_total)
    ok = len(result_ok)
    # for item in result:
    #     if item.state == "1":
    #         ok += 1
    print("Returned data: ")
    print(str(ok * 100 / total) + "%")
    return jsonify({"rectification_rate": str(ok * 100 / total) + "%"})


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskLevelData
# Purpose: 初始化页面显示隐患风险等级高、中、低风险及其对应的累计隐患数量
# Parameter: null
# Return: 风险等级及对应的累计隐患数量的json文件
@app.route('/api/land_ehs_screen_top_right', methods=['POST'])
def ehs_get_init_risk_level_data():
    print("In function ehs_get_init_risk_level_data")
    result = RiskPrjDangerRecord.query.all()
    actual_data = {1: 0, 2: 0, 3: 0}
    for item in result:
        if item.risk_level == "1":
            actual_data[1] += 1
        elif item.risk_level == "2":
            actual_data[2] += 1
        elif item.risk_level == "3":
            actual_data[3] += 1
        else:
            print("Unexpected value")
    print("Returned data: ")
    print(actual_data)
    return jsonify(actual_data)
# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskIndexData
# Purpose: 初始化页面显示根据项目综合&专业风险指数排序的结果
# Parameter: null
# Return: 根据项目综合&专业风险指数排序后的项目名称的json文件

# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskNumberRank
# Purpose: 初始化页面得到按照高风险数量排名的项目名称
# Parameter: null
# Return: 对高风险数量排序后的项目名称json文件

# 置地总部EHS数据大屏页面
#
# FunctionName: getInitImage
# Purpose: 初始化时得到所有项目未整改高风险隐患图片
# Parameter: null
# Return: 返回包含未整改高风险图片的json文件

# 置地总部EHS数据大屏页面
#
# FunctionName: getInitNumberTop
# Purpose: 初始化页面得到所有项目中出现隐患数量排名前10的隐患
# Parameter: null
# Return: 包含在置地总部所有项目中隐患数量排名前10的隐患描述的json文件

# overview页面右侧初始化数据加载
@app.route('/api/overview_right_init', methods=['POST'])
def overview_right_init():
    error = None
    if request.method == 'POST':
        return jsonify({'msg': '没问题'})
    return jsonify({'msg': '出错了'})


@app.route('/api/land_headquarters', methods=['POST'])
def land_headquarters():
    error = None
    if request.method == 'POST':
        return jsonify({'msg': '没问题'})
    return jsonify({'msg': '出错了'})


@app.route('/api/search_module', methods=['POST'])
def search_module():
    error = None
    if request.method == 'POST' and request.form.get("component_name"):
        datax = request.form.to_dict()
        component_namex = datax.get("component_name")
        # DEBUG
        print(component_namex)
        res = RiskModule.query.filter_by(component_name=component_namex).all()
        ret = []
        for x in res:
            ret.append(x.to_json())
            # print(ret)
        print(ret)
        return jsonify(ret)
    return jsonify({'msg': '出错了'})


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100),
        'abc': 123
    }
    return jsonify(response)


@app.route('/api/random')
def pie_chart():
    return jsonify(data)


@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        datax = request.form.to_dict()
        usernamex = datax.get("username")
        passwordx = datax.get("password")
        print(usernamex, passwordx)
        if usernamex and passwordx:
            for da in data:
                if da.get('username') == usernamex and da.get('password') == passwordx:
                    response = {'code': 200, 'msg': usernamex + '您好，恭喜登录成功！'}
                    print(response)
                    return jsonify(response)
                # return redirect(url_for('login'), 200)
            return jsonify({"code": 1002, "msg": "用户名或密码错误！！！"})
    else:
        return jsonify({"code": 1001, "msg": "用户名或密码不能为空！！！"})


# @app.route('/', methods=['GET'])
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# def read_json(json_name):
#     filename = json_name + '.json'
#     try:
#         with open('/' + filename) as f:
#             jsonStr = json.load(f)
#             return json.dumps(jsonStr)
#     except Exception as e:
#         return jsonify({"code": "异常", "message": "{}".format(e)})

# def index():
def catch_all(path):
    print(ret)
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    # return render_template("index.html")
    return "hello world"
    # name='index')  # 使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。


CORS(app, supports_credentials=True)


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))
@app.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    # return jsonify({"code":"0", "data":data, "msg":"操作成功"})
    return data


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id > 0 and user_id <= len(data):
        return jsonify({"code": "0", "data": data[user_id - 1], "msg": "操作成功"})
    return jsonify({"code": "1", "msg": "用户不存在"})


@app.route("/register", methods=['POST', 'GET'])
def user_register():
    username = request.values.get("username")
    password = request.values.get("password")
    # dd["username"] = request.json.get("username").strip()
    # dd["password"] = request.json.get("password").strip()
    # if dd["username"] and dd["password"] and dd["telephone"]:
    if username and password:
        import re
        if username == "wintest":
            # if dd["username"] == "wintest":
            # for da in data:
            #     if da.get('username') == dd["username"] and da.get('password') == dd["password"] and da.get('telephone') == dd["telephone"]:
            return jsonify({"code": 2002, "msg": "用户名已存在！！！"})
        else:
            # data.append(dd)
            return jsonify({"code": 200, "msg": "恭喜，注册成功！"})
    else:
        return jsonify({"code": 2001, "msg": "用户名/密码不能为空，请检查！！！"})


if __name__ == '__main__':
    app.run(debug=True)
