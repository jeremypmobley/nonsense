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
import calmap

from utils.helper_functions import move_data_google_sheets_to_s3


BUCKET = "jeremyruns.com"


def calc_runstats(df: pd.DataFrame, num_days_back: int):
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


def calc_textbox_stats(df: pd.DataFrame, num_days_back: int):
    """
    Function to calculate text box stats
    """
    num_days_run = sum(df.tail(num_days_back)['Miles']>0)
    tot_miles_run = round(df.tail(num_days_back)['Miles'].sum(),1)
    miles_per_day = round(tot_miles_run/num_days_back,2)
    miles_per_run = round(tot_miles_run/num_days_run,2)
    return num_days_run, tot_miles_run, miles_per_day, miles_per_run


def calc_prev_df(df: pd.DataFrame, num_days_back):
    """
    Function to calculate previous text box stats
    """
    prev_df = df.tail(num_days_back*2)
    prev_df = prev_df.head(num_days_back)
    return calc_textbox_stats(prev_df, num_days_back)


def create_metrics_text_from_dict(metrics_dict: dict):
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


def create_last_run_text(df: pd.DataFrame) -> str:
    """ Function to create text about the most recent run from df """
    last_run_date = pd.Timestamp(df[df['Miles'] > 0].tail(1)['Date'].values[0])
    last_run_distance = df[df['Miles'] > 0].tail(1)['Miles'].values[0]
    last_run_notes = df[df['Miles'] > 0].tail(1)['Notes'].values[0]
    if pd.isnull(df[df['Miles'] > 0].tail(1)['Notes'].values[0]):
        last_run_text = f"Last Run: {last_run_date.strftime('(%m/%d)')} - {last_run_distance} miles"
    else:
        last_run_text = f"Last Run: {last_run_date.strftime('(%m/%d)')} - {last_run_distance} miles ({last_run_notes})"
    return last_run_text


