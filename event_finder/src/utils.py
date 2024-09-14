import pandas as pd
import boto3
from io import BytesIO, StringIO
import datetime


s3 = boto3.client('s3', region_name='eu-west-2')

class AWSTools:
    "Static methods for retrieving and uploading s3 csv data"

    @staticmethod
    def df_to_bucket(df, file_name, bucket_name):
        "Convert Pandas df to csv and upload to aws bucket."
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_content)

    @staticmethod
    def bucket_to_df(file_name, bucket_name):
        "Get csv from bucket and convert to df"
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read()
        df = pd.read_csv(BytesIO(content))
        return df


def add_end_date_to_df(df):
    """Finds last date of event and appends to df"""
    # First separate into first and last dates
    dates_with_start_end = df[df.date.str.contains('-')]
    single_date = df[~df.date.str.contains('-')]

    # Expand dates with start-end into two sep cols
    dates_separated = dates_with_start_end['date'].str.split('-', expand=True, )
    dates_separated.columns = ['date_start', 'date_end']
    dates_with_start_end = dates_with_start_end.join(dates_separated)
    dates_with_start_end = dates_with_start_end.drop(['date_start'], axis=1)

    # Add end date to single date records
    single_date['date_end'] = single_date.date
    df_w_end_date = pd.concat((dates_with_start_end, single_date)) 

    # Separate dates that don't include year.
    contains_year_bool = df_w_end_date.date_end.str.contains(r'\d{4}', regex=True)
    df_w_end_date_w_year = df_w_end_date[contains_year_bool]
    df_w_end_date_wo_year = df_w_end_date[~contains_year_bool]

    # create datetime objects and account for leap years...
    is_leap_year_bool = df_w_end_date_wo_year.date_end.str.contains('29 February')
    # df_w_end_date_wo_year.loc[~is_leap_year_bool, 'date_end'] = df_w_end_date_wo_year.date_end + ' ' +  str(datetime.datetime.now().year)
    df_w_end_date_wo_year.loc[:, 'date_end'] = df_w_end_date_wo_year.date_end + ' ' +  str(datetime.datetime.now().year)
    # df_w_end_date_wo_year.loc[is_leap_year_bool, 'date_end'] = pd.to_datetime(df_w_end_date_wo_year['date_end'] + str(datetime.datetime.now().year), format='mixed') + pd.Timedelta(days=365) 
    ######  ^^^ make 29 feb datetime then add year/365 days


    df_w_end_date = pd.concat((df_w_end_date_w_year, df_w_end_date_wo_year), axis=0)
    df_w_end_date.date_end = pd.to_datetime(df_w_end_date.date_end, format='mixed')

    curr_month = datetime.datetime.now().month
    curr_year = datetime.datetime.now().year
    
    # some events are for next year but don't include year
    # code will automatically add curr year so this fixes that
    df_w_end_date.date_end = df_w_end_date.date_end.apply(
        lambda d: d + pd.DateOffset(years=1) if (d.month<curr_month & d.year==curr_year) else d
    )

    return df_w_end_date

