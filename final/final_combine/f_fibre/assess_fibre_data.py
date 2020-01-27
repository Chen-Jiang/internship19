'''

This file is to assess the validity of columns in the files provided, by using DataFrame
Currently, evaluate the validity of email and phone_number

plus: check the repeats of different fields' values to check the validity again

'''

import pandas as pd
import io
import re

# input field
# input_file = 'matrix_output1.csv'
# output_file = 'matrix_assessed_data_output.csv'


def assess_columns_using_dataframe(file):

    if isinstance(file, io.TextIOWrapper):
        # extract the name of the file
        fileName = file.name
    elif isinstance(file, str):
        fileName = file
    print("this is the file:", fileName)
    # read the csv output file
    data = pd.read_csv(fileName)
    print(data)

    # remove the first column("unique_id") when analyzing the columns
    data = data.drop(data.columns[0], axis=1)

    # to see the type of all the columns in the file
    print(data.dtypes)

    data_framed = pd.DataFrame(data)
    data_framed['dob'] = pd.to_datetime(data_framed['dob'])

    print(data_framed.describe(include = 'all'))

#  use regular expression to evaluate the validity of each content in the field
def assess_columns_using_dataframe_and_reg(file, fieldsname):

    if isinstance(file, io.TextIOWrapper):
        # extract the name of the file
        fileName = file.name
    elif isinstance(file, str):
        fileName = file
    print("this is the file:", fileName)
    # read the csv output file
    data = pd.read_csv(fileName)

    # remove the first column("unique_id") when analyzing the columns
    data = data.drop(data.columns[0], axis=1)

    # transfer data to dataframe format
    data_framed = pd.DataFrame(data)

    # to see the type of all the columns in the file
    print(data.dtypes)

    # see the general situation of data columns
    print(data_framed.describe(include = 'all'))

    # extract all the email contents from column and save to a dictionary
    # use regex to find the valid contents' format
    if "email" in data_framed.columns:
        email_records = data_framed['email'].to_dict()
        em_reg = "[^@]+@[^@]+"
        calculate_validity_of_single_column(email_records,em_reg,"email")

    phone_reg = "(\d)+$"

    # extract all the email contents from column and save to a dictionary
    phone_records = data_framed['phone_number'].to_dict()
    calculate_validity_of_single_column(phone_records,phone_reg,"phone_number")

    # use #non-null/#records to calculate the validity of the column
    for i in range(1,len(fieldsname)):
        # setting new name for non_null count
        name = fieldsname[i]
        # count non-null of a single column
        non_null_result = data_framed[fieldsname[i]].count()

        # calculate the non-null probability
        null_possibility = non_null_result/len(phone_records)
        print(name, "not null possibility:",null_possibility)

# calculate the specific possibility of different fields' validity and null situation
def calculate_validity_of_single_column(records, regexpression,name):

    print("starts!!", name)
    # find and calculate the validity of email column
    em_invalid_count = 0
    em_null_count = 0

    # loop all the items in the input records
    for (k,v) in records.items():

        # initialize a list, and add the single v to the list
        single_field_records = []

        # identify phone field, extract the contents of phone list
        if "(" in str(v) and ")" in str(v):

            v = v.strip("(").strip(")").strip(",").strip("\'")
            if "\', \'" in v:
                single_field_records = v.split("', '")
            # print("single_field_records:",single_field_records)
        else:
            single_field_records.append(v)
            # print("single_field_records:",single_field_records)

        # loop all the contents in the single_field_record, and identify if every
        # single content is qualified
        for single_field_item in single_field_records:
            # use regex to find valid format of contents
            reg_result = re.match(regexpression,str(single_field_item))
            # count the number of invalid emails
            if not reg_result:
                em_invalid_count += 1
                # print("may not emails",v)
                # count the number of null
                if str(v) == "nan":
                    em_null_count += 1
                    # print("may not emails",v)
    print("may not emails count:", em_invalid_count)
    print("null contents:", em_null_count)
    # calculate the validity possibility of email column
    validity_possibility = 1 - (em_invalid_count/len(records))
    # calculate the null possibility of email column
    null_possibility = em_null_count/len(records)
    print(name, "info validity:", validity_possibility)
    print(name, "null possibility:",null_possibility)


def check_columns(records):

    # the key is the address, and the value is a list containing id which has the same key
    checked_values = {}

    for item in records:
        ids = []
        id = records[item]['unique_id'][0]
        ids.append(id)
        # checked "address_line" and "phone_number"
        values = records[item]['phone_number']  # records[item]['address_line'] is a tuple type, so use index to get the specific values
        if values != "null":
            for i in range(len(values)):
                value = values[i]
                if value not in checked_values.keys():
                    checked_values[value] = ids
                else:
                    this_value = checked_values[value]
                    this_value.extend(ids)
                    checked_values[value] = this_value

    for item in checked_values:
        if len(checked_values[item]) > 5:
            print(item, len(checked_values[item]), checked_values[item])









# assess_columns_using_dataframe(input_file)
# assess_columns_using_dataframe_and_reg(input_file)
