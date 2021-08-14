from datetime import datetime

from flask import Blueprint, jsonify, request

import functions.cache_data as gl

insight_func_blueprint = Blueprint('insight_func', __name__, url_prefix='/api/analyze/insight_func')


# 红线问题分析
#
# FunctionName: analyze_red_line_data
# Purpose: 获取红线问题
# Parameter: json -> list of (check_key, start, end, flag)
# Return: json -> resp_data = {"code": 10000, "data": {"消防管网末端无水比例达到百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "中庭区域疏散指示或应急照明故障": {"total": 0.0, "ratio": {}},
#                                          "消防风机不能远程多线启动": {"total": 0.0, "ratio": {}},
#                                          "出现280度排烟防火阀关闭后不能连锁排烟风机停止": {"total": 0.0, "ratio": {}},
#                                          "点位、回路故障率达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "报警主机存在死机、延迟等情况": {"total": 0.0, "ratio": {}},
#                                          "物理地址描述不详或错误、未定义达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "消防联动逻辑关系错误率达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "流量开关、低压压力开关不能连锁启泵": {"total": 0.0, "ratio": {}},
#                                          "消防水泵不能远程多线启动": {"total": 0.0, "ratio": {}},
#                                          "排烟阀不能联动相应排烟风机自动启动": {"total": 0.0, "ratio": {}},
#                                          "气体模拟测试时防护区内风机、风阀等设备未联动关闭": {"total": 0.0, "ratio": {}},
#                                          "任一组水泵不能正常运行": {"total": 0.0, "ratio": {}},
#                                          "中庭区域消防广播故障": {"total": 0.0, "ratio": {}},
#                                          "防火门监控系统故障较多": {"total": 0.0, "ratio": {}}}}
# @insight_func_blueprint.route('/red_line', methods=['POST', 'GET'])
# def analyze_red_line_data():
#     print("In function analyze_red_line_data")
#     start_t = datetime.now()
#     cache_final_record = gl.get_value("final_record")
#     cache_final_tag = gl.get_value("final_tag")
#     resp_data = {"code": 10000, "data": {"消防管网末端无水比例达到百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "中庭区域疏散指示或应急照明故障": {"total": 0.0, "ratio": {}},
#                                          "消防风机不能远程多线启动": {"total": 0.0, "ratio": {}},
#                                          "出现280度排烟防火阀关闭后不能连锁排烟风机停止": {"total": 0.0, "ratio": {}},
#                                          "点位、回路故障率达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "报警主机存在死机、延迟等情况": {"total": 0.0, "ratio": {}},
#                                          "物理地址描述不详或错误、未定义达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "消防联动逻辑关系错误率达百分之十及以上": {"total": 0.0, "ratio": {}},
#                                          "流量开关、低压压力开关不能连锁启泵": {"total": 0.0, "ratio": {}},
#                                          "消防水泵不能远程多线启动": {"total": 0.0, "ratio": {}},
#                                          "排烟阀不能联动相应排烟风机自动启动": {"total": 0.0, "ratio": {}},
#                                          "气体模拟测试时防护区内风机、风阀等设备未联动关闭": {"total": 0.0, "ratio": {}},
#                                          "任一组水泵不能正常运行": {"total": 0.0, "ratio": {}},
#                                          "中庭区域消防广播故障": {"total": 0.0, "ratio": {}},
#                                          "防火门监控系统故障较多": {"total": 0.0, "ratio": {}}}}
#     # flag=1 check_key = headquarter_name/region_name
#     # flag=2 check_key = headquarter_name/region_name/project_name
#     # flag=3 check_key = check_code
#     # Test:
#     # flag = 1  # request.values.get("flag")
#     # check_key = "华润置地/华东大区"  # request.values.get("check_key")
#     flag = request.values.get("flag")
#     check_key = request.values.get("check_key")
#     # 若没有传入时间参数，则start为最小时间，end为最大时间
#     start = datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#     end = datetime.strptime("9999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
#     if request.values.get("start") is not None:
#         start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
#     if request.values.get("end") is not None:
#         end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
#     contained_check_map = {}
#     print("Received time " + str(start) + " to " + str(end))
#     if flag == "1":
#         print("Received region_name " + str(check_key))
#         # 找到所有在该区域下的检查
#         for item in cache_final_tag:
#             if str(item.headquarter_tag) + "/" + str(item.region_tag) == check_key:
#                 contained_check_map[item.code] = 0
#         for item in cache_final_record:
#             # 如果当前检查在这个区域中,并且在时间范围内
#             if item.project_code in contained_check_map.keys() and \
#                     end >= item.create_time >= start:
#                 # 找到每一个红线问题，level为3，消防专业，并除去两端空格
#                 if str(item.risk_level).strip() == "3" and str(item.major_name).strip() == "消防专业" and \
#                         item.alert_indicator is not None:
#                     # 若problem i不为空，则看其是否已经存在在字典中
#                     # 若存在则对应红线指标的problem i计数加一，若不存在则将其数量置为1加入字典
#                     if item.problem1 is not None and \
#                             item.problem1 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] += 1.0
#                     elif item.problem1 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] = 1.0
#
#                     if item.problem2 is not None and \
#                             item.problem2 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] += 1.0
#                     elif item.problem2 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] = 1.0
#
#                     if item.problem3 is not None and \
#                             item.problem3 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] += 1.0
#                     elif item.problem3 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] = 1.0
#
#                     if item.problem4 is not None and \
#                             item.problem4 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] += 1.0
#                     elif item.problem4 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] = 1.0
#
#                     if item.problem5 is not None and \
#                             item.problem5 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] += 1.0
#                     elif item.problem5 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] = 1.0
#
#     if flag == "2":
#         print("Received project_name " + str(check_key))
#         # 找到所有在该项目下的检查
#         for item in cache_final_tag:
#             if str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag) == check_key:
#                 contained_check_map[item.code] = 0
#         for item in cache_final_record:
#             # 如果当前检查在这个项目中，并且在时间范围内
#             if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
#                 # 红线问题，level为3，消防专业，并除去两端空格
#                 if str(item.risk_level).strip() == "3" and str(item.major_name).strip() == "消防专业" and \
#                         item.alert_indicator is not None:
#                     # 若problem i不为空，则看其是否已经存在在字典中
#                     # 若存在则对应红线指标的problem i计数加一，若不存在则将其数量置为1加入字典
#                     if item.problem1 is not None and \
#                             item.problem1 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] += 1.0
#                     elif item.problem1 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] = 1.0
#
#                     if item.problem2 is not None and \
#                             item.problem2 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] += 1.0
#                     elif item.problem2 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] = 1.0
#
#                     if item.problem3 is not None and \
#                             item.problem3 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] += 1.0
#                     elif item.problem3 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] = 1.0
#
#                     if item.problem4 is not None and \
#                             item.problem4 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] += 1.0
#                     elif item.problem4 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] = 1.0
#
#                     if item.problem5 is not None and \
#                             item.problem5 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] += 1.0
#                     elif item.problem5 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] = 1.0
#
#     if flag == "3":
#         print("Received check_code " + str(check_key))
#         for item in cache_final_record:
#             # 如果当前检查在这个项目中，并且在时间范围内
#             if item.project_code == check_key and end >= item.create_time >= start:
#                 # 红线问题，level为3，消防专业，并除去两端空格
#                 if str(item.risk_level).strip() == "3" and str(item.major_name).strip() == "消防专业" and \
#                         item.alert_indicator is not None:
#                     # 若problem i不为空，则看其是否已经存在在字典中
#                     # 若存在则对应红线指标的problem i计数加一，若不存在则将其数量置为1加入字典
#                     if item.problem1 is not None and \
#                             item.problem1 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] += 1.0
#                     elif item.problem1 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem1] = 1.0
#
#                     if item.problem2 is not None and \
#                             item.problem2 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] += 1.0
#                     elif item.problem2 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem2] = 1.0
#
#                     if item.problem3 is not None and \
#                             item.problem3 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] += 1.0
#                     elif item.problem3 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem3] = 1.0
#
#                     if item.problem4 is not None and \
#                             item.problem4 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] += 1.0
#                     elif item.problem4 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem4] = 1.0
#
#                     if item.problem5 is not None and \
#                             item.problem5 in resp_data["data"][item.alert_indicator]["ratio"].keys():
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] += 1.0
#                     elif item.problem5 is not None:
#                         resp_data["data"][item.alert_indicator]["total"] += 1.0
#                         resp_data["data"][item.alert_indicator]["ratio"][item.problem5] = 1.0
#
#     # 每一个问题：计数/问题总数，求出占比，若红线指标计数为0，则返回-1
#     for item in resp_data["data"]:
#         for ele in resp_data["data"][item]["ratio"]:
#             if resp_data["data"][item]["total"] != 0:
#                 ratio = resp_data["data"][item]["ratio"][ele] / resp_data["data"][item]["total"]
#                 resp_data["data"][item]["ratio"][ele] = round(ratio, 3)
#             # 不存在红线问题
#             else:
#                 resp_data["data"][item]["ratio"][ele] = -1
#
#     end_t = datetime.now()
#     print(resp_data)
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

