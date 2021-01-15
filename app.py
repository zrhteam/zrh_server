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
import time, datetime

import requests
import pymysql
import os
import pdb
from datetime import datetime

# import test
from functions.file_reader import get_scatter, get_top_k, get_trend, get_correlation

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


class RiskCustomer(db.Model):
    __tablename__ = 'risk_customer'

    id = db.Column(db.BigInteger, primary_key=True, info='主键')
    name = db.Column(db.String(40, 'utf8_bin'), nullable=False, info='姓名')
    code = db.Column(db.String(40, 'utf8_bin'), nullable=False, info='编码')
    password = db.Column(db.String(40, 'utf8_bin'), nullable=False)
    role_ids = db.Column(db.String(1024, 'utf8_bin'), info='角色')
    type = db.Column(db.String(2, 'utf8_bin'), info='类型')
    phone = db.Column(db.String(20, 'utf8_bin'), nullable=False, info='电话')
    province_code = db.Column(db.String(10, 'utf8_bin'), info='省编码')
    province_name = db.Column(db.String(20, 'utf8_bin'), info='省名')
    city_code = db.Column(db.String(10, 'utf8_bin'), info='市编码')
    city_name = db.Column(db.String(20, 'utf8_bin'), info='市名')
    district_code = db.Column(db.String(10, 'utf8_bin'), info='区域编码')
    district_name = db.Column(db.String(20, 'utf8_bin'), info='区域名')
    full_address = db.Column(db.String(255, 'utf8_bin'))
    address = db.Column(db.String(255, 'utf8_bin'), info='详细地址')
    contacts1 = db.Column(db.String(40, 'utf8_bin'), info='联系人')
    contacts1_tel = db.Column(db.String(20, 'utf8_bin'), info='联系人电话')
    contacts2 = db.Column(db.String(40, 'utf8_bin'), info='备用联系人')
    contacts2_tel = db.Column(db.String(20, 'utf8_bin'), info='备用联系人电话')
    note = db.Column(db.String(255, 'utf8_bin'), info='备注')
    is_enable = db.Column(BIT(1), info='是否启用：0禁用 1启用')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1), info='是否删除:0未删除 1删除')
    version = db.Column(db.Integer, server_default=db.FetchedValue(), info='版本')


class RiskContract(db.Model):
    __tablename__ = 'risk_contract'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(32, 'utf8_bin'), info='合同编码')
    name = db.Column(db.String(255, 'utf8_bin'), info='合同名称')
    pcode = db.Column(db.String(255, 'utf8_bin'), info='父合同编码')
    pcodes = db.Column(db.String(255, 'utf8_bin'), info='所有父级code')
    type = db.Column(db.String(2, 'utf8_bin'), info='合同类型 1:开口合同  2:闭口合同')
    level = db.Column(db.Integer, info='层级')
    contract_body = db.Column(db.String(32, 'utf8_bin'), info='签约主体')
    our_contractor = db.Column(db.String(100, 'utf8_bin'), info='我方签约人')
    cust_code = db.Column(db.String(32, 'utf8_bin'), info='客户名称')
    amount = db.Column(db.Numeric(18, 2), info='合同金额')
    escalation = db.Column(db.Numeric(18, 2), info='合同调差')
    settlement_amount = db.Column(db.Numeric(18, 2), info='结算金额')
    recepit_amount = db.Column(db.Numeric(18, 2))
    start_time = db.Column(db.DateTime, info='合同执行起始日')
    end_time = db.Column(db.DateTime, info='合同执行结束日')
    files_ids = db.Column(db.String(255, 'utf8_bin'), info='附件文件id')
    mark = db.Column(db.String(100, 'utf8_bin'), info='说明')
    create_time = db.Column(db.DateTime, info='创建时间')
    create_user = db.Column(db.BigInteger, info='创建人')
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.BigInteger, info='更新人')
    del_ind = db.Column(BIT(1), info='删除标识 0:未删除  1:已删除')
    version = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='乐观锁')
    unit_key = db.Column(db.String(36, 'utf8_bin'), info='唯一标识，用于树形结构')


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


