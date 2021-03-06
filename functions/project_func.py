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
# FunctionName: getProjectRiskLevel
# Purpose: 显示项目中各风险等级及其对应的隐患数量
# Parameter:
# Return:
# @project_blueprint.route('/project_risk_level', methods=['POST', 'GET'])
# def project_risk_level():
#     print("In function project_risk_level")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             resp_data["data"]["risk_level"][str(item.risk_level)] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_risk_level', methods=['POST', 'GET'])
def project_risk_level():
    print("In function project_risk_level")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        # 如果检查在map里面 则进入判断条件
        if item.project_code in contained_check_map.keys():
            resp_data["data"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# project页面部分
#
# FunctionName: getCheckLevelYear
# Purpose: 显示项目中各风险等级及其对应的隐患数量
# Parameter:
# Return:
# @project_blueprint.route('/project_level_year', methods=['POST', 'GET'])
# def project_level_year():
#     print("In function project_level_year")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name: " + str(project_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if project_name == item.project_name:
#             cur_year = str(item.create_time).split('-')[0]
#             if cur_year not in resp_data["data"].keys():
#                 resp_data["data"][cur_year] = {"1": 0, "2": 0, "3": 0}
#             resp_data["data"][cur_year][item.risk_level] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_level_year', methods=['POST', 'GET'])
def project_level_year():
    print("In function project_level_year")
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
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            cur_year = str(item.create_time).split('-')[0]
            if cur_year not in resp_data["data"].keys():
                resp_data["data"][cur_year] = {"1": 0, "2": 0, "3": 0}
            resp_data["data"][cur_year][item.risk_level] += 1
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
# @project_blueprint.route('/project_risk_ratio', methods=['POST', 'GET'])
# def project_risk_ratio():
#     print("In function project_risk_ratio")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     resp_data = {"code": 10000, "data": {}}
#     cnt_check_num = 0
#     major_map = {}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             cnt_check_num += 1
#             if item.major_name not in major_map.keys():
#                 major_map[item.major_name] = 0
#             major_map[item.major_name] += 1
#     if cnt_check_num == 0:
#         resp_data["code"] = -1
#     else:
#         for (major_name, appear_num) in major_map.items():
#             resp_data["data"][major_name] = appear_num
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_risk_ratio', methods=['POST', 'GET'])
def project_risk_ratio():
    print("In function project_risk_ratio")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    resp_data = {"code": 10000, "data": {}}
    cnt_check_num = 0
    major_map = {}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
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
# FunctionName: getProjectHighImage
# Purpose: 显示当前项目中最近一次检查top张高风险隐患图片
# Parameter:
# Return:
# @project_blueprint.route('/project_high_image', methods=['POST', 'GET'])
# def project_high_image():
#     print("In function project_high_image")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     top = int(request.form.get("top"))
#     print("Received project_name " + str(project_name))
#     print("Received top " + str(top))
#     resp_data = {"code": 10000, "data": {"image_list": []}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     cache_sys_file = gl.get_value("cache_sys_file")
#     image_id_list = {}
#     # 找到最近一次的项目 code
#     latest_map = {"time": "2000-01-01 23:59:59", "check_code": ""}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             cur_time = item.create_time
#             if int(time.mktime(time.strptime(str(cur_time), "%Y-%m-%d %H:%M:%S"))) > int(time.mktime(time.strptime(str(latest_map["time"]), "%Y-%m-%d %H:%M:%S"))):
#                 latest_map["time"] = cur_time
#                 latest_map["check_code"] = item.project_code
#     resp_data["check_code"] = latest_map["check_code"]
#     resp_data["check_time"] = latest_map["time"]
#     for item in cache_cascade_record:
#         if latest_map["check_code"] == item.project_code:
#             tmp_image_id_list = str(item.images_file_id).split(",")
#             for ele in tmp_image_id_list:
#                 image_id_list[ele] = {"note": item.note, "check_name": item.project_name}
#     for ele in cache_sys_file:
#         if str(ele.id) in image_id_list.keys():
#             image_url = ele.upload_host + ele.directory + ele.name
#             resp_data["data"]["image_list"].append({"image_url": image_url, "check_name":
#                 image_id_list[str(ele.id)]["check_name"], "note": image_id_list[str(ele.id)]["note"]})
#     # 取top n张
#     resp_data["data"]["image_list"] = resp_data["data"]["image_list"][0: top]
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_high_image', methods=['POST', 'GET'])
def project_high_image():
    print("In function project_high_image")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    top = int(request.form.get("top"))
    print("Received project_name " + str(project_name))
    print("Received top " + str(top))
    resp_data = {"code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    cache_sys_file = gl.get_value("sys_file")
    image_id_list = {}
    # 找到最近一次的项目 code
    latest_map = {"time": "2000-01-01 23:59:59", "check_code": ""}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            cur_time = item.create_time
            if int(time.mktime(time.strptime(str(cur_time), "%Y-%m-%d %H:%M:%S"))) > int(time.mktime(time.strptime(str(latest_map["time"]), "%Y-%m-%d %H:%M:%S"))):
                latest_map["time"] = cur_time
                latest_map["check_code"] = item.project_code
    resp_data["check_code"] = latest_map["check_code"]
    resp_data["check_time"] = latest_map["time"]
    for item in cache_cascade_record:
        if latest_map["check_code"] == item.project_code:
            tmp_image_id_list = str(item.images_file_id).split(",")
            for ele in tmp_image_id_list:
                image_id_list[ele] = {"note": item.note, "check_name": item.project_name}
    for ele in cache_sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append({"image_url": image_url, "check_name":
                image_id_list[str(ele.id)]["check_name"], "note": image_id_list[str(ele.id)]["note"]})
    # 取top n张
    resp_data["data"]["image_list"] = resp_data["data"]["image_list"][0: top]
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# project页面部分
#
# FunctionName: getInitProjectSystem
# Purpose: 显示在不同专业下属于不同隐患子系统的隐患数量
# Parameter:
# Return:
# @project_blueprint.route('/project_major_system', methods=['POST', 'GET'])
# def project_major_system():
#     print("In function project_major_system")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     major = request.form.get("major")
#     print("Received project_name " + str(project_name))
#     print("Received major " + str(major))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if major == "all" or major == item.major_name:
#                 if item.major_name not in resp_data["data"].keys():
#                     resp_data["data"][item.major_name] = {}
#                 if item.system_name not in resp_data["data"][item.major_name].keys():
#                     resp_data["data"][item.major_name][item.system_name] = 0
#                 resp_data["data"][item.major_name][item.system_name] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_major_system', methods=['POST', 'GET'])
def project_major_system():
    print("In function project_major_system")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    major = request.form.get("major")
    print("Received project_name " + str(project_name))
    print("Received major " + str(major))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if major == "all" or major == item.major_name:
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
# FunctionName: getInitProjectReason
# Purpose: 显示在不同专业情况下在不同致因阶段的隐患数量
# Parameter:
# Return:
# @project_blueprint.route('/project_major_stage', methods=['POST', 'GET'])
# def project_major_stage():
#     print("In function project_major_stage")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     major = request.form.get("major")
#     print("Received project_name " + str(project_name))
#     print("Received major " + str(major))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if major == "all" or major == item.major_name:
#                 # stage = "not defined stage" if item.stage == '' else item.stage
#                 stage = ''
#                 if item.stage == '':
#                     stage = "未定义"
#                 else:
#                     stage = item.stage.split("阶段")[0]
#                 if item.major_name not in resp_data["data"].keys():
#                     resp_data["data"][item.major_name] = {}
#                 if stage not in resp_data["data"][item.major_name].keys():
#                     resp_data["data"][item.major_name][stage] = 0
#                 resp_data["data"][item.major_name][stage] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_major_stage', methods=['POST', 'GET'])
def project_major_stage():
    print("In function project_major_stage")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    major = request.form.get("major")
    print("Received project_name " + str(project_name))
    print("Received major " + str(major))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if major == "all" or major == item.major_name:
                # stage = "not defined stage" if item.stage == '' else item.stage
                stage = ''
                if item.stage == '':
                    stage = "未定义"
                else:
                    stage = item.stage.split("阶段")[0]
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
# FunctionName: getInitProjectRegionDistribution
# Purpose: 显示在不同专业情况下，隐患区域分布的情况
# Parameter:
# Return:
# @project_blueprint.route('/project_major_area', methods=['POST', 'GET'])
# def project_major_area():
#     print("In function project_major_area")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     major = request.form.get("major")
#     print("Received project_name " + str(project_name))
#     print("Received major " + str(major))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if major == "all" or major == item.major_name:
#                 area = "not defined area" if item.area == '' else item.area
#                 if item.major_name not in resp_data["data"].keys():
#                     resp_data["data"][item.major_name] = {}
#                 if area not in resp_data["data"][item.major_name].keys():
#                     resp_data["data"][item.major_name][area] = 0
#                 resp_data["data"][item.major_name][area] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_major_area', methods=['POST', 'GET'])
def project_major_area():
    print("In function project_major_area")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    major = request.form.get("major")
    print("Received project_name " + str(project_name))
    print("Received major " + str(major))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if major == "all" or major == item.major_name:
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
# FunctionName: getInitProjectRiskTop
# Purpose: 显示在不同筛选条件（专业/系统/设备/组件）下，出现次数排名前top的隐患描述
# Parameter:
# Return:
# @project_blueprint.route('/project_risk_top', methods=['POST', 'GET'])
# def projectrisk_top():
#     print("In function project_risk_top")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     condition = request.form.get("condition")
#     top = int(request.form.get("top"))
#     print("Received project_name " + str(project_name))
#     print("Received condition " + str(condition))
#     print("Received top " + str(top))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_note_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.note not in risk_note_map.keys():
#                 if condition == "major":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.major_name}
#                 elif condition == "system":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.system_name}
#                 elif condition == "equipment":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.equipment_name}
#                 elif condition == "module":
#                     risk_note_map[item.note] = {"appear_time": 0, condition: item.module_name}
#             risk_note_map[item.note]["appear_time"] += 1
#     res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == top:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_risk_top', methods=['POST', 'GET'])
def projectrisk_top():
    print("In function project_risk_top")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    condition = request.form.get("condition")
    top = int(request.form.get("top"))
    print("Received project_name " + str(project_name))
    print("Received condition " + str(condition))
    print("Received top " + str(top))
    cache_cascade_record = gl.get_value("final_record")
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
                if condition == "major":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.major_name}
                elif condition == "system":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.system_name}
                elif condition == "equipment":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.equipment_name}
                elif condition == "module":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.module_name}
            risk_note_map[item.note]["appear_time"] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = ele[1]
        idx += 1
        if idx == top:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# project页面部分