# 7.21 修改版本
@insight_func_blueprint.route('/red_line', methods=['POST', 'GET'])
def analyze_red_line_data():
    print("In function analyze_red_line_data")
    print(request.values.get('check_key'))
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    resp_data = {"code": 10000, "data": {"消防管网末端无水比例达到百分之十及以上": {"total": 0.0, "ratio": {}},
                                         "中庭区域疏散指示或应急照明故障": {"total": 0.0, "ratio": {}},
                                         "消防风机不能远程多线启动": {"total": 0.0, "ratio": {}},
                                         "出现280度排烟防火阀关闭后不能连锁排烟风机停止": {"total": 0.0, "ratio": {}},
                                         "点位、回路故障率达百分之十及以上": {"total": 0.0, "ratio": {}},
                                         "报警主机存在死机、延迟等情况": {"total": 0.0, "ratio": {}},
                                         "物理地址描述不详或错误、未定义达百分之十及以上": {"total": 0.0, "ratio": {}},
                                         "消防联动逻辑关系错误率达百分之十及以上": {"total": 0.0, "ratio": {}},
                                         "流量开关、低压压力开关不能连锁启泵": {"total": 0.0, "ratio": {}},
                                         "消防水泵不能远程多线启动": {"total": 0.0, "ratio": {}},
                                         "排烟阀不能联动相应排烟风机自动启动": {"total": 0.0, "ratio": {}},
                                         "气体模拟测试时防护区内风机、风阀等设备未联动关闭": {"total": 0.0, "ratio": {}},
                                         "任一组水泵不能正常运行": {"total": 0.0, "ratio": {}},
                                         "中庭区域消防广播故障": {"total": 0.0, "ratio": {}},
                                         "防火门监控系统故障较多": {"total": 0.0, "ratio": {}}}}
    # flag=1 check_key = headquarter_name/region_name
    # flag=2 check_key = headquarter_name/region_name/project_name
    # flag=3 check_key = check_code
    # Test:
    # flag = 1  # request.values.get("flag")
    # check_key = "华润置地/华东大区"  # request.values.get("check_key")
    # flag = request.values.get("flag")
    check_key = request.values.get('check_key')
    # 若没有传入时间参数，则start为最小时间，end为最大时间
    start = datetime.strptime("0001-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime("9999-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    if request.values.get('start') is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get('end') is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    contained_check_map = check_key.split("%")
    print("Received time " + str(start) + " to " + str(end))
    print("Received check_key " + check_key)
    for item in cache_final_record:
        if item.project_code in contained_check_map and end >= item.create_time >= start:
            # 找到每一个红线问题，level为3，消防专业，并除去两端空格
            if str(item.risk_level) == "3" and str(item.major_name) == "消防专业" and item.alert_indicator is not None:
                # 若problem i不为空，则看其是否已经存在在字典中
                # 若存在则对应红线指标的problem i计数加一，若不存在则将其数量置为1加入字典
                if item.problem1 is not None and \
                        item.problem1 in resp_data["data"][item.alert_indicator]["ratio"].keys():
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem1] += 1.0
                elif item.problem1 is not None:
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem1] = 1.0

                if item.problem2 is not None and \
                        item.problem2 in resp_data["data"][item.alert_indicator]["ratio"].keys():
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem2] += 1.0
                elif item.problem2 is not None:
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem2] = 1.0

                if item.problem3 is not None and \
                        item.problem3 in resp_data["data"][item.alert_indicator]["ratio"].keys():
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem3] += 1.0
                elif item.problem3 is not None:
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem3] = 1.0

                if item.problem4 is not None and \
                        item.problem4 in resp_data["data"][item.alert_indicator]["ratio"].keys():
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem4] += 1.0
                elif item.problem4 is not None:
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem4] = 1.0

                if item.problem5 is not None and \
                        item.problem5 in resp_data["data"][item.alert_indicator]["ratio"].keys():
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem5] += 1.0
                elif item.problem5 is not None:
                    resp_data["data"][item.alert_indicator]["total"] += 1.0
                    resp_data["data"][item.alert_indicator]["ratio"][item.problem5] = 1.0

    # 每一个问题：计数/问题总数，求出占比，若红线指标计数为0，则返回-1
    for item in resp_data["data"]:
        for ele in resp_data["data"][item]["ratio"]:
            if resp_data["data"][item]["total"] != 0:
                ratio = resp_data["data"][item]["ratio"][ele] / resp_data["data"][item]["total"]
                resp_data["data"][item]["ratio"][ele] = round(ratio, 3)
            # 不存在红线问题
            else:
                resp_data["data"][item]["ratio"][ele] = -1

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析A 趋势图
#
# FunctionName: analyze_tendency_headquarter
# Purpose: 可以选择纵坐标为隐患数量（隐患总数、高风险数量、专业隐患总数、专业高风险数量），横坐标为时间点，对比对象可选
# Parameter: json -> {"headquarter_name":{}, "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "data": {"headquarter_name_1": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            },
#                                                      "headquarter_name_2": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            }
#                                                     }
#                             }
# @insight_func_blueprint.route('/tendency_headquarter', methods=['POST', 'GET'])
# def analyze_tendency_headquarter():
#     print("In function analyze_tendency_headquarter")
#     start_t = datetime.now()
#     cache_final_record = gl.get_value("final_record")
#     cache_final_tag = gl.get_value("final_tag")
#     # Test:"华润置地%菜鸟物流"
#     headquarter_name = request.values.get("headquarter_name").split("%")
#     if headquarter_name is None:
#         print("Missing headquarter parameter")
#         return None
#     # Test:"消防专业"
#     major_name = request.values.get("major_name")
#     # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
#     start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#     end = datetime.now()
#     if request.values.get("start") is not None:
#         start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
#     if request.values.get("end") is not None:
#         end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
#     resp_data = {"code": 10000, "data": {}}
#     year_end = end.year
#     month_end = end.month
#     print("Received time " + str(start) + " to " + str(end))
#     print("Received headquarter_name " + str(headquarter_name))
#     print("Received major_name " + str(major_name))
#     # 对于每个总部，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
#     for item in headquarter_name:
#         resp_data["data"][item] = {}
#         year_start = start.year
#         month_start = start.month
#         while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
#             # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
#             resp_data["data"][item][str(year_start) + "-" + str(month_start)] = {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#             month_start += 1
#             if month_start > 12:
#                 year_start += 1
#                 month_start = 1
#
#     # 找到所有在该总部下的检查，并将check_code与总部名称做映射
#     contained_check_map = {}
#     for item in cache_final_tag:
#         if item.headquarter_tag in headquarter_name:
#             contained_check_map[item.code] = item.headquarter_tag
#
#     # 遍历record表
#     for item in cache_final_record:
#         # 如果当前记录所属的检查在这个总部中，并且在时间范围内
#         if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
#             year = item.create_time.year
#             month = item.create_time.month
#             # 通过contained_check_map用check_code取出对应的总部名称，更新相对应的隐患数量
#             resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)]["risk"] += 1
#             # 高风险隐患数量
#             if item.risk_level == "3":
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "risk_high"] += 1
#             # 专业隐患数量
#             if item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk"] += 1
#             # 专业高风险隐患数量
#             if item.risk_level == "3" and item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk_high"] += 1
#     end_t = datetime.now()
#     print(resp_data)
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