# overview页面地图部分
#
# FunctionName: getProjectionMap
# Purpose:      初始化保存三种code的对应关系
# Parameter:    null
# Return:       code对应关系的map
@app.route('/api/overview_get_projection_map', methods=['POST'])
def overview_get_projection_map():
    print("In function overview_get_projection_map")
    start_t = datetime.now()
    actual_data = {}
    customer_info = RiskCustomer.query.all()
    idx = 0
    for item in customer_info:
        print("idx: " + str(idx))
        idx += 1
        actual_data[item.name] = {}
        contract_info = RiskContract.query.filter(RiskContract.cust_code == item.code).all()
        for ele in contract_info:
            actual_data[item.name][ele.name] = []
            project_info = RiskProject.query.filter(RiskProject.ctr_code == ele.code).all()
            for i in project_info:
                actual_data[item.name][ele.name].append(i.name)

    print("Returned data: ")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
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
    start_t = datetime.now()
    print(request.form)
    cust_name = request.form.get("cust_name")
    # cust_name = "华润置地华东大区"
    print("Received cust_name: " + str(cust_name))
    cust_code = RiskCustomer.query.filter(RiskCustomer.name == cust_name).first()
    sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
    state_ok = 0
    state_nok = 0
    for ele in sub_code:
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for i in q_all_code:
            if i.state == "5":
                state_ok += 1
            else:
                state_nok += 1
    rate = str((state_ok * 100) / (state_ok + state_nok)) + "%"
    print("rate" + str(rate))
    actual_data = {"rectification_rate": str(rate)}
    print("Returned data: ")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    # print(str(ok * 100 / total) + "%")
    return jsonify(actual_data)


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskLevelData
# Purpose: 初始化页面显示隐患风险等级高、中、低风险及其对应的累计隐患数量
# Parameter: null
# Return: 风险等级及对应的累计隐患数量的json文件
@app.route('/api/land_ehs_screen_top_right', methods=['POST'])
def ehs_get_init_risk_level_data():
    print("In function ehs_get_init_risk_level_data")
    start_t = datetime.now()
    cust_name = request.form.get("cust_name")
    # cust_name = "华润置地华东大区"
    print("Received cust_code: " + str(cust_name))
    actual_data = {"risk_level": {1: 0, 2: 0, 3: 0}}
    cust_code = RiskCustomer.query.filter(RiskCustomer.name == cust_name).first()
    print(cust_code.name)
    sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
    idx = 0
    for ele in sub_code:
        # print(idx)
        idx += 1
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for i in q_all_code:
            if i.risk_level == "1":
                actual_data["risk_level"][1] += 1
            elif i.risk_level == "2":
                actual_data["risk_level"][2] += 1
            elif i.risk_level == "3":
                actual_data["risk_level"][3] += 1
    print("Returned data: ")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskIndexData
# Purpose: 初始化页面显示根据项目综合&专业风险指数排序的结果
# Parameter: null
# Return: 根据项目综合&专业风险指数排序后的项目名称的json文件
@app.route('/api/land_ehs_screen_index_rank', methods=['POST'])
def ehs_get_init_risk_index_data():
    return jsonify({})


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitRiskNumberRank
# Purpose: 初始化页面得到按照高风险数量排名的项目名称
# Parameter: null
# Return: 对高风险数量排序后的项目名称json文件
@app.route('/api/land_ehs_screen_risk_number', methods=['POST'])
def ehs_get_init_risk_number_rank():
    print("In function ehs_get_init_risk_number_rank")
    start_t = datetime.now()
    cust_name = request.form.get("cust_name")
    print("Received cust_code: " + str(cust_name))
    # cust_name = "华润置地华东大区"
    actual_data = {}
    cust_code = RiskCustomer.query.filter(RiskCustomer.name == cust_name).first()
    sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
    idx = 0
    for ele in sub_code:
        print(idx)
        idx += 1
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        cnt = 0
        for i in q_all_code:
            if i.risk_level == "3":
                cnt += 1
        actual_data[ele.code] = cnt
    res = sorted(actual_data.items(), key=lambda d: d[1], reverse=True)
    actual_data = {}
    idx = 1
    for ele in res:
        actual_data[ele[0]] = {"rank": idx, "high_risk_count": ele[1]}
        idx += 1
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitImage
# Purpose: 初始化时得到所有项目未整改高风险隐患图片
# Parameter: null
# Return: 返回包含未整改高风险图片的json文件
# TODO: Query time is to large, need to polish.
@app.route('/api/land_ehs_screen_image', methods=['POST'])
def ehs_get_init_image():
    print("In function ehs_get_init_image")
    start_t = datetime.now()
    cust_name = request.form.get("cust_name")
    print("Received cust_code: " + str(cust_name))
    # cust_name = "华润置地华东大区"
    actual_data = {}
    cust_code = RiskCustomer.query.filter(RiskCustomer.name == cust_name).first()
    sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
    idx = 0
    for ele in sub_code:
        print(idx)
        idx += 1
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        image_list = []
        for i in q_all_code:
            get_image = SysFile.query.filter(SysFile.id == i.images_file_id).first()
            image_url = get_image.upload_host + get_image.directory + get_image.name
            image_list.append(image_url)
        actual_data[ele.code] = image_list
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 置地总部EHS数据大屏页面
#
# FunctionName: getInitNumberTop
# Purpose: 初始化页面得到所有项目中出现隐患数量排名前10的隐患
# Parameter: null
# Return: 包含在置地总部所有项目中隐患数量排名前10的隐患描述的json文件
@app.route('/api/data_ehs_screen_top10', methods=['POST'])
def ehs_get_init_number_top():
    print("In function ehs_get_init_number_top")
    start_t = datetime.now()
    cust_name = request.form.get("cust_name")
    print("Received cust_code: " + str(cust_name))
    # cust_name = "华润置地华东大区"
    cust_code = RiskCustomer.query.filter(RiskCustomer.name == cust_name).first()
    actual_data = {}
    sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
    idx = 0
    for ele in sub_code:
        print(idx)
        idx += 1
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for i in q_all_code:
            if i.note not in actual_data.keys():
                actual_data[i.note] = 0
            actual_data[i.note] += 1
    res = sorted(actual_data.items(), key=lambda d: d[1], reverse=True)
    print(res)
    actual_data = {}
    idx = 1
    for ele in res:
        actual_data[ele[0]] = {"rank": idx, "appear_time": ele[1]}
        idx += 1
        if idx == 11:
            break
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)

