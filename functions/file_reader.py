import datetime
import random
import time

import pandas as pd
import os


# 用于insight point
FILE_ABS_PATH = os.path.dirname(__file__)
SERVER_PATH = os.path.join(FILE_ABS_PATH, os.path.pardir)

INSIGHT_FILE_PATH = os.path.join(SERVER_PATH, 'data/insight.csv')
AGGREGATE_FILE_PATH = os.path.join(SERVER_PATH, 'data/aggregation.csv')

subspace_col_name = ['project_code', 'major_name', 'plan_end_time', 'project_tag', 'profession_tag']


def filter_subspace(row):
    df = pd.read_csv(AGGREGATE_FILE_PATH)
    subspace = row.subspace.split(';')
    for i in range(len(subspace)):
        if subspace[i] != '*':
            df = df.loc[df[subspace_col_name[i]] == subspace[i]]
    return df


# def get_scatter():
#     df_insight = pd.read_csv(INSIGHT_FILE_PATH, header=0, encoding="gb2312")
#
#     res = []
#     random.seed(3)
#     for index, row in df_insight.iterrows():
#         '''(id, x, y, type)'''
#         res.append((index, row[1], random.random(), row[3]))
#     return res
def get_scatter():
    df_insight = pd.read_csv(INSIGHT_FILE_PATH, header=0, encoding="gb2312")

    res = []
    random.seed(3)
    for index, row in df_insight.iterrows():
        '''(id, x, y, type)'''
        res.append((index, row[1], row[-1], row[3]))
    return res


def get_top_k(id, k):
    df_insight = pd.read_csv(INSIGHT_FILE_PATH, header=0, encoding="gb2312")
    insight_row = df_insight.iloc[id]

    df = filter_subspace(insight_row)
    df = df.groupby(insight_row.breakdown).agg({insight_row.measure: 'sum'})
    df = df.sort_values(by=insight_row.measure, ascending=False).iloc[:k]

    res = []
    for index, df_row in df.iterrows():
        # todo: 缺失breakdown与breakdown value
        res.append(df_row[0])

    '''y-cord str, int list'''
    return insight_row.measure, res


def get_trend(id):
    df_insight = pd.read_csv(INSIGHT_FILE_PATH, header=0, encoding="gb2312")
    insight_row = df_insight.iloc[id]

    df = filter_subspace(insight_row)
    df[insight_row.breakdown] = df[insight_row.breakdown].apply(
        lambda x: str(time.strptime(x, '%Y/%m/%d %H:%M').tm_year) + '年'
                  + str(time.strptime(x, '%Y/%m/%d %H:%M').tm_mon) + '月'
    )
    df = df.groupby(insight_row.breakdown, as_index=False).agg(
        {insight_row.breakdown: 'first', insight_row.measure: 'sum'})

    breakdown_value = []
    measure_value = []
    for index, df_row in df.iterrows():
        breakdown_value.append(df_row[0])
        measure_value.append(df_row[1])

    '''x-cord str, y-cord str, x-label list, num list'''
    # todo: 缺失拟合后的直线信息（如斜率）
    return insight_row.breakdown, insight_row.measure, breakdown_value, measure_value


def get_correlation(id):
    df_insight = pd.read_csv(INSIGHT_FILE_PATH, header=0, encoding="gb2312")
    insight_row = df_insight.iloc[id]
    measure = insight_row.measure.split(';')

    df = filter_subspace(insight_row)
    df = df.groupby(insight_row.breakdown, as_index=False).agg(
        {insight_row.breakdown: 'first', measure[0]: 'sum', measure[1]: 'sum'})

    x_label_list = []
    res = [{'col': measure[0], 'list': []},
           {'col': measure[1], 'list': []}]
    for index, df_row in df.iterrows():
        x_label_list.append(df_row[insight_row.breakdown])
        res[0]['list'].append(df_row[measure[0]])
        res[1]['list'].append(df_row[measure[1]])

    '''x-cord str, dict with type and (x,y)'''
    return insight_row.breakdown, x_label_list, res


if __name__ == '__main__':
    # todo:缺失subspace信息
    # print(get_scatter())
    # print(get_top_k(30, 10))
    print(get_trend(1))
    print(get_correlation(77))
