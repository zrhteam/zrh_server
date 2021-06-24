from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time

region_ls_blueprint = Blueprint('region_ls', __name__, url_prefix='/api/region_ls')


# 1.	隐患数量
# 2.	高风险排名
# 3.	不同专业的隐患数量
# 4.	隐患项目数量排行
# 5.	不同专业下的不同致因阶段
# 6.	不同分布区域的隐患数量

# 1.隐患数量
@region_ls_blueprint.route('/region_ls_risk_num', methods=['POST', 'GET'])
def region_ls_risk_num():
    print("In function region_ls_risk_num")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {"risk_num": 0}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
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


# 2.高风险排名
@region_ls_blueprint.route('/region_ls_risk_num_rank', methods=['POST', 'GET'])
def region_ls_risk_num_rank():
    print("In function region_ls_risk_num_rank")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = {"project_tag": item.project_tag, "region_tag": item.region_tag,
                                              "headquarter_tag": item.headquarter_tag}
    risk_num_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if str(item.risk_level) == "3":
                if contained_check_map[item.project_code]["project_tag"] not in risk_num_map.keys():
                    risk_num_map[contained_check_map[item.project_code]["project_tag"]] = 0
                risk_num_map[contained_check_map[item.project_code]["project_tag"]] += 1
    res = sorted(risk_num_map.items(), key=lambda d: d[1], reverse=True)
    # resp_data["data"] = {}
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"appear_time": ele[1], "rank": idx}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 3.不同专业的隐患数量
@region_ls_blueprint.route('/region_ls_major_num', methods=['POST', 'GET'])
def region_ls_major_num():
    print("In function region_ls_major_num")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = 0
            resp_data["data"][item.major_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 4.隐患项目数量排行
@region_ls_blueprint.route('/region_ls_check_num_rank', methods=['POST', 'GET'])
def region_ls_check_num_rank():
    print("In function region_ls_check_num_rank")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = 0
    check_num_map = {}
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.project_code not in check_num_map.keys():
                check_num_map[item.project_code] = 0
            check_num_map[item.project_code] += 1
    res = sorted(check_num_map.items(), key=lambda d: d[1], reverse=True)
    # resp_data["data"] = {}
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"appear_time": ele[1], "rank": idx}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 5.不同专业下的不同致因阶段
@region_ls_blueprint.route('/region_ls_major_stage_info', methods=['POST', 'GET'])
def region_ls_major_stage_info():
    print("In function region_ls_major_stage_info")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = {}
            if item.stage not in resp_data["data"][item.major_name].keys():
                resp_data["data"][item.major_name][item.stage] = 0
            resp_data["data"][item.major_name][item.stage] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 6.不同分布区域的隐患数量
@region_ls_blueprint.route('/region_ls_area_num', methods=['POST', 'GET'])
def region_ls_area_num():
    print("In function region_ls_area_num")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = 0
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            if item.area not in resp_data["data"].keys():
                resp_data["data"][item.area] = 0
            resp_data["data"][item.area] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 7.下方表格
# 隐患专业（部位）、问题描述、风险等级、致因阶段、分布区域、法规名称
# major_name, note, risk_level, stage, area, rule_name
@region_ls_blueprint.route('/region_ls_table', methods=['POST', 'GET'])
def region_ls_table():
    print("In function region_ls_table")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    contained_check_map = {}
    # 找到所有在此项目下的检查
    for item in cache_final_tag:
        if item.region_tag == region_name:
            contained_check_map[item.code] = 0
    cnt = 0
    resp_data["data"]["record_list"] = []
    for item in cache_cascade_record:
        if item.project_code in contained_check_map.keys():
            tmp_dict = {}
            tmp_dict["major_name"] = item.major_name
            tmp_dict["note"] = item.note
            # tmp_dict["risk_level"] = item.risk_level
            if str(item.risk_level) == "3":
                tmp_dict["risk_level"] = "高"
            elif str(item.risk_level) == "2":
                tmp_dict["risk_level"] = "中"
            elif str(item.risk_level) == "1":
                tmp_dict["risk_level"] = "低"
            else:
                tmp_dict["risk_level"] = "未定"
            tmp_dict["stage"] = item.stage
            tmp_dict["area"] = item.area
            tmp_dict["rule_name"] = item.rule_name
            resp_data["data"]["record_list"].append(tmp_dict)
            cnt += 1
            if cnt == 10:
                break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)
