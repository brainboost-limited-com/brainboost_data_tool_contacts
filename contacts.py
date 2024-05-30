from brainboost_data_tools_json_package.JSonProcessor import JSonProcessor
from brainboost_data_tools_contacts.EmailProcessor import EmailProcessor
from brainboost_data_tools_contacts.NameProcessor import NameProcessor

import os
import json
import csv
from tinydb import TinyDB, Query
from progress.bar import Bar
import sys

start_path = '/brainboost/brainboost_data/data_storage/storage_local/storage_contacts'
db_path = '/brainboost/brainboost_data/data_storage/storage_local/storage_contacts/storage_user_agents_database.json'

# CSV header
facebook_ads_audience_header_csv = 'email,fn,ln\n'

# Initialize JSonProcessor and load data into TinyDB
jp = JSonProcessor()
brainboost_data_storage_local_contacts = jp.to_tinydb(from_path=start_path, to_tinydb_json_file=db_path, log=True)

# Initialize processors
email_processor = EmailProcessor()
name_processor = NameProcessor()

# Prepare CSV data
csv_lines = [facebook_ads_audience_header_csv.strip()]  # Start with the header

contacts = brainboost_data_storage_local_contacts.all()
contact_query = Query()

# Progress bar setup
bar = Bar('Processing Contacts ', max=len(contacts))

for contact in contacts:
    #possible_emails = email_processor.generate_email_variations(company=contact.get('company'), name=contact.get('name'))
    company = contact.get('company').replace(' ','')
    name = contact.get('name').replace(' ','')
    possible_emails = name + '@' + company + '.com'
    if possible_emails:
        first_possible_email = possible_emails[0]
        brainboost_data_storage_local_contacts.update({'email': first_possible_email}, (contact_query.name == contact.get('name')) & (contact_query.company == contact.get('company')))
        parsed_name = name_processor.extract_first_last_name(contact.get('name'))
        fn = parsed_name[0] if parsed_name else ''
        ln = parsed_name[1] if parsed_name else ''
        csv_line = f"{first_possible_email},{fn},{ln}"
        csv_lines.append(csv_line)
    bar.next()
    sys.stdout.flush()  # Ensure the output is flushed

bar.finish()


# Progress bar setup
bar_1 = Bar('Processing Contacts ', max=len(contacts))

# Write to CSV file
csv_file_path = 'brainboost_marketing_audience.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for line in csv_lines:
        csvwriter.writerow(line.split(','))

bar_1.finish()

print(f"CSV file '{csv_file_path}' has been created.")
