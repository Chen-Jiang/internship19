'''

This file is to add the country column to the neighbourly file so that they can be compared with other two files
Suppose that all the users are in the New Zealand, this is why the system do not have "country" field

Input is the final result: csvFormat_output.csv
Output is a new csv file which includes "country" column

'''

import csv

# input = "csvFormat_output.csv"


def add_country_column(file):

    print("start writing...")

    output = "neighbourly_output.csv"
    add_country_data = {}
    id = 0

    with open(output,'a') as o_f:
        original_fields = ['Cluster ID','confidence_score','unique_id','first_name','last_name','address_line','suburb','city','postcode','eaddress','domain','phone_number','origin']
        fields = ['Cluster ID','confidence_score','unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
        writer = csv.DictWriter(o_f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()

        with open(file,encoding="ISO-8859-1") as i_f:
            reader = csv.DictReader(i_f, delimiter=",", lineterminator=",")
            for row in reader:
                single_record = {}
                for i in range(len(original_fields)):
                    if i < 7:
                        single_record[fields[i]] = row[original_fields[i]]
                    elif i == 7:
                        single_record[fields[i]] = row[original_fields[i]]
                        single_record[fields[i+1]] = "new zealand"
                    elif i > 7:  # i = 8
                        single_record[fields[i+1]] = row[original_fields[i]]
                add_country_data[id] = single_record
                writer.writerow(add_country_data[id])
                # print(single_record)
                id += 1
    print("Writing completed")

# add_country_column(input)
