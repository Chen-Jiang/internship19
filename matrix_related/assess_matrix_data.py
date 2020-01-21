'''

This file is to assess the validity of columns in the HOMESUB and BUSSUB files separated from matrix file provided, by using DataFrame
Currently, evaluate the validity of email and phone_number


'''

import pandas as pd
import io
import re
import collections

# input field
input_file = 'HOMESUB_output.csv'
output_file = 'HOMESUB_assessed_data_output.csv'


def assess_columns_using_dataframe(file):

    pd.set_option('display.expand_frame_repr', False)

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
    print(data_framed.describe(include = 'all'))

#  use regular expression to evaluate the validity of each content in the field
def assess_columns_using_dataframe_and_reg(file):

    # fieldnames
    fieldsname = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
    # fieldsname = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
    # fieldsname = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','dob','email','phone_1','phone_2','phone_3']

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

    origin_records = data_framed['origin'].to_dict()

    # transfer data type
    # data_framed['dob'] = pd.to_datetime(data_framed['dob'])

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


    # new zealand's phone number formats
    # phone_reg = "([34679]{1}(\d){7}$)|(^2(\d){7}$)|(^2(\d){8}$)|(^2(\d){9}$)|(^8[367]{1}(\d){6}$)|(508(\d){6}$)|(800(\d){6}$)"
    # consider there are many countries, and every country has several phone number formats,
    # which means it is very hard to consider validity based on the format of the phone number
    phone_reg = "(\d)+$"

    # use #non-null/#records to calculate the validity of the column
    for i in range(1,len(fieldsname)):
        # setting new name for non_null count
        name = fieldsname[i]
        # count non-null of a single column
        non_null_result = data_framed[fieldsname[i]].count()

        # calculate the non-null probability
        null_possibility = non_null_result/len(origin_records)
        print(name, "not null possibility:",null_possibility)


    # review_repeat_email_contents(email_records)

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

            # for those not satisfy the regex requirements, add the em_invalid_count
            # NOTICE: the em_invalid_count contains the null situations
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


def review_repeat_email_contents(records):

    email = {}

    for (k,v) in records.items():
        if v not in email:
            email[v] = 1
        else:
            email[v] += 1

    # kv:kv[0] assumed: ordered by keys
    # sorted_email_by_key = sorted(email.items(), key = lambda kv:kv[0])
    sorted_email_by_value = sorted(email.items(), key = lambda kv:kv[1], reverse = True)

    # email_dict_keys = collections.OrderedDict(sorted_email_by_key)
    email_dict_values = collections.OrderedDict(sorted_email_by_value)

    for (k,v) in email_dict_values.items():
        print(k,":",v)

# assess_columns_using_dataframe(input_file)
# assess_columns_using_dataframe_and_reg(input_file)
