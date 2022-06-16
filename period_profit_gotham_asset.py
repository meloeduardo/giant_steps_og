#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd

pd.set_option("display.precision", 8)
pd.set_option('expand_frame_repr', False)


def get_json(dataInicial='dd/mm/yy', dataFinal='dd/mm/yy'):
    payload = {'formato': 'json',
               'dataInicial': dataInicial,
               'dataFinal': dataFinal}
    api_url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados'
    response = requests.get(api_url, params=payload)
    return response.json()


def hist_data(start_date, end_date, capital, frequency):
    assert capital > 0, "Capital arg must be greater than 0"
    assert frequency in ['day', 'month',
                         'year'], "frequency arg must be day, month or year."
    assert pd.to_datetime(start_date) > pd.to_datetime(
        '1995-01-01'), "start_date must be greater than 1995-01-01"
    assert (pd.to_datetime(start_date) > pd.to_datetime(end_date)
            ) is False, "start_date arg must be greater than end_date arg"
    df = pd.DataFrame(get_json())
    df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
    df['valor'] = pd.to_numeric(df['valor'])
    df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]
    df.reset_index(drop=True, inplace=True)
    df.loc[0, 'capital'] = capital
    for i in range(len(df)):
        df.loc[i, 'Amount earned'] = df.loc[i,
                                            'capital'] - df.loc[0, 'capital']
        df.loc[i+1, 'capital'] = df.loc[i, 'capital'] + \
            (df.loc[i, 'valor'] * df.loc[i, 'capital']/100)
    df.dropna(inplace=True)
    if(frequency == 'day'):
        pass
    if(frequency == 'month'):
        df = df.loc[df.groupby(pd.Grouper(
            key='data', freq='1M')).data.idxmax()]
    if(frequency == 'year'):
        df = df.loc[df.groupby(pd.Grouper(
            key='data', freq='1Y')).data.idxmax()]
    df.rename(columns={'data': 'Date', 'capital': 'Capital'}, inplace=True)
    df = df.drop(columns=['valor'])
    return df


def most_profitable_period(start_date, end_date):
    """use example: most_profitable_period('01-01-2000', '31-03-2022')."""
    df = hist_data(start_date, end_date, 100, 'day')
    df.set_index('Date', inplace=True)
    df.index.names = ['end_date']
    df['%.increase'] = df['Capital'].pct_change(periods=500, freq='D')
    df.sort_values(by='%.increase', ascending=False, inplace=True)
    df['start'] = df.index - pd.to_timedelta(500, unit='d')
    df.drop(columns=['Amount earned', 'Capital'], inplace=True)
    df.dropna(inplace=True)
    return df


print(most_profitable_period('2000-01-01', '2022-03-31'))
