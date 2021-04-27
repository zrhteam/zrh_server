from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl
import time

region_blueprint = Blueprint('region', __name__, url_prefix='/api/region')


# region页面部分
#
# FunctionName: getRegionIndex
# Purpose: 显示该区域整体安全指数以及各专业安全指数
# Parameter:
# Return:

# region页面部分
#
# FunctionName: getRectificationNumber
# Purpose: 显示当前已检查项目数量
# Parameter:
# Return:
@region_blueprint.route('/region_project', methods=['POST'])
def region_project():
    print("In function get_region_number")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    cache_prj_with_tag = gl.get_value("cache_prj_with_tag")
    resp_data = {"code": 10000, "data": {"rectification_number": 0}}
    for item in cache_prj_with_tag:
        if region_name == item.region_tag:
            resp_data["data"]["rectification_number"] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getInitRegionRiskLevel
# Purpose: 显示该区域各风险等级对应的隐患数量
# Parameter:
# Return:
@region_blueprint.route('/region_risk_level', methods=['POST', 'GET'])
def region_risk_level():
    print("In function region_risk_level")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = {"code": 10000, "data": {"risk_level": {"1": 0, "2": 0, "3": 0}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            resp_data["data"]["risk_level"][str(item.risk_level)] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionRiskLevelYear
# Purpose: 按照年份显示该区域各等级风险对应的隐患数量
# Parameter:
# Return:
@region_blueprint.route('/region_risk_level_year', methods=['POST', 'GET'])
def region_risk_level_year():
    print("In function region_risk_level_year")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            cur_year = str(item.create_time).split('-')[0]
            if cur_year not in resp_data["data"].keys():
                resp_data["data"][cur_year] = {"1": 0, "2": 0, "3": 0}
            resp_data["data"][cur_year][item.risk_level] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionHighRIsk
# Purpose: 显示该区域未整改高风险隐患描述列表
# Parameter:
# Return:
@region_blueprint.route('/region_risk_list', methods=['POST', 'GET'])
def region_risk_list():
    print("In function region_risk_list")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = {"code": 10000, "data": {"note_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.risk_level == "3" and item.state != "5":
                resp_data["data"]["note_list"].append(item.note)
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# # region页面部分
# #
# # FunctionName: getRegionHighImage
# # Purpose: 显示该区域最新出现的10张未整改高风险隐患图片及该图片对应的检查名称和隐患描述
# # Parameter:
# # Return:
# @region_blueprint.route('/region_high_image', methods=['POST', 'GET'])
# def region_high_image():
#     print("In function region_high_image")
#     start_t = datetime.now()
#     region_name = request.form.get("region_name")
#     print("Received region_name " + str(region_name))
#     resp_data = { "code": 10000, "data": {"image_list": []}}
#     cache_cascade_record = gl.get_value("cache_cascade_record")
#     cache_sys_file = gl.get_value("cache_sys_file")
#     image_id_list = {}
#     for item in cache_cascade_record:
#         if region_name == item.region_tag:
#             if item.risk_level == "3" and item.state != "5":
#                 tmp_image_id_list = str(item.images_file_id).split(",")
#                 for ele in tmp_image_id_list:
#                     image_id_list[ele] = 0
#     for ele in cache_sys_file:
#         if str(ele.id) in image_id_list.keys():
#             image_url = ele.upload_host + ele.directory + ele.name
#             resp_data["data"]["image_list"].append(image_url)
#     print("Returned data: ")
#     print(resp_data)
#     end_t = datetime.now()
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

# region页面部分
#
# FunctionName: getInitRegionImage
# Purpose: 显示该区域最新出现的10张未整改高风险隐患图片及该图片对应的检查名称和隐患描述
# Parameter:
# Return:
@region_blueprint.route('/region_high_image', methods=['POST', 'GET'])
def region_high_image():
    print("In function region_high_image")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    # top = int(request.form.get("top"))
    print("Received region_name " + str(region_name))
    # print("Received top " + str(top))
    resp_data = {"code": 10000, "data": {"image_list": []}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    cache_sys_file = gl.get_value("cache_sys_file")
    image_id_list = {}
    # resp_data["check_code"] = latest_map["check_code"]
    # resp_data["check_time"] = latest_map["time"]
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            tmp_image_id_list = str(item.images_file_id).split(",")
            for ele in tmp_image_id_list:
                image_id_list[ele] = {}
                image_id_list[ele]["check_name"] = item.project_name
                image_id_list[ele]["note"] = item.note
                print("debug..." + str(item.create_time))
                image_id_list[ele]["create_time"] = int(
                    time.mktime(time.strptime(str(item.create_time), "%Y-%m-%d %H:%M:%S")))
    res = sorted(image_id_list.items(), key=lambda d: d[1]["create_time"], reverse=True)
    image_id_list = {}
    idx = 0
    # 取出前10张
    for ele in res:
        image_id_list[ele[0]] = ele[1]
        idx += 1
        if idx == 10:
            break
    for ele in cache_sys_file:
        if str(ele.id) in image_id_list.keys():
            image_url = ele.upload_host + ele.directory + ele.name
            resp_data["data"]["image_list"].append({"image_url": image_url, "check_name":
                image_id_list[str(ele.id)]["check_name"], "note": image_id_list[str(ele.id)]["note"]})
    # # 取前10张
    # resp_data["data"]["image_list"] = resp_data["data"]["image_list"][0: 10]
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionDistribution
# Purpose: 显示该区域各项目隐患数量在各风险等级和在各专业上的分布
# Parameter:
# Return:
@region_blueprint.route('/region_distribution', methods=['POST', 'GET'])
def region_distribution():
    print("In function region_distribution")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = {"code": 10000, "data": {"project_distribution": {}}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.project_tag not in resp_data["data"]["project_distribution"].keys():
                resp_data["data"]["project_distribution"][item.project_tag] = {"risk_level": {"1": 0, "2": 0, "3": 0},
                                                                               "major": {}}
            resp_data["data"]["project_distribution"][item.project_tag]["risk_level"][str(item.risk_level)] += 1
            if item.major_name not in resp_data["data"]["project_distribution"][item.project_tag]["major"].keys():
                resp_data["data"]["project_distribution"][item.project_tag]["major"][item.major_name] = 0
            resp_data["data"]["project_distribution"][item.project_tag]["major"][item.major_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getInitRegionNumberTop
# Purpose: 显示在不同筛选条件（专业/系统）下隐患数量排名前top的隐患描述
# Parameter:
# Return:
@region_blueprint.route('/region_rank_top', methods=['POST', 'GET'])
def region_rank_top():
    print("In function region_rank_top")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    condition = request.form.get("condition")
    top = int(request.form.get("top"))
    print("Received region_name " + str(region_name))
    print("Received condition " + str(condition))
    print("Received top " + str(top))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_note_map = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.note not in risk_note_map.keys():
                if condition == "major":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.major_name}
                elif condition == "system":
                    risk_note_map[item.note] = {"appear_time": 0, condition: item.system_name}
            risk_note_map[item.note]["appear_time"] += 1
    res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
        if idx == top:
            break
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionOtherTop
# Purpose: 显示在不同筛选条件（风险等级(1, 2,3, all)/致因阶段/分布区域）下，出现次数排名前top的隐患描述
# Parameter:
# Return:
@region_blueprint.route('/region_other_top', methods=['POST', 'GET'])
def region_other_top():
    print("In function region_other_top")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    flag = int(request.form.get("flag"))
    top = int(request.form.get("top"))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    if flag == 1:  # 致因阶段
        stage = request.form.get("stage")
        print("Received stage " + str(stage))
        for item in cache_cascade_record:
            t_stage = ''
            if item.stage == '':
                t_stage = "未定义"
            else:
                t_stage = item.stage.split("阶段")[0]
            if region_name == item.region_tag and t_stage == stage:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 2:  # 风险等级
        risk_level = request.form.get("risk_level")
        print("Received risk_level " + str(risk_level))
        for item in cache_cascade_record:
            if region_name == item.region_tag:
                if risk_level == "all" or risk_level == item.risk_level:
                    if item.note not in resp_data["data"].keys():
                        resp_data["data"][item.note] = 0
                    resp_data["data"][item.note] += 1
    elif flag == 3:  # 专业
        major_name = request.form.get("major_name")
        print("Received major_name " + str(major_name))
        for item in cache_cascade_record:
            if region_name == item.region_tag and major_name == item.major_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 4:  # 专业 + 系统
        major_name = request.form.get("major_name")
        system_name = request.form.get("system_name")
        print("Received major_name " + str(major_name))
        print("Received system_name " + str(system_name))
        for item in cache_cascade_record:
            if region_name == item.region_tag and major_name == item.major_name and system_name == item.system_name:
                if item.note not in resp_data["data"].keys():
                    resp_data["data"][item.note] = 0
                resp_data["data"][item.note] += 1
    elif flag == 5:  # 专业 + 区域
        major_name = request.form.get("major_name")
        area = request.form.get("area")
        print("Received major_name " + str(major_name))
        print("Received area " + str(area))
        for item in cache_cascade_record:
            if region_name == item.region_tag and major_name == item.major_name and area == item.area:
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
    # print("In function region_other_top")
    # start_t = datetime.now()
    # region_name = request.form.get("region_name")
    # condition = request.form.get("condition")
    # level = request.form.get("level")
    # top = int(request.form.get("top"))
    # print("Received region_name " + str(region_name))
    # print("Received condition " + str(condition))
    # print("Received top " + str(top))
    # cache_cascade_record = gl.get_value("cache_cascade_record")
    # resp_data = {"code": 10000, "data": {}}
    # risk_note_map = {}
    # for item in cache_cascade_record:
    #     if region_name == item.region_tag:
    #         if item.note not in risk_note_map.keys():
    #             if condition == "risk_level":
    #                 risk_note_map[item.note] = {"appear_time": 0, condition: level}
    #             elif condition == "stage":
    #                 risk_note_map[item.note] = {"appear_time": 0, condition: item.stage}
    #             elif condition == "area":
    #                 risk_note_map[item.note] = {"appear_time": 0, condition: item.area}
    #         if condition == "risk_level":
    #             if level == "all":
    #                 risk_note_map[item.note]["appear_time"] += 1
    #             else:
    #                 if str(level) == item.risk_level:
    #                     risk_note_map[item.note]["appear_time"] += 1
    #         else:
    #             risk_note_map[item.note]["appear_time"] += 1
    # res = sorted(risk_note_map.items(), key=lambda d: d[1]["appear_time"], reverse=True)
    # idx = 0
    # for ele in res:
    #     resp_data["data"][ele[0]] = ele[1]
    #     idx += 1
    #     if idx == top:
    #         break
    # print("Returned data: ")
    # print(resp_data)
    # end_t = datetime.now()
    # print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    # return jsonify(resp_data)


# region页面部分
#
# FunctionName: getInitRegionRiskRank
# Purpose: 显示按照隐累计高风险患数量排名后的项目名称
# Parameter:
# Return:
@region_blueprint.route('/region_index_rank', methods=['POST', 'GET'])
def region_index_rank():
    print("In function region_index_rank")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_project_map = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.project_tag not in risk_project_map.keys():
                risk_project_map[item.project_tag] = 0
            if str(item.risk_level) == "3":
                risk_project_map[item.project_tag] += 1
    res = sorted(risk_project_map.items(), key=lambda d: d[1], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionCheckRank
# Purpose: 基于该区域每个项目的检查次数对项目排名 ?
# Parameter:
# Return:
@region_blueprint.route('/region_check_rank', methods=['POST', 'GET'])
def region_check_rank():
    print("In function region_check_rank")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    risk_project_map = {}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            if item.project_tag not in risk_project_map.keys():
                risk_project_map[item.project_tag] = 0
            risk_project_map[item.project_tag] += 1
    res = sorted(risk_project_map.items(), key=lambda d: d[1], reverse=True)
    idx = 0
    for ele in res:
        resp_data["data"][ele[0]] = {"rank": idx, "count": ele[1]}
        idx += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionMajorRatio
# Purpose: 按照年份显示该区域各等级风险对应的隐患数量
# Parameter:
# Return:
@region_blueprint.route('/region_major_ratio', methods=['POST', 'GET'])
def region_major_ratio():
    print("In function region_major_ratio")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
            # cur_year = str(item.create_time).split('-')[0]
            if item.major_name not in resp_data["data"].keys():
                resp_data["data"][item.major_name] = 0
            resp_data["data"][item.major_name] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionSystemRatio
# Purpose: 显示该区域不同专业下各系统隐患占比情况
# Parameter:
# Return:
@region_blueprint.route('/region_system_ratio', methods=['POST', 'GET'])
def region_system_ratio():
    print("In function region_system_ratio")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    major = request.form.get("major")
    print("Received region_name " + str(region_name))
    print("Received major " + str(major))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
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


# region页面部分
#
# FunctionName: getRegionStageRatio
# Purpose: 根据隐患数量显示不同致因阶段的占比情况
# Parameter:
# Return:
@region_blueprint.route('/region_stage_ratio', methods=['POST', 'GET'])
def region_stage_ratio():
    print("In function region_stage_ratio")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
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


# region页面部分
#
# FunctionName: getRegionAreaRatio
# Purpose: 根据隐患数量显示不同分布区域的占比情况
# Parameter: major_name
# Return:
#
@region_blueprint.route('/region_area_ratio', methods=['POST', 'GET'])
def region_area_ratio():
    print("In function region_area_ratio")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    major_name = request.form.get("major_name")
    # 新增 major 入参
    print("Received region_name " + str(region_name))
    print("Received major_name " + str(major_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if region_name == item.region_tag and major_name == item.major_name:
            area = "未定义" if item.area == '' else item.area
            # if item.major_name not in resp_data["data"].keys():
            #     resp_data["data"][item.major_name] = {}
            if area not in resp_data["data"].keys():
                resp_data["data"][area] = 0
            resp_data["data"][area] += 1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# region页面部分
#
# FunctionName: getRegionRiskLevelRatio
# Purpose: 不同专业下风险等级占比
# Parameter:
# Return:
@region_blueprint.route('/region_risk_level_ratio', methods=['POST', 'GET'])
def region_risk_level_ratio():
    print("In function region_risk_level_ratio")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name " + str(region_name))
    cache_cascade_record = gl.get_value("cache_cascade_record")
    resp_data = {"code": 10000, "data": {}}
    for item in cache_cascade_record:
        if region_name == item.region_tag:
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


# region页面部分
#
# FunctionName: getRegionDangerProblem
# Purpose: 显示该区域存在的红线问题及其对应的原因
# Parameter:
# Return:
@region_blueprint.route('/region_danger_problem', methods=['POST', 'GET'])
def region_danger_problem():
    print("In function region_danger_problem")
    start_t = datetime.now()
    region_name = request.form.get("region_name")
    print("Received region_name: " + str(region_name))
    resp_data = {"code": 10000, "data": {}}
    cache_cascade_record = gl.get_value("cache_cascade_record")
    for item in cache_cascade_record:
        if region_name == item.region_tag:
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
