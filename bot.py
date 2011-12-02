#!/usr/bin/env python

from oauthtwitter import OAuthApi
from settings import OAUTH_SETTINGS, TWITTER_SETTINGS
from db import create

import datetime
import re

date = ''
time = ''

Alert = create.Alerts
insert = Alert.insert()
and_ = create.and_
def auth():
	twitter = OAuthApi( \
				OAUTH_SETTINGS['consumer_key'], \
				OAUTH_SETTINGS['consumer_secret'], \
				OAUTH_SETTINGS['oauth_token'], \
				OAUTH_SETTINGS['oauth_token_secret'], \
				)
	return twitter

def generate_alerts(twitter):
	global date
	global time

	now = datetime.datetime.now()

	if now.minute < 10:
		minute = "0" + str(now.minute)
	else:
		minute = str(now.minute)

	if now.hour < 10:
		hr = "0" + str(now.hour)
	else:
		hr = str(now.hour)

	if now.day < 10:
		dy = "0" + str(now.day)
	else:
		dy = str(now.day)

	if now.month < 10:
		mh = "0" + str(now.month)
	else:
		mh = str(now.month)

	date = dy + str(mh) + str(now.year)
	time = hr + ":" + minute


	timeline = twitter.GetUserTimeline()
	for twitt in timeline[:2]:
		if re.search("@pytterhub", twitt['text']) and re.search("#ToDo", twitt['text']):
			dateTwitt = twitt['text'][:31].split(" ")
			timeAlert = dateTwitt[3]
			dateAlert = dateTwitt[2]

			datetimeAlert = now.replace( \
				year = int(dateAlert[4:]), \
				month = int(dateAlert[2:4]), \
				day = int(dateAlert[:2]), \
				hour = int(timeAlert[:2]), \
				minute = int(timeAlert[3:]), \
				)

			msg = twitt['text'][31:]
			found = _check_alerts(dateAlert, timeAlert, msg)

			if datetimeAlert >= now and found:
				insert.execute({'date': dateAlert, 'time': timeAlert, 'msg': msg})

def get_alerts():
	select = Alert.select()
	return _run(select)

def _run(select):
	calendar = {}
	result = select.execute()
	
	for row in result:
		if not calendar.has_key(row[1]):
			calendar = {row[1]: {row[2] : row[3]}}
		else:
			temp = calendar[row[1]]
			temp[row[2]] = row[3]
			calendar[row[1]] = temp
	
	return calendar

def _check_alerts(date, time, msg):
	found = Alert.select(and_(Alert.c.date == date, Alert.c.time == time, Alert.c.msg == msg))
	s = _run(found)
	
	if len(s) > 0:
		return False
	else:
		return True
	
def send_alerts_by_dm(calendar, twitter):
	for k,v in calendar.items():
		if k == date:
			if v.has_key(time):
				twitter.SendDM(TWITTER_SETTINGS['bot'], v[time])
				print "Mensaje directo enviado"

def main():
	twitter = auth()
	generate_alerts(twitter)
	calendar = get_alerts()
	send_alerts_by_dm(calendar, twitter)

if __name__ == "__main__":
	main()