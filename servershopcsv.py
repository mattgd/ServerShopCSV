import csv
import os
import fnmatch
import yaml
import sys
import logging

logger = logging.getLogger('servershopcsv')

OUTPUT_DIR = 'output'

def shop_yaml_to_csv(file_name):
    logger.info('YAML to CSV conversion started for ' + file_name)
    
    shop_data = None
    with open(file_name, 'r') as yaml_file:
        shop_data = yaml.load(yaml_file.read())

    output_file_name = os.path.join(OUTPUT_DIR, os.path.splitext(file_name)[0] + '.csv')      
    with open(output_file_name, 'w') as csv_file:
        fields = ('Slot', 'Type', 'Reward', 'Pricetype', 'Price', 'Sell', 'Amount', 'Displayname', 'Command', 'lore', 'Permission', 'Enchantments')
        writer = csv.DictWriter(csv_file, fieldnames=fields, lineterminator='\n')
        writer.writeheader()

        for slot in shop_data['stock']:
            row = shop_data['stock'][slot]
            row['Slot'] = slot # Add slot number to row
            writer.writerow(row)
    
    logger.info('YAML to CSV conversion completed for ' + file_name)

def shop_csv_to_yaml(file_name):
    logger.info('CSV to YAML conversion started for ' + file_name)
    
    shop_data = {}
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row = dict(row)
            slot = row['Slot']
            shop_data[slot] = {}
            del row['Slot'] # Delete the Slot row; only need it as dictionary key
            shop_data[slot] = row
    
    shop_data = {
        'slots': shop_data
    }
    
    output_file_name = os.path.join(OUTPUT_DIR, os.path.splitext(file_name)[0] + '.yml')  
    stream = open(OUTPUT_DIR + output_file_name, 'w')
    yaml.dump(shop_data, stream) 

    logger.info('CSV to YAML conversion completed for ' + file_name)

if __name__ == "__main__":
    to_conversion = sys.argv[1].lower()
    file_match = sys.argv[2]

    # Decide which conversion function to use
    conversion_func = None
    if to_conversion in ['yaml', 'yml'] :
        conversion_func = shop_csv_to_yaml
    elif to_conversion == 'csv':
        conversion_func = shop_yaml_to_csv
    else:
        print('Invalid conversion type.')

    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if conversion_func:
        for file_name in os.listdir('.'):
            if fnmatch.fnmatch(file_name, file_match):
                conversion_func(file_name)
            