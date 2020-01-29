'''

This file is to combine same records into one record, after identifying all the same records within a single file,
this script is used after csvFormat_output.csv is generated by program

input is the neighbourly_output.csv file
output is a csv file, which all the same records are combined as one record

'''

import csv
from datetime import datetime


# input = "neighbourly_output.csv"
# output = "combined_neighbourly.csv"
input = "csvFormat_output.csv"
output = "combined_fibre.csv"


def write_to_new_file(file):

    print("start writing...")
    start = datetime.now()
    print("start time:", start)

    with open(output,'a') as out_file:

        # write the header of the file
        fieldNames = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
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

            print("1")
            # all_records store all the recoreds from neighbourly file
            for row in reader:
                all_records[row['unique_id']] = dict(row)
                if row['confidence_score']:
                    # duplicate_records is a dictionary, the key is the cluster id and the value is a list containing all the records' unique_id who has the same cluster id
                    # like {'0':[19991,82763],'1':[7883,90938]}
                    if row['Cluster ID'] not in duplicate_records.keys():
                        value = []
                        value.append(row['unique_id'])
                        duplicate_records[row['Cluster ID']] = value
                    elif row['Cluster ID'] in duplicate_records.keys():
                        values = duplicate_records[row['Cluster ID']]
                        values.append(row['unique_id'])
                        duplicate_records[row['Cluster ID']] = values
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
                same_records = {}
                for ele in duplicate_records[item]:
                    same_records[count] = all_records[ele]
                    count += 1
                new_record[num] = combine_same_records(same_records)
                # print("new row",new_record[num] )
                writer.writerow(new_record[num])
            end2 = datetime.now()
            print("finish time:", end2-end2)

            print("3")
            for item in unique_records:
                this_record = {}
                for i in range(len(fieldNames)): # i<12
                    if i != 10:
                        value = []
                        # print("mark:", unique_records[item][fieldNames[i]])
                        value.append(unique_records[item][fieldNames[i]].strip("\""))
                        this_record[fieldNames[i]] = tuple(item for item in value)
                    elif i == 10:
                        if unique_records[item][fieldNames[i]] == "null":
                            this_record[fieldNames[i]] = "null"
                        else:
                            value = unique_records[item][fieldNames[i]]
                            this_record[fieldNames[i]] = value

                writer.writerow(this_record)
            end3 = datetime.now()
            print("finish time:", end3-end3)

    print("finished")


# the input is a dictionary, whose key is 0,1,2, the value is the whole record
def combine_same_records(same_records):

    fieldNames = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']
    # print("more than one:",same_records)
    combined_dict = {}

    for i in range(len(fieldNames)):
        field_values = []

        for index in same_records:
            item = same_records[index]
            print("item",item,type(item))
            value = item[fieldNames[i]]  # tuple type
            value1 = tuple(value)
            print("value",value)
            print("value1",value1,type(value1))

            for j in range(len(value1)):
                if value[j] != "null" and value[j] not in field_values:
                    field_values.append(value[j])

        # if the rows have several different values, keep these values inside a tuple,
        # and add the tuple as the final value of this field
        if len(field_values) > 0:
            combined_dict[fieldNames[i]] = tuple(j for j in field_values)
        # if the several value of this field is the same, the final value of this field is just one value
        elif len(field_values) == 0:
            combined_dict[fieldNames[i]] = "null"















        #
        # if i != 10:  # except phone_numbers field
        #     for index in same_records:
        #         item = same_records[index]
        #         value = item[fieldNames[i]].strip("\"").strip(" ")
        #         if item[fieldNames[i]] != "null":
        #             if value not in field_values:
        #                 field_values.append(item[fieldNames[i]].strip("\"").strip(" "))
        #     # if the rows have several different values, keep these values inside a tuple,
        #     # and add the tuple as the final value of this field
        #     if len(field_values) > 0:
        #         combined_dict[fieldNames[i]] = tuple(j for j in field_values)
        #     # if the several value of this field is the same, the final value of this field is just one value
        #     elif len(field_values) == 0:
        #         combined_dict[fieldNames[i]] = "null"
        # elif i == 10:
        #     phone_list = []
        #     for index in same_records:
        #         single_phone_list = []
        #         phone = same_records[index][fieldNames[i]]
        #         if phone != "null":
        #             phone = phone.strip("(").strip(")").strip(",")
        #             # print(phone)
        #             if "," in phone:
        #                 single_phone_list = phone.split(", ")
        #                 for m in range(len(single_phone_list)):
        #                     single_phone_list[m] = single_phone_list[m].strip("\'")
        #             elif "," not in phone:
        #                 single_phone_list.append(phone.strip("\'"))
        #             # print("single_phone_list",single_phone_list)
        #             phone_list.extend(single_phone_list)
        #     if len(phone_list) == 0:
        #         combined_dict[fieldNames[i]] = "null"
        #     else:
        #         # remove duplicates in the phone_list
        #         phone_list = list(dict.fromkeys(phone_list))
        #         combined_dict[fieldNames[i]] = tuple(item for item in phone_list)
        #     # print("phone list", combined_dict[fieldNames[i]])


    return combined_dict




write_to_new_file(input)