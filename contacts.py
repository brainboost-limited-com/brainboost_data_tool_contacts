from brainboost_data_tools_json_package.JSonProcessor import JSonProcessor
from brainboost_data_tools_contacts.EmailProcessor import EmailProcessor
from brainboost_data_tools_contacts.NameProcessor import NameProcessor

import os
import csv
import random
import re
import sys
from tinydb import TinyDB, Query
from alive_progress import alive_bar

# Paths to the databases and output CSV
start_path = '/brainboost/brainboost_data/data_storage/storage_local/brainboost_data_storage_local_contacts/investors'
db_path = '/brainboost/brainboost_data/data_storage/storage_local/brainboost_data_storage_local_contacts/contacts_investors.json'
csv_file_path = '/brainboost/brainboost_data/data_storage/storage_local/brainboost_data_storage_local/brainboost_marketing_audience_investors_only.csv'
company_domains_db_path = '/brainboost/brainboost_data/data_storage/storage_company_names_and_domains/company_domains.json'

# Ensure the database file and directory exist
os.makedirs(os.path.dirname(db_path), exist_ok=True)
if not os.path.exists(db_path):
    open(db_path, 'w').close()

# Ensure the CSV file directory exists
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# CSV header
facebook_ads_audience_header_csv = 'email,email,fn,ln\n'

# Initialize JSonProcessor and load data into TinyDB
jp = JSonProcessor()
brainboost_data_storage_local_contacts = jp.to_tinydb(from_path=start_path, to_tinydb_json_file=db_path, log=True)

# Initialize processors
name_processor = NameProcessor()
company_domains_db = TinyDB(company_domains_db_path)
company_query = Query()

# Retrieve all contacts from the database
contacts = brainboost_data_storage_local_contacts.all()

# Determine the starting point by counting the lines in the existing CSV file
start_index = 0
existing_emails = set()
if os.path.exists(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        start_index = sum(1 for row in reader) - 1  # Subtract 1 for the header
        csvfile.seek(0)
        next(reader)  # Skip header
        for row in reader:
            existing_emails.add(row[0])  # Add the first_possible_email to the set

# Function to sanitize strings for email
def sanitize_string(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s)

# Open the CSV file in append mode
with open(csv_file_path, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # If the file is new or empty, write the header
    if start_index <= 0:
        csvwriter.writerow(['first_possible_email', 'second_possible_email', 'fn', 'ln'])

    # Progress bar setup
    with alive_bar(len(contacts) - start_index, title='Processing Contacts') as bar:
        for index, contact in enumerate(contacts[start_index:], start=start_index):
            if isinstance(contact, dict):  # Ensure contact is a dictionary
                company = contact.get('company')
                name = contact.get('name')
                
                # Check for None values and skip if necessary
                if not company or not name:
                    bar.text = f"Skipping contact due to missing 'company' or 'name': {contact}"
                    bar()
                    continue
                
                # Extract first and last names
                parsed_name = name_processor.extract_first_last_name(contact.get('name'))
                fn = parsed_name[0] if parsed_name else ''
                ln = parsed_name[1] if parsed_name else ''

                # Skip if first name or last name is missing
                if not fn or not ln:
                    bar.text = f"Skipping contact due to missing 'fn' or 'ln': {contact}"
                    bar()
                    continue
                
                # Sanitize names for email
                fn_sanitized = sanitize_string(fn)
                ln_sanitized = sanitize_string(ln)
                company_sanitized = sanitize_string(company).lower()
                
                # Generate the first possible email using company domain
                company_record = company_domains_db.get(company_query.company == company)
                if company_record:
                    domain = company_record['domain']
                else:
                    domain = company_sanitized + '.com'
                first_possible_email = f"{fn_sanitized}.{ln_sanitized}@{domain}"
                
                # Generate the second possible email with a random domain
                random_domain = random.choice(['gmail.com', 'hotmail.com', 'outlook.com'])
                second_possible_email = f"{fn_sanitized}{ln_sanitized}@{random_domain}"
                
                # Skip if email already exists
                if first_possible_email in existing_emails:
                    bar.text = f"Skipping duplicated email: {first_possible_email}"
                    bar()
                    continue
                
                # Add email to the set of existing emails
                existing_emails.add(first_possible_email)
                
                # Write to CSV
                csv_line = [first_possible_email, second_possible_email, fn, ln]
                csvwriter.writerow(csv_line)

            bar()  # Update the progress bar
            sys.stdout.flush()  # Ensure the output is flushed

print(f"CSV file '{csv_file_path}' has been updated.")