# 7.22修改版本
@insight_func_blueprint.route('/tendency_headquarter', methods=['POST', 'GET'])
def analyze_tendency_headquarter():
    print("In function analyze_tendency_headquarter")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:"华润置地%菜鸟物流"
    headquarter_name = request.values.get("headquarter_name").split("%")
    if headquarter_name is None:
        print("Missing headquarter parameter")
        return None
    # Test:"消防专业"
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "data": {}}
    year_end = end.year
    month_end = end.month
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name " + str(headquarter_name))
    print("Received major_name " + str(major_name))
    # 对于每个总部，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
    for item in headquarter_name:
        resp_data["data"][item] = {}
        year_start = start.year
        month_start = start.month
        while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
            # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
            if month_start < 10:
                resp_data["data"][item][str(year_start) + "-0" + str(month_start)] = {"risk": 0.0,
                                                                                      "risk_high": 0.0,
                                                                                      "major_risk": 0.0,
                                                                                      "major_risk_high": 0.0,
                                                                                      "total_check": 0.0}
            else:
                resp_data["data"][item][str(year_start) + "-" + str(month_start)] = {"risk": 0.0,
                                                                                     "risk_high": 0.0,
                                                                                     "major_risk": 0.0,
                                                                                     "major_risk_high": 0.0,
                                                                                     "total_check": 0.0}
            month_start += 1
            if month_start > 12:
                year_start += 1
                month_start = 1
    # 找到所有在该总部下的检查，若时间符合，当月总检查数+1，并将check_code与总部名称和月份做映射
    contained_check_map = {}
    contained_time_map = {}
    for item in cache_final_tag:
        if item.headquarter_tag in headquarter_name:
            # 若当前检查时间与所选时间有重合，则将其加入目标检查中
            if item.plan_start_time <= end and item.plan_end_time >= start:
                contained_check_map[item.code] = item.headquarter_tag
                year_check = item.plan_end_time.year
                month_check = item.plan_end_time.month
                time = str(year_check)
                if month_check < 10:
                    time = time + "-0" + str(month_check)
                else:
                    time = time + "-" + str(month_check)

                # 计算总检查数
                if time in resp_data["data"][item.headquarter_tag]:
                    resp_data["data"][item.headquarter_tag][time]["total_check"] += 1.0
                    contained_time_map[item.code] = time
                else:
                    if month_end < 10:
                        resp_data["data"][item.headquarter_tag][str(year_end) + "-0" + str(month_end)][
                            "total_check"] += 1.0
                        contained_time_map[item.code] = str(year_end) + "-0" + str(month_end)
                    else:
                        resp_data["data"][item.headquarter_tag][str(year_end) + "-" + str(month_end)][
                            "total_check"] += 1.0
                        contained_time_map[item.code] = str(year_end) + "-" + str(month_end)

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在check_map中，则为符合条件的记录
        if item.project_code in contained_check_map.keys():
            # 通过contained_check_map用check_code取出对应的总部名称，更新相对应的隐患数量
            resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                "risk"] += 1
            # 高风险隐患数量
            if item.risk_level == "3":
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "risk_high"] += 1
            # 专业隐患数量
            if item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "major_risk"] += 1
            # 专业高风险隐患数量
            if item.risk_level == "3" and item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "major_risk_high"] += 1

    # 风险总数为 当月风险总数/当月总检查数
    for head in resp_data["data"]:
        for month in resp_data["data"][head]:
            if resp_data["data"][head][month]["total_check"] != 0:
                resp_data["data"][head][month]["risk"] /= resp_data["data"][head][month]["total_check"]
                resp_data["data"][head][month]["risk"] = round(resp_data["data"][head][month]["risk"], 1)
                resp_data["data"][head][month]["risk_high"] /= resp_data["data"][head][month]["total_check"]
                resp_data["data"][head][month]["risk_high"] = round(resp_data["data"][head][month]["risk_high"], 1)
                # 如果为全部专业则不筛选
                if major_name == "全部专业":
                    resp_data["data"][head][month]["major_risk"] = resp_data["data"][head][month]["risk"]
                    resp_data["data"][head][month]["major_risk_high"] = resp_data["data"][head][month]["risk_high"]
                else:
                    resp_data["data"][head][month]["major_risk"] /= resp_data["data"][head][month]["total_check"]
                    resp_data["data"][head][month]["major_risk"] = round(resp_data["data"][head][month]["major_risk"],
                                                                         1)
                    resp_data["data"][head][month]["major_risk_high"] /= resp_data["data"][head][month]["total_check"]
                    resp_data["data"][head][month]["major_risk_high"] = round(
                        resp_data["data"][head][month]["major_risk_high"], 1)

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析A 趋势图
#
# FunctionName: analyze_tendency_region
# Purpose: 可以选择纵坐标为隐患数量（隐患总数、高风险数量、专业隐患总数、专业高风险数量），横坐标为时间点，对比对象可选
# Parameter: json -> {"region_name":{"headquarter_name/region_name"}, "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "data": {"headquarter_name/region_name_1": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            },
#                                                      "headquarter_name/region_name_2": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            }
#                                                     }
#                             }
# @insight_func_blueprint.route('/tendency_region', methods=['POST', 'GET'])
# def analyze_tendency_region():
#     print("In function analyze_tendency_region")
#     start_t = datetime.now()
#     cache_final_record = gl.get_value("final_record")
#     cache_final_tag = gl.get_value("final_tag")
#     # Test: "华润置地/华东大区%菜鸟物流/华东区域"
#     region_name = request.values.get("region_name").split("%")
#     if region_name is None:
#         print("Missing region parameter")
#         return None
#     major_name = request.values.get("major_name")  # Test: "消防专业"
#     # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
#     start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#     end = datetime.now()
#     if request.values.get("start") is not None:
#         start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
#     if request.values.get("end") is not None:
#         end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
#     resp_data = {"code": 10000, "data": {}}
#
#     year_end = end.year
#     month_end = end.month
#     print("Received time " + str(start) + " to " + str(end))
#     print("Received headquarter_name/region_name " + str(region_name))
#     print("Received major_name " + str(major_name))
#     # 对于每个区域，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
#     for item in region_name:
#         resp_data["data"][item] = {}
#         year_start = start.year
#         month_start = start.month
#         while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
#             # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
#             resp_data["data"][item][str(year_start) + "-" + str(month_start)] \
#                 = {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#             month_start += 1
#             if month_start > 12:
#                 year_start += 1
#                 month_start = 1
#
#     # 找到所有在该区域下的检查，并将check_code与区域名称做映射
#     contained_check_map = {}
#     for item in cache_final_tag:
#         if str(item.headquarter_tag) + "/" + str(item.region_tag) in region_name:
#             contained_check_map[item.code] = str(item.headquarter_tag) + "/" + str(item.region_tag)
#
#     # 遍历record表
#     for item in cache_final_record:
#         # 如果当前记录所属的检查在这个区域中，并且在时间范围内
#         if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
#             year = item.create_time.year
#             month = item.create_time.month
#             # 通过contained_check_map用check_code取出对应的区域名称，更新相对应的隐患数量
#             resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)]["risk"] += 1
#             # 高风险隐患数量
#             if item.risk_level == "3":
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "risk_high"] += 1
#             # 专业隐患数量
#             if item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk"] += 1
#             # 专业高风险隐患数量
#             if item.risk_level == "3" and item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk_high"] += 1
#     end_t = datetime.now()
#     print(resp_data)
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

