
# Send happy text

import twilio
from twilio.rest import TwilioRestClient

from twilio_credentialsguy import *


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

message_body = "BE HAPPY - Life is GREAT!!"


client.messages.create(
    to="+17045768532", 
    from_="+13123132044", 
    body=message_body
)




