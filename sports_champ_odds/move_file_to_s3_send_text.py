

# move file to s3, send text

import boto3
from botocore.client import Config
import datetime
import twilio
from twilio.rest import TwilioRestClient

import pandas as pd


# import aws s3 credentials
from aws_s3_credentialsguy import *

# import Twilio Credentials
from twilio_credentialsguy import *

s3 = boto3.resource('s3', 
					config=Config(signature_version='s3v4'),
                    aws_access_key_id=S3_ACCESS_KEY,
                    aws_secret_access_key=S3_SECRET_KEY)

# move file to s3
file_name = "sports_odds_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".csv"
file_dir = "C:/Users/Jeremy/Desktop/sports_odds/"
file_loc = file_dir + file_name
data = open(file_loc, 'rb')
s3.Bucket('sports-odds').put_object(Key=file_name, Body=data)

df = pd.read_csv(file_loc)

nba_rows = len(df[df['sport']=="nba"])
nfl_rows = len(df[df['sport']=="nfl"])
nhl_rows = len(df[df['sport']=="nhl"])
mlb_rows = len(df[df['sport']=="mlb"])

row_counts_text = "Record counts- NBA: " + str(nba_rows) + " NFL: " + str(nfl_rows) + " NHL: " + str(nhl_rows) + " MLB: " + str(mlb_rows)


# send text that file was moved
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

message_body = "Today's file was successfully moved to s3. " + row_counts_text

client.messages.create(
    to="+17045768532", 
    from_="+13123132044", 
    body=message_body
)




