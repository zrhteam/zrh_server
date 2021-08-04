import time
from datetime import datetime
from models.final_record import FinalRecord
from models.final_tag import FinalTag
from models.risk_project import RiskProject
from models.risk_project_module import RiskProjectModule
from models.risk_user import RiskUser
from models.sys_file import SysFile
from ops import scheduler  # 很关键的一步，导入初始化过的scheduler对象
import functions.cache_data as gl


def auto_update():
    with scheduler.app.app_context():
        print("数据更新中...请稍候")
        start_t = datetime.now()
        # gl._init() 不需要重新声明字典了，直接在原来的基础上更新即可

        # 缓存表 risk_user
        begin_t = datetime.now()
        cache_risk_user = RiskUser.query.all()
        gl.set_value("risk_user", cache_risk_user)
        print("Time to query table [1]risk_user is " + str((datetime.now() - begin_t).seconds) + "s")
        # print("risk_user 更新完成")

        # 缓存表 prj_with_tag
        # cache_prj_with_tag = PrjWithTag.query.all()
        # end_t2 = datetime.now()
        # gl.set_value("cache_prj_with_tag", cache_prj_with_tag)
        # print("Time to query table 2 is " + str((end_t2 - end_t1).seconds) + "s")
        # print(cache_prj_with_tag[0])

        # 缓存表 new_cascade_risk_prj_danger_record
        # cache_cascade_record = NewCascadeRiskPrjDangerRecord.query.all()
        # cache_cascade_record = FinalAllRecord.query.all()
        # end_t3 = datetime.now()
        # gl.set_value("cache_cascade_record", cache_cascade_record)
        # print("Time to query table 3 is " + str((end_t3 - end_t2).seconds) + "s")

        # 缓存表 sys_file
        begin_t = datetime.now()
        cache_sys_file = SysFile.query.all()
        gl.set_value("sys_file", cache_sys_file)
        print("Time to query [2]sys_file is " + str((datetime.now() - begin_t).seconds) + "s")
        # print("sys_file 更新完成")
        # cache_check_location_map = {}
        # for item in cache_cascade_record:
        #     if item.project_code not in cache_check_location_map.keys():
        #         cache_check_location_map[item.project_code] = {"lat": item.lat, "lng": item.lng, "index": round(random.uniform(1.0, 99.99), 2)}
        # gl.set_value("cache_check_location_map", cache_check_location_map)

        # modified
        begin_t = datetime.now()
        cache_final_record = FinalRecord.query.all()
        gl.set_value("final_record", cache_final_record)
        print("Time to query [3]final_record is " + str((datetime.now() - begin_t).seconds) + "s")
        # print("final_record 更新完成")

        begin_t = datetime.now()
        cache_final_tag = FinalTag.query.all()
        gl.set_value("final_tag", cache_final_tag)
        print("Time to query [4]final_tag is " + str((datetime.now() - begin_t).seconds) + "s")
        # print("final_tag 更新完成")

        begin_t = datetime.now()
        cache_risk_project = RiskProject.query.all()
        gl.set_value("risk_project", cache_risk_project)
        print("Time to query [5]risk_project is " + str((datetime.now() - begin_t).seconds) + "s")

        begin_t = datetime.now()
        cache_risk_project_module = RiskProjectModule.query.all()
        gl.set_value("risk_project_module", cache_risk_project_module)
        print("Time to query [6]risk_project_module is " + str((datetime.now() - begin_t).seconds) + "s")
        # print("risk_project 更新完成")
        end_t = datetime.now()
        print("Time to query all is " + str((end_t - start_t).seconds) + "s")
        print("更新完成！！！\n更新日期:")
        print(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
