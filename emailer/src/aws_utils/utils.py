import pandas as pd
import boto3
from io import BytesIO, StringIO
import datetime
import os



class AWS_tools:

    def __init__(self,):   
        self.s3 = boto3.client('s3', region_name='eu-west-2') 
        self.ses = boto3.client('ses', region_name='eu-west-2') 
    
    def df_to_bucket(self, df, file_name, bucket_name):
        "Convert Pandas df to csv and upload to aws bucket."
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        self.s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_content)

    def bucket_to_df(self, file_name, bucket_name):
        "Get csv from bucket and convert to df"
        response = self.s3.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read()
        df = pd.read_csv(BytesIO(content))
        return df
    
    def send_email(self, address_list, source_email_address, html, bcc=True):
        # html = events_df.to_html(index=False, )
        if bcc:
            send_type = 'BccAddresses'
        else:
            send_type = 'ToAddresses'
        CHARSET = "UTF-8"
        message = {
                "Body": {"Html": {"Charset": CHARSET, "Data": html}},
                "Subject": {"Charset": CHARSET, "Data": 'New Events'},
        }

        response = self.ses.send_email(
            Destination={send_type: address_list},
            Message=message,
            Source=source_email_address,
        )





def get_active_events_dataset(aws_tools_instance):
    """Gets active events dataset and removes past events"""

    active_events_df = aws_tools_instance.bucket_to_df('active_events.csv', 'nhs-free-events')
    # active_events_df = pd.read_csv('data/active_events_reformatted.csv')
    active_events_df.date_end = pd.to_datetime(active_events_df.date_end)
    today = datetime.datetime.now()
    today_date = today.date()
    
    not_active = active_events_df.query("date_end<@today_date")
    # Store past events into event history dataset
    update_event_history(not_active, aws_tools_instance)
    
    active = active_events_df.query("date_end>=@today_date")

    return active

def events_to_email(new_df, active_events, aws_tools_instance):
    """Compares new search to active events dataset.
    returns new events and adds then to active events."""

    # Create url sets for both dataframes. Returns a list of urls that are in newer df and not the other.
    urls_active = set(active_events.url)
    urls_new = set(new_df.url)

    diff_list = [*urls_new.difference(urls_active)]
    new_events_df = new_df.loc[new_df.url.isin(diff_list)]
    today = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")
    new_events_df['time_added'] = today

    #  Check that records don't exist in event history
    event_history_df = aws_tools_instance.bucket_to_df('event_history.csv', 'nhs-free-events')
    new_events_df = new_events_df[~new_events_df[['event_name', 'date', 'location']].isin(event_history_df.to_dict(orient='list')).all(axis=1)]
    
    return new_events_df

def update_active_events(active, new_events, aws_tools_instance):
    active = pd.concat((active, new_events), axis=0)
    aws_tools_instance.df_to_bucket(active, 'active_events.csv', 'nhs-free-events')


def update_event_history(non_active_event_df, aws_tools_instance):
    event_history_df = aws_tools_instance.bucket_to_df('event_history.csv', 'nhs-free-events')
    # non_active_event_df.date_end = non_active_event_df.date_end.dt.strftime("%d/%m/%y")
    event_history_df = pd.concat((event_history_df, non_active_event_df), axis=0)
    event_history_df = event_history_df.drop(['url', 'website'], axis=1)
    aws_tools_instance.df_to_bucket(event_history_df, 'event_history.csv', 'nhs-free-events')




def add_end_date_to_df(df):
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
    print(df_w_end_date)
    # Some dates without year specified are next year however are dated this year.
    # the code below fixes said dates
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    # lambda func to increase date by one year
    dt_plus_one_year = lambda x: x + pd.DateOffset(years=1)
    df_w_end_date.date_end = df_w_end_date.date_end.apply(lambda x: dt_plus_one_year(x) if (x.month<current_month & x.year==current_year) else x)

    return df_w_end_date




# if __name__ == '__main__':
#    active_evs = AWS_tools().bucket_to_df('active_events.csv', 'nhs-free-events')
#    active_evs = active_evs[~active_evs.url.str.startswith("http")]
#    AWS_tools().df_to_bucket(active_evs, 'active_events.csv', 'nhs-free-events')
    # pd.to_datetime('4 Feb', format='mixed')

#     aws_tools_instance = AWS_tools()
#     active_events_df = aws_tools_instance.bucket_to_df('active_events.csv', 'nhs-free-events')
#     history_df = aws_tools_instance.bucket_to_df('event_history.csv', 'nhs-free-events')
   

#    active_events_df


#     active_events_df[~active_events_df[['event_name', 'date', 'location']].isin(history_df.to_dict(orient='list')).all(axis=1)]