#
# FunctionName: getProjectOtherTop
# Purpose: 显示在不同筛选条件（风险等级(1, 2,3, all)/致因阶段/分布区域）下，出现次数排名前top的隐患描述
# Parameter:
# Return:
# @project_blueprint.route('/project_other_top', methods=['POST', 'GET'])
# def project_other_top():
#     print("In function project_other_top")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     flag = int(request.form.get("flag"))
#     top = int(request.form.get("top"))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     if flag == 1:  # 致因阶段
#         stage = request.form.get("stage")
#         print("Received stage " + str(stage))
#         for item in cache_cascade_record:
#             t_stage = ''
#             if item.stage == '':
#                 t_stage = "未定义"
#             else:
#                 t_stage = item.stage.split("阶段")[0]
#             if project_name == item.project_tag and t_stage == stage:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 2:  # 风险等级
#         risk_level = request.form.get("risk_level")
#         print("Received risk_level " + str(risk_level))
#         for item in cache_cascade_record:
#             if project_name == item.project_tag:
#                 if risk_level == "all" or risk_level == item.risk_level:
#                     if item.note not in resp_data["data"].keys():
#                         resp_data["data"][item.note] = 0
#                     resp_data["data"][item.note] += 1
#     elif flag == 3:  # 专业
#         major_name = request.form.get("major_name")
#         print("Received major_name " + str(major_name))
#         for item in cache_cascade_record:
#             if project_name == item.project_tag and major_name == item.major_name:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 4:  # 专业 + 系统
#         major_name = request.form.get("major_name")
#         system_name = request.form.get("system_name")
#         print("Received major_name " + str(major_name))
#         print("Received system_name " + str(system_name))
#         for item in cache_cascade_record:
#             if project_name == item.project_tag and major_name == item.major_name and system_name == item.system_name:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#     elif flag == 5:  # 专业 + 区域
#         major_name = request.form.get("major_name")
#         area = request.form.get("area")
#         print("Received major_name " + str(major_name))
#         print("Received area " + str(area))
#         for item in cache_cascade_record:
#             if project_name == item.project_tag and major_name == item.major_name and area == item.area:
#                 if item.note not in resp_data["data"].keys():
#                     resp_data["data"][item.note] = 0
#                 resp_data["data"][item.note] += 1
#
#     res = sorted(resp_data["data"].items(), key=lambda d: d[1], reverse=True)
#     resp_data["data"] = {}
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == top:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)
@project_blueprint.route('/project_other_top', methods=['POST', 'GET'])
def project_other_top():
    print("In function project_other_top")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    flag = int(request.form.get("flag"))
    top = int(request.form.get("top"))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    if flag == 1:  # 致因阶段
        stage = request.form.get("stage")
        print("Received stage " + str(stage))
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.project_tag == project_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys():
                t_stage = ''
                if item.stage == '':
                    t_stage = "未定义"
                else:
                    t_stage = item.stage.split("阶段")[0]
                if t_stage == stage:
                    if item.note not in resp_data["data"].keys():
                        resp_data["data"][item.note] = 0
                    resp_data["data"][item.note] += 1
    elif flag == 2:  # 风险等级
        risk_level = request.form.get("risk_level")
        print("Received risk_level " + str(risk_level))
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.project_tag == project_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys():
                if risk_level == "all" or risk_level == item.risk_level:
                    if item.note not in resp_data["data"].keys():
                        resp_data["data"][item.note] = 0
                    resp_data["data"][item.note] += 1
    elif flag == 3:  # 专业
        major_name = request.form.get("major_name")
        print("Received major_name " + str(major_name))
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.project_tag == project_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 4:  # 专业 + 系统
        major_name = request.form.get("major_name")
        system_name = request.form.get("system_name")
        print("Received major_name " + str(major_name))
        print("Received system_name " + str(system_name))
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.project_tag == project_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name and system_name == item.system_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 5:  # 专业 + 区域
        major_name = request.form.get("major_name")
        area = request.form.get("area")
        print("Received major_name " + str(major_name))
        print("Received area " + str(area))
        contained_check_map = {}
        # 找到所有在此项目下的检查
        for item in cache_final_tag:
            if item.project_tag == project_name:
                contained_check_map[item.code] = 0
        for item in cache_cascade_record:
            if item.project_code in contained_check_map.keys() and major_name == item.major_name and area == item.area:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1

    res = sorted(resp_data["data"].items(), key=lambda d: d[1], reverse=True)
    resp_data["data"] = {}
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = ele[1]
        idx += 1
        if idx == top:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# project页面部分
