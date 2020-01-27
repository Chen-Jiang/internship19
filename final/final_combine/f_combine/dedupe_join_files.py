'''

This is to read joined files(combined_fibre.csv, combined_neighbourly.csv, combined_matrix_home.csv) and then run active learning algorithm on the joined data

the input is two files (here is combined_fibre.csv and combined_neighbourly.csv)
the output should be a new csv file which records all the same records of the two datasets

'''

from collections import defaultdict
from collections import OrderedDict
from future.builtins import next

import csv
import os
import logging
import optparse
from datetime import datetime

import dedupe
from unidecode import unidecode

input1 = "combined_fibre.csv"
input2 = "combined_neighbourly.csv"
input3 = "combined_matrix_home.csv"
# input = ["combined_fibre", "combined_neighbourly", "combined_matrix_home"]
combined_file = "combined.csv"
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'
output_file = 'combined_output.csv'


# read two files every time and save them to a dictionary called data which is passed to the active learning algorithm
def read_separate_files(input1,input2):

    print("start reading two filed...")
    t1 = datetime.now()
    print("t1:",t1)
    data = {}
    index = 0
    unique_id = 0

    fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']

    with open(combined_file,'a') as combined_output:

        writer = csv.DictWriter(combined_output, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()

        with open(input1,encoding = "ISO-8859-1") as input1:
            reader1 = csv.DictReader(input1, delimiter=",", lineterminator=",")
            # print(type(reader1))
            # print("reader1", reader1)
            for row in reader1:
                single_row = dict(row)
                # rewrite the original unique_id
                single_row['unique_id'] = unique_id
                data[index] = single_row
                writer.writerow(data[index])
                unique_id += 1
                # print("new record",data[index])
                index += 1

        t2 = datetime.now()
        print("t2:",t2)

        with open(input2,encoding = "ISO-8859-1") as input2:
            reader2 = csv.DictReader(input2, delimiter=",", lineterminator=",")
            for row in reader2:
                single_row = dict(row)
                single_row['unique_id'] = unique_id
                data[index] = single_row
                writer.writerow(data[index])
                unique_id += 1
                # print("new record",data[index])
                index += 1
        t3 = datetime.now()
        print("t3:",t3)

    print("Writing finished...")
    print("joined_data length:", len(data))
    return data

def read_combined_file(combined_file):

    data = {}
    index = 0

    with open(combined_file, encoding = "ISO-8859-1") as input:
        reader = csv.DictReader(input, delimiter=",", lineterminator=",")
        for row in reader:
            # print("row",row)
            data[index] = dict(row)
            index += 1
        print("data length:", len(data))
    return data

print("start...")
start = datetime.now()
if os.path.exists(combined_file):
    print("combined.csv exists...")
    data = read_combined_file(combined_file)
else:
    data = read_separate_files(input1, input2)

# If a settings file already exists, just load the file and skip training
if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file, 'rb') as f:
        ## StaticDedupe is a method used to load the settings_file
        deduper = dedupe.StaticDedupe(f)
## need training
else:
    ## define the attributes
    fields = [
        {'field':'first_name','type': 'Set','has missing' : True},
        {'field':'last_name','type': 'Set','has missing' : True},
        {'field':'address_line','type': 'Set','has missing' : True},
        # {'field':'suburb','type': 'Set','has missing' : True},
        {'field':'city','type': 'Set','has missing' : True},
        # {'field':'postcode','type': 'Set','has missing' : True},
        {'field':'eaddress','type': 'Set','has missing' : True},
        {'field':'domain','type': 'Set','has missing' : True},
        {'field':'phone_number','type': 'Set','has missing' : True},
        # {'field':'phone_mobile','type': 'Exact','has missing' : True},
        ]

    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)

    # deduper.sample(data, 20,0.5,None)

    ## if training_file has existed, we load the file
    ## else we train the data
    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file, 'rb', encoding = "ISO-8859-1") as f:
            deduper.prepare_training(data, f)
    else:
        deduper.prepare_training(data, None,15000,0.5,None)

    ## Start Active learning
    print('starting active labeling...')
    dedupe.consoleLabel(deduper)

    ## train model with examples we labeled
    deduper.train()

    # When finished, save our training and write to training_file
    with open(training_file, 'w') as tf:
        deduper.writeTraining(tf)

    # Save weights and predicates
    with open(settings_file, 'wb') as sf:
        deduper.writeSettings(sf)

## set threshold
threshold = deduper.threshold(data, recall_weight=1.5)
print('# threshold',threshold)

print('clustering...')
## return the same records found by dedupe, when the score is bigger than threshold
clustered_dupes = deduper.match(data, threshold)

print('# duplicate sets', len(clustered_dupes))

# ## Writing Results

# Write our original data back out to a CSV with new columns
# 'Cluster ID' indicates which records refer to each other.
# 'confidence_score' indicates the matching scores between several records

cluster_membership = {}
cluster_id = 0
for (cluster_id, cluster) in enumerate(clustered_dupes):
    print(cluster_id)
    print(cluster)
    id_set, scores = cluster
    ## cluster_d should be the whole record if it is included in the clustered_dupes
    cluster_d = [data[c] for c in id_set]
    # canonical_rep = dedupe.canonicalize(cluster_d)
    for record_id, score in zip(id_set, scores):
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            # "canonical representation" : canonical_rep,
            "confidence": score
        }

singleton_id = cluster_id + 1

## write output_file
with open(output_file, 'w') as f_output, open(combined_file, encoding = "ISO-8859-1") as f_input:
    writer = csv.writer(f_output)
    reader = csv.reader(f_input)

    heading_row = next(reader)

    ## add some columns
    ## represent the similarity score
    heading_row.insert(0, 'confidence_score')
    ## the same ID represents the same record
    heading_row.insert(0, 'Cluster ID')
    # canonical_keys = canonical_rep.keys()
    # for key in canonical_keys:
    #     heading_row.append('canonical_' + key)

    writer.writerow(heading_row)

    for row in reader:
        # blocks = row.items().split("|")
        blocks = row[0].split("|")
        print("row[0]",row[0],type(row[0]))
        row_id = int(blocks[0])
        ## make sure if the record is in the same record pairs list
        if row_id in cluster_membership:
            cluster_id = cluster_membership[row_id]["cluster id"]
            # canonical_rep = cluster_membership[row_id]["canonical representation"]
            row.insert(0, cluster_membership[row_id]['confidence'])
            row.insert(0, cluster_id)
            # for key in canonical_keys:
            #     row.append(canonical_rep[key].encode('utf8'))
        else:
            ## if the record is unique
            row.insert(0, None)
            row.insert(0, singleton_id)
            singleton_id += 1
            # for key in canonical_keys:
            #     row.append(None)
        writer.writerow(row)

end = datetime.now()
print("Time needs: ", end-start)
