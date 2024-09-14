import datetime
from src.parse_events.parse_events import EventParser 
from src.html_generator.html_generator import render_html
from src.aws_utils.utils import (
  AWS_tools, 
  get_active_events_dataset, 
  events_to_email, 
  add_end_date_to_df, 
  update_active_events
)

def find_events():
    # fetches and parses new events from 3 websites
    print("Finding events...")
    event_dic = EventParser.new_events() 
    all_events_df = event_dic['events']
    all_events_df = add_end_date_to_df(all_events_df)
    all_events_df['url'] = all_events_df.website + all_events_df.url
    tfg_status = event_dic['tfg_status']

    # Compares new search to the previous
    aws_tools_instance = AWS_tools()
    active_events_df = get_active_events_dataset(aws_tools_instance)
    new_events_df = events_to_email(new_df = all_events_df, active_events = active_events_df, aws_tools_instance = aws_tools_instance)
    # concat columns to form link then render new events html
    
    
    html = render_html(new_events_df, tfg_status)

    # Email new events 
    aws_tools_instance.send_email(
        address_list=['callumtaylor955@gmail.com'], # , 'tomebbatson@live.co.uk', 'jennykent94@googlemail.com', 'emilypatrick01@hotmail.com', 'colindavid92@gmail.com']
        source_email_address='callumtaylor955@gmail.com', 
        html=html
    )

    update_active_events(active_events_df, new_events_df, aws_tools_instance)

    





if __name__ == '__main__':
    find_events()
    aws_tools = AWS_tools()
    ses = aws_tools.ses
#     message = {
#         "Subject": {"Data": "test"},
#         "Body": {"Text": {"Data": "test"}},
#     }
#     response = ses.send_email(
#     Destination={"ToAddresses": ["callumtaylor955@gmail.com"]},
#     Source="callumtaylor955@gmail.com",
#     Message=message
# )
    
    # Create the message structure
    message = {
        "Subject": {"Data": "Test Email"},
        "Body": {"Text": {"Data": f"Email sent at: {datetime.datetime.now()}"}},
    }

    # Send the email
    # try:
    #     response = ses.send_email(
    #         Destination={"ToAddresses": ["callumtaylor955+1@gmail.com"]},
    #         Source="callumtaylor955+1@gmail.com",
    #         Message=message
    #     )
    #     print("Email sent! Message ID:", response['MessageId'])
    # except Exception as e:
    #     print("Error sending email:", str(e))
    #     print(response)
    # event_dic = EventParser.new_events() 
    # all_events_df = event_dic['events']
    # all_events_df = add_end_date_to_df(all_events_df)
    # all_events_df

#     find_events()
    # # fetches and parses new events from 3 websites
    # # event_dic = EventParser.new_events() 
    # all_events_df = pd.read_csv('data/test_all_events.csv')

    # # all_events_df.to_csv('data/test_all_events.csv')
    # tfg_status = True

    # # Compares new search to the previous
    # aws_tools_instance = AWS_tools()
    # active_events_df = pd.read_csv('data/active_events_test.csv')

    # new_events_df = events_to_email(all_events_df, active_events_df)
    # new_events_df
    # # update_active_events(active_events_df, new_events_df, aws_tools_instance)
    # # concat columns to form link then render new events html
    # new_events_df['url'] = new_events_df.website + new_events_df.url
    # html = render_html(new_events_df, tfg_status, r"/src/html_templates/new_events_email_template/jinja_template.html")


    # # Email new events 
    # aws_tools_instance.send_email(
    #     address_list=['callumtaylor955@gmail.com', ], 
    #     source_email_address='callumtaylor955@gmail.com', 
    #     html=html
    # )


