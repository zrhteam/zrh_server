from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl

login_blueprint = Blueprint('login', __name__, url_prefix='/login')


@login_blueprint.route('/get_grant', methods=['POST', 'GET'])
def get_grant():
    print("In function get_grant")
    start_t = datetime.now()
    name = request.form.get("name")
    password = request.form.get("pwd")
    print("Received name: " + str(name))
    print("Received password: " + str(password))
    flag = 0
    resp_data = {"code": 0,
                 "msg": {"user_grant": "",
                         "headquarter_tag": "",
                         "region_tag": "",
                         "project_tag": ""}}
    cache_risk_user = gl.get_value("cache_risk_user")
    for item in cache_risk_user:
        if item.name == name:
            if item.password == password:
                resp_data["msg"]["user_grant"] = item.user_grant
                resp_data["msg"]["headquarter_tag"] = item.headquarter_tag
                resp_data["msg"]["region_tag"] = item.region_tag
                resp_data["msg"]["project_tag"] = item.project_tag
                flag = 1
            else:
                resp_data["code"] = -1
            break
    return jsonify(resp_data)
