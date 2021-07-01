class APSchedulerJobConfig(object):
    JOBS = [
        {
            'id': 'auto_update',
            'func': 'task:auto_update',  # 路径：job函数名
            'args': '',
            'trigger': {
                'type': 'cron',  # 类型
                'day_of_week': "0-6",  # 可定义具体哪几天要执行
                'hour': '23',  # 小时数
                'minute': '55'
            }
            # 'trigger': 'interval',
            # 'seconds': 180  # 每隔3分钟执行一次
        }
    ]
    # SCHEDULER_API_ENABLED = True
    # SQLALCHEMY_ECHO = True
