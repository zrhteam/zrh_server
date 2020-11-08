import decimal

from flask import Flask, make_response, json, jsonify, redirect, url_for, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker
from random import *

import requests
import pymysql
import os
import pdb

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://liqian:123456@10.20.36.64:3306/zrh_data'
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


class BuildingTroubleDataConverted(db.Model):
    __tablename__ = 'building_trouble_dataV2.1_converted'
    # __abstract__ = True
    id = db.Column('ID', db.Integer, primary_key=True)
    project_name = db.Column('项目名称', db.Text)
    risk_description = db.Column('隐患描述', db.Text)
    risk_cnt = db.Column('隐患数量', db.Integer)
    system_name = db.Column('系统名称', db.Text)
    equipment_name = db.Column('设备名称', db.Text)
    component_name = db.Column('组件名称', db.Text)
    risk_position = db.Column('隐患地点/位置', db.Text)
    risk_level = db.Column('风险等级', db.Integer)
    area = db.Column('分布区域', db.Text)
    cause_phase = db.Column('致因阶段', db.Text)
    risk_picture = db.Column('隐患图片', db.Integer)
    entered_name = db.Column('录入人姓名', db.Text)
    state = db.Column('状态', db.Integer)
    appear_frequency = db.Column('出现频率', db.Text)
    create_time = db.Column('创建时间', db.Text)
    related_item = db.Column('相关条款', db.Text)
    code_number = db.Column('法规编号', db.Text)
    legislation_name = db.Column('法规名称', db.Text)
    legislation_content = db.Column('条款内容', db.Text)
    risk_rate = db.Column('隐患风险等级', db.Text)
    project_leader = db.Column('项目组长', db.Text)
    province = db.Column('省份', db.Text)
    city = db.Column('城市', db.Text)
    region = db.Column('区域', db.Text)
    longitude = db.Column('经度', db.Float(asdecimal=False))
    latitude = db.Column('纬度', db.Float(asdecimal=False))
    predict_start_time = db.Column('预计开始时间', db.Text)
    predict_end_time = db.Column('预计结束时间', db.Text)
    project_implement_state = db.Column('项目执行状态', db.Text)
    project_check_type = db.Column('项目检查类型', db.Text)
    belonged_major_name = db.Column('所属专业名称', db.Text)
    risk_picture1 = db.Column('隐患图片.1', db.Text)

    def __repr__(self):
        return "location id = {}, longitude = {}, latitude = {}".format(repr(self.id),
                                                                        repr(self.longitude),
                                                                        repr(
                                                                            self.latitude)
                                                                        )

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


# overview页面地图部分
@app.route('/api/overview', methods=['POST'])
def overview():
    error = None
    # DEBUG
    res = BuildingTroubleDataConverted.query.filter(BuildingTroubleDataConverted.longitude != '').all()
    # print(res)
    ret = []
    for x in res:
        ret.append(x.to_json())
    print(ret)
    return jsonify(ret)


# overview页面根据项目名称查询
@app.route('/api/overview_prjname', methods=['POST'])
def overview_prjname():
    error = None
    if request.method == 'POST' and request.form.get("project_name"):
        datax = request.form.get("project_name")
        print(datax)
        return jsonify({'msg': '没问题'})
    return jsonify({'msg': '出错了'})


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
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")  # ,
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
    user = RiskModule.query.filter_by(id=1).all()
    # user = db.session.query(RiskModule).filter(RiskModule.id == 1)
    # print(user)
    app.run(debug=True)
