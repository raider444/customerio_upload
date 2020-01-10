"""
This code uploads data from CSV to CustomerIO
"""
import csv
import logging
from customerio import CustomerIO, CustomerIOException
from config import *

try:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename=LOG_FILE)
except Exception as error_desc:
    print('Can not open logfile.\r\n', error_desc)
    exit(13)

cio = CustomerIO(SITE_ID, API_KEY)
logger = logging.getLogger(__name__)

def print_progress_bar(iteration, total, prefix='', suffix='',
                       decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    p_bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, p_bar, percent, suffix), end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

def upload_devices(csv_file):
    """
    Upload device token bindings to api
    @params:
        csv_files   - Required  : path to csv file (Int)
    """
    try:
        with open(csv_file, 'r') as device_tokens:
            data = csv.DictReader(device_tokens)
            csv_lines = sum(1 for line in open(csv_file)) - 1
            logging.debug(data.fieldnames)
            errors = 0
            i = 0
            print(csv_lines)
            for row in data:
                i = i + 1
                try:
                    cio.add_device(customer_id=row['user_id'], device_id=row['registration_token'],
                                   platform=row['operation_system'].lower())
                except CustomerIOException as err_put:
                    logging.error("Failed to associate %s. Error: %s", row['user_id'], err_put)
                    errors = errors + 1
                else:
                    logging.info("%s is associated with %s device id=%s",
                                 row['user_id'], row['operation_system'], row['registration_token'])
                print_progress_bar(i, csv_lines, prefix='Progress:', suffix=
                                   f'Complete, line {i} of {csv_lines}, errors: {errors}, current id: {row["user_id"]}',
                                   length=50)
    except Exception as err_open:
        print('Failed to open file: ', err_open)

def main():
    """
    Main
    """
    upload_devices(FILE)

if __name__ == "__main__":
    main()