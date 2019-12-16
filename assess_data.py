'''

This file is to assess the validity of columns in the files provided

'''

import pandas as pd
import io

# input field
input_file = 'matrix_output.csv'
output_file = 'matrix_assessed_data_output.csv'


def assess_columns(file):

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
    data_framed['phone_1'] = pd.to_numeric(data_framed['phone_1'])
    data_framed['phone_2'] = pd.to_numeric(data_framed['phone_2'])
    data_framed['phone_3'] = pd.to_numeric(data_framed['phone_3'])
    print(data_framed.describe(include = 'all'))





# assess_columns(input_file)
