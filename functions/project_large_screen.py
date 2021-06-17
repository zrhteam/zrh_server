from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time

project_ls_blueprint = Blueprint('project_ls', __name__, url_prefix='/api/project_ls')

# 所需函数
# 1.	隐患数量
# 2.	不同专业的隐患数量
# 3.	隐患数量排行
# 4.	消防专业发现的隐患数量 以及消防专业下的风险种类数量
# 5.	不同致因阶段的不同系统下的数量
# 6.	消防专业的高风险隐患数量排行

# 1.隐患数量
@project_ls_blueprint.route('/project_ls_risk_num', methods=['POST', 'GET'])
def project_ls_risk_num():
    print("In function project_ls_risk_num")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    resp_data = {"code": 10000, "data": {"risk_num": 0}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    risk_num_cnt = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            risk_num_cnt += 1
    resp_data["data"]["risk_num"] = risk_num_cnt
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 2.不同专业的隐患数量
@project_ls_blueprint.route('/project_ls_major_ratio', methods=['POST', 'GET'])
def project_ls_major_ratio():
    print("In function project_ls_major_ratio")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name: " + str(project_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    major_map = {}
    cnt_project_num = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            cnt_project_num += 1
            if item.major_name not in major_map.keys():
                major_map[item.major_name] = 0
            major_map[item.major_name] += 1
    if cnt_project_num == 0:
        resp_data["code"] = -1
    resp_data["data"] = major_map
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 3.隐患数量排行 前10
@project_ls_blueprint.route('/project_ls_note_top_10', methods=['POST', 'GET'])
def project_ls_note_top_10():
    print("In function project_ls_note_top_10")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    print("Received project_name: " + str(project_name))
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    risk_note_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.note not in risk_note_map.keys():
                risk_note_map[item.note] = {"appear_time": 0}
            risk_note_map[item.note]["appear_time"] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = ele[1]
        idx += 1
        if idx == 10:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 4.消防专业发现的隐患数量 以及消防专业下的风险种类数量
@project_ls_blueprint.route('/project_ls_fire', methods=['POST', 'GET'])
def project_ls_fire():
    print("In function project_ls_fire")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    print("Received project_name: " + str(project_name))
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name == "消防专业":
                resp_data["data"]["risk_num"] += 1
                resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 5.不同致因阶段的不同系统下的数量
# 消防栓系统
@project_ls_blueprint.route('/project_ls_high_risk', methods=['POST', 'GET'])
def project_ls_high_risk():
    print("In function project_ls_high_risk")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    print("Received project_name: " + str(project_name))
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name == "消防专业":
                resp_data["data"]["risk_num"] += 1
                resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# 6.消防专业的高风险隐患数量排行 ?
@project_ls_blueprint.route('/project_ls_high_risk', methods=['POST', 'GET'])
def project_ls_high_risk():
    print("In function project_ls_high_risk")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    print("Received project_name: " + str(project_name))
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name == "消防专业":
                resp_data["data"]["risk_num"] += 1
                resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)