# overview页面右侧初始化数据加载
# @app.route('/api/data_ehs_screen_top10', methods=['POST'])
# def ehs_get_init_number_top():
#     print("In function ehs_get_init_risk_number_rank")
#     cust_code = "SCYH"
#     actual_data = {}
#     sub_code = RiskProject.query.filter(RiskProject.cust_code == cust_code).all()
#     idx = 0
#     for ele in sub_code:
#         print(idx)
#         idx += 1
#         q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()


# 地产事业部页面
#
# FunctionName: getRegionInitIndex
# Purpose: 初始化页面显示总的安全指数以及不同专业的安全指数
# Parameter: null
# Return: 包含总体安全指数、消防指数、电梯指数、燃气指数、电气指数的json文件
@app.route('/api/region_index', methods=['POST'])
def estate_get_region_init_index():
    print("In function estate_get_region_init_index")
    return jsonify({})


# 地产事业部页面
#
# FunctionName: getInitRegionProjectNumber
# Purpose: 初始化页面展示目前已检查的项目数量
# Parameter: null
# Return: 包含当前已检查项目数量的json文件
@app.route('/api/region_project_number', methods=['POST'])
def estate_get_init_region_project_number():
    print("In function estate_get_init_region_project_number")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    # for ele in sub_code:
    actual_data = {"project_num": str(len(sub_code))}
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionRiskLevel
# Purpose: 初始化页面展示不同风险等级及其对应的累计发现隐患数量
# Parameter: null
# Return: 包含高、中、低风险对应的累计发现隐患数量的json文件
@app.route('/api/region_project_risk_level', methods=['POST'])
def estate_get_init_region_risk_level():
    print("In function estate_get_init_region_risk_level")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {"risk_level": {1: 0, 2: 0, 3: 0}}
    for ele in sub_code:
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.risk_level == "1":
                actual_data["risk_level"][1] += 1
            elif item.risk_level == "2":
                actual_data["risk_level"][2] += 1
            elif item.risk_level == "3":
                actual_data["risk_level"][3] += 1
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionHighRisk
# Purpose: 初始化页面展示当前未整改高风险隐患描述列表
# Parameter:null
# Return: 包含当前未整改的高风险隐患描述的json文件
@app.route('/api/region_project_high_risk', methods=['POST'])
def estate_get_init_region_high_risk():
    print("In function estate_get_init_region_high_risk")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {"note_list": []}
    for ele in sub_code:
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.risk_level == "3" and item.state != "5":
                actual_data["note_list"].append(item.note)
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionImage
# Purpose: 初始化页面展示当前未整改高风险隐患图片
# Parameter: null
# Return: 包含未整改高风险隐患图片的json文件
@app.route('/api/region_project_Image', methods=['POST'])
def estate_get_init_region_image():
    print("In function estate_get_init_region_image")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {"image_list": []}
    for ele in sub_code:
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.risk_level == "3" and item.state != "5":
                get_image = SysFile.query.filter(SysFile.id == item.images_file_id).first()
                image_url = get_image.upload_host + get_image.directory + get_image.name
                actual_data["image_list"].append(image_url)
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionMajor
# Purpose: 初始化页面展示各个项目发现的不同风险等级隐患在不同专业上的分布
# Parameter: risk_level(高中低）
# Return: 包含按照项目+专业+风险等级聚类结果的json文件
@app.route('/api/region_major', methods=['POST'])
def estate_get_init_region_major():
    print("In function estate_get_init_region_major")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {}
    for ele in sub_code:
        project_map = {"major": {}}
        q_all_code = []
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.major_name not in project_map["major"].keys():
                project_map['major'][item.major_name] = {"1": 0, "2": 0, "3": 0}
            project_map['major'][item.major_name][item.risk_level] += 1
        actual_data[ele.code] = project_map
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionNumberTop
# Purpose: 初始化页面展示在所有项目中数量排名前10的隐患
# Parameter: null
# Return: 包含隐患数量在当前所有项目中排名前10的隐患描述的json文件
@app.route('/api/region_project_number_top', methods=['POST'])
def estate_get_init_region_number_top():
    print("In function estate_get_init_region_number_top")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {}
    for ele in sub_code:
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.note not in actual_data:
                actual_data[item.note] = 0
            actual_data[item.note] += 1
    res = sorted(actual_data.items(), key=lambda d: d[1], reverse=True)
    print(res)
    actual_data = {}
    idx = 1
    for ele in res:
        actual_data[ele[0]] = {"rank": idx, "appear_time": ele[1]}
        idx += 1
        if idx == 11:
            break
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 地产事业部页面
#
# FunctionName: getInitRegionSafetyIndex
# Purpose: 初始化页面展示按照项目安全指数排名的情况
# Parameter: null
# Return: 包含按照项目安全指数排序后的项目名称

