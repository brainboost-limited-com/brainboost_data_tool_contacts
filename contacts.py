from brainboost_data_tools_json_package.JSonProcessor import JSonProcessor
from brainboost_data_tools_contacts.EmailProcessor import EmailProcessor
from brainboost_data_tools_contacts.NameProcessor import NameProcessor

import os
import csv
from tinydb import TinyDB, Query
from progress.bar import Bar
import sys

start_path = '/brainboost/brainboost_data/data_storage/storage_local/brainboost_data_storage_local_contacts'
db_path = '/brainboost/brainboost_data/data_storage/storage_local/brainboost_data_storage_local_contacts/contacts.json'
csv_file_path = 'brainboost_marketing_audience.csv'

# Ensure the database file and directory exist
os.makedirs(os.path.dirname(db_path), exist_ok=True)
if not os.path.exists(db_path):
    open(db_path, 'w').close()

# CSV header
facebook_ads_audience_header_csv = 'email,email,fn,ln\n'

# Initialize JSonProcessor and load data into TinyDB
jp = JSonProcessor()
brainboost_data_storage_local_contacts = jp.to_tinydb(from_path=start_path, to_tinydb_json_file=db_path, log=True)

# Initialize processors
email_processor = EmailProcessor()
name_processor = NameProcessor()

contacts = brainboost_data_storage_local_contacts.all()
contact_query = Query()

# Function to extract nested contact data
def extract_contacts(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                yield from extract_contacts(value)
            else:
                yield data
                break
    elif isinstance(data, list):
        for item in data:
            yield from extract_contacts(item)

# Flatten contacts
flat_contacts = []
for contact in contacts:
    flat_contacts.extend(extract_contacts(contact))

# Debugging: Print the structure of flat_contacts
print("Debugging: Flattened Contact structure")
for contact in flat_contacts:
    print(contact)

# Determine the starting point by counting the lines in the existing CSV file
start_index = 0
if os.path.exists(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        start_index = sum(1 for row in reader) - 1  # Subtract 1 for the header

# Open the CSV file in append mode
with open(csv_file_path, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # If the file is new, write the header
    if start_index == 0:
        csvwriter.writerow(facebook_ads_audience_header_csv.strip().split(','))

    # Progress bar setup
    bar = Bar('Processing Contacts ', max=len(flat_contacts) - start_index)

    for index, contact in enumerate(flat_contacts[start_index:], start=start_index):
        if isinstance(contact, dict):  # Ensure contact is a dictionary
            company = contact.get('company')
            name = contact.get('name')
            
            # Check for None values and skip if necessary
            if not company or not name:
                print(f"Skipping contact due to missing 'company' or 'name': {contact}")
                continue
            
            company = company.replace(' ', '')
            name = name.replace(' ', '')
            possible_emails = [name + '@' + company + '.com', name + '@' + 'gmail.com']
            
            if possible_emails:
                first_possible_email = possible_emails[0]
                second_possible_email = possible_emails[1]
                brainboost_data_storage_local_contacts.update({'email': first_possible_email}, {'email': second_possible_email}, (contact_query.name == contact.get('name')) & (contact_query.company == contact.get('company')))
                parsed_name = name_processor.extract_first_last_name(contact.get('name'))
                fn = parsed_name[0] if parsed_name else ''
                ln = parsed_name[1] if parsed_name else ''
                csv_line = [first_possible_email, second_possible_email, fn, ln]
                csvwriter.writerow(csv_line)

            bar.next()
            sys.stdout.flush()  # Ensure the output is flushed
        else:
            print(f"Skipping non-dictionary contact: {contact}")

    bar.finish()

print(f"CSV file '{csv_file_path}' has been updated.")