# 7.30修改版本
@insight_func_blueprint.route('/tendency_region', methods=['POST', 'GET'])
def analyze_tendency_region():
    print("In function analyze_tendency_region")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test: "华润置地/华东大区%菜鸟物流/华东区域"
    region_name = request.values.get("region_name").split("%")
    major_name = request.values.get("major_name")  # Test: "消防专业"
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "data": {}}

    year_end = end.year
    month_end = end.month
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name/region_name " + str(region_name))
    print("Received major_name " + str(major_name))
    # 对于每个区域，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
    for item in region_name:
        resp_data["data"][item] = {}
        year_start = start.year
        month_start = start.month
        while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
            # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
            if month_start < 10:
                resp_data["data"][item][str(year_start) + "-0" + str(month_start)] = {"risk": 0.0,
                                                                                      "risk_high": 0.0,
                                                                                      "major_risk": 0.0,
                                                                                      "major_risk_high": 0.0,
                                                                                      "total_check": 0.0}
            else:
                resp_data["data"][item][str(year_start) + "-" + str(month_start)] = {"risk": 0.0,
                                                                                     "risk_high": 0.0,
                                                                                     "major_risk": 0.0,
                                                                                     "major_risk_high": 0.0,
                                                                                     "total_check": 0.0}
            month_start += 1
            if month_start > 12:
                year_start += 1
                month_start = 1

    # 找到所有在该区域下的检查，并将check_code与区域名称做映射
    contained_check_map = {}
    contained_time_map = {}
    for item in cache_final_tag:
        region_key = str(item.headquarter_tag) + "/" + str(item.region_tag)
        if region_key in region_name:
            # 若当前检查时间与所选时间有重合，则将其加入目标检查中
            if item.plan_start_time <= end and item.plan_end_time >= start:
                contained_check_map[item.code] = region_key
                # 将检查的结束时间作为判定时间
                year_check = item.plan_end_time.year
                month_check = item.plan_end_time.month
                time = str(year_check)
                if month_check < 10:
                    time = time + "-0" + str(month_check)
                else:
                    time = time + "-" + str(month_check)
                # 计算总检查数
                if time in resp_data["data"][region_key]:
                    resp_data["data"][region_key][time]["total_check"] += 1.0
                    contained_time_map[item.code] = time
                else:
                    if month_end < 10:
                        resp_data["data"][region_key][str(year_end) + "-0" + str(month_end)][
                            "total_check"] += 1.0
                        contained_time_map[item.code] = str(year_end) + "-0" + str(month_end)
                    else:
                        resp_data["data"][region_key][str(year_end) + "-" + str(month_end)][
                            "total_check"] += 1.0
                        contained_time_map[item.code] = str(year_end) + "-" + str(month_end)

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在check_map中，则为符合条件的记录
        if item.project_code in contained_check_map.keys():
            # 通过contained_check_map用check_code取出对应的总部名称，更新相对应的隐患数量
            resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                "risk"] += 1
            # 高风险隐患数量
            if item.risk_level == "3":
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "risk_high"] += 1
            # 专业隐患数量
            if item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "major_risk"] += 1
            # 专业高风险隐患数量
            if item.risk_level == "3" and item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][contained_time_map[item.project_code]][
                    "major_risk_high"] += 1

    # 风险总数为 当月风险总数/当月总检查数
    for region in resp_data["data"]:
        for month in resp_data["data"][region]:
            if resp_data["data"][region][month]["total_check"] != 0:
                resp_data["data"][region][month]["risk"] /= resp_data["data"][region][month]["total_check"]
                resp_data["data"][region][month]["risk"] = round(resp_data["data"][region][month]["risk"], 1)
                resp_data["data"][region][month]["risk_high"] /= resp_data["data"][region][month]["total_check"]
                resp_data["data"][region][month]["risk_high"] = round(resp_data["data"][region][month]["risk_high"], 1)
                if major_name == "全部专业":
                    resp_data["data"][region][month]["major_risk"] = resp_data["data"][region][month]["risk"]
                    resp_data["data"][region][month]["major_risk_high"] = resp_data["data"][region][month]["risk_high"]
                else:
                    resp_data["data"][region][month]["major_risk"] /= resp_data["data"][region][month]["total_check"]
                    resp_data["data"][region][month]["major_risk"] = round(
                        resp_data["data"][region][month]["major_risk"], 1)
                    resp_data["data"][region][month]["major_risk_high"] /= resp_data["data"][region][month][
                        "total_check"]
                    resp_data["data"][region][month]["major_risk_high"] = round(
                        resp_data["data"][region][month]["major_risk_high"], 1)
    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析A 趋势图
