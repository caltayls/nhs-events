import pandas as pd
import os
import datetime
from dotenv import load_dotenv
from src.html_generator.html_generator import render_html
from src.aws_utils.utils import AWS_tools
from src.aws_utils.load_dynamodb import load_dynamodb
from src.utils.utils import get_areas_from_county

load_dotenv()

AWS_BUCKET = os.getenv("AWS_BUCKET")
SOURCE_EMAIL_ADDRESS = os.getenv("SOURCE_EMAIL_ADDRESS")
ACTIVE_EVENTS_FILENAME = os.getenv("ACTIVE_EVENTS_FILENAME")
LOCATIONS_CSV_ENDPOINT = os.getenv("LOCATIONS_CSV_ENDPOINT")

active_events = AWS_tools().bucket_to_df(ACTIVE_EVENTS_FILENAME, AWS_BUCKET)
active_events.time_added = pd.to_datetime(active_events.time_added, format='%d/%m/%y-%H:%M')
active_events = active_events.dropna().sort_values("time_added")

def create_email_html(active_events, tfg_status):
	"""returns list of dicts of:
		{
			email_address: qweqwre,
			html: html
		}
	"""

	email_addr_content = []

	dt_now = datetime.datetime.now()
	day_of_week_now = dt_now.strftime("%A")

	users_df = load_dynamodb()
	# should contain uuid which will be injected into email html

	# collective email to users subscribed to all times and locations
	users_all_times = users_df[(users_df.frequency == "hourly") & (users_df.locations == ["All"])]
	# create dicts for each and append to list

	for user in users_all_times.itertuples():
		html = render_html(active_events, user.uuid)
		obj = {
			'email_address': user.email,
			'html': html 
		}
		email_addr_content.append(obj)
	
	# remaining users
	users_remaining = users_df[(users_df.frequency != "hourly") & (users_df.locations != ["All"])]
	location_df = pd.read_csv(LOCATIONS_CSV_ENDPOINT, index_col=0)
    
	for user in users_remaining.itertuples():
		# hourly
		user_areas = get_areas_from_county(user, location_df)
		events_refined = active_events[active_events.location.str.contains("|".join(user_areas), regex=True)] # creates regex or expr
		if user.frequency == "hourly":
			if len(events_refined) == 0: continue
			html = render_html(events_refined, user.uuid)
			# aws_instance.send_email(address_list= user.email,source_email_address= source_email, html=html)
			print("=========================")
			print(user.email)
			print(html)
			# daily
		elif user.frequency == "daily" & dt_now.hour == 17:
			daily_events = events_refined[events_refined.time_added.dt.strftime("%d%m") == dt_now.strftime("%d%m")]
			if len(daily_events) == 0: continue
			html = render_html(daily_events, user.uuid)
			# aws_instance.send_email(address_list= user.email, source_email_address= source_email, html=html)
			print("=========================")
			print(user.email)
			print(html)
		# weekly at 1700 on Fridays
		elif user.frequency == "weekly" & dt_now.hour == 17 & day_of_week_now == "Friday":
			weekly_events = events_refined[events_refined.time_added.dt.isocalendar().week == dt_now.isocalendar()[1]]
			if len(weekly_events) == 0: continue
			# aws_instance.send_email(address_list= user.email, source_email_address= source_email, html=html)
			
			html = render_html(daily_events, user.uuid)
			print("=========================")
			print(user.email)
			print(html)
		
		obj = {
			'email_address': user.email,
			'html': html 
		}
		email_addr_content.append(obj)
	
	return email_addr_content


