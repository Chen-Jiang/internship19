'''

This is to evaluate the performance of dedupe_join_files
the major difference between this evaluation and others lies that almost all the fields' type are Set

input is combined_output.csv
output will be the accurate rate from this training shown on the terminal

'''

import Levenshtein, distance
import csv
from datetime import datetime

input = "matrix_output.csv"


def calculate_two_recoeds_score(field_values, fields_len):

    field_score = 0
    # print("222",field_values, type(field_values),len(field_values))

    if len(field_values) == 2:

        lev = 0
        sor = 0
        jac = 0

        score = 0
        need_break = False

        v0 = field_values[0]
        v1 = field_values[1]
        for i in range(len(v0)):
            if not need_break:
                for j in range(len(v1)):
                    if v0[i] != "null" and v1[j] != "null" and v0[i] != "" and v1[j] != "" and v0[i] != " " and v1[j] != " ":
                        lev = Levenshtein.ratio(v0[i],v1[j])
                        sor = 1 - distance.sorensen(v0[i],v1[j])
                        jac = 1 - distance.jaccard(v0[i],v1[j])

                        aver = (lev+sor+jac)/3

                    elif v0[i] == "null" or v1[j] == "null" or v0[i] == "" or v1[j] == "" or v0[i] == " " or v1[j] == " ":
                        aver = 0

                    if aver == 1:
                        score = aver
                        need_break = True
                        break
                    elif aver < 1 and aver > score:
                        score = aver
            else:
                break
        field_score = score

    elif len(field_values) > 2:
        field_score = 0

    return field_score

def compare_same_records(same_records):

    compare_score = 0
    fields = []      # fields = ['Cluster ID', 'confidence_score', 'unique_id', 'first_name', 'last_name', 'address_line', 'suburb', 'city', 'country', 'postcode', 'eaddress', 'domain', 'phone_number', 'origin']
    keys = same_records[0].keys()

    for item in keys:
        fields.append(item)
    same_records_len = len(same_records)

    for i in range(3,len(fields)-1):
        field_values = [] # this list should contain tuple type elements
        for j in range(same_records_len):
            single_field_values = []  # store single_field_values, the element's type is tuple
            # same_records[j] is dict, same_records[j][fields[i]] is String
            value = same_records[j][fields[i]].strip("\"").strip("(").strip(")").strip(",")
            if "," not in value:
                single_field_values.append(value.strip("\'"))
            else:
                value = value.strip("\'")
                single_field_values = value.split("\', \'")
                for m in range(len(single_field_values)):
                    single_field_values[m] = single_field_values[m].strip("\'")
            single_field_values_tuple = tuple(s for s in single_field_values)
            field_values.append(single_field_values_tuple)
            # print("here field_values:", field_values)

            # field_values.append(same_records[j][fields[i]])   # the element inside field_value is tuple
        compare_score += calculate_two_recoeds_score(field_values, len(fields))

    compare_score = compare_score/11

    # compare_score is the total mating score of the two records
    return compare_score


def extract_same_records(file):

    output = "combined_same_records.csv"
    all_same_records = {}
    index = 0
    cluster_id = {}
    total_score = 0
    compare_score = 0
    accurate_rate = 0
    valid_count = 0
    average_matching_score = 0

    with open(output,'a') as output:

        headers = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']

        writer = csv.DictWriter(output, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()

        with open(file, encoding="ISO-8859-1") as f:
            reader = csv.DictReader(f, delimiter=",", lineterminator=",")

            start = datetime.now()

            for row in reader:
                if row['confidence_score']:
                    if row['Cluster ID'] not in cluster_id.keys():
                        values = []
                        records = []
                        # make the values list be the value of this key
                        values.append(row['unique_id'])
                        cluster_id[row['Cluster ID']] = values
                        # make the records list be the value of this key
                        records.append(dict(row))
                        all_same_records[row['Cluster ID']] = records
                    else:
                        values = []
                        records = []
                        # add the former list
                        values.extend(cluster_id[row['Cluster ID']])
                        # add the new unique_id to the original list and make it be the value of this key
                        values.append(row['unique_id'])
                        cluster_id[row['Cluster ID']] = values
                        # extract the value of this key and add the new value to it
                        records.extend(all_same_records[row['Cluster ID']])
                        records.append(dict(row))
                        all_same_records[row['Cluster ID']] = records
            end1 = datetime.now()
            print("extract same records needs:", end1-start)

            for item in cluster_id:
                same_group = {}
                # get an array containing the whole records
                same_group = all_same_records[item]
                for ele in same_group:
                    writer.writerow(ele)
                if len(same_group) == 2:
                    total_score += 1
                    compare_score = compare_same_records(same_group)
                    if compare_score > 0.5:
                        valid_count += 1
                        average_matching_score += compare_score
                elif len(same_group) > 2:
                    for a in range(len(same_group)-1):  # a=0,1 b=1,2
                        for b in range(a+1,len(same_group)):
                            part_group = []
                            part_group.append(same_group[a])
                            part_group.append(same_group[b])
                            total_score += 1
                            compare_score = compare_same_records(part_group)
                            if compare_score > 0.5:
                                valid_count += 1
                                average_matching_score += compare_score

            # calculate the accurate rate, use the number of valid matching among all the groups / the total number of groups
            accurate_rate = valid_count/total_score
            print("number of instances accurate_rate:", accurate_rate)

            average_matching_score = average_matching_score/valid_count
            print("average matching score among valid pairs:", average_matching_score)


            end2 = datetime.now()
            print("calculate accuracy needs:", end2-end1)

extract_same_records(input)