#
# FunctionName: getProjectSystemNumber
# Purpose: 显示隐患次数排名前10的系统名称
# Parameter:
# Return:
# @project_blueprint.route('/project_system_number', methods=['POST', 'GET'])
# def project_system_number():
#     print("In function project_system_number")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_system_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.system_name not in risk_system_map.keys():
#                 risk_system_map[item.system_name] = {"appear_time": 0}
#             risk_system_map[item.system_name]["appear_time"] += 1
#     res = sorted(risk_system_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == 10:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_system_number', methods=['POST', 'GET'])
def project_system_number():
    print("In function project_system_number")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    risk_system_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.system_name not in risk_system_map.keys():
                risk_system_map[item.system_name] = {"appear_time": 0}
            risk_system_map[item.system_name]["appear_time"] += 1
    res = sorted(risk_system_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
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


# project页面部分
#
# FunctionName: getProjectEquipmentNumber
# Purpose: 显示隐患次数排名前10的设备名称
# Parameter:
# Return:
# @project_blueprint.route('/project_equipment_number', methods=['POST', 'GET'])
# def project_equipment_number():
#     print("In function project_equipment_number")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_equipment_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.equipment_name not in risk_equipment_map.keys():
#                 risk_equipment_map[item.equipment_name] = {"appear_time": 0}
#             risk_equipment_map[item.equipment_name]["appear_time"] += 1
#     res = sorted(risk_equipment_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == 10:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_equipment_number', methods=['POST', 'GET'])
def project_equipment_number():
    print("In function project_equipment_number")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    risk_equipment_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.equipment_name not in risk_equipment_map.keys():
                risk_equipment_map[item.equipment_name] = {"appear_time": 0}
            risk_equipment_map[item.equipment_name]["appear_time"] += 1
    res = sorted(risk_equipment_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
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


# project页面部分
#
# FunctionName: getProjectModuleNumber
# Purpose: 显示隐患次数排名前10的组件名称
# Parameter:
# Return:
# @project_blueprint.route('/project_module_number', methods=['POST', 'GET'])
# def project_module_number():
#     print("In function project_module_number")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_module_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.module_name not in risk_module_map.keys():
#                 risk_module_map[item.module_name] = {"appear_time": 0}
#             risk_module_map[item.module_name]["appear_time"] += 1
#     res = sorted(risk_module_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == 10:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_module_number', methods=['POST', 'GET'])
def project_module_number():
    print("In function project_module_number")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    risk_module_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.module_name not in risk_module_map.keys():
                risk_module_map[item.module_name] = {"appear_time": 0}
            risk_module_map[item.module_name]["appear_time"] += 1
    res = sorted(risk_module_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
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


# project页面部分
#
# FunctionName: getProjectRules
# Purpose: 显示违反次数排名前10的法规、违反次数及其相关条款号和内容
# Parameter:
# Return:
# @project_blueprint.route('/project_rules', methods=['POST', 'GET'])
# def project_rules():
#     print("In function project_rules")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_rule_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             rule_name = item.rule_name if item.rule_name is not None else ''
#             clause = item.clause if item.clause is not None else ''
#             clause_contact = item.clause_contact if item.clause_contact is not None else ''
#             if rule_name not in risk_rule_map.keys():
#                 risk_rule_map[rule_name] = {"appear_time": 0, "clause": clause
#                     , "clause_contact": clause_contact}
#             risk_rule_map[rule_name]["appear_time"] += 1
#     res = sorted(risk_rule_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == 10:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_rules', methods=['POST', 'GET'])
def project_rules():
    print("In function project_rules")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    risk_rule_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            rule_name = item.rule_name if item.rule_name is not None else ''
            clause = item.clause if item.clause is not None else ''
            clause_contact = item.clause_contact if item.clause_contact is not None else ''
            if rule_name not in risk_rule_map.keys():
                risk_rule_map[rule_name] = {"appear_time": 0, "clause": clause
                    , "clause_contact": clause_contact}
            risk_rule_map[rule_name]["appear_time"] += 1
    res = sorted(risk_rule_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
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


# project页面部分
#
# FunctionName: getProjectRiskTop
# Purpose: 显示在历次检查中，出现次数排名前5的隐患描述及其所属专业和出现次数
# Parameter:
# Return:
# @project_blueprint.route('/project_risk_top', methods=['POST', 'GET'])
# def project_risk_top():
#     print("In function project_risk_top")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_note_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.note not in risk_note_map.keys():
#                 risk_note_map[item.note] = {"appear_time": 0, "belonged_major": item.major_name}
#             risk_note_map[item.note]["appear_time"] += 1
#     res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
#     idx = 0
#     for ele in res:
#         resp_data["data"][ele[0]] = ele[1]
#         idx += 1
#         if idx == 5:
#             break
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)
@project_blueprint.route('/project_risk_top', methods=['POST', 'GET'])
def project_risk_top():
    print("In function project_risk_top")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
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
                risk_note_map[item.note] = {"appear_time": 0, "belonged_major": item.major_name}
            risk_note_map[item.note]["appear_time"] += 1
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
# @project_blueprint.route('/project_risk_change', methods=['POST', 'GET'])
# def project_risk_change():
#     print("In function project_risk_change")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     risk_note_map = {}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.project_code not in resp_data["data"].keys():
#                 resp_data["data"][item.project_code] = {"risk_num": 0, "start_time": "7258175999"}
#             resp_data["data"][item.project_code]["risk_num"] += 1
#             create_time = str(item.create_time).split(" ")[0]
#             time_array = time.strptime(create_time, "%Y-%m-%d")
#             time_stamp = int(time.mktime(time_array))
#             if time_stamp < int(resp_data["data"][item.project_code]["start_time"]):
#                 resp_data["data"][item.project_code]["start_time"] = str(time_stamp)
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_risk_change', methods=['POST', 'GET'])
def project_risk_change():
    print("In function project_risk_change")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
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



# project页面部分
#
# FunctionName: getProjectRiskLevelRatio
# Purpose: 不同专业下风险等级占比
# Parameter:
# Return:
# @project_blueprint.route('/project_risk_level_ratio', methods=['POST', 'GET'])
# def project_risk_level_ratio():
#     print("In function project_risk_level_ratio")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name " + str(project_name))
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     resp_data = {"code": 10000, "data": {}}
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.major_name not in resp_data["data"].keys():
#                 resp_data["data"][item.major_name] = {}
#             if item.risk_level not in resp_data["data"][item.major_name].keys():
#                 resp_data["data"][item.major_name][item.risk_level] = 0
#             resp_data["data"][item.major_name][item.risk_level] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

@project_blueprint.route('/project_risk_level_ratio', methods=['POST', 'GET'])
def project_risk_level_ratio():
    print("In function project_risk_level_ratio")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    print("Received project_name " + str(project_name))
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if item.risk_level not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][item.risk_level] = 0
            resp_data["data"][item.major_name][item.risk_level] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)



# project页面部分
#
# FunctionName: getProjectDangerProblem
# Purpose: 显示该项目存在的红线问题及其对应的原因
# Parameter:
# Return:
# @project_blueprint.route('/project_danger_problem', methods=['POST', 'GET'])
# def project_danger_problem():
#     print("In function project_danger_problem")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     print("Received project_name: " + str(project_name))
#     resp_data = {"code": 10000, "data": {}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     for item in cache_cascade_record:
#         if project_name == item.project_tag:
#             if item.alert_indicator is not None:
#                 if item.alert_indicator not in resp_data["data"].keys():
#                     resp_data["data"][item.alert_indicator] = {"appear_time": 0, "problem": {}}
#                 resp_data["data"][item.alert_indicator]["appear_time"] += 1
#                 if item.problem1 is not None:
#                     if item.problem1 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem1] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem1]["appear_time"] += 1
#                 if item.problem2 is not None:
#                     if item.problem2 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem2] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem2]["appear_time"] += 1
#                 if item.problem3 is not None:
#                     if item.problem3 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem3] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem3]["appear_time"] += 1
#                 if item.problem4 is not None:
#                     if item.problem4 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem4] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem4]["appear_time"] += 1
#                 if item.problem5 is not None:
#                     if item.problem5 not in resp_data["data"][item.alert_indicator]["problem"].keys():
#                         resp_data["data"][item.alert_indicator]["problem"][item.problem5] = {"appear_time": 0}
#                     resp_data["data"][item.alert_indicator]["problem"][item.problem5]["appear_time"] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)


@project_blueprint.route('/project_danger_problem', methods=['POST', 'GET'])
def project_danger_problem():
    print("In function project_danger_problem")
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
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.alert_indicator is not None:
                if item.alert_indicator not in resp_data["data"].keys():
                    resp_data["data"][item.alert_indicator] = {"appear_time": 0, "problem": {}}
                resp_data["data"][item.alert_indicator]["appear_time"] += 1
                if item.problem1 is not None:
                    if item.problem1 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem1] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem1]["appear_time"] += 1
                if item.problem2 is not None:
                    if item.problem2 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem2] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem2]["appear_time"] += 1
                if item.problem3 is not None:
                    if item.problem3 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem3] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem3]["appear_time"] += 1
                if item.problem4 is not None:
                    if item.problem4 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem4] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem4]["appear_time"] += 1
                if item.problem5 is not None:
                    if item.problem5 not in resp_data["data"][item.alert_indicator]["problem"].keys():
                        resp_data["data"][item.alert_indicator]["problem"][item.problem5] = {"appear_time": 0}
                    resp_data["data"][item.alert_indicator]["problem"][item.problem5]["appear_time"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)