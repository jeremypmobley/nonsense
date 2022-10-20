"""
Script to update jeremyruns.com website

Runs from local nonsense/jeremyruns directory path
Reads data in from csv in s3 - daily_run_log.csv from bucket jeremyruns.com
Writes html and png file to s3 for static hosting

"""

import os
import datetime
import pandas as pd
import boto3
import matplotlib.pyplot as plt


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


def create_all_charts(df, s3_resource_bucket):
    """ Function to create all charts in one single png """

    fig, ax = plt.subplots(4, 1, figsize=(10, 20))

    days_back = 30
    ax[0].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_30day'])
    ax[0].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_10day'])
    ax[0].scatter(df.tail(days_back)['Date'], df.tail(days_back)['Miles'])
    ax[0].legend(['MA_30day', 'MA_10day'])
    ax[0].set_ylabel('Miles')
    text_summary = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=days_back))
    ax[0].set_title(f'{text_summary}')
    ax[0].title.set_size(16)

    days_back = 90
    ax[1].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_30day'])
    ax[1].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_10day'])
    ax[1].scatter(df.tail(days_back)['Date'], df.tail(days_back)['Miles'])
    ax[1].legend(['MA_30day', 'MA_10day'])
    ax[1].set_ylabel('Miles')
    text_summary = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=days_back))
    ax[1].set_title(f'{text_summary}')
    ax[1].title.set_size(16)

    days_back = 365
    ax[2].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_30day'])
    ax[2].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_10day'])
    ax[2].scatter(df.tail(days_back)['Date'], df.tail(days_back)['Miles'])
    ax[2].legend(['MA_30day', 'MA_10day'])
    ax[2].set_ylabel('Miles')
    text_summary = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=days_back))
    ax[2].set_title(f'{text_summary}')
    ax[2].title.set_size(16)

    days_back = 3650
    ax[3].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_30day'])
    ax[3].plot(df.tail(days_back)['Date'], df.tail(days_back)['MA_10day'])
    ax[3].scatter(df.tail(days_back)['Date'], df.tail(days_back)['Miles'])
    ax[3].legend(['MA_30day', 'MA_10day'])
    ax[3].set_ylabel('Miles')
    text_summary = create_metrics_text_from_dict(calc_runstats(df=df, num_days_back=days_back))
    ax[3].set_title(f'{text_summary}')
    ax[3].title.set_size(16)

    fig.tight_layout(pad=3.0)

    fig.savefig('all_charts.png')

    s3_resource_bucket.upload_file(f'all_charts.png', f'all_charts.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove(f'all_charts.png')


def preprocess_raw_df(df_) -> pd.DataFrame:
    """ Function to preprocess raw daily data """
    df_ = (df_
           .assign(Date=pd.to_datetime(df_["Date"]))  # Make Date a datetime object
           .assign(Miles=lambda x: df_['Miles'].fillna(0))  # Fill missing miles with 0
           # .assign(MA_10day=df_['Miles'].rolling(window=10).mean())  # Create rolling averages
           # .assign(MA_30day=df_['Miles'].rolling(window=30).mean())
           .sort_values('Date')
           )
    return df_


def main():
    """
    Main function to run update process

    :return: None
    """

    # Read in data from s3
    bucket = "jeremyruns.com"
    file_name = "daily_run_log.csv"
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    raw_data_df = pd.read_csv(obj['Body'])
    print(f'Records read in: {raw_data_df.shape[0]}')

    # Process data, create rolling averages
    df = raw_data_df.copy()
    df = df.pipe(preprocess_raw_df)
    df = df[df['Date'] < datetime.datetime.today()]
    df['MA_10day'] = df['Miles'].rolling(window=10).mean()
    df['MA_30day'] = df['Miles'].rolling(window=30).mean()

    last_run_text = create_last_run_text(df)
    site_last_updated = datetime.datetime.now().strftime('(%m/%d)')

    style_text = """
    <style>

    h1 {text-align: center;}

    .center {
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }

    </style>
    """

    html_string = f"""

    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>jeremyruns.com</title>
        <link rel="icon" type="image/png" href="https://s3.us-east-2.amazonaws.com/jeremyruns.com/favicon.png">
    </head>

    {style_text}

    <body>
        <h1>JEREMYRUNS.COM</h1>

        <img src="https://s3.us-east-2.amazonaws.com/jeremyruns.com/all_charts.png" class="center">

        <h4>{last_run_text}</h4>

        <h4>Updated as of {site_last_updated}</h4>

        <p></p>

        <a href="https://jeremyruns.com/jeremyruns_architecture.html">Site Architecture Diagram</a>

        <p></p>

        <a href="https://github.com/jeremypmobley/nonsense/tree/master/jeremyruns">GitHub Code Repo</a>

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
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket('jeremyruns.com')

    print('Upload index file')
    bucket.upload_file('index.html', 'index.html', ExtraArgs={'ContentType': 'text/html'})

    print('Create, upload image file to s3')
    create_all_charts(df=df, s3_resource_bucket=bucket)


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
