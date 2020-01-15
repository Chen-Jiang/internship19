'''

This is to evaluate the performance of dedupe_join_files
the major difference between this evaluation and others lies that almost all the fields' type are Set

input is combined_output.csv
output will be the accurate rate from this training shown on the terminal

'''

import Levenshtein, distance
import csv

input = "combined_output_1.csv"

def extract_same_records(file):

    all_same_records = {}
    index = 0
    cluster_id = {}

    with open(file, encoding="ISO-8859-1") as f:
        reader = csv.DictReader(f, delimiter=",", lineterminator=",")

        for row in reader:
            if row['confidence_score']:
                if row['Cluster ID'] not in cluster_id.keys():
                    values = []
                    values.append(row['unique_id'])
                    cluster_id[row['Cluster ID']] = values
                    # print("values", values)
                else:
                    print(cluster_id[row['Cluster ID']])
                    print(row)
                    value = cluster_id[row['Cluster ID']]
                    print("original value",value,type(row['unique_id']))
                    value = value.append(row['unique_id'])
                    print("new value", value)
                    cluster_id[row['Cluster ID']] = value
                    # print("new value:", value)
        print("cluster_id", cluster_id)

extract_same_records(input)
