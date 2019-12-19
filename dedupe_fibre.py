## this is to use dedupe to analyse data

from collections import defaultdict
from collections import OrderedDict
from future.builtins import next
import assess_data

import os
import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode

## files
input_file = 'experian_fibre.csv'
# input_file = 'copy.csv'
output_file = 'csvFormat_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'

## according to the dedupe examples, adjust our original csv files to a standard csv format file, and write to a new csv file
## preprocess the format of data
def preProcessFile(fileName):
    with open('fibre_csvFormat1.csv','a') as file:
        ## set new csv file's headers (all the headers from the original files)
        fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
        with open(fileName, encoding = "ISO-8859-1") as f:
            reader = csv.DictReader(f, delimiter="\n")
            ## create a dictionary: data to store all the records
            data = {}
            for row in reader:
                for (k,v) in row.items():
                    ## create a dictionry to store the single records
                    singleData = {}
                    ## split keys and values to a list, then match every key-value pair to a dictionary
                    keys = k.split("|")
                    values = v.split("|")
                    i = 0
                    ## to delete all the ",,," at the end of each row, len(keys)-1
                    while i < len(keys)-1:
                        if not values[i].strip("\"").strip("-").strip():
                            values[i] = "null"
                        else:
                            if "," not in values[i]:
                                # transform the format of phone number delete "+64"
                                if i == 9 or i == 10 or i == 11:
                                    values[i] = values[i].replace("+64","")
                                    values[i] = values[i].replace("-","")
                                ## delete all the "" of the words
                                # lower all the words to make sure all these letters are capital insensible
                                singleData[keys[i].strip("\"")] = values[i].lower().strip("\"")
                                i += 1
                                ## some contents are written in a single cell
                                ## separate into different cells
                            else:
                                contents = values[i].split(",")
                                for j in range(len(contents)):
                                ## delete all the "" of the words
                                    singleData[keys[i].strip("\"")] = contents[j].lower().strip("\"")
                                    i = i + 1
                    ## add the single record to data dictionary, key is the unique_id of the records, and the value is all the contents
                    id = int(singleData["unique_id"])
                    ## transfer orderedDict to regular dictionary
                    data[id] = dict(singleData)
                    writer.writerow(data[id])

        print("writing completed")
        file.close()
        assess_data.assess_columns_using_dataframe_and_reg(file)
        return data
        #readData('csvFormat.csv')

## read the adjusted csv file and create a dictionary of recoreds
def readData(fileName):
    data = {}
    with open(fileName) as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
    return data

print('read file...')
data = preProcessFile(input_file)

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
        {'field':'first_name','type': 'String','has missing' : True},
        {'field':'last_name','type': 'String','has missing' : True},
        {'field':'address_line','type': 'String','has missing' : True},
        {'field':'city','type': 'String','has missing' : True},
        {'field':'postcode','type': 'Exact','has missing' : True},
        {'field':'country','type': 'String','has missing' : True},
        {'field':'email','type': 'String','has missing' : True},
        {'field':'phone_main','type': 'Exact','has missing' : True},
        {'field':'phone_mobile','type': 'Exact','has missing' : True},
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
    canonical_rep = dedupe.canonicalize(cluster_d)
    for record_id, score in zip(id_set, scores):
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            "canonical representation" : canonical_rep,
            "confidence": score
        }

singleton_id = cluster_id + 1

## write output_file
with open(output_file, 'w') as f_output, open('csvFormat.csv', encoding = "ISO-8859-1") as f_input:
    writer = csv.writer(f_output)
    reader = csv.reader(f_input)

    heading_row = next(reader)

    ## add some columns
    ## represent the similarity score
    heading_row.insert(0, 'confidence_score')
    ## the same ID represents the same record
    heading_row.insert(0, 'Cluster ID')
    canonical_keys = canonical_rep.keys()
    for key in canonical_keys:
        heading_row.append('canonical_' + key)

    writer.writerow(heading_row)

    for row in reader:
        # blocks = row.items().split("|")
        blocks = row[0].split("|")
        row_id = int(blocks[0])
        ## make sure if the record is in the same record pairs list
        if row_id in cluster_membership:
            cluster_id = cluster_membership[row_id]["cluster id"]
            canonical_rep = cluster_membership[row_id]["canonical representation"]
            row.insert(0, cluster_membership[row_id]['confidence'])
            row.insert(0, cluster_id)
            for key in canonical_keys:
                row.append(canonical_rep[key].encode('utf8'))
        else:
            ## if the record is unique
            row.insert(0, None)
            row.insert(0, singleton_id)
            singleton_id += 1
            for key in canonical_keys:
                row.append(None)
        writer.writerow(row)
