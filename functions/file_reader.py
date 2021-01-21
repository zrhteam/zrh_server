import datetime
import random
import time

import pandas as pd
import os

subspace_col_name = ['project_code', 'major_name', 'plan_end_time', 'area',
                     'project_tag', 'region_tag', 'headquarter_tag', 'profession_tag']
measure_list = ['sum of danger_number', 'count of risk_level=3']
time_col = 'plan_end_time'

FILE_ABS_PATH = os.path.dirname(__file__)
SERVER_PATH = os.path.join(FILE_ABS_PATH, os.path.pardir)
insight = os.path.join(SERVER_PATH, 'data/insight_top50.csv')
aggregate = os.path.join(SERVER_PATH, 'data/aggregation_new.csv')

def get_subspace(row):
    df = pd.read_csv(aggregate)

    for index, value in row.iteritems():
        if index in subspace_col_name and value != '*':
            df = df.loc[df[index] == value]
    return df


def get_scatter():
    df_insight = pd.read_csv(insight, header=0, encoding="utf-8")

    res = []
    random.seed(3)
    for index, row in df_insight.iterrows():
        '''(id, x, y, type)'''
        res.append((index, row.impact, row.sig, row.insight))
    return res


def get_top10(id):
    df_insight = pd.read_csv(insight, header=0)
    insight_row = df_insight.iloc[id]

    if insight_row.insight != 'top1':
        return

    df = get_subspace(insight_row)
    df = df.groupby(insight_row.breakdown).agg({insight_row.measure: 'sum'})
    df = df.sort_values(by=insight_row.measure, ascending=False).iloc[0:10]

    res = []
    for index, df_row in df.iterrows():
        res.append(df_row[0])

    '''y-cord str, int list'''
    return insight_row.measure, res


def get_trend(id):
    df_insight = pd.read_csv(insight, header=0)
    insight_row = df_insight.iloc[id]

    if insight_row.insight != 'trend':
        return

    df = get_subspace(insight_row)
    df = df.groupby(insight_row.breakdown, as_index=False).agg(
        {insight_row.breakdown: 'first', insight_row.measure: 'sum'})
    df = df.sort_values(by=insight_row.breakdown)

    df[insight_row.breakdown] = df[insight_row.breakdown].apply(
        lambda x: str(time.strptime(x, '%Y/%m/%d %H:%M').tm_year) + '年'
                  + str(time.strptime(x, '%Y/%m/%d %H:%M').tm_mon) + '月'
    )
    breakdown_value = []
    measure_value = []
    for index, df_row in df.iterrows():
        breakdown_value.append(df_row[0])
        measure_value.append(df_row[1])

    '''x-cord str, y-cord str, x-label list, num list'''
    return insight_row.breakdown, insight_row.measure, breakdown_value, measure_value


def get_correlation(id):
    df_insight = pd.read_csv(insight, header=0, encoding="gb2312")
    insight_row = df_insight.iloc[id]

    if insight_row.insight != 'correlation':
        return

    measure = insight_row.measure.split(';')

    df = get_subspace(insight_row)
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


def get_change_point_and_outlier(id):
    df_insight = pd.read_csv(insight, header=0)
    insight_row = df_insight.iloc[id]

    if insight_row.insight != 'change point' \
            and insight_row.insight != 'outlier':
        return

    df = get_subspace(insight_row)
    df = df.groupby(insight_row.breakdown, as_index=False).agg(
        {insight_row.breakdown: 'first', insight_row.measure: 'sum'})
    df = df.sort_values(by=time_col)

    y_val = df.loc[df[insight_row.breakdown]
                   == insight_row['breakdown_value']][insight_row.measure]

    df[insight_row.breakdown] = df[insight_row.breakdown].apply(
        lambda x: str(time.strptime(x, '%Y/%m/%d %H:%M').tm_year) + '年'
                  + str(time.strptime(x, '%Y/%m/%d %H:%M').tm_mon) + '月'
    )

    breakdown_value = []
    measure_value = []
    idx = 0
    for index, df_row in df.iterrows():
        if df_row[1] == y_val.values[0]:
            idx = len(breakdown_value)
        breakdown_value.append(df_row[0])
        measure_value.append(df_row[1])

    '''x-cord str, y-cord str, x-label list, num list, idx'''
    return insight_row.breakdown, insight_row.measure, breakdown_value, measure_value, idx


def get_attribution(id):
    df_insight = pd.read_csv(insight, header=0)
    insight_row = df_insight.iloc[id]

    if insight_row.insight != 'attribution':
        return

    df = get_subspace(insight_row)
    df = df.groupby(insight_row.breakdown, as_index=False).agg(
        {insight_row.breakdown: 'first', insight_row.measure: 'sum'})
    df = df.sort_values(by=insight_row.measure)

    breakdown_value = []
    measure_value = []
    for index, df_row in df.iterrows():
        breakdown_value.append(df_row[0])
        measure_value.append(df_row[1])

    '''name list, value list'''
    return breakdown_value, measure_value


if __name__ == '__main__':
    # print(get_scatter())
    # print(get_top10(79))
    print(get_trend(297))
    # print(get_correlation(77))
    # print(get_change_point_and_outlier(100))
    # print(get_attribution(203))