# 地产事业部页面
#
# FunctionName: getInitRegionRiskRank
# Purpose: 初始化页面展示按照累计出现高风险数量排名的项目名称
# Parameter: null
# Return: 包含按照累计出现高风险数量排序后的项目名称
@app.route('/api/region_project_risk_rank', methods=['POST'])
def estate_get_init_region_risk_rank():
    print("In function estate_get_init_region_risk_rank")
    start_t = datetime.now()
    ctr_name = request.form.get("ctr_name")
    print("Received ctr_name: " + str(ctr_name))
    # ctr_name = "宋城壹号"
    ctr_code = RiskContract.query.filter(RiskContract.name == ctr_name).first()
    sub_code = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
    print("length of sub_code: " + str(len(sub_code)))
    actual_data = {}
    for ele in sub_code:
        actual_data[ele.name] = 0
        q_all_code = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == ele.code).all()
        for item in q_all_code:
            if item.risk_level == "3":
                actual_data[ele.name] += 1

    res = sorted(actual_data.items(), key=lambda d: d[1], reverse=True)
    print(res)
    actual_data = {}
    idx = 1
    for ele in res:
        actual_data[ele[0]] = {"rank": idx, "high_risk_count": ele[1]}
        idx += 1
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectIndex
# Purpose: 初始化页面展示项目危险指数和不同专业的指数
# Parameter: null
# Return: 包含项目危险指数、消防指数、电梯指数、燃气指数、电气指数的json文件
# TODO

# 项目级页面
#
# FunctionName: getInitProjectRectification
# Purpose: 初始化页面展示当前整改率
# Parameter: null
# Return: 包含当前项目整改率的json文件
@app.route('/api/region_project_rectification', methods=['POST'])
def project_get_init_project_rectification():
    # print("In function project_get_init_project_rectification")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    # print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    state_ok = 0
    for item in all_check:
        if item.state == "5":
            state_ok += 1
    actual_data = {"project_rectification": str((state_ok * 100) / len(all_check)) + "%"}
    # print("Returned result:")
    # print(actual_data)
    end_t = datetime.now()
    # print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectRiskNumber
