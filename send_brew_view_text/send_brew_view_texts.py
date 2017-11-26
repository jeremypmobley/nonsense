#!/usr/bin/python
############################################################################

import pandas as pd
import twilio
from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup
import urllib
import time

# import Twilio Credentials
from twilio_credentialsguy import ACCOUNT_SID, AUTH_TOKEN


def remove_double_spaces(string):
    """
    Function to remove double spaces from a string
    """
    return ' '.join(string.split())


def get_brew_view_movies():
    """
    Function to scrape brew and view website
    Returns list of first two movies in first table of website
    """
    website = "http://brewview.com/"
    r = urllib.urlopen(website).read()
    soup = BeautifulSoup(r, "lxml")
    html_table = pd.read_html(soup.select("table")[1].prettify())[0]
    return [html_table[1][0], html_table[1][1]]


def main():
	brew_view_movies = get_brew_view_movies()
	for i in range(len(brew_view_movies)):
		message_body = "Brew & View is playing " + remove_double_spaces(brew_view_movies[i])
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
		client.messages.create(
			to="+17045768532", 
			from_="+13123132044", 
			body=message_body
		)
		time.sleep(10)


if __name__ == '__main__':
    main()




