'''

This file is to assess the validity of columns in the files provided

'''

import pandas as pd
import io
import re

# input field
input_file = 'matrix_output1.csv'
output_file = 'matrix_assessed_data_output.csv'

# fieldnames
fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','dob','email','phone_1','phone_2','phone_3']


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
def assess_columns_using_dataframe_and_reg(file, fieldnames):
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
    phone1_records = data_framed['phone_1'].to_dict()
    calculate_validity_of_single_column(phone1_records,phone_reg,"phone1")

    phone2_records = data_framed['phone_2'].to_dict()
    calculate_validity_of_single_column(phone2_records,phone_reg,"phone2")

    phone3_records = data_framed['phone_3'].to_dict()
    calculate_validity_of_single_column(phone3_records,phone_reg,"phone3")


def calculate_validity_of_single_column(records, regexpression,name):

    print("starts!!", name)
    # find and calculate the validity of email column
    em_invalid_count = 0
    em_null_count = 0

    # loop all the items in the email_records
    for (k,v) in records.items():
        # during dataframe, phone_1 transfer from numeric class to float class,
        # has mixed types in the single column; so need to deal with it separately
        if isinstance(v, float):
            if "." in str(v):
                v = int(v)
        # use regex to find valid format of email contents
        reg_result = re.match(regexpression,str(v))
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





















    #
    # # run a loop to see the validity of each column
    # for i in range(1,len(fieldnames)):
    #
    #     # emails needs to have only one @
    #     # quoted strings must be dot separated or the only element making up the local-part
    #     if i == 9:
    #         print("emails")
    #         email_result = []
    #         for item in data_framed.items():
    #             print("item type", type(data_framed['email']))
    #             print("item",data_framed['email'])
            #     result = re.search("[^@]+@[^@]+",str(item))
            #     if not result:
            #         count += 1
            #         # print("not email", item, type(item))
            #         if type(item) == str:
            #             num += 1
            #             # if "." in item:
            #                 # print("maybe email", item)
            # print("count",count)
            # print("num",num)
            # email_result = re.finditer("(\w)+@(\w)+.",data_framed[fieldnames[i]])
            # email_result = re.findall("[^@]+@[^@]+",data_framed[fieldnames[i]])
            # for item in email_result:
            #     # print(item.group(0))
            #     local, domain = item.group(0).split("@")
            #     if len(local) <= 64:
            #         print(item.group(0))

            # email_result = [item for str(item) in data_framed[fieldnames[i]] if re.search("[^@]+@[^@]+",item)]
            # print(email_result)












# assess_columns_using_dataframe(input_file)
assess_columns_using_dataframe_and_reg(input_file, fieldnames)
