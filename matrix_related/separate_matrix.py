'''

This file is to separate different types of users in the matrix file

the input is matrix_label.csv
the output is several new csv files where the headers and the organization is the same with fibre and neighbourly file,
each file will contain only one type of users

'''

import csv
from datetime import datetime
import re

input = "matrix_label.csv"
home_output = "home_output.csv"
bussiness_output = "business_output.csv"


# read the original file and write to new file
def read_and_write_files(fileName):
    type = ["HOMESUB","BUSSUB"]
    output = ["HOMESUB_output.csv", "BUSSUB_output.csv"]
    fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']

    for s in range(len(output)):
        with open(output[s],"a") as file:
            writer = csv.DictWriter(file, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()

            with open(fileName, encoding = "ISO-8859-1") as f:
                reader = csv.DictReader(f, delimiter=",", lineterminator=",")

                # this dict is to record all the HOMESUB and BUSSUB records
                type_records = {}
                # step1: just keep HOMESUB and BUSSUB
                t1 = datetime.now()
                for row in reader:
                    if row['subtype_id'] == type[s]:
                        type_records[row['subs_id']] = dict(row)
                        # record = homesub_and_bussub_records[row['subs_id']]
                        # print(homesub_and_bussub_records[row['subs_id']])
                t2 = datetime.now()
                print("extract all the record needs:", t2-t1)

                t3 = datetime.now()
                for item in type_records:
                    update_record = separate_matrix_file(type_records[item])
                    # print("update_record", type(update_record), update_record)
                    writer.writerow(update_record)
                t4 = datetime.now()
                print("Writing finished, time need:",t4-t3)


# revise and combine the columns to be aligned with other two files;
# also according to the type of the record to parse the record to different method to write into new files
def separate_matrix_file(record):

    fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
    original_fields = ['subs_id','first_name','last_name','PersContact3','Home','Work','Mobile','AddrLine3','AddrLine4','AddrLine5','AddrLine6','CountryName','subtype_id']
    # step2: combine related columns
    # update_record is the updated record which is aligned with new headers
    update_record = {}
    all_fields_values = []
    phone = []

    id = record['subs_id']
    all_fields_values.append(id)
    all_fields_values.append(record['first_name'].lower())
    all_fields_values.append(record['last_name'].lower())

    # AddrLine3,4 will be combined to address_line
    add3 = record['AddrLine3'].lower()
    add4 = record['AddrLine4'].lower()
    address_line = add3 + "," + add4
    if "null" in address_line:
        address_line = re.sub('NULL','',address_line)
    address_line = address_line.strip(" ,")
    all_fields_values.append(address_line)

    # AddrLine5 will be suburb
    add5 = record['AddrLine5'].lower()
    suburb = add5
    all_fields_values.append(suburb)
    # print("suburb",suburb)

    # AddrLine6 will be city and postcode
    add6 = record['AddrLine6'].lower()
    has_postcode = re.search(r'[0-9]+$',add6)
    if has_postcode:
        postcode = re.search(r'(\s)*[0-9]+$',add6)
        postcode = postcode.group(0).strip(" ")
    else:
        postcode = "null"
    all_fields_values.append(postcode)
    # print("postcode",postcode)

    has_city = re.search(r'[a-zA-Z]+',add6)
    if has_city:
        city = re.search(r'[a-zA-Z]+(\s)*[a-zA-Z]*',add6).group(0)
    else:
        city = "null"
    all_fields_values.append(city)
    # print("city",city)

    all_fields_values.append(record['CountryName'].lower())

    # Home, Work, Mobile combined to phone_number
    for i in range(4,7):
        mobile = record[original_fields[i]]
        if mobile != "NULL" and mobile not in phone:
            phone.append(mobile)
    phone_number = phone
    all_fields_values.append(phone_number)
    # print("phone_number", phone_number, type(phone_number))

    # PersContact3 will be eaddress and domain
    email = record['PersContact3'].lower()
    counter = email.count("@")
    if counter == 1:
        eaddress, domain = email.split("@")
    else:
        if "NO EMAIL" in email or "N/A" in email:
            email = "null"
        eaddress = email
        domain = email
    all_fields_values.append(eaddress)
    all_fields_values.append(domain)

    # origin will be "matrix" + subtype_id
    origin = "matrix_" + record['subtype_id'].lower()
    all_fields_values.append(origin)
    # put this record into the new dict so that can be writen into the file

    # step3: parse the record to different method according to the subtype_id
    for m in range(len(fields)):
        update_record[fields[m]] = all_fields_values[m]


    return update_record

read_and_write_files(input)