# Purpose: 初始化页面展示历次发现的不同风险等级的隐患数量
# Parameter: null
# Return: 包含不同风险等级及其对应的历次发现的隐患数量的json文件
@app.route('/api/region_project_risk_number', methods=['POST'])
def project_get_init_project_risk_number():
    # print("In function project_get_init_project_risk_number")
    start_t = datetime.now()
    query_level = request.form.get("query_level") # can be cust or ctr
    # print("Received query_level: " + str(query_level))
    corresponding_name = ""
    if query_level == "cust":
        corresponding_name = request.form.get("cust_name")
    elif query_level == "ctr":
        corresponding_name = request.form.get("ctr_name")
    else:
        return jsonify({"msg": "Unexpected query level!"})
    # print("Received corresponding name: " + str(corresponding_name))

    # debug for cust
    # query_level = "cust"
    # corresponding_name = "华润置地华东大区"
    # debug for ctr
    # query_level = "ctr"
    # corresponding_name = "宋城壹号"
    actual_data = {}
    if query_level == "cust":
        cust_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            project_map = {"time": "", "1": 0, "2": 0, "3": 0}
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                start_time = time_stamp if time_stamp < start_time else start_time
                if ele.risk_level == "1":
                    project_map["1"] += 1
                elif ele.risk_level == "2":
                    project_map["2"] += 1
                elif ele.risk_level == "1":
                    project_map["3"] += 1
            # time_array = time.localtime(start_time)
            if start_time == 100000000000:
                project_map["time"] = "no record"
            else:
                # project_map["time"] = time.strftime("%Y-%m-%d", time_array)
                project_map["time"] = ''
            actual_data[item.name] = project_map
    elif query_level == "ctr":
        ctr_code = RiskContract.query.filter(RiskContract.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == ctr_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            project_map = {"time": "", "1": 0, "2": 0, "3": 0}
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                start_time = time_stamp if time_stamp < start_time else start_time
                if ele.risk_level == "1":
                    project_map["1"] += 1
                elif ele.risk_level == "2":
                    project_map["2"] += 1
                elif ele.risk_level == "1":
                    project_map["3"] += 1
            time_array = time.localtime(start_time)
            if start_time == 100000000000:
                project_map["time"] = "no record"
            else:
                project_map["time"] = time.strftime("%Y-%m-%d", time_array)
            actual_data[item.name] = project_map
    # print("Returned result:")
    # print(actual_data)
    end_t = datetime.now()
    # print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectNumberChange
# Purpose: 初始化页面展示历次检查隐患数量变化的情况
# Parameter: null
# Return: 包含历次检查的隐患数量的json文件
@app.route('/api/region_project_number_change', methods=['POST'])
def project_get_init_project_number_change():
    print("In function project_get_init_project_number_change")
    start_t = datetime.now()
    query_level = request.form.get("query_level") # can be cust or ctr
    print("Received query_level: " + str(query_level))
    corresponding_name = ""
    if query_level == "cust":
        corresponding_name = request.form.get("cust_name")
    elif query_level == "ctr":
        corresponding_name = request.form.get("ctr_name")
    else:
        return jsonify({"msg": "Unexpected query level!"})
    print("Received corresponding name: " + str(corresponding_name))

    # debug for cust
    # query_level = "cust"
    # corresponding_name = "华润置地华东大区华润置地华东大区"
    # debug for ctr
    # query_level = "ctr"
    # corresponding_name = "宋城壹号"
    actual_data = {}
    if query_level == "cust":
        cust_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            project_map = {"time": "", "risk_number": 0}
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                start_time = time_stamp if time_stamp < start_time else start_time
            project_map["risk_number"] = len(all_record)
            # time_array = time.localtime(start_time)
            if start_time == 100000000000:
                project_map["time"] = "no record"
            else:
                # project_map["time"] = time.strftime("%Y-%m-%d", time_array)
                project_map["time"] = "2020-07-18"
            actual_data[item.name] = project_map
    elif query_level == "ctr":
        ctr_code = RiskContract.query.filter(RiskContract.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == ctr_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            project_map = {"time": "", "risk_number": 0}
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                start_time = time_stamp if time_stamp < start_time else start_time
            project_map["risk_number"] = len(all_record)
            # time_array = time.localtime(start_time)
            if start_time == 100000000000:
                project_map["time"] = "no record"
            else:
                # project_map["time"] = time.strftime("%Y-%m-%d", time_array)
                project_map["time"] = ""
            actual_data[item.name] = project_map
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)

# 项目级页面
#
# FunctionName: getInitProjectNearestPerception
# Purpose: 初始化页面饼图展示最近一次检查不同专业隐患占比情况
# Parameter: null
# Return: 包含消防、电梯、电气、燃气4个专业在最近一次检查中发现隐患数量的json文件
@app.route('/api/region_project_Nearest', methods=['POST'])
def project_get_init_project_nearest_perception():
    print("In function project_get_init_project_number_change")
    start_t = datetime.now()
    query_level = request.form.get("query_level") # can be cust or ctr
    print("Received query_level: " + str(query_level))
    corresponding_name = ""
    if query_level == "cust":
        corresponding_name = request.form.get("cust_name")
    elif query_level == "ctr":
        corresponding_name = request.form.get("ctr_name")
    else:
        return jsonify({"msg": "Unexpected query level!"})
    print("Received corresponding name: " + str(corresponding_name))

    # debug for cust
    # query_level = "cust"
    # corresponding_name = "华润置地华东大区华润置地华东大区"
    # debug for ctr
    # query_level = "ctr"
    # corresponding_name = "宋城壹号"
    actual_data = {"time": "", "nearest_project_name": "", "major_list": {}}
    if query_level == "cust":
        cust_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
        project_name = ""
        idx = 1
        start_time = 100000000000
        str_time = ""
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                if time_stamp < start_time:
                    start_time = time_stamp
                    project_name = ele.project_name
            # time_array = time.localtime(start_time)
            if start_time == 100000000000:
                str_time = "no record"
            else:
                # str_time = time.strftime("%Y-%m-%d", time_array)
                str_time = ''
        if project_name == "":
            actual_data["nearest_project_name"] = "no record"
        else:
            actual_data["nearest_project_name"] = project_name
            get_record_by_prj_name = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_name == project_name).all()
            print("record length of nearest_project" + str(len(get_record_by_prj_name)))
            for ele in get_record_by_prj_name:
                if ele.major_name not in actual_data["major_list"].keys():
                    actual_data["major_list"][ele.major_name] = 0
                actual_data["major_list"][ele.major_name] += 1
        actual_data["time"] = str_time
    elif query_level == "ctr":
        ctr_code = RiskContract.query.filter(RiskContract.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == ctr_code.code).all()
        project_name = ""
        idx = 1
        start_time = 100000000000
        str_time = ""
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            for ele in all_record:
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                if time_stamp < start_time:
                    start_time = time_stamp
                    project_name = ele.project_name
            time_array = time.localtime(start_time)
            if start_time == 100000000000:
                str_time = "no record"
            else:
                str_time = time.strftime("%Y-%m-%d", time_array)
        if project_name == "":
            actual_data["nearest_project_name"] = "no record"
        else:
            actual_data["nearest_project_name"] = project_name
            get_record_by_prj_name = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_name == project_name).all()
            print("record length of nearest_project" + str(len(get_record_by_prj_name)))
            for ele in get_record_by_prj_name:
                if ele.major_name not in actual_data["major_list"].keys():
                    actual_data["major_list"][ele.major_name] = 0
                actual_data["major_list"][ele.major_name] += 1
        actual_data["time"] = str_time
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectHistoryPerception
# Purpose: 初始化页面饼图展示历次检查中不同专业隐患占比情况
# Parameter: null
# Return: 包含消防、电梯、电气、燃气4个专业在历次检查中发现的隐患数量的json文件
@app.route('/api/region_project_perception', methods=['POST'])
def project_get_init_project_history_perception():
    print("In function project_get_init_project_history_perception")
    start_t = datetime.now()
    query_level = request.form.get("query_level") # can be cust or ctr
    print("Received query_level: " + str(query_level))
    corresponding_name = ""
    if query_level == "cust":
        corresponding_name = request.form.get("cust_name")
    elif query_level == "ctr":
        corresponding_name = request.form.get("ctr_name")
    else:
        return jsonify({"msg": "Unexpected query level!"})
    print("Received corresponding name: " + str(corresponding_name))

    # debug for cust
    # query_level = "cust"
    # corresponding_name = "华润置地华东大区"
    # debug for ctr
    # query_level = "ctr"
    # corresponding_name = "宋城壹号"
    actual_data = {}
    if query_level == "cust":
        cust_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            actual_data[item.name] = {"time": start_time, "major_list": {}}
            for ele in all_record:
                if ele.major_name not in actual_data[item.name]["major_list"].keys():
                    actual_data[item.name]["major_list"][ele.major_name] = 0
                actual_data[item.name]["major_list"][ele.major_name] += 1
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                if time_stamp < start_time:
                    start_time = time_stamp
            # time_array = time.localtime(start_time)
            if start_time == 100000000000:
                actual_data[item.name]["time"] = "no record"
            else:
                # actual_data[item.name]["time"] = time.strftime("%Y-%m-%d", time_array)
                actual_data[item.name]["time"] = ''
    elif query_level == "ctr":
        ctr_code = RiskContract.query.filter(RiskContract.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == ctr_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            start_time = 100000000000
            actual_data[item.name] = {"time": start_time, "major_list": {}}
            for ele in all_record:
                if ele.major_name not in actual_data[item.name]["major_list"].keys():
                    actual_data[item.name]["major_list"][ele.major_name] = 0
                actual_data[item.name]["major_list"][ele.major_name] += 1
                create_time = str(ele.create_time).split(" ")[0]
                # print(create_time)
                time_array = time.strptime(create_time, "%Y-%m-%d")
                time_stamp = int(time.mktime(time_array))
                if time_stamp < start_time:
                    start_time = time_stamp
            time_array = time.localtime(start_time)
            if start_time == 100000000000:
                actual_data[item.name]["time"] = "no record"
            else:
                actual_data[item.name]["time"] = time.strftime("%Y-%m-%d", time_array)
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)

