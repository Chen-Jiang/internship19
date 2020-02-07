'''

This file is to modify data from homesub and bussub: in homesub, there are much data has accounts payable,
which seems not a home user, so I put all these data to bussub
After modification, the BUSSUB_output.csv will be extended, and the HOMESUB_output will be shortened

Input is "HOMESUB_output.csv", which is come from 1_separate_matrix.py
Output is a new "BUSSUB_output.csv"

'''

from datetime import datetime
import csv
import check_validity_of_data as check

# input file
input = "HOMESUB_output.csv"
output = "BUSSUB_output.csv"
sub_output = "BUSSUB_modified.csv"


# rewrite the output, which adds the new "bussub" data
def write_data_to_file(data):

    fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','email','eaddress','domain','phone_number','origin']

    with open(sub_output,'a') as f:
            writer = csv.DictWriter(f,fieldnames=fields, extrasaction='ignore')
            writer.writeheader()

            # check the validity of data in the bussub file
            data = check.check_bus_columns(data,fields)

            for ele in data:
                # print(data[ele])
                writer.writerow(data[ele])
    t3 = datetime.now()
    print("write new file ends:", t3)




# from HOMESUB_output to find all the records whose first name, last name has "accounts payable"
# and put all these data to a new dict which will be passed to another method
# ALSO modify the input file: remove all the bussub records
def find_bus_data(file,file2):

    output1 = "HOMESUB_modified.csv"
    t1 = datetime.now()
    print("start:", t1)

    bus_data = {}
    home_data = {}
    index = 0

    with open(file, encoding='ISO-8859-1') as input, open(file2, encoding='ISO-8859-1') as input2, open(output1,'a') as o:
        fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','email','eaddress','domain','phone_number','origin']
        writer = csv.DictWriter(o,fieldnames=fields, extrasaction='ignore')

        writer.writeheader()

        reader = csv.DictReader(input, delimiter=",", lineterminator=",")
        reader2 = csv.DictReader(input2, delimiter=",", lineterminator=",")

        for row in reader:
            fname = row['first_name'].lower()
            lname = row['last_name'].lower()

            if "accounts payable" in fname or "accounts payable" in lname:
                # write all the "like" bussub data into a new dictionary
                bus_data[row['unique_id']] = dict(row)
            else:
                home_data[row['unique_id']] = dict(row)
        print("has", len(bus_data), "bus data in homesub")

        for row in reader2:
            if row['unique_id'] not in bus_data.keys():
                bus_data[row['unique_id']] = dict(row)
            else:
                id = row['unique_id'] + "home"
                bus_data[id] = dict(row)
        print("the total number of bussub", len(bus_data))

        t2 = datetime.now()
        print("finish classifying all the bus data:", t2-t1)

        # check the validity of data in the homesub file
        home_data = check.check_home_columns(home_data,fields)
        for item in home_data:
            # print("new_dict[item]",new_dict[item])
            writer.writerow(home_data[item])

        t3 = datetime.now()
        print("finish writing homesub file needs:", t3-t2)
        print("bussub data count",len(bus_data))


    write_data_to_file(bus_data)

# find_bus_data(input)
