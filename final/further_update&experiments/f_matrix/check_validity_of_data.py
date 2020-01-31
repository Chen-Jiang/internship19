'''

As a step in separate_matrix.py
This file is to check the validity of each column in the matrix_label.csv and remove the
unreasonable data if find some.
The input is "matrix_label.csv", getting from separate_matrix
The output will be transferred back to separate_matrix

'''

import csv
from datetime import datetime
import operator

# input = "HOMESUB_output1.csv"
# output = "validity_file.csv"

def check_home_columns(records_dict, fields):

    print("enter home")

    dict = {}
    counter_null = 0
    strange_phones = {}
    phone_id_dict = {}

    # just check address_line, phone_number field
    indexes = [3,11]
    for i in indexes:
        for item in records_dict:
            ids = []
            # get the phone_number value of this record
            value = records_dict[item][fields[i]]
            # get the unique_id of this record and save it to the ids list
            id = records_dict[item][fields[0]]
            ids.append(id)
            if value != "null":
                # create a dictionary, the key is the phone_number, the value is the id list,
                # like {'0001283834':[01,02]}
                if value not in phone_id_dict.keys():
                    phone_id_dict[value] = ids
                else:
                    current_ids = phone_id_dict[value]
                    current_ids.extend(ids)
                    phone_id_dict[value] = current_ids

        for item in phone_id_dict:
            ids = phone_id_dict[item]
            if len(ids) >= 10:
                for ele in ids:
                    records_dict[ele][fields[i]] = None

    return records_dict


def check_bus_columns(records_dict, fields):

    print("enter bus")

    dict = {}
    counter_null = 0
    strange_phones = {}
    lname_id_dict = {}

    # just check last_name field
    i = 2
    for item in records_dict:
        ids = []
        # get the phone_number value of this record
        value = records_dict[item][fields[i]]
        # get the unique_id of this record and save it to the ids list
        id = records_dict[item][fields[0]]
        ids.append(id)
        if value != "null":
            # create a dictionary, the key is the phone_number, the value is the id list,
            # like {'0001283834':[01,02]}
            if value not in lname_id_dict.keys():
                lname_id_dict[value] = ids
            else:
                current_ids = lname_id_dict[value]
                current_ids.extend(ids)
                lname_id_dict[value] = current_ids

    for item in lname_id_dict:
        ids = lname_id_dict[item]
        if len(ids) >= 10:
            for ele in ids:
                records_dict[ele]['last_name'] = None

    return records_dict



def check_file_columns(input):

    print("enter...")

    fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']

    dict = {}
    counter_null = 0

    with open(output,'w') as f:

        fieldsname = ['field','counter']
        writer = csv.DictWriter(f,fieldnames=fieldsname, extrasaction='ignore')
        writer.writeheader()


        with open(input, encoding = 'ISO-8859-1') as input_f:
            reader = csv.DictReader(input_f, delimiter=",", lineterminator=",")

            t1 = datetime.now()
            for row in reader:
                dict[row['unique_id']] = row

            t2 = datetime.now()
            print("time needs:", t2-t1)

            i = 10
            # for i in range(1, len(fields)-1):
            field_values = {}
            sorted_field_values = {}
            for item in dict:
                value = dict[item][fields[i]].strip("(").strip(")").strip(",").strip("\'")


                if value not in field_values.keys():
                    field_values[value] = 1
                else:
                    v = field_values[value]
                    v += 1
                    field_values[value] = v

            # after this method, the dictionary transformed to a list whose elements are tuple, like this:
            # [('null', 169961), ('john', 9089),...]
            sorted_field_values = sorted(field_values.items(), key = operator.itemgetter(1), reverse = True)

            for ele in  sorted_field_values:
                print(ele)


            print("finish writing",fields[i])

# check_file_columns(input)
