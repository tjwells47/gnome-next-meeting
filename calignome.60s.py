#!/usr/bin/env python3

from __future__ import print_function
import httplib2
import os

import dateutil.parser

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import rfc3339      # for date object -> date string
import iso8601      # for date string -> date object

from datetime import timezone

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'CaliGnome'

title = "Cali Gnome"

def get_date_object(date_string):
  return iso8601.parse_date(date_string)



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)


    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC timee
    # print('3 Events from Each Calendar|size=12')
    # print('Today\'s date is {}'.format(datetime.datetime.now().isoformat('T')))
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    eventsHumanCogResult = service.events().list(
        calendarId='iegu2d75h7ctvhm6q2prs6jbkg@group.calendar.google.com', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    eventsHumanCog = eventsHumanCogResult.get('items', [])

    eventsCompArcResult = service.events().list(
        calendarId='9brnc7m0ln5ucj87jcidh3gva8@group.calendar.google.com', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    eventsCompArc = eventsCompArcResult.get('items', [])

    eventsParDist = service.events().list(
        calendarId='55sj12bisinmvh79sv1ob3cl6k@group.calendar.google.com', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    eventsParDist = eventsParDist.get('items', [])

    eventsSoftEng = service.events().list(
        calendarId='kdi5gngashktqcgpdb2kccoeq4@group.calendar.google.com', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    eventsSoftEng = eventsSoftEng.get('items', [])

    eventsProjMan = service.events().list(
        calendarId='4e57h6fmurmv9sj6h9c54tbiek@group.calendar.google.com', timeMin=now, maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    eventsProjMan = eventsProjMan.get('items', [])



    mostRecent = {}

    x = 0

    # print("Project Management")
    for event in eventsProjMan:
        if x is 0:
            mostRecent = event
            x+= 1
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(get_date_object(start).day)
        # print(event['summary'] + "<span color='#2d5c7f'> - " + start + "</span>")

    x = 0

    # print("Software Engineering")
    for event in eventsSoftEng:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(event['summary'] + "<span color='#ff8f56'> - " + start + "</span>")
        dateRecent = get_date_object(start)
        dateMostRecent = get_date_object(mostRecent['start'].get('dateTime', event['start'].get('date')))
        if x is 0:
            if dateRecent < dateMostRecent:
                mostRecent = event
                x+= 1


    x = 0
    # print("Parallel and Distributed")
    for event in eventsParDist:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(event['summary'] + "<span color='#fff1a8'> - " + start + "</span>")
        dateRecent = get_date_object(start)
        dateMostRecent = get_date_object(mostRecent['start'].get('dateTime', event['start'].get('date')))
        if x is 0:
            if dateRecent < dateMostRecent:
                mostRecent = event
                x+= 1


    x = 0
    # print("Intro to Cog Sci")
    for event in eventsHumanCog:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(event['summary'] + "<span color='#E67C73'> - " + start + "</span>")
        dateRecent = get_date_object(start)
        dateMostRecent = get_date_object(mostRecent['start'].get('dateTime', event['start'].get('date')))
        if x is 0:
            if dateRecent < dateMostRecent:
                mostRecent = event
                x+= 1


    x = 0
    # print("Intro to Comp Arc")
    for event in eventsCompArc:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(event['summary'] + "<span color='#984a59'> - " + start + "</span>")
        dateRecent = get_date_object(start)
        dateMostRecent = get_date_object(mostRecent['start'].get('dateTime', event['start'].get('date')))
        if x is 0:
            if dateRecent < dateMostRecent:
                mostRecent = event
                x+= 1


    if not events:
        print('No upcoming events found.')

    # print("General")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # print(event['summary'] + "<span color='#554677'> - " + start + "</span>")


    b = datetime.datetime.now(timezone.utc)
    a = get_date_object(mostRecent['start'].get('dateTime', event['start'].get('date')))


    c = a - b
    print(":date: <span>{} in {} days {} hrs {} mins</span>".format(mostRecent['summary'],days_hours_minutes(c)[0],days_hours_minutes(c)[1],days_hours_minutes(c)[2]))
    print("---")
    print(mostRecent['summary'])
    print("In {} days {} hrs {} mins".format(days_hours_minutes(c)[0],days_hours_minutes(c)[1],days_hours_minutes(c)[2]))


    # print("At {}".format(mostRecent['start'].get('dateTime', event['start'].get('date'))))


def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60




main()
