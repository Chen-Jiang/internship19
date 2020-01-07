'''

This file is to assess the validity of columns in the files provided, by using DataFrame
Currently, evaluate the validity of email and phone_number

'''

import pandas as pd
import io
import re

# input field
input_file = 'neighbourly_output1.csv'
output_file = 'neighbourly_assessed_data_output.csv'


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
    # transfer the type of postcode
    # however, it seems different countries have different postcode rules, cannot transfer to numeric format easily
    # data_framed['postcode'] = pd.to_numeric(data_framed['postcode'])
    data_framed['dob'] = pd.to_datetime(data_framed['dob'])
    # print(data_framed['first_name'])
    # data_framed['phone_1'] = pd.to_numeric(data_framed['phone_1'])
    # data_framed['phone_2'] = pd.to_numeric(data_framed['phone_2'])
    # data_framed['phone_3'] = pd.to_numeric(data_framed['phone_3'])
    print(data_framed.describe(include = 'all'))

#  use regular expression to evaluate the validity of each content in the field
def assess_columns_using_dataframe_and_reg(file):

    # fieldnames
    # fieldsname = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','dob','email','phone_number']
    # fieldsname = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
    fieldsname = ['unique_id','first_name','last_name','address_line','suburb_name','city','postcode','email','phone_number']

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

    # transfer data type
    # data_framed['dob'] = pd.to_datetime(data_framed['dob'])

    # to see the type of all the columns in the file
    print(data.dtypes)

    # see the general situation of data columns
    print(data_framed.describe(include = 'all'))

    # extract all the email contents from column and save to a dictionary
    # use regex to find the valid contents' format
    email_records = data_framed['email'].to_dict()
    em_reg = "[^@]+@[^@]+"
    calculate_validity_of_single_column(email_records,em_reg,"email")


    # new zealand's phone number formats
    # phone_reg = "([34679]{1}(\d){7}$)|(^2(\d){7}$)|(^2(\d){8}$)|(^2(\d){9}$)|(^8[367]{1}(\d){6}$)|(508(\d){6}$)|(800(\d){6}$)"
    # consider there are many countries, and every country has several phone number formats,
    # which means it is very hard to consider validity based on the format of the phone number
    phone_reg = "(\d)+$"

    # extract all the email contents from column and save to a dictionary
    phone_records = data_framed['phone_number'].to_dict()
    calculate_validity_of_single_column(phone_records,phone_reg,"phone_number")


    # for experiment separate phone columns and one phone column
    # phone_records = data_framed['phone_main'].to_dict()
    # calculate_validity_of_single_column(phone_records,phone_reg,"phone_main")
    #
    # phone_records = data_framed['phone_mobile'].to_dict()
    # calculate_validity_of_single_column(phone_records,phone_reg,"phone_mobile")
    #
    # phone_records = data_framed['phone_fax'].to_dict()
    # calculate_validity_of_single_column(phone_records,phone_reg,"phone_fax")





    # use #non-null/#records to calculate the validity of the column
    for i in range(1,len(fieldsname)):
        # setting new name for non_null count
        name = fieldsname[i]
        # count non-null of a single column
        non_null_result = data_framed[fieldsname[i]].count()

        # calculate the non-null probability
        null_possibility = non_null_result/len(email_records)
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


        # during dataframe, phone_1 transfer from numeric class to float class,
        # has mixed types in the single column; so need to deal with it separately
        # if isinstance(v, float):
        #     if "." in str(v):
        #         v = int(v)


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






# assess_columns_using_dataframe(input_file)
assess_columns_using_dataframe_and_reg(input_file)