#
# FunctionName: analyze_tendency_project
# Purpose: 可以选择纵坐标为隐患数量（隐患总数、高风险数量、专业隐患总数、专业高风险数量），横坐标为时间点，对比对象可选
# Parameter: json -> {"project_name":{"headquarter_name/region_name/project_name"}, "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "data": {"headquarter_name/region_name/project_name_1": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            },
#                                                      "headquarter_name/region_name/project_name_2": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            }
#                                                     }
#                             }
# @insight_func_blueprint.route('/tendency_project', methods=['POST', 'GET'])
# def analyze_tendency_project():
#     print("In function analyze_tendency_project")
#     start_t = datetime.now()
#     cache_final_record = gl.get_value("final_record")
#     cache_final_tag = gl.get_value("final_tag")
#     # Test: "华润置地/华东大区/上海万象城%菜鸟物流/东北区域/菜鸟大件沈阳安得仓&菜鸟大件标品沈阳安得仓"
#     project_name = request.values.get("project_name").split("%")
#     if project_name is None:
#         print("Missing project parameter")
#         return None
#     major_name = request.values.get("major_name")  # Test: "消防专业"
#     # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
#     start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#     end = datetime.now()
#     if request.values.get("start") is not None:
#         start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
#     if request.values.get("end") is not None:
#         end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
#     resp_data = {"code": 10000, "data": {}}
#     year_end = end.year
#     month_end = end.month
#     print("Received time " + str(start) + " to " + str(end))
#     print("Received headquarter_name/region_name/project_name " + str(project_name))
#     print("Received major_name " + str(major_name))
#     # 对于每个项目，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
#     for item in project_name:
#         resp_data["data"][item] = {}
#         year_start = start.year
#         month_start = start.month
#         while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
#             # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
#             resp_data["data"][item][str(year_start) + "-" + str(month_start)] \
#                 = {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#             month_start += 1
#             if month_start > 12:
#                 year_start += 1
#                 month_start = 1
#
#     # 找到所有在该项目下的检查，并将check_code与项目名称做映射
#     contained_check_map = {}
#     for item in cache_final_tag:
#         if str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag) in project_name:
#             contained_check_map[item.code] = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(
#                 item.project_tag)
#
#     # 遍历record表
#     for item in cache_final_record:
#         # 如果当前记录所属的检查在这个项目中，并且在时间范围内
#         if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
#             year = item.create_time.year
#             month = item.create_time.month
#             # 通过contained_check_map用check_code取出对应的项目名称，更新相对应的隐患数量
#             resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)]["risk"] += 1
#             # 高风险隐患数量
#             if item.risk_level == "3":
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "risk_high"] += 1
#             # 专业隐患数量
#             if item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk"] += 1
#             # 专业高风险隐患数量
#             if item.risk_level == "3" and item.major_name == major_name:
#                 resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
#                     "major_risk_high"] += 1
#     end_t = datetime.now()
#     print(resp_data)
#     print("Query total time is: " + str((end_t - start_t).seconds) + "s")
#     return jsonify(resp_data)

# 7.22 修改版本
@insight_func_blueprint.route('/tendency_project', methods=['POST', 'GET'])
def analyze_tendency_project():
    print("In function analyze_tendency_project")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test: "华润置地/华东大区/上海万象城%菜鸟物流/东北区域/菜鸟大件沈阳安得仓&菜鸟大件标品沈阳安得仓"
    project_name = request.values.get("project_name").split("%")
    if project_name is None:
        print("Missing project parameter")
        return None
    major_name = request.values.get("major_name")  # Test: "消防专业"
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "size": 0, "data": {}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name/region_name/project_name " + str(project_name))
    print("Received major_name " + str(major_name))
    # 对于每个项目，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
    for item in project_name:
        resp_data["data"][item] = {}

    # 找到所有在该项目下的检查，并将check_code与项目名称做映射
    contained_check_map = {}
    for item in cache_final_tag:
        temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
        if temp in project_name:
            # 满足时间范围
            if item.plan_start_time <= end and item.plan_end_time >= start:
                contained_check_map[item.code] = temp
                resp_data["data"][temp][item.code] = {"risk": 0,
                                                      "risk_high": 0,
                                                      "major_risk": 0,
                                                      "major_risk_high": 0}
    # 将检查数量对齐，全部补零
    maxLength = 0
    for item in contained_check_map.values():
        if len(resp_data["data"][item]) > maxLength:
            maxLength = len(resp_data["data"][item])
    # for item in contained_check_map.values():
    #     if len(resp_data["data"][item]) < maxLength:
    #         for i in range(maxLength - len(resp_data["data"][item])):
    #             resp_data["data"][item]["NaC" + str(i)] = {"risk": 0,
    #                                                        "risk_high": 0,
    #                                                        "major_risk": 0,
    #                                                        "major_risk_high": 0}
    resp_data["size"] = maxLength
    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个项目中
        if item.project_code in contained_check_map.keys():
            # 通过contained_check_map用check_code取出对应的项目名称，更新相对应的隐患数量
            resp_data["data"][contained_check_map[item.project_code]][item.project_code]["risk"] += 1
            # 高风险隐患数量
            if item.risk_level == "3":
                resp_data["data"][contained_check_map[item.project_code]][item.project_code]["risk_high"] += 1
            # 专业隐患数量
            if item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][item.project_code]["major_risk"] += 1
            if major_name == '全部专业':
                resp_data["data"][contained_check_map[item.project_code]][item.project_code]["major_risk"] = \
                    resp_data["data"][contained_check_map[item.project_code]][item.project_code]["risk"]
            # 专业高风险隐患数量
            if item.risk_level == "3" and item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][item.project_code]["major_risk_high"] += 1
            if major_name == '全部专业':
                resp_data["data"][contained_check_map[item.project_code]][item.project_code]["major_risk_high"] = \
                    resp_data["data"][contained_check_map[item.project_code]][item.project_code]["risk_high"]
    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析A 趋势图
#
# FunctionName: analyze_tendency_profession
# Purpose: 可以选择纵坐标为隐患数量（隐患总数、高风险数量、专业隐患总数、专业高风险数量），横坐标为时间点，对比对象可选
# Parameter: json -> {"profession_name":{}, "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "data": {"profession_name_1": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            },
#                                                      "profession_name_2": {
#                                                                             "month_1": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0},
#                                                                             "month_2": {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
#                                                                            }
#                                                     }
#                             }
@insight_func_blueprint.route('/tendency_profession', methods=['POST', 'GET'])
def analyze_tendency_profession():
    print("In function analyze_tendency_profession")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    profession_name = request.values.get("profession_name").split("%")
    if profession_name is None:
        print("Missing profession parameter")
        return None
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "data": {}}
    year_end = end.year
    month_end = end.month
    print("Received time " + str(start) + " to " + str(end))
    print("Received profession_name " + str(profession_name))
    print("Received major_name " + str(major_name))
    # 对于每个行业，映射start到end的每一个月份，日期格式为字符串“%Y-%m”
    for item in profession_name:
        resp_data["data"][item] = {}
        year_start = start.year
        month_start = start.month
        while (year_start <= year_end and month_start <= month_end) or year_start < year_end:
            # 分别映射隐患、高风险隐患、专业区分的隐患、专业区分的高风险隐患的数量，并将四种需要统计的隐患数量均初始化为0
            resp_data["data"][item][str(year_start) + "-" + str(month_start)] \
                = {"risk": 0, "risk_high": 0, "major_risk": 0, "major_risk_high": 0}
            month_start += 1
            if month_start > 12:
                year_start += 1
                month_start = 1

    # 找到所有在该行业下的检查，并将check_code与行业名称做映射
    contained_check_map = {}
    for item in cache_final_tag:
        if item.profession_tag in profession_name:
            contained_check_map[item.code] = item.profession_tag

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个行业中，并且在时间范围内
        if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
            year = item.create_time.year
            month = item.create_time.month
            # 通过contained_check_map用check_code取出对应的总部名称，更新相对应的隐患数量
            resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)]["risk"] += 1
            # 高风险隐患数量
            if item.risk_level == "3":
                resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
                    "risk_high"] += 1
            # 专业隐患数量
            if item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
                    "major_risk"] += 1
            # 专业高风险隐患数量
            if item.risk_level == "3" and item.major_name == major_name:
                resp_data["data"][contained_check_map[item.project_code]][str(year) + "-" + str(month)][
                    "major_risk_high"] += 1
    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析B 占比分析图(饼图)
