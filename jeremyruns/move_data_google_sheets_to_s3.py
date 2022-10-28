#!/usr/bin/env python
# coding: utf-8

"""
Move data from google sheets to s3
"""


from io import StringIO
import datetime
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe
import boto3


def main():
    """
    Main function to run script
    :return: None
    """
    print('Starting')
    print('Set up gspread service connection')
    service_account = gspread.service_account()

    print('Open workout log sheet, get worksheet')
    sheet = service_account.open("Workout log")
    worksheet = sheet.get_worksheet(0)

    print('Pull down worksheet to local')
    raw_df = get_as_dataframe(worksheet,
                              parse_dates=True,
                              usecols=[0, 1, 2],
                              skiprows=None)
    df = raw_df[pd.notnull(raw_df['Date'])]

    bucket = "jeremyruns.com"
    file_name = "daily_run_log.csv"

    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())


if __name__ == '__main__':
    print('Starting')
    START_TIME = datetime.datetime.now()
    try:
        main()
        print('Job complete')
    except Exception as err:
        raise err
    finally:
        print(f'Processing time: {datetime.datetime.now() - START_TIME}')
