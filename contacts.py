from brainboost_data_tools_json_package.JSonProcessor import JSonProcessor
from brainboost_data_tools_contacts.EmailProcessor import EmailProcessor
from brainboost_data_tools_contacts import EmailProcessor

import os
import json
from tinydb import TinyDB, where


data_source = '/brainboost/brainboost_data/data_tools/tools_goldenthinkerextractor_dataprocessing/resources/resources_data/data_subjective'
db_path = '/brainboost/brainboost_data/data_storage/storage_user_agents_database.json'


facebook_ads_sample = 'email,email,email,phone,phone,phone,madid,fn,ln,zip,ct,st,country,dob,doby,gen,age,uid,value'



def insert_json_to_tinydb(db_path, start_path):
    # Initialize TinyDB database
    db = TinyDB(db_path)

    def scan_and_insert(path):
        # Iterate over all items in the directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # If the item is a directory, recursively scan it
                scan_and_insert(item_path)
            elif item_path.endswith('.json'):
                # If the item is a .json file, read and insert its content into TinyDB
                with open(item_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        if isinstance(data, list):
                            db.insert_multiple(data)
                        else:
                            db.insert(data)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file: {item_path}")

    # Start the recursive scan from the given path
    scan_and_insert(start_path)





json_processor = JSonProcessor()
json_data = json_processor.load_json_files_recursively(data_source)


email_processor = EmailProcessor()

possible_emails = email_processor.generate_email_variations()


for email_variation in possible_emails:

    updated_records = json_processor.add_calculated_field_to_the_objects_from_an_array(
        json_data,
        'email',
        email_variation
    )


