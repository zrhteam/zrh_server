from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time

project_ls_blueprint = Blueprint('project_ls', __name__, url_prefix='/api/project_ls')


# 所需函数
# 1.	隐患数量
# 2.	不同专业的隐患数量
# 3.	高中低风险的数量
# 4.	stage（致因阶段）的占比
# 5.	高风险的隐患描述 前20
# 6.	四大专业的隐患图片（各3张 + 隐患描述）
# 7.    下方表格

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


# 3.高中低风险的数量
@project_ls_blueprint.route('/project_ls_risk_level', methods=['POST', 'GET'])
def project_ls_risk_level():
    print("In function project_ls_risk_level")
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
    resp_data = {"code": 10000, "data": {"risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 4.stage（致因阶段）的占比
@project_ls_blueprint.route('/project_ls_stage_ratio', methods=['POST', 'GET'])
def project_ls_stage_ratio():
    print("In function project_ls_stage_ratio")
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
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.stage not in resp_data["data"].keys():
                resp_data["data"][str(item.stage)] = 0
            resp_data["data"][str(item.stage)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 5.高风险的隐患描述 前20
@project_ls_blueprint.route('/project_ls_high_risk_note', methods=['POST', 'GET'])
def project_ls_high_risk_note():
    print("In function project_ls_high_risk_note")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    print("Received project_name: " + str(project_name))
    resp_data = {"code": 10000, "data": {"note_list": []}}
    cnt = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys() and str(item.risk_level) == "3":  # 高风险
            resp_data["data"]["note_list"].append(item.note)
            cnt += 1
            if cnt == 20:
                break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 6.四大专业的隐患图片（各3张 + 隐患描述）
@project_ls_blueprint.route('/project_ls_picture_note', methods=['POST', 'GET'])
def project_ls_picture_note():
    print("In function project_ls_picture_note")
    start_t = datetime.now()
    project_name = request.form.get("project_name")
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.project_tag == project_name:
            contained_check_map[item.code] = 0
    sys_file = gl.get_value("sys_file")
    print("Received project_name: " + str(project_name))
    resp_data = {"code": 10000, "data": {}}
    cnt_map = {}
    image_id_list = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name not in cnt_map.keys():
                cnt_map[item.major_name] = 0
            cnt_map[item.major_name] += 1
            if cnt_map[item.major_name] > 3:  # 只传递3张
                continue
            cur_img_id = str(item.images_file_id).split(",")[0]
            image_id_list[cur_img_id] = {}
            image_id_list[cur_img_id]["note"] = item.note
            image_id_list[cur_img_id]["major_name"] = item.major_name
    for ele in sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            cur_img_id = str(ele.id)
            if image_id_list[cur_img_id]["major_name"] not in resp_data["data"].keys():
                resp_data["data"][image_id_list[cur_img_id]["major_name"]] = []
            resp_data["data"][image_id_list[cur_img_id]["major_name"]].append({"image_url": image_url,
                                                                               "note": image_id_list[str(ele.id)]["note"]})
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 7.下方表格
# 录入时间、录入人员(?)、隐患位置(?)、系统类型、隐患部位、问题描述、风险等级、致因阶段、分布区域、法规名称、相关条款、条款内容
# create_time, system_name, major_name, note, stage, area, risk_level, rule_name, clause, clause_contact
@project_ls_blueprint.route('/project_ls_table', methods=['POST', 'GET'])
def project_ls_table():
    print("In function project_ls_table")
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
    cnt = 0
    resp_data["data"]["record_list"] = []
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            tmp_dict = {}
            tmp_dict["create_time"] = str(item.create_time)
            tmp_dict["system_name"] = item.system_name
            tmp_dict["major_name"] = item.major_name
            tmp_dict["note"] = item.note
            tmp_dict["stage"] = item.stage
            tmp_dict["area"] = item.area
            if str(item.risk_level) == "3":
                tmp_dict["risk_level"] = "高"
            elif str(item.risk_level) == "2":
                tmp_dict["risk_level"] = "中"
            elif str(item.risk_level) == "1":
                tmp_dict["risk_level"] = "低"
            else:
                tmp_dict["risk_level"] = "未定"
            tmp_dict["rule_name"] = item.rule_name
            tmp_dict["clause"] = item.clause
            tmp_dict["clause_contact"] = item.clause_contact
            resp_data["data"]["record_list"].append(tmp_dict)
            cnt += 1
            if cnt == 10:
                break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)

# # 3.隐患数量排行 前10
# @project_ls_blueprint.route('/project_ls_note_top_10', methods=['POST', 'GET'])
# def project_ls_note_top_10():
#     print("In function project_ls_note_top_10")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     cache_cascade_record = gl.get_value("final_record")
#     print("Received project_name: " + str(project_name))
#     cache_final_tag = gl.get_value("final_tag")
#     contained_check_map = {}
#     # 找到所有在此项目下的检查
#     for item in cache_final_tag:
#         if item.project_tag == project_name:
#             contained_check_map[item.code] = 0
#     resp_data = {"code": 10000, "data": {}}
#     risk_note_map = {}
#     for item in cache_cascade_record:
#         if item.project_code in contained_check_map.keys():
#             if item.note not in risk_note_map.keys():
#                 risk_note_map[item.note] = {"appear_time": 0}
#             risk_note_map[item.note]["appear_time"] += 1
#     res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
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
#
# # 4.消防专业发现的隐患数量 以及消防专业下的风险种类数量
# @project_ls_blueprint.route('/project_ls_fire', methods=['POST', 'GET'])
# def project_ls_fire():
#     print("In function project_ls_fire")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     cache_cascade_record = gl.get_value("final_record")
#     print("Received project_name: " + str(project_name))
#     cache_final_tag = gl.get_value("final_tag")
#     contained_check_map = {}
#     # 找到所有在此项目下的检查
#     for item in cache_final_tag:
#         if item.project_tag == project_name:
#             contained_check_map[item.code] = 0
#     resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
#     for item in cache_cascade_record:
#         if item.project_code in contained_check_map.keys():
#             if item.major_name == "消防专业":
#                 resp_data["data"]["risk_num"] += 1
#                 resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)
#
# # 5.不同致因阶段的不同系统下的数量
# # 消防栓系统
# @project_ls_blueprint.route('/project_ls_stage_system_info', methods=['POST', 'GET'])
# def project_ls_stage_system_info():
#     print("In function project_ls_stage_system_info")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     cache_cascade_record = gl.get_value("final_record")
#     print("Received project_name: " + str(project_name))
#     cache_final_tag = gl.get_value("final_tag")
#     contained_check_map = {}
#     # 找到所有在此项目下的检查
#     for item in cache_final_tag:
#         if item.project_tag == project_name:
#             contained_check_map[item.code] = 0
#     resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
#     for item in cache_cascade_record:
#         if item.project_code in contained_check_map.keys():
#             if item.major_name == "消防专业":
#                 resp_data["data"]["risk_num"] += 1
#                 resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)
#
# # 6.消防专业的高风险隐患数量排行 ?
# @project_ls_blueprint.route('/project_ls_high_risk', methods=['POST', 'GET'])
# def project_ls_high_risk():
#     print("In function project_ls_high_risk")
#     start_t = datetime.now()
#     project_name = request.form.get("project_name")
#     cache_cascade_record = gl.get_value("final_record")
#     print("Received project_name: " + str(project_name))
#     cache_final_tag = gl.get_value("final_tag")
#     contained_check_map = {}
#     # 找到所有在此项目下的检查
#     for item in cache_final_tag:
#         if item.project_tag == project_name:
#             contained_check_map[item.code] = 0
#     resp_data = {"code": 10000, "data": {"risk_num": 0, "risk_level_ratio": {"1": 0, "2": 0, "3": 0}}}
#     for item in cache_cascade_record:
#         if item.project_code in contained_check_map.keys():
#             if item.major_name == "消防专业":
#                 resp_data["data"]["risk_num"] += 1
#                 resp_data["data"]["risk_level_ratio"][str(item.risk_level)] += 1
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)