#
# FunctionName: analyze_ratio_headquarter
# Purpose: 隐患各风险等级占比，专业隐患各风险等级占比
# Parameter: json -> {"headquarter_name", "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "headquarter_name": str(headquarter_name), "major_name": str(major_name),
#                              "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0, "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
@insight_func_blueprint.route('/ratio_headquarter', methods=['POST', 'GET'])
def analyze_ratio_headquarter():
    print("In function analyze_ratio_headquarter")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:华润置地
    headquarter_name = request.values.get("headquarter_name")
    # Test: 消防专业
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "headquarter_name": str(headquarter_name), "major_name": str(major_name),
                 "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0,
                           "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name " + str(headquarter_name))
    print("Received major_name " + str(major_name))

    # 找到所有在该总部下的检查
    contained_check_map = {}
    for item in cache_final_tag:
        if item.headquarter_tag == headquarter_name:
            contained_check_map[item.code] = 0

    # 隐患计数
    total_risk = 0.0
    total_major_risk = 0.0

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个总部中，并且在时间范围内
        if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
            # 隐患总数自增
            total_risk += 1.0
            # 先判断risk_level，再判断major_name
            if item.risk_level == "1":
                resp_data["ratio"]["level_1"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_1"] += 1.0
            elif item.risk_level == "2":
                resp_data["ratio"]["level_2"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_2"] += 1.0
            elif item.risk_level == "3":
                resp_data["ratio"]["level_3"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_3"] += 1.0

    # 除以总数求比例，并保留三位小数，若不存在，则全部返回-1
    if total_risk != 0:
        resp_data["ratio"]["level_1"] /= total_risk
        resp_data["ratio"]["level_2"] /= total_risk
        resp_data["ratio"]["level_3"] /= total_risk
        resp_data["ratio"]["level_1"] = round(resp_data["ratio"]["level_1"], 3)
        resp_data["ratio"]["level_2"] = round(resp_data["ratio"]["level_2"], 3)
        resp_data["ratio"]["level_3"] = round(resp_data["ratio"]["level_3"], 3)
    else:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0

    if total_major_risk != 0:
        resp_data["ratio"]["major_level_1"] /= total_major_risk
        resp_data["ratio"]["major_level_2"] /= total_major_risk
        resp_data["ratio"]["major_level_3"] /= total_major_risk
        resp_data["ratio"]["major_level_1"] = round(resp_data["ratio"]["major_level_1"], 3)
        resp_data["ratio"]["major_level_2"] = round(resp_data["ratio"]["major_level_2"], 3)
        resp_data["ratio"]["major_level_3"] = round(resp_data["ratio"]["major_level_3"], 3)
    else:
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    if headquarter_name is None:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析B 占比分析图(饼图)
#
# FunctionName: analyze_ratio_region
# Purpose: 隐患各风险等级占比，专业隐患各风险等级占比
# Parameter: json -> {"headquarter_name/region_name", "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "region_name": str(headquarter_name/region_name), "major_name": str(major_name),
#                              "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0, "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
@insight_func_blueprint.route('/ratio_region', methods=['POST', 'GET'])
def analyze_ratio_region():
    print("In function analyze_ratio_region")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:"华润置地/华东大区"
    region_name = request.values.get("region_name")
    # Test:消防专业
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "region_name": str(region_name), "major_name": str(major_name),
                 "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0,
                           "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name/region_name " + str(region_name))
    print("Received major_name " + str(major_name))

    # 找到所有在该区域下的检查
    contained_check_map = {}
    for item in cache_final_tag:
        if str(item.headquarter_tag) + "/" + str(item.region_tag) == str(region_name):
            contained_check_map[item.code] = 0

    # 隐患计数
    total_risk = 0.0
    total_major_risk = 0.0

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个区域中，并且在时间范围内
        if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
            # 隐患总数自增
            total_risk += 1.0
            # 先判断risk_level，再判断major_name
            if item.risk_level == "1":
                resp_data["ratio"]["level_1"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_1"] += 1.0
            elif item.risk_level == "2":
                resp_data["ratio"]["level_2"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_2"] += 1.0
            elif item.risk_level == "3":
                resp_data["ratio"]["level_3"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_3"] += 1.0

    # 除以总数求比例，并保留三位小数，若不存在，则全部返回-1
    if total_risk != 0:
        resp_data["ratio"]["level_1"] /= total_risk
        resp_data["ratio"]["level_2"] /= total_risk
        resp_data["ratio"]["level_3"] /= total_risk
        resp_data["ratio"]["level_1"] = round(resp_data["ratio"]["level_1"], 3)
        resp_data["ratio"]["level_2"] = round(resp_data["ratio"]["level_2"], 3)
        resp_data["ratio"]["level_3"] = round(resp_data["ratio"]["level_3"], 3)
    else:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0

    if total_major_risk != 0:
        resp_data["ratio"]["major_level_1"] /= total_major_risk
        resp_data["ratio"]["major_level_2"] /= total_major_risk
        resp_data["ratio"]["major_level_3"] /= total_major_risk
        resp_data["ratio"]["major_level_1"] = round(resp_data["ratio"]["major_level_1"], 3)
        resp_data["ratio"]["major_level_2"] = round(resp_data["ratio"]["major_level_2"], 3)
        resp_data["ratio"]["major_level_3"] = round(resp_data["ratio"]["major_level_3"], 3)
    else:
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析B 占比分析图(饼图)
#
# FunctionName: analyze_ratio_project
# Purpose: 隐患各风险等级占比，专业隐患各风险等级占比
# Parameter: json -> {"headquarter_name/region_name/project_name", "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "project_name": str(headquarter_name/region_name/project_name), "major_name": str(major_name),
#                              "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0, "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
@insight_func_blueprint.route('/ratio_project', methods=['POST', 'GET'])
def analyze_ratio_project():
    print("In function analyze_ratio_project")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:"华润置地/华东大区/上海万象城"
    project_name = request.values.get("project_name")
    # Test:"消防专业"
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "project_name": str(project_name), "major_name": str(major_name),
                 "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0,
                           "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received headquarter_name/region_name/project_name " + str(project_name))
    print("Received major_name " + str(major_name))

    # 找到所有在该区域下的检查
    contained_check_map = {}
    for item in cache_final_tag:
        if str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag) == str(project_name):
            contained_check_map[item.code] = 0

    # 隐患计数
    total_risk = 0.0
    total_major_risk = 0.0

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个项目中，并且在时间范围内
        if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
            # 隐患总数自增
            total_risk += 1.0
            # 先判断risk_level，再判断major_name
            if item.risk_level == "1":
                resp_data["ratio"]["level_1"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_1"] += 1.0
            elif item.risk_level == "2":
                resp_data["ratio"]["level_2"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_2"] += 1.0
            elif item.risk_level == "3":
                resp_data["ratio"]["level_3"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_3"] += 1.0

    # 除以总数求比例，并保留三位小数，若不存在，则全部返回-1
    if total_risk != 0:
        resp_data["ratio"]["level_1"] /= total_risk
        resp_data["ratio"]["level_2"] /= total_risk
        resp_data["ratio"]["level_3"] /= total_risk
        resp_data["ratio"]["level_1"] = round(resp_data["ratio"]["level_1"], 3)
        resp_data["ratio"]["level_2"] = round(resp_data["ratio"]["level_2"], 3)
        resp_data["ratio"]["level_3"] = round(resp_data["ratio"]["level_3"], 3)
    else:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0

    if total_major_risk != 0:
        resp_data["ratio"]["major_level_1"] /= total_major_risk
        resp_data["ratio"]["major_level_2"] /= total_major_risk
        resp_data["ratio"]["major_level_3"] /= total_major_risk
        resp_data["ratio"]["major_level_1"] = round(resp_data["ratio"]["major_level_1"], 3)
        resp_data["ratio"]["major_level_2"] = round(resp_data["ratio"]["major_level_2"], 3)
        resp_data["ratio"]["major_level_3"] = round(resp_data["ratio"]["major_level_3"], 3)
    else:
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 灵活查询统计分析B 占比分析图(饼图)
#
# FunctionName: analyze_ratio_profession
# Purpose: 隐患各风险等级占比，专业隐患各风险等级占比
# Parameter: json -> {"headquarter_name", "major_name", "start", "end"}
# Return: json -> resp_data = {"code": 10000, "profession_name": str(profession_name), "major_name": str(major_name),
#                              "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0, "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
@insight_func_blueprint.route('/ratio_profession', methods=['POST', 'GET'])
def analyze_ratio_profession():
    print("In function analyze_ratio_profession")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:"仓储物流"
    profession_name = request.values.get("profession_name")
    # Test:"消防专业"
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "profession_name": str(profession_name), "major_name": str(major_name),
                 "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0,
                           "major_level_1": 0.0, "major_level_2": 0.0, "major_level_3": 0.0}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received profession_name " + str(profession_name))
    print("Received major_name " + str(major_name))

    # 找到所有在该行业下的检查
    contained_check_map = {}
    for item in cache_final_tag:
        if item.profession_tag == profession_name:
            contained_check_map[item.code] = 0

    # 隐患计数
    total_risk = 0.0
    total_major_risk = 0.0

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个行业中，并且在时间范围内
        if item.project_code in contained_check_map.keys() and end >= item.create_time >= start:
            # 隐患总数自增
            total_risk += 1.0
            # 先判断risk_level，再判断major_name
            if item.risk_level == "1":
                resp_data["ratio"]["level_1"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_1"] += 1.0
            elif item.risk_level == "2":
                resp_data["ratio"]["level_2"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_2"] += 1.0
            elif item.risk_level == "3":
                resp_data["ratio"]["level_3"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_3"] += 1.0

    # 除以总数求比例，并保留三位小数，若不存在，则全部返回-1
    if total_risk != 0:
        resp_data["ratio"]["level_1"] /= total_risk
        resp_data["ratio"]["level_2"] /= total_risk
        resp_data["ratio"]["level_3"] /= total_risk
        resp_data["ratio"]["level_1"] = round(resp_data["ratio"]["level_1"], 3)
        resp_data["ratio"]["level_2"] = round(resp_data["ratio"]["level_2"], 3)
        resp_data["ratio"]["level_3"] = round(resp_data["ratio"]["level_3"], 3)
    else:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0

    if total_major_risk != 0:
        resp_data["ratio"]["major_level_1"] /= total_major_risk
        resp_data["ratio"]["major_level_2"] /= total_major_risk
        resp_data["ratio"]["major_level_3"] /= total_major_risk
        resp_data["ratio"]["major_level_1"] = round(resp_data["ratio"]["major_level_1"], 3)
        resp_data["ratio"]["major_level_2"] = round(resp_data["ratio"]["major_level_2"], 3)
        resp_data["ratio"]["major_level_3"] = round(resp_data["ratio"]["major_level_3"], 3)
    else:
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    if profession_name is None:
        resp_data["ratio"]["level_1"] = -1.0
        resp_data["ratio"]["level_2"] = -1.0
        resp_data["ratio"]["level_3"] = -1.0
        resp_data["ratio"]["major_level_1"] = -1.0
        resp_data["ratio"]["major_level_2"] = -1.0
        resp_data["ratio"]["major_level_3"] = -1.0

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 7.22修改版本 入参为多个检查拼接成的字符串 每个检查以"%"隔开
@insight_func_blueprint.route('/ratio', methods=['POST', 'GET'])
def analyze_ratio():
    print("In function analyze_ratio")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    # Test:检查1%检查2 ——> ["检查1"，"检查2"] 选择多个对象，以"%"隔开
    check_code_list = request.values.get("check_key").split("%")
    # Test: 消防专业
    major_name = request.values.get("major_name")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    resp_data = {"code": 10000, "major_name": str(major_name), "total_risk": 0, "total_major_risk": 0,
                 "ratio": {"level_1": 0.0, "level_2": 0.0, "level_3": 0.0,
                           "major_level_1": 0.0, "major_level_2": 0.0,
                           "major_level_3": 0.0}}
    print("Received time " + str(start) + " to " + str(end))
    print("Received check_key " + str(check_code_list))
    print("Received major_name " + str(major_name))

    # 从这些检查中筛选出符合时间段的检查
    contained_check_map = {}
    for item in cache_final_tag:
        if item.code in check_code_list:
            if item.plan_start_time <= end and item.plan_end_time >= start:
                contained_check_map[item.code] = 0

    # 隐患计数
    total_risk = 0.0
    total_major_risk = 0.0

    # 遍历record表
    for item in cache_final_record:
        # 如果当前记录所属的检查在这个总部中，并且在时间范围内
        if item.project_code in contained_check_map.keys():
            # 隐患总数自增
            total_risk += 1.0
            # 先判断risk_level，再判断major_name
            if item.risk_level == "1":
                resp_data["ratio"]["level_1"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_1"] += 1.0
            elif item.risk_level == "2":
                resp_data["ratio"]["level_2"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_2"] += 1.0
            elif item.risk_level == "3":
                resp_data["ratio"]["level_3"] += 1.0
                if item.major_name == major_name:
                    total_major_risk += 1.0
                    resp_data["ratio"]["major_level_3"] += 1.0

    # 除以总数求比例，并保留三位小数，若不存在，则全部返回-1
    if total_risk != 0:
        resp_data["ratio"]["level_1"] /= total_risk
        resp_data["ratio"]["level_2"] /= total_risk
        resp_data["ratio"]["level_3"] /= total_risk
        resp_data["ratio"]["level_1"] = round(resp_data["ratio"]["level_1"], 3)
        resp_data["ratio"]["level_2"] = round(resp_data["ratio"]["level_2"], 3)
        resp_data["ratio"]["level_3"] = round(resp_data["ratio"]["level_3"], 3)

    if total_major_risk != 0:
        resp_data["ratio"]["major_level_1"] /= total_major_risk
        resp_data["ratio"]["major_level_2"] /= total_major_risk
        resp_data["ratio"]["major_level_3"] /= total_major_risk
        resp_data["ratio"]["major_level_1"] = round(resp_data["ratio"]["major_level_1"], 3)
        resp_data["ratio"]["major_level_2"] = round(resp_data["ratio"]["major_level_2"], 3)
        resp_data["ratio"]["major_level_3"] = round(resp_data["ratio"]["major_level_3"], 3)

    if major_name == '全部专业':
        resp_data["ratio"]["major_level_1"] = resp_data["ratio"]["level_1"]
        resp_data["ratio"]["major_level_2"] = resp_data["ratio"]["level_2"]
        resp_data["ratio"]["major_level_3"] = resp_data["ratio"]["level_3"]
        total_major_risk = total_risk
    resp_data['total_risk'] = total_risk
    resp_data['total_major_risk'] = total_major_risk
    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


# 7.29
@insight_func_blueprint.route('/get_headquarter_tag', methods=['POST', 'GET'])
def get_headquarter_tag():
    print("In function get_headquarter_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if item.headquarter_tag not in contain_map and item.headquarter_tag is not None:
            resp_data.append({"value": item.headquarter_tag, "label": item.headquarter_tag})
            contain_map.append(item.headquarter_tag)
    print(resp_data)
    return jsonify(resp_data)


@insight_func_blueprint.route('/get_region_tag', methods=['POST', 'GET'])
def get_region_tag():
    print("In function get_region_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        if str(item.headquarter_tag) + "/" + str(item.region_tag) not in contain_map and item.region_tag is not None:
            resp_data.append({"value": str(item.headquarter_tag) + "/" + str(item.region_tag),
                              "label": str(item.headquarter_tag) + "/" + str(item.region_tag)})
            contain_map.append(str(item.headquarter_tag) + "/" + str(item.region_tag))
    print(resp_data)
    return jsonify(resp_data)


@insight_func_blueprint.route('/get_project_tag', methods=['POST', 'GET'])
def get_project_tag():
    print("In function get_project_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_map = []
    resp_data = []
    for item in cache_final_tag:
        temp = str(item.headquarter_tag) + "/" + str(item.region_tag) + "/" + str(item.project_tag)
        if temp not in contain_map and item.project_tag is not None:
            resp_data.append({"value": temp, "label": str(item.headquarter_tag) + "/" + str(item.project_tag)})
            contain_map.append(temp)
    print(resp_data)
    return jsonify(resp_data)


@insight_func_blueprint.route('/get_level_query', methods=['POST', 'GET'])
def get_level_query():
    print("In function get_level_query")
    cache_final_tag = gl.get_value("final_tag")
    contain_head_map = {}
    resp_data = []
    # 首先筛选所有总部
    for item in cache_final_tag:
        if item.headquarter_tag not in contain_head_map.keys():
            contain_head_map[str(item.headquarter_tag)] = {}
    # 再筛选所有区域
    for item in cache_final_tag:
        if item.region_tag not in contain_head_map[str(item.headquarter_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
    # 再筛选所有项目
    for item in cache_final_tag:
        if item.project_tag not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
    for item in cache_final_tag:
        contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)
    # 将返回数据格式化
    for head in contain_head_map:
        if head != "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": head, "value": head, "children": region_list})
    for head in contain_head_map:
        if head == "None":
            region_list = []
            for region in contain_head_map[head]:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"label": check_code, "value": check_code})
                    project_list.append({"label": project if project != "None" else "其他", "value": project,
                                         "children": check_code_list})
                region_list.append(
                    {"label": region if region != "None" else "其他", "value": region, "children": project_list})
            resp_data.append({"label": "其他", "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)


@insight_func_blueprint.route('/get_kpi', methods=['POST', 'GET'])
def get_kpi():
    print("In function get_kpi")
    start_t = datetime.now()
    cache_final_record = gl.get_value("final_record")
    cache_final_tag = gl.get_value("final_tag")
    cache_risk_project_module = gl.get_value("risk_project_module")
    resp_data = []
    # Test:检查1%检查2 ——> ["检查1"，"检查2"] 选择多个对象，以"%"隔开
    check_code_list = request.values.get("check_key").split("%")
    # 若没有传入时间参数，则start为表中的最早时间，end为当前时间
    start = datetime.strptime("2020-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    if request.values.get("start") is not None:
        start = datetime.strptime(request.values.get("start"), "%Y-%m-%d %H:%M:%S")
    if request.values.get("end") is not None:
        end = datetime.strptime(request.values.get("end"), "%Y-%m-%d %H:%M:%S")
    print("Received time " + str(start) + " to " + str(end))
    print("Received check_key " + str(check_code_list))
    contained_check_map = []
    for item in cache_final_record:
        if item.project_code in check_code_list:
            if item.system_name == '消火栓系统' and item.equipment_name == '室内消火栓' and item.module_name == '消火栓静压':
                if item.note == '室内消火栓静压小于0.07Mpa' or item.note == '室内消火栓静压小于0.07Mpa' or item.note == '室内消火栓静压小于0.07Mpa':
                    contained_check_map.append(item.code)

    end_t = datetime.now()
    print(resp_data)
    print("Query total time is: " + str((end_t - start_t).seconds) + "s")
    return jsonify(resp_data)


@insight_func_blueprint.route('/get_hide_tag', methods=['POST', 'GET'])
def get_hide_tag():
    print("In function get_hide_tag")
    cache_final_tag = gl.get_value("final_tag")
    contain_head_map = {}
    head_hide_tag_map = {}
    region_hide_tag_map = {}
    project_hide_tag_map = {}
    resp_data = []
    # 首先筛选所有总部
    for item in cache_final_tag:
        if item.headquarter_tag is not None and str(item.headquarter_tag) not in contain_head_map.keys():
            contain_head_map[str(item.headquarter_tag)] = {}
            if item.headquarter_tag not in head_hide_tag_map.keys():
                if item.headquarter_hide_tag is not None:
                    head_hide_tag_map[str(item.headquarter_tag)] = str(item.headquarter_hide_tag)
                else:
                    if len(str(item.headquarter_tag)) <= 3:
                        head_hide_tag_map[str(item.headquarter_tag)] = str(item.headquarter_tag)[0] + '***'
                    else:
                        head_hide_tag_map[str(item.headquarter_tag)] = str(item.headquarter_tag)[0] + '***' + \
                                                                       str(item.headquarter_tag)[-1]
    # 再筛选所有区域
    for item in cache_final_tag:
        if item.headquarter_tag is not None and str(item.region_tag) not in contain_head_map[str(item.headquarter_tag)].keys():
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)] = {}
            if str(item.headquarter_tag) + '/' + str(item.region_tag) not in region_hide_tag_map.keys():
                if item.region_hide_tag is not None:
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = str(
                        item.region_hide_tag)
                else:
                    region_hide_tag_map[str(item.headquarter_tag) + '/' + str(item.region_tag)] = str(item.region_tag)[
                                                                                                      0] + '***' + \
                                                                                                  str(item.region_tag)[
                                                                                                      -1]
    # 再筛选所有项目
    for item in cache_final_tag:
        if item.project_tag is not None and item.headquarter_tag is not None:
            if str(item.project_tag) not in contain_head_map[str(item.headquarter_tag)][str(item.region_tag)].keys():
                contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)] = []
                if str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(
                        item.project_tag) not in project_hide_tag_map.keys():
                    if item.project_hide_tag is not None:
                        project_hide_tag_map[
                            str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                            str(item.project_hide_tag)
                    else:
                        project_hide_tag_map[
                            str(item.headquarter_tag) + '/' + str(item.region_tag) + '/' + str(item.project_tag)] = \
                            str(item.project_tag)[0] + '***' + str(item.project_tag)[-1]
    # 筛选所有检查
    for item in cache_final_tag:
        if item.headquarter_tag is not None and item.project_tag is not None:
            contain_head_map[str(item.headquarter_tag)][str(item.region_tag)][str(item.project_tag)].append(item.code)

    # 将返回数据格式化
    for head in contain_head_map:
        region_list = []
        for region in contain_head_map[head]:
            if region != 'None':
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"level": 4, "label": check_code, "value": check_code})
                    project_list.append(
                        {"level": 3, "label": project_hide_tag_map[head + '/' + region + '/' + project],
                         "value": project, "children": check_code_list})
                region_list.append(
                    {"level": 2, "label": region_hide_tag_map[head + '/' + region], "value": region,
                     "children": project_list})
            else:
                project_list = []
                for project in contain_head_map[head][region]:
                    check_code_list = []
                    for check_code in contain_head_map[head][region][project]:
                        check_code_list.append({"level": 4, "label": check_code, "value": check_code})
                    project_list.append(
                        {"level": 3, "label": project_hide_tag_map[head + '/' + region + '/' + project],
                         "value": project, "children": check_code_list})
                region_list = project_list
        resp_data.append({"level": 1, "label": head_hide_tag_map[head], "value": head, "children": region_list})
    print(resp_data)
    return jsonify(resp_data)
