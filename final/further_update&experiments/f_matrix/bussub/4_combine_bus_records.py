'''

This is to combine same records based on the result of dedupe, all the records whose matching score is higher than 0.5
will be combined as one record, others will not be combined

The input is the csvFormat_output.csv
The output is the combined_result.csv

'''

from datetime import datetime
import csv
from decimal import *

input = "csvFormat_output.csv"
output = "combined_bussub_result.csv"


def write_to_new_file(file):

    print("start writing...")
    start = datetime.now()
    print("start time:", start)

    with open(output,'a') as out_file:

        # write the header of the file
        fieldNames = ['company_info','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
        writer = csv.DictWriter(out_file, fieldnames=fieldNames, extrasaction='ignore')
        writer.writeheader()

        # write rows of the file
        # if the row has the same one, combine the rows into one row;
        # else if the row does not have other similiar ones, just keep it
        with open(input,encoding = "ISO-8859-1") as in_file:
            reader = csv.DictReader(in_file, delimiter=",", lineterminator=",")
            duplicate_records = {}
            all_records = {}
            unique_records = {}
            new_record = {}
            num = 0
            n = 0
            unsatisfied_matching = {}

            print("1")
            for row in reader:
                all_records[row['unique_id']] = dict(row)
                if row['confidence_score']:
                    # put the satisfied records into duplicate_records which needs adding company_info column
                    if Decimal(row['confidence_score']) >= 0.5 and row['Cluster ID'] not in unsatisfied_matching.keys():
                        if row['Cluster ID'] not in duplicate_records.keys():
                            value = []
                            value.append(row['unique_id'])
                            duplicate_records[row['Cluster ID']] = value
                        elif row['Cluster ID'] in duplicate_records.keys():
                            values = duplicate_records[row['Cluster ID']]
                            values.append(row['unique_id'])
                            duplicate_records[row['Cluster ID']] = values
                    # the unsatisfied ecords just keep the same
                    else:
                        # unsatisfied_matching: {'2':'2837','63737'}
                        if row['Cluster ID'] not in unsatisfied_matching.keys():
                            value = []
                            value.append(row['unique_id'])
                            unsatisfied_matching[row['Cluster ID']] = value
                            unique_records[n] = dict(row)
                            n += 1
                else:
                    unique_records[n] = dict(row)
                    n += 1
            end1 = datetime.now()
            print("finish time:", end1-start)
                # all_records[n1] = dict(row)
                # n1 += 1
            print("2")
            count = 0
            for item in duplicate_records:
                single_record = duplicate_records[item]  # single_record is a list containing all the ids whose Cluster id is the key
                same_records = {}
                for ele in single_record:
                    this_record = {}
                    this_record['company_info'] = all_records[ele]['domain'].strip("(").strip(")").strip(",").strip("\'")
                    for i in range(len(fieldNames)-1):
                        this_record[fieldNames[i+1]] = all_records[ele][fieldNames[i+1]]

                #     same_records[count] = all_records[ele]
                #     count += 1
                # new_record[num] = combine_same_records(same_records)
                # print("new row",new_record[num] )
                    writer.writerow(this_record)
            end2 = datetime.now()
            print("finish time:", end2-end1)

            print("3")
            for item in unique_records:
                this_record = {}
                for i in range(len(fieldNames)): # i<12
                    if i == 0:
                        field_value = None
                    else:
                        field_value = unique_records[item][fieldNames[i]]
                    # print("mark:", field_value, type(field_value))
                    if i > 0 and i != 10:
                        value = []
                        field_value = field_value.strip("(").strip(")").strip(",").strip("\'")
                        value.append(field_value)
                        this_record[fieldNames[i]] = tuple(item for item in value)
                    elif i == 10:
                        this_record[fieldNames[i]] = field_value
                        # if unique_records[item][fieldNames[i]] == "null":
                        #     this_record[fieldNames[i]] = "null"
                        # else:
                        #     value = unique_records[item][fieldNames[i]]
                        #     this_record[fieldNames[i]] = value

                writer.writerow(this_record)
            end3 = datetime.now()
            print("finish time:", end3-end2)

    print("finished")


# the input is a dictionary, whose key is 0,1,2, the value is the whole record
def combine_same_records(same_records):

    fieldNames = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
    # print("more than one:",same_records)
    combined_dict = {}

    for i in range(len(fieldNames)):
        field_values = []

        for index in same_records:
            # single_record_list = []
            item = same_records[index]  # get the whole dictionary
            value = item[fieldNames[i]]  # get the field value String type ('joshua dylan',) or ('8789670', '998364785')
            if "(" in value:
                value = value.strip("(").strip(")").strip(",")
                if "," in value:
                    tem_list = (value.split("\', \'"))  # need to remove '' later "" will added to every element automatically
                    for item in tem_list:
                        item = item.strip("\"").strip("\'")
                        if item not in field_values and value != None and value != "":
                            field_values.append(item)
                else:
                    if value.strip("\'") not in field_values and value.strip("\'") != None and value.strip("\'") != "":
                        field_values.append(value.strip("\'"))
            else:
                # print(222)
                # print("value",value)
                if value not in field_values and value != "":
                    # print(333)
                    field_values.append(value)
        # if the rows have several different values, keep these values inside a tuple,
        # and add the tuple as the final value of this field
        if len(field_values) > 0:
            combined_dict[fieldNames[i]] = tuple(j for j in field_values)
        # if the several value of this field is the same, the final value of this field is just one value
        elif len(field_values) == 0:
            combined_dict[fieldNames[i]] = None

    return combined_dict




write_to_new_file(input)
