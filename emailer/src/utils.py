import boto3
import pandas as pd
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Create cache for func
def get_areas_from_county(user_row, location_df) -> pd.Series:
	# create new locations column containing towns/cities within counties selected.
	user_locs = user_row["locations"]

	if user_locs[0] == "All":
		return location_df["Built-up area"]
	
	user_counties = pd.DataFrame(user_locs, columns=["County"])
	return location_df.merge(user_counties,  how="inner")["Built-up area"]

def get_users() -> list[dict]:
	"filters users based on their freq preference and date/time"
	dynamo = boto3.client("dynamodb")
	table = dynamo.Table("users")

	dt = datetime.today()
	hour = dt.hour
	weekday = dt.weekday()

	if hour != 17 and weekday != 4:
		users = table.query(KeyConditionExpression=Key("freq").eq("hourly"))["Items"]
	elif hour == 17 and weekday != 4:
		users_hr = table.query(KeyConditionExpression=Key("freq").eq("hourly"))["Items"]
		users_dly = table.query(KeyConditionExpression=Key("freq").eq("daily"))["Items"]
		users = users_hr + users_dly
	else:
		users = table.scan()["Items"]
	return users






