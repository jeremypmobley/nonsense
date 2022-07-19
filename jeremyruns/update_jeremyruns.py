"""
Script to update jeremyruns.com website

Runs from local /Downloads folder
    - need to update read in data path to execute in other env

Reads data in from csv in downloads folder
Writes html and png files to s3

"""

import datetime
import pandas as pd
import boto3
import matplotlib.pyplot as plt
import seaborn as sns

LOCAL_FILE_LOC = 'C:/Users/jerem/Downloads/Workout log - DailyRunLog.csv'


def calc_runstats(df: pd.DataFrame, num_days_back):
    """

    Function to calculate stats from daily running dataframe

    :input: df: pd.DataFrame
    :return: dict
    """
    runstats_output = {'num_days_back': num_days_back}
    num_days_run = sum(df.tail(num_days_back)['Miles'] > 0)
    runstats_output['num_days_run'] = num_days_run
    runstats_output['pct_days_run'] = round(100.0 * num_days_run / num_days_back, 1)
    tot_miles_run = round(df.tail(num_days_back)['Miles'].sum(), 1)
    runstats_output['tot_miles_run'] = tot_miles_run
    runstats_output['miles_per_day'] = round(tot_miles_run / num_days_back, 2)
    runstats_output['miles_per_run'] = round(tot_miles_run / num_days_run, 2)
    return runstats_output


def create_metrics_text_from_dict(metrics_dict):
    """
    Function to create text string from metrics dict
    """

    metrics_text_string = f"""Last {metrics_dict['num_days_back']} days: \
{metrics_dict['num_days_run']} runs, \
{metrics_dict['pct_days_run']}% of days, \
{metrics_dict['tot_miles_run']} miles, \
{metrics_dict['miles_per_day']} miles/day, \
{metrics_dict['miles_per_run']} miles/run\
"""
    return metrics_text_string


def create_last_run_text(df):
    """ Function to create text about the most recent run from df """
    last_run_date = pd.Timestamp(df[df['Miles'] > 0].tail(1)['Date'].values[0])
    last_run_distance = df[df['Miles'] > 0].tail(1)['Miles'].values[0]
    last_run_notes = df[df['Miles'] > 0].tail(1)['Notes'].values[0]

    if pd.isnull(df[df['Miles'] > 0].tail(1)['Notes'].values[0]):
        last_run_text = f"Last Run: {last_run_date.strftime('(%m/%d)')} - {last_run_distance} miles"
    else:
        last_run_text = f"Last Run: {last_run_date.strftime('(%m/%d)')} - {last_run_distance} miles ({last_run_notes})"

    return last_run_text


def create_ma_over_time_chart(df: pd.DataFrame, num_days_back):
    """ Function to create and save chart of MA over past num_days_back from df """
    sns.set(rc={'figure.figsize': (10, 6)})
    sns.scatterplot(data=df.tail(num_days_back), x="Date", y="Miles")
    sns.lineplot(x='Date', y='value', hue='variable',
                 data=pd.melt(df.tail(num_days_back)[['Date', 'MA_30day', 'MA_10day']], 'Date'))
    plt.title(f'Last {num_days_back} days')
    plt.legend(['MA_30day', 'MA_10day'])
    plt.savefig(f'last_{num_days_back}_days_MA_over_time.png')


def preprocess_raw_df(df_) -> pd.DataFrame:
    """ Function to preprocess raw daily data """
    df_ = (df_
           .assign(Date=pd.to_datetime(df_["Date"]))  # Make Date a datetime object
           .assign(Miles=lambda x: df_['Miles'].fillna(0))  # Fill missing miles with 0
           .assign(MA_10day=df_['Miles'].rolling(window=10).mean())  # Create rolling averages
           .assign(MA_30day=df_['Miles'].rolling(window=30).mean())
           .sort_values('Date')
           )
    return df_


def main():
    # Read in data from s3
    bucket = "jeremyruns.com"
    file_name = "daily_run_log.csv"

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    raw_data_df = pd.read_csv(obj['Body'])
    print(f'Records read in: {raw_data_df.shape[0]}')

    df = raw_data_df.copy()
    df = df.pipe(preprocess_raw_df)
    # Remove days in future
    df = df[df['Date'] < datetime.datetime.today()]

    last_run_text = create_last_run_text(df)
    site_last_updated = datetime.datetime.now().strftime('(%m/%d)')
    last_30_text = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=30))
    last_180_text = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=180))
    last_365_text = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=365))
    all_data_text = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=df.shape[0]))

    html_string = f"""

<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
    <title>jeremyruns.com</title>
    <link rel="icon" type="image/png" src="s3://jeremyruns.com/favicon.png">
</head>
<body>
    <h1>Welcome to jeremyruns.com</h1>

    <h2>{last_run_text}</h2>

    Updated as of {site_last_updated}

    <h2>{last_30_text}</h2>
    <img src="https://s3.us-east-2.amazonaws.com/jeremyruns.com/last_31_days_MA_over_time.png">

    <h2>{last_180_text}</h2>
    <img src="https://s3.us-east-2.amazonaws.com/jeremyruns.com/last_180_days_MA_over_time.png">

    <h2>{last_365_text}</h2>
    <img src="https://s3.us-east-2.amazonaws.com/jeremyruns.com/last_365_days_MA_over_time.png">

    <h2>{all_data_text}</h2>

</body>
</html>

"""

    # Creating an HTML file
    html_file = open("index.html", "w")
    # Adding input data to the HTML file
    html_file.write(html_string)
    # Saving the data into the HTML file
    html_file.close()

    # Upload files to s3
    s3_client = boto3.resource('s3')
    bucket = s3_client.Bucket('jeremyruns.com')

    print('Upload index file')
    bucket.upload_file('index.html', 'index.html', ExtraArgs={'ContentType': 'text/html'})

    print('Create image files locally')
    create_ma_over_time_chart(df=df, num_days_back=31)
    create_ma_over_time_chart(df=df, num_days_back=180)
    create_ma_over_time_chart(df=df, num_days_back=365)

    print('Upload image files')
    bucket.upload_file('last_31_days_MA_over_time.png', 'last_31_days_MA_over_time.png',
                       ExtraArgs={'ContentType': 'image/png'})
    bucket.upload_file('last_180_days_MA_over_time.png', 'last_180_days_MA_over_time.png',
                       ExtraArgs={'ContentType': 'image/png'})
    bucket.upload_file('last_365_days_MA_over_time.png', 'last_365_days_MA_over_time.png',
                       ExtraArgs={'ContentType': 'image/png'})


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
