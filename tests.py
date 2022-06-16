#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from period_profit_gotham_asset import hist_data, most_profitable_period


def test_basic():
    test1 = hist_data('2010-01-01', '2021-03-01', 657.43, 'day')
    test1.set_index('Date', inplace=True)
    test1_actual = pd.read_csv('csv_tests/hist_data_test_day.csv')
    test1_actual['Date'] = pd.to_datetime(test1_actual['Date'])
    test1_actual.set_index('Date', inplace=True)
    pd.testing.assert_frame_equal(test1, test1_actual)
    print('test 1 - OK')

    test2 = hist_data('2010-01-01', '2021-03-01', 657.43, 'month')
    test2.set_index('Date', inplace=True)
    test2_actual = pd.read_csv('csv_tests/hist_data_test_month.csv')
    test2_actual['Date'] = pd.to_datetime(test2_actual['Date'])
    test2_actual.set_index('Date', inplace=True)
    pd.testing.assert_frame_equal(test2, test2_actual)
    print('test 2 - OK')

    test3 = hist_data('2010-01-01', '2021-03-01', 657.43, 'year')
    test3.set_index('Date', inplace=True)
    test3_actual = pd.read_csv('csv_tests/hist_data_test_year.csv')
    test3_actual['Date'] = pd.to_datetime(test3_actual['Date'])
    test3_actual.set_index('Date', inplace=True)
    pd.testing.assert_frame_equal(test3, test3_actual)
    print('test 3 - OK')

    test4 = most_profitable_period('01-01-2000', '31-03-2022')
    test4_actual = pd.read_csv('csv_tests/most_profitable_period.csv')
    test4_actual['end_date'] = pd.to_datetime(test4_actual['end_date'])
    test4_actual['start'] = pd.to_datetime(test4_actual['start'])
    test4_actual.set_index('end_date', inplace=True)
    pd.testing.assert_frame_equal(test4, test4_actual)
    print('test 4 - OK')


test_basic()