# 项目级页面
#
# FunctionName: getInitProjectRisk
# Purpose: 初始化页面展示当前未整改的高风险隐患列表
# Parameter: null
# Return: 包含当前未整改的高风险隐患描述的json文件
@app.route('/api/region_project_risk', methods=['POST'])
def project_get_init_project_risk():
    print("In function project_get_init_project_risk")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    actual_data = {"note_list": []}
    for item in all_check:
        if item.risk_level == "3" and item.state != "5":
            actual_data["note_list"].append(item.note)
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectImage
# Purpose: 初始化页面展示当前未整改高风险隐患图片
# Parameter: null
# Return: 包含当前未整改高风险隐患图片的json文件
@app.route('/api/region_project_image', methods=['POST'])
def project_get_init_project_image():
    print("In function project_get_init_project_image")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    actual_data = {"image_list": []}
    for item in all_check:
        if item.risk_level == "3" and item.state != "5":
            get_image = SysFile.query.filter(SysFile.id == item.images_file_id).first()
            image_url = get_image.upload_host + get_image.directory + get_image.name
            actual_data["image_list"].append(image_url)
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectSystem
# Purpose: 初始化页面展示不同专业所有隐患子系统占比情况
# Parameter: major（专业：消防、电梯、电气、燃气，all）
# Return: 包含在不同专业情况下属于不同隐患子系统的隐患数量的json文件
@app.route('/api/project_system', methods=['POST'])
def project_get_init_project_system():
    # print("In function project_get_init_project_system")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    # print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = []
    actual_data = {}
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    for item in all_check:
        if item.major_name not in actual_data.keys():
            actual_data[item.major_name] = {}
        if item.system_name not in actual_data[item.major_name].keys():
            actual_data[item.major_name][item.system_name] = 0
        actual_data[item.major_name][item.system_name] += 1
    # print("Returned result:")
    # print(actual_data)
    end_t = datetime.now()
    # print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectReason
