'''
this file is used to read matrix file to extract data from file and use active learning

ideas about how to extract data from matrix file:
1. deal with "\n" firstly: separate records like that firstly
2. deal with has the same makrs with delimiter
3. deal witn the records who has less fields

'''


## this is to use dedupe to analyse data

from collections import defaultdict
from collections import OrderedDict
from future.builtins import next
# import assess_matrix_data as assess_data

import os
import csv
import re
import logging
import optparse
from datetime import datetime

import dedupe
from unidecode import unidecode

## files
input_file = 'HOMESUB_output.csv'
# input_file = 'BUSSUB_output.csv'
# the last file recording matching results
output_file = 'csvFormat_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'

def read_matrix_data(file):

    data = {}
    t1 = datetime.now()
    with open(file, encoding = 'ISO-8859-1') as f:
        reader = csv.DictReader(f, delimiter=",", lineterminator=",")

        for row in reader:
            data[row['unique_id']] = dict(row)
        t2 = datetime.now()
        print("read all the home sub data needs:", t2-t1)
    return data

print('read file...')
print("assess data...")
# assess_data.assess_columns_using_dataframe_and_reg(input)
data = read_matrix_data(input_file)

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
        # {'field':'country','type': 'Set','has missing' : True},
        {'field':'eaddress','type': 'Set','has missing' : True},
        {'field':'domain','type': 'Set','has missing' : True},
        {'field':'phone_number','type': 'Set','has missing' : True},
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
    # print(cluster_id)
    # print(cluster)
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
with open(output_file, 'w') as f_output, open(input_file, encoding = "ISO-8859-1") as f_input:
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
        row_id = row[0]
        ## make sure if the record is in the same record pairs list
        if row_id in cluster_membership:
            # cluster_id = cluster_membership[row_id]["cluster id"]
            # canonical_rep = cluster_membership[row_id]["canonical representation"]
            row.insert(0, cluster_membership[row_id]['confidence'])
            row.insert(0, cluster_membership[row_id]['cluster id'])
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
