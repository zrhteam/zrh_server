from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time
project_blueprint = Blueprint('project', __name__, url_prefix='/api/project')

# project页面部分
#
# FunctionName: getProjectIndex
# Purpose: 显示项目的整体危险指数以及各专业的危险指数
# Parameter:
# Return:
# @project_blueprint.route('/project_index', methods=['POST'])
# def project_index():

# project页面部分
#
# FunctionName: getProjectRectification
# Purpose: 显示项目整改率
# Parameter:
# Return:
@project_blueprint.route('/project_rectification', methods=['POST'])
def project_rectification():
    print("In function project_rectification")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {"rectification": "0%"}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    state_ok = 0
    state_nok = 0
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.state == 5:
                state_ok += 1
            else:
                state_nok += 1
    if state_ok + state_nok != 0:
        resp_data["data"]["rectification"] = str(round(state_ok * 100 / (state_ok + state_nok), 2)) + "%"
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectRiskLevel
# Purpose: 显示项目中各风险等级及其对应的隐患数量
# Parameter:
# Return:
@project_blueprint.route('/project_risk_level', methods=['POST', 'GET'])
def project_risk_level():
    print("In function project_risk_level")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            resp_data["data"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectRiskRatio
# Purpose: 显示该项目中不同专业的隐患占比情况
# Parameter:
# Return:
@project_blueprint.route('/project_risk_ratio', methods=['POST', 'GET'])
def project_risk_ratio():
    print("In function project_risk_ratio")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {}}
    cnt_check_num = 0
    major_map = {}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            cnt_check_num += 1
            if item.major_name not in major_map.keys():
                major_map[item.major_name] = 0
            major_map[item.major_name] += 1
    if cnt_check_num == 0:
        resp_data["code"] = -1
    else:
        for (major_name, appear_num) in major_map.items():
            resp_data["data"][major_name] = appear_num
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectHighRisk
# Purpose: 显示当前项目中未整改的高风险隐患描述
# Parameter:
# Return:
@project_blueprint.route('/project_high_risk', methods=['POST', 'GET'])
def project_high_risk():
    print("In function project_high_risk")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {"note_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.risk_level == "3" and item.state != "5":
                resp_data["data"]["note_list"].append(item.note)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectHighImage
# Purpose: 显示当前项目中未整改的高风险隐患图片
# Parameter:
# Return:
@project_blueprint.route('/project_high_image', methods=['POST', 'GET'])
def project_high_image():
    print("In function project_high_image")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    cache_sys_file = gl.get_value("cache_sys_file")
    image_id_list = {}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.risk_level == "3" and item.state != "5":
                tmp_image_id_list = str(item.images_file_id).split(",")
                for ele in tmp_image_id_list:
                    image_id_list[ele] = 0
    for ele in cache_sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append(image_url)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectMajorSystem
# Purpose: 显示在不同专业下属于不同隐患子系统的隐患数量
# Parameter:
# Return:
@project_blueprint.route('/project_major_system', methods=['POST', 'GET'])
def project_major_system():
    print("In function project_major_system")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if item.system_name not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][item.system_name] = 0
            resp_data["data"][item.major_name][item.system_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# project页面部分
#
# FunctionName: getProjectMajorStage
# Purpose: 显示在不同专业情况下在不同致因阶段的隐患数量
# Parameter:
# Return:
@project_blueprint.route('/project_major_stage', methods=['POST', 'GET'])
def project_major_stage():
    print("In function project_major_stage")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            stage = "not defined stage" if item.stage == '' else item.stage
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if stage not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][stage] = 0
            resp_data["data"][item.major_name][stage] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectMajorArea
# Purpose: 显示在不同专业情况下，隐患区域分布的情况
# Parameter:
# Return:
@project_blueprint.route('/project_major_area', methods=['POST', 'GET'])
def project_major_area():
    print("In function project_major_area")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            area = "not defined area" if item.area == '' else item.area
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if area not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][area] = 0
            resp_data["data"][item.major_name][area] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectRiskTop
# Purpose: 显示在历次检查中，出现次数排名前5的隐患描述及其所属专业和出现次数
# Parameter:
# Return:
@project_blueprint.route('/project_risk_top', methods=['POST', 'GET'])
def project_risk_top():
    print("In function project_risk_top")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    risk_note_map = {}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.note not in risk_note_map.keys():
                risk_note_map[item.note] = {"appear_time": 0, "belonged_major": item.major_name}
            risk_note_map[item.note] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = ele[1]
        idx += 1
        if idx == 5:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getProjectRiskChange
# Purpose: 显示历次检查中隐患数量的变化
# Parameter:
# Return:
@project_blueprint.route('/project_risk_change', methods=['POST', 'GET'])
def project_risk_change():
    print("In function project_risk_change")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    risk_note_map = {}
    for item in cache_cascade_record:
        if project_name == item.project_tag:
            if item.project_code not in resp_data["data"].keys():
                resp_data["data"][item.project_code] = {"risk_num": 0, "start_time": "7258175999"}
            resp_data["data"][item.project_code]["risk_num"] += 1
            create_time = str(item.create_time).split(" ")[0]
            time_array = time.strptime(create_time, "%Y-%m-%d")
            time_stamp = int(time.mktime(time_array))
            if time_stamp < int(resp_data["data"][item.project_code]["start_time"]):
                resp_data["data"][item.project_code]["start_time"] = str(time_stamp)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)