# Purpose: 初始化页面展示所有隐患在不同专业情况下不同致因阶段的数量
# Parameter: major（专业：消防、电梯、电气、燃气，all）
# Return: 包含在不同专业情况下的隐患在不同致因（运营、施工等）阶段的数量的json文件
@app.route('/api/project_reason', methods=['POST'])
def project_get_init_project_reason():
    print("In function project_get_init_project_reason")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = []
    actual_data = {}
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    for item in all_check:
        # print(item.)
        stage = "not defined stage" if item.stage == '' else item.stage
        if item.major_name not in actual_data.keys():
            actual_data[item.major_name] = {}
        if stage not in actual_data[item.major_name].keys():
            actual_data[item.major_name][stage] = 0
        actual_data[item.major_name][stage] += 1
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectRegionDistribution
# Purpose: 初始化页面展示在不同专业情况下隐患区域分布情况
# Parameter: major（专业：消防、电梯、电气、燃气，all)
# Return: 包含在不同专业情况下不同区域的隐患数量的json文件
@app.route('/api/project_distribution', methods=['POST'])
def project_get_init_project_region_distribution():
    print("In function project_get_init_project_region_distribution")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    # project_name = "宋城壹号01"
    project_code = RiskProject.query.filter(RiskProject.name == project_name).first()
    all_check = []
    actual_data = {}
    all_check = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == project_code.code).all()
    for item in all_check:
        print(item.area)
        area = "not defined area" if item.area == '' else item.area
        if item.major_name not in actual_data.keys():
            actual_data[item.major_name] = {}
        if area not in actual_data[item.major_name].keys():
            actual_data[item.major_name][area] = 0
        actual_data[item.major_name][area] += 1
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# 项目级页面
#
# FunctionName: getInitProjectRiskTop
# Purpose: 初始化页面展示出现次数排前5的隐患以及所属专业和出现频率
# Parameter: null
# Return: 包含在历次检查中出现次数排前5的隐患描述及其所属专业和出现次数的json文件
@app.route('/api/region_project_risk_top', methods=['POST'])
def project_get_init_project_risk_top():
    print("In function project_get_init_project_risk_top")
    start_t = datetime.now()

    query_level = request.form.get("query_level") # can be cust or ctr
    print("Received query_level: " + str(query_level))
    corresponding_name = ""
    if query_level == "cust":
        corresponding_name = request.form.get("cust_name")
    elif query_level == "ctr":
        corresponding_name = request.form.get("ctr_name")
    else:
        return jsonify({"msg": "Unexpected query level!"})
    print("Received corresponding name: " + str(corresponding_name))

    # debug for cust
    # query_level = "cust"
    # corresponding_name = "华润置地华东大区"
    # debug for ctr
    # query_level = "ctr"
    # corresponding_name = "宋城壹号"
    actual_data = {}
    if query_level == "cust":
        cust_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.cust_code == cust_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            for ele in all_record:
                if ele.note not in actual_data.keys():
                    actual_data[ele.note] = {"appear_time": 0, "belonged_major": ele.major_name}
                actual_data[ele.note]["appear_time"] += 1
        res = sorted(actual_data.items(), key=lambda d: d[1]["appear_time"], reverse=True)
        print(res)
        actual_data = {}
        idx = 0
        for ele in res:
            actual_data[ele[0]] = ele[1]
            idx += 1
            if idx == 5:
                break
    elif query_level == "ctr":
        ctr_code = RiskCustomer.query.filter(RiskCustomer.name == corresponding_name).first()
        all_project = RiskProject.query.filter(RiskProject.ctr_code == ctr_code.code).all()
        idx = 1
        for item in all_project:  # for each project
            # 计算这个project的开始时间
            print("Processing project: " + str(idx))
            idx += 1
            all_record = RiskPrjDangerRecord.query.filter(RiskPrjDangerRecord.project_code == item.code).all()
            for ele in all_record:
                if ele.note not in actual_data.keys():
                    actual_data[ele.note] = {"appear_time": 0, "belonged_major": ele.major_name}
                actual_data[ele.note]["appear_time"] += 1
        res = sorted(actual_data.items(), key=lambda d: d[1]["appear_time"], reverse=True)
        print(res)
        actual_data = {}
        idx = 0
        for ele in res:
            actual_data[ele[0]] = ele[1]
            idx += 1
            if idx == 5:
                break
    print("Returned result:")
    print(actual_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(actual_data)


# Analyze相关页面
#
# FunctionName: analyzeGetMainChartData
# Purpose: 获取Insight用于渲染散点图
# Parameter: None
# Return: json -> list of (pid, x, y, type)
# Comments: 前端实现未完成
@app.route('/api/analyze/main', methods=['GET'])
def analyze_get_main_chart_data():
    print("In function analyze_get_main_chart_data")
    start_t = datetime.now()

    # insight_list = [(1, 1, 2, 'top1'), (2, 3, 4, 'trend'), (3, 4, 5, 'correlation')]
    insight_list = get_scatter()

    print("Returned result:")
    print(insight_list)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(insight_list)


# FunctionName: analyzeGetRefChartData
# Purpose: 获取Insight点击后出现的小图的数据
# Parameter: pid: insight的id, type: insight的种类
# Return: json
# Comments: 前端实现未完成
@app.route('/api/analyze/ref', methods=['GET'])
def analyze_get_ref_chart_data():
    print("In function analyze_get_ref_chart_data")
    pid = int(request.args.get("pid"))
    print("Received pid: " + str(pid))
    type_ = request.args.get("type")
    print("Received type: " + str(type_))
    start_t = datetime.now()

    res = {}
    if type_ == 'top1':
        y_coord_str, data_list = get_top_k(pid, 10)
        res['y_coord_str'] = y_coord_str
        res['data_list'] = [int(num) for num in data_list]
    elif type_ == 'trend':
        x_coord_str, y_coord_str, x_label_list, data_list = get_trend(pid)
        res['x_coord_str'] = x_coord_str
        res['y_coord_str'] = y_coord_str
        res['x_label_list'] = x_label_list
        res['data_list'] = [int(num) for num in data_list]
    elif type_ == 'correlation':
        x_coord_str, x_label_list, data_list = get_correlation(pid)
        res['x_coord_str'] = x_coord_str
        for item in data_list:
            item['list'] = [int(x) for x in item['list']]
        res['x_label_list'] = x_label_list
        res['data_list'] = data_list
    else:
        print(f'Type Error: {type_}')

    print("Returned result:")
    print(res)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(res)


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
