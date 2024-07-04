#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:31:23 2023

@author: windhoos
"""

import csv
import os
from datetime import datetime
from ics import Calendar, Event
import pytz

def read_csv_file(file_path):
    events = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            event = {
                'Subject': row['Subject'],
                'Start Date': row['Start Date'],
                'Start Time': row['Start Time'],
                'End Date': row['End Date'],
                'End Time': row['End Time'],
                'All Day': row['All Day'],
                'Description': row['Description'],
                'Location': row['Location'],
                'UID': row['UID'],
                'Categories': row['Categories']
            }
            events.append(event)
    return events

def group_events_by_category(events):
    grouped_events = {}
    for event in events:
        category = event['Categories']
        if category not in grouped_events:
            grouped_events[category] = []
        grouped_events[category].append(event)
    return grouped_events

def write_csv_file(events, file_path):
    fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time',
                  'All Day', 'Description', 'Location', 'UID', 'Categories']
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

def convert_to_ics_file(events, file_path):
    cal = Calendar()
    for event in events:
        e = Event()
        e.name = event['Subject']
        # Get the timezone from the event data
        tzid = event.get('TZID', 'Europe/Amsterdam')  # Default to Europe/Amsterdam if not provided
        try:
            tz = pytz.timezone(tzid)
        except pytz.UnknownTimeZoneError:
            print(f"Warning: Unknown timezone '{tzid}'. Using 'Europe/Amsterdam' instead.")
            tz = pytz.timezone('Europe/Amsterdam')
        print(e.name)
        # Parse Start Date/Time with timezone
        start_datetime_str = event['Start Date'] + ' ' + event['Start Time']
        start_datetime = datetime.strptime(start_datetime_str, '%d-%m-%y %H:%M').replace(tzinfo=tz)
        e.begin = start_datetime

        # Parse End Date/Time with timezone (same format as start)
        end_datetime_str = event['End Date'] + ' ' + event['End Time']
        end_datetime = datetime.strptime(end_datetime_str, '%d-%m-%y %H:%M').replace(tzinfo=tz)
        e.end = end_datetime
        e.description = event['Description']
        e.location = event['Location']
        e.uid = event['UID']
        cal.events.add(e)
    with open(file_path, 'w') as ics_file:
        ics_file.writelines(cal)

def main(input_file):
    events = read_csv_file(input_file)
    grouped_events = group_events_by_category(events)
    base_dir = os.path.dirname(input_file)

    for category, events in grouped_events.items():
        category_file = os.path.join(base_dir, f"{category}.csv")
        write_csv_file(events, category_file)
        ics_file = os.path.join(base_dir, f"{category}.ics")
        convert_to_ics_file(events, ics_file)

if __name__ == '__main__':
    input_file = 'minor2425V1.csv'  # Replace with the path to your input CSV file
    '''
    required fields in csv (CASE SENSITIVE):
    'Subject',
    'Start Date',
    'Start Time',
    'End Date',
    'End Time',
    'All Day',
    'Description',
    'Location',
    'UID',
    'Categories'
    '''
    main(input_file)
