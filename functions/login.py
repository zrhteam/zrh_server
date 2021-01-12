from flask import Blueprint, jsonify, request, render_template, session, json
from datetime import datetime
import functions.cache_data as gl

login_blueprint = Blueprint('login', __name__, url_prefix='/api/login')


@login_blueprint.route('/get_grant', methods=['POST', 'GET'])
def get_grant():
    print("In function get_grant")
    start_t = datetime.now()
    name = request.values.get("username")
    password = request.values.get("password")
    print("Received name: " + str(name))
    print("Received password: " + str(password))
    flag = 0
    resp_data = {"code": 10000,
                 "data": {"user_grant": "",
                          "headquarter_tag": "",
                          "region_tag": "",
                          "project_tag": "",
                          "value": {}}}
    cache_risk_user = gl.get_value("cache_risk_user")
    cache_prj_with_tag = gl.get_value("cache_prj_with_tag")
    cache_check_location_map = gl.get_value("cache_check_location_map")
    print(cache_check_location_map)
    print(len(cache_check_location_map))
    for item in cache_risk_user:
        if item.name == name:
            if item.password == password:
                resp_data["data"]["user_grant"] = item.user_grant
                resp_data["data"]["headquarter_tag"] = item.headquarter_tag
                resp_data["data"]["region_tag"] = item.region_tag
                resp_data["data"]["project_tag"] = item.project_tag
                value = {}
                if item.user_grant == "超级用户":
                    value["headquarter_tag"] = {}
                    for ele in cache_prj_with_tag:
                        if ele.headquarter_tag is None:
                            continue
                        if ele.headquarter_tag not in value["headquarter_tag"].keys():
                            value["headquarter_tag"][ele.headquarter_tag] = {"region_tag": {}}
                        if ele.region_tag is None:
                            if "project_tag" not in value["headquarter_tag"][ele.headquarter_tag].keys():
                                value["headquarter_tag"][ele.headquarter_tag]["project_tag"] = {}
                            if ele.project_tag is None: # 如果project都为null，那么可以判断为测试项目，跳过
                                resp_data["code"] = -1
                                break
                            if ele.project_tag not in value["headquarter_tag"][ele.headquarter_tag]["project_tag"].keys():
                                value["headquarter_tag"][ele.headquarter_tag]["project_tag"][ele.project_tag] = []
                            # print(ele.project_code)
                            if ele.project_code in cache_check_location_map.keys():
                                value["headquarter_tag"][ele.headquarter_tag]["project_tag"][ele.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                        else:
                            if ele.region_tag not in value["headquarter_tag"][ele.headquarter_tag]["region_tag"].keys():
                                value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag] = {"project_tag": {}}
                            if ele.project_tag is None: # 如果project都为null，那么可以判断为测试项目，跳过
                                resp_data["code"] = -1
                                break
                            if ele.project_tag not in value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag]["project_tag"].keys():
                                value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag]["project_tag"][ele.project_tag] = []
                            # print(ele.project_code)
                            if ele.project_code in cache_check_location_map.keys():
                                value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag]["project_tag"][ele.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                elif item.user_grant == "总部":
                    value["headquarter_tag"] = {item.headquarter_tag: {"region_tag": {}}}
                    for ele in cache_prj_with_tag:
                        if ele.headquarter_tag == item.headquarter_tag:
                            if ele.region_tag is None:
                                if "project_tag" not in value["headquarter_tag"][item.headquarter_tag].keys():
                                    value["headquarter_tag"][item.headquarter_tag]["project_tag"] = {}
                                if ele.project_tag is None:  # 如果project都为null，那么可以判断为测试项目，跳过
                                    resp_data["code"] = -1
                                    break
                                if ele.project_tag not in value["headquarter_tag"][item.headquarter_tag][
                                    "project_tag"].keys():
                                    value["headquarter_tag"][item.headquarter_tag]["project_tag"][ele.project_tag] = []
                                # print(ele.project_code)
                                if ele.project_code in cache_check_location_map.keys():
                                    value["headquarter_tag"][item.headquarter_tag]["project_tag"][ele.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                            else:
                                if ele.region_tag not in value["headquarter_tag"][ele.headquarter_tag][
                                    "region_tag"].keys():
                                    value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag] = {"project_tag": {}}
                                if ele.project_tag is None:  # 如果project都为null，那么可以判断为测试项目，跳过
                                    continue
                                if ele.project_tag not in value["headquarter_tag"][item.headquarter_tag]["region_tag"][ele.region_tag][
                                    "project_tag"].keys():
                                    value["headquarter_tag"][item.headquarter_tag]["region_tag"][ele.region_tag]["project_tag"][ele.project_tag] = []
                                # print(ele.project_code)
                                if ele.project_code in cache_check_location_map.keys():
                                    value["headquarter_tag"][ele.headquarter_tag]["region_tag"][ele.region_tag][
                                    "project_tag"][ele.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                elif item.user_grant == "区域":
                    value["headquarter_tag"] = {item.headquarter_tag: {"region": {item.region_tag: {"project_tag": {}}}}}
                    for ele in cache_prj_with_tag:
                        if ele.region_tag == item.region_tag:
                            # print(ele.project_tag)
                            if ele.project_tag not in value["headquarter_tag"][item.headquarter_tag]["region_tag"][item.region_tag]["project_tag"].keys():
                                value["headquarter_tag"][item.headquarter_tag]["region_tag"][item.region_tag]["project_tag"][ele.project_tag] = []
                            # print(ele.project_code)
                            if ele.project_code in cache_check_location_map.keys():
                                value["headquarter_tag"][item.headquarter_tag]["region_tag"][item.region_tag]["project_tag"][
                                ele.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                elif item.user_grant == "项目":
                    value["headquarter_tag"] = {item.headquarter_tag: {"region": {item.region_tag: {"project_tag": {item.project_tag: []}}}}}
                    for ele in cache_prj_with_tag:
                        if ele.project_tag == item.project_tag:
                            # print(ele.project_code)
                            if ele.project_code in cache_check_location_map.keys():
                                value["headquarter_tag"][item.headquarter_tag]["region"][item.region_tag]["project_tag"][
                                item.project_tag].append({ele.project_code: cache_check_location_map[ele.project_code]})
                else:
                    resp_data["code"] = -1
                resp_data["data"]["value"] = value
                flag = 1

            else:
                resp_data["code"] = -1
            break
    if resp_data["data"]["user_grant"] == "":
        resp_data["code"] = -1
    print("Returned data: ")
    print(resp_data)
    end_t = datetime.now()
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)