def create_last2wks_charts(df: pd.DataFrame, s3_resource_bucket):
    """ Function to create last 2 weeks daily chart """
    days_back = 14

    daily_plot_df = df.tail(days_back).reset_index()

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    plt.xticks(rotation=45)
    ax.bar(daily_plot_df['date_str_label'], daily_plot_df['Miles'])
    ax.set_xticks(daily_plot_df['date_str_label'])
    ax.plot(daily_plot_df['date_str_label'], daily_plot_df['MA_10day'], color='green')
    ax.legend(['MA_10day'])
    ax.set_ylabel('Miles')
    title = ax.set_title(f'Miles Per Day (past two weeks)', pad=20)
    title.set_weight('bold')
    title.set_size(16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for i in range(days_back):
        plt.text(i,
                 daily_plot_df['Miles'][i] + 0.1,
                 round(daily_plot_df['Miles'][i], 1), ha='center')
    fig.savefig('last_2wks_daily.png')
    s3_resource_bucket.upload_file('last_2wks_daily.png', 'last_2wks_daily.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('last_2wks_daily.png')


def create_wkly_miles_chart(wkly_sum_df: pd.DataFrame, s3_resource_bucket: object) -> object:
    """ Function to create weekly miles chart """
    wkly_plot_df = wkly_sum_df.tail(13).reset_index()

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    plt.xticks(rotation=45)
    title = ax.set_title('Miles Per Week (past quarter)', pad=20)
    title.set_weight('bold')
    title.set_size(16)
    ax.set_ylabel('Miles')
    ax.bar(wkly_plot_df['yr_wk'],wkly_plot_df['wklyavg'])
    ax.plot(wkly_plot_df['yr_wk'], wkly_plot_df['3wks_rolling'], color='green')
    ax.legend(['3 wk rolling avg'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for i in range(len(wkly_plot_df['yr_wk'])):
        plt.text(i,
                 wkly_plot_df['wklyavg'][i]+0.2,
                 round(wkly_plot_df['wklyavg'][i]), ha='center')
    fig.savefig('weekly_miles.png')
    s3_resource_bucket.upload_file('weekly_miles.png', 'weekly_miles.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('weekly_miles.png')


def create_monthly_miles_chart(monthly_sum_df, s3_resource_bucket):
    """ Function to create monthly miles chart """
    month_plot_df = monthly_sum_df.tail(12).reset_index()

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    plt.xticks(rotation=45)
    title = ax.set_title('Miles Per Month (past year)', pad=20)
    title.set_weight('bold')
    title.set_size(16)
    ax.set_ylabel('Miles')
    ax.bar(month_plot_df['yr_month'], month_plot_df['miles_sum'])
    ax.plot(month_plot_df['yr_month'], month_plot_df['3mo_rolling'], color='green')
    ax.legend(['3 month rolling avg'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for i in range(len(month_plot_df['yr_month'])):
        plt.text(i,
                 month_plot_df['miles_sum'][i]+0.8,
                 round(month_plot_df['miles_sum'][i]), ha='center')
    fig.savefig('monthly_miles.png')
    s3_resource_bucket.upload_file('monthly_miles.png', 'monthly_miles.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('monthly_miles.png')


def create_yearly_miles_chart(yrly_sum_df, s3_resource_bucket):
    """ Function to create yearly miles chart """
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    plt.xticks(rotation=45)
    title = ax.set_title('Miles Per Year (past ten years)', pad=20)
    title.set_weight('bold')
    title.set_size(16)
    ax.bar(yrly_sum_df['Date'], yrly_sum_df['miles_sum'])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for i in range(len(yrly_sum_df['Date'])):
        plt.text(i,
                 yrly_sum_df['miles_sum'][i]+5,
                 round(yrly_sum_df['miles_sum'][i]), ha='center')
    fig.savefig('yrly_miles.png')
    s3_resource_bucket.upload_file('yrly_miles.png', 'yrly_miles.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('yrly_miles.png')


def create_all_charts(df: pd.DataFrame, s3_resource_bucket):
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

    s3_resource_bucket.upload_file('all_charts.png', 'all_charts.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('all_charts.png')


def create_calmap(df, yr, s3_resource_bucket):
    """ Function to create calmap plot for given year """
    calmap_data = pd.Series(df['Miles'].values, index=df['Date'])
    plt.figure(figsize=(15, 5))
    plt.title(f'CALENDAR HEATMAP')
    calmap.yearplot(calmap_data,
                    year=int(yr),
                    fillcolor='lightgrey')
    plt.savefig(f'yr_calmap.png')
    s3_resource_bucket.upload_file('yr_calmap.png', 'yr_calmap.png',
                                   ExtraArgs={'ContentType': 'image/png'})
    # remove local file
    os.remove('yr_calmap.png')


def preprocess_raw_data(df):
    """
    Function to preprocess raw dataframe
    """
    def convert_date_to_datetime(_df):
        return _df.assign(Date=pd.to_datetime(_df['Date']))

    def fill_missing_miles_with_zero(_df):
        return _df.fillna({'Miles': 0})

    def filter_dates_prior_to_today(_df):
        return _df[_df['Date'] < datetime.datetime.today()]

    def calculate_rolling_averages(_df):
        _df['MA_10day'] = _df['Miles'].rolling(window=10).mean().fillna(0)
        _df['MA_30day'] = _df['Miles'].rolling(window=30).mean().fillna(0)
        return _df.sort_values('Date')

    pipeline = [
        convert_date_to_datetime,
        fill_missing_miles_with_zero,
        filter_dates_prior_to_today,
        calculate_rolling_averages,
    ]
    for func in pipeline:
        df = func(df)

    df['date_str_label'] = df['Date'].dt.strftime('%b-%d')

    return df


def main():
    """
    Main function to run update process

    :return: None
    """

    print('Moving data from google sheets to s3')
    move_data_google_sheets_to_s3()

    print('Read in data from s3')
    file_name = "daily_run_log.csv"
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=BUCKET, Key=file_name)
    raw_data_df = pd.read_csv(obj['Body'])
    print(f'Records read in: {raw_data_df.shape[0]}')

    # Process data, create rolling averages
    _df = raw_data_df.copy()
    _df = preprocess_raw_data(df=_df)

    last_run_text = create_last_run_text(_df)
    print(f'Last run: {last_run_text}')
    site_last_updated = datetime.datetime.now().strftime('(%m/%d)')
    print(f'Site last updated: {site_last_updated}')

    print('Calculating text box stats')
    num_days_run, tot_miles_run, miles_per_day, miles_per_run = calc_textbox_stats(df=_df, num_days_back=14)
    runs_prev14, miles_prev14, miles_per_day_prev14, miles_per_run_prev14 = calc_prev_df(df=_df, num_days_back=14)

    # read in html
    with open('index_template.html', 'r') as file:
        html_template_string = file.read()

    # read in css
    with open('jeremyruns_style.txt', 'r') as file:
        style_text = file.read()

    # Create index.html string
    html_string = html_template_string.format(style_text=style_text,
                                              last_run_text=last_run_text,
                                              site_last_updated=site_last_updated,
                                              runs_last14=num_days_run,
                                              miles_last14=tot_miles_run,
                                              miles_per_day_last14=miles_per_day,
                                              miles_per_run_last14=miles_per_run,
                                              runs_prev14=runs_prev14,
                                              miles_prev14=miles_prev14,
                                              miles_per_day_prev14=miles_per_day_prev14,
                                              miles_per_run_prev14=miles_per_run_prev14
                                              )

    # Creating an HTML file
    html_file = open("index.html", "w")
    # Adding input data to the HTML file
    html_file.write(html_string)
    # Saving the data into the HTML file
    html_file.close()

    # Upload files to s3
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(BUCKET)

    print('Upload index file')
    bucket.upload_file('index.html', 'index.html', ExtraArgs={'ContentType': 'text/html'})

    print('Create, upload image file to s3')
    create_all_charts(df=_df, s3_resource_bucket=bucket)

    print('Create last_2wks_daily chart')
    create_last2wks_charts(df=_df, s3_resource_bucket=bucket)

    # TODO: update create_wkly_miles_chart, create_monthly_miles_chart to take in _df
    print('Create weekly chart')
    _df['week_of_yr'] = _df['Date'].dt.strftime('%V')
    _df['yr_wk'] = _df['Date'].dt.strftime('%Y') + "-" + _df['week_of_yr']
    wkly_sum_df = _df.groupby(_df['yr_wk']).agg(wklyavg=('Miles', 'sum')).reset_index()
    wkly_sum_df['6wks_rolling'] = wkly_sum_df['wklyavg'].rolling(window=6).mean()
    wkly_sum_df['3wks_rolling'] = wkly_sum_df['wklyavg'].rolling(window=3).mean()
    wkly_sum_df = wkly_sum_df[wkly_sum_df['yr_wk'] <= datetime.datetime.now().strftime("%Y-%V")]
    create_wkly_miles_chart(wkly_sum_df=wkly_sum_df, s3_resource_bucket=bucket)

    print('Create monthly miles chart')
    _df['yr_month'] = _df['Date'].dt.strftime('%Y') + "-" + _df['Date'].dt.strftime('%m')
    monthly_sum_df = _df.groupby(_df['yr_month']).agg(miles_sum=('Miles', 'sum')).reset_index()
    monthly_sum_df['6mo_rolling'] = monthly_sum_df['miles_sum'].rolling(window=6).mean()
    monthly_sum_df['3mo_rolling'] = monthly_sum_df['miles_sum'].rolling(window=3).mean()
    create_monthly_miles_chart(monthly_sum_df=monthly_sum_df, s3_resource_bucket=bucket)

    print('Create yrly chart')
    yrly_sum_df = _df.groupby(_df['Date'].dt.strftime('%Y')).agg(miles_sum=('Miles', 'sum')).reset_index()
    create_yearly_miles_chart(yrly_sum_df=yrly_sum_df, s3_resource_bucket=bucket)

    print('Create calmap chart')
    create_calmap(df=_df,
                  yr=str(datetime.datetime.now().strftime("%Y")),
                  s3_resource_bucket=bucket)


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
