###
# jeremy runs development helper functions
###

import pandas as pd
import boto3
from io import StringIO


def move_data_google_sheets_to_s3():
    """ Function to copy data from Google sheets daily run log to s3 """
    import gspread
    from gspread_dataframe import get_as_dataframe

    # Set up service account object
    service_account = gspread.service_account()
    sheet = service_account.open("Workout log")
    worksheet = sheet.get_worksheet(0)
    # Pull down worksheet as dataframe
    raw_df = get_as_dataframe(worksheet,
                              parse_dates=True,
                              usecols=[0, 1, 2],
                              skiprows=None)
    _df = raw_df[pd.notnull(raw_df['Date'])]

    # Write dataframe to s3
    file_name = "daily_run_log.csv"
    csv_buffer = StringIO()
    _df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object("jeremyruns.com", file_name).put(Body=csv_buffer.getvalue())
