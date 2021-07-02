from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time

province_info_blueprint = Blueprint('province_info', __name__, url_prefix='/api/province_info')

# province info

# FunctionName: province_check_and_record_num
# Purpose: 显示该省当前已检查项目数量
# Parameter:
# Return:
@province_info_blueprint.route('/province_check_and_record_num', methods=['POST'])
def province_check_and_record_num():
    print("In function province_check_and_record_num")
    start_t = datetime.now()
    risk_project = gl.get_value("risk_project")
    final_record = gl.get_value("final_record")
    resp_data = {"code": 10000, "data": {}}
    check_code_map = {}
    for item in risk_project:
        if item.province_name is not None:
            check_code_map[item.code] = item.province_name
            if item.province_name not in resp_data["data"].keys():
                resp_data["data"][item.province_name] = {"check_num": 0, "record_num": 0, "lng": item.lng, "lat": item.lat} # 取出第一个检查的坐标作为该省的位置
            resp_data["data"][item.province_name]["check_num"] += 1
    for item in final_record:
        if item.project_code in check_code_map.keys():
            resp_data["data"][check_code_map[item.project_code]]["record_num"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)