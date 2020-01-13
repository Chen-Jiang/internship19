## this is to use dedupe to analyse data

from collections import defaultdict
from collections import OrderedDict
from future.builtins import next
# import assess_fibre_data as assess_data

import os
import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode

## files
input_file = 'experian_fibre.csv'
csv_output = 'fibre_csvFormat.csv'
output_file = 'csvFormat_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'

## according to the dedupe examples, adjust our original csv files to a standard csv format file, and write to a new csv file
## preprocess the format of data
def preProcessFile(fileName):
    with open(csv_output,'a') as file:
        ## set new csv file's headers (all the headers from the original files)
        original_fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']

        fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','eaddress','domain','phone_number','origin']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
        with open(fileName, encoding = "ISO-8859-1") as f:
            reader = csv.DictReader(f, delimiter="\n")
            ## create a dictionary: data to store all the records
            data = {}
            for row in reader:

                phone_number = []
                for (k,v) in row.items():
                    ## create a dictionry to store the single records
                    singleData = {}
                    ## split keys and values to a list, then match every key-value pair to a dictionary
                    keys = k.split("|")  #len(keys) = 13, including ",,,"
                    keys.pop(7)  #len(keys) = 12
                    values = v.split("|")
                    values.pop(7)  #len(values) = 12
                    output_keys_len = len(fieldnames) #output_keys_len = 11
                    i = 0
                    ## to delete all the ",,," at the end of each row, len(keys)-1
                    while i < output_keys_len: #i<11  len()
                        # fields before phones
                        if i < output_keys_len-4:  # if i < 7
                            if not values[i].strip("\"").strip("-").strip():
                                values[i] = "null"
                            else:
                                if "," not in values[i]:
                                    ## delete all the "" of the words
                                    # lower all the words to make sure all these letters are capital insensible
                                    singleData[fieldnames[i]] = values[i].lower().strip("\"")
                                    i += 1
                                    ## some contents are written in a single cell
                                    ## separate into different cells
                                else:
                                    contents = values[i].split(",")
                                    for j in range(len(contents)):
                                    ## delete all the "" of the words
                                        singleData[fieldnames[i]] = contents[j].lower().strip("\"")
                                        i = i + 1

                        # when comes to email field
                        if i == output_keys_len-4:  # i = 7
                            counter = values[i].count("@")
                            if counter == 1:
                                email, domain = values[i].strip("\"").split("@")
                                singleData[fieldnames[i]] = email
                                singleData[fieldnames[i+1]] = domain
                            else:
                                singleData[fieldnames[i]] = values[i]
                                singleData[fieldnames[i+1]] = values[i]
                            i += 1
                        # when comes to phone field
                        elif i == output_keys_len-3:  # i == 8
                            j = i # j = 8
                            while j < len(keys)-1: # j=8,9,10
                                # preprocess the format of phone number
                                while "+64" in values[j] or "-" in values[j] or "(" in values[j] or ")" in values[j] or " " in values[j] or "\"" in values[j]:
                                    values[j] = values[j].replace("+64","")
                                    values[j] = values[j].replace("-","")
                                    values[j] = values[j].replace("(","")
                                    values[j] = values[j].replace(")","")
                                    values[j] = values[j].replace(" ","")
                                    values[j] = values[j].replace("\"","")
                                if values[j].startswith("64"):
                                    values[j] = values[j][2:]
                                if values[j]:
                                    # if the two or three numbers are the same, just keep the number once
                                    if values[j] not in phone_number:
                                        phone_number.append(values[j])
                                j += 1
                            if len(phone_number) > 0:
                                singleData[fieldnames[i+1].strip("\"")] = tuple(i for i in phone_number)
                            else:
                                singleData[fieldnames[i+1].strip("\"")] = "null"
                            break
                    singleData["origin"] = "fibre"
                    ## add the single record to data dictionary, key is the unique_id of the records, and the value is all the contents
                    id = int(singleData["unique_id"])
                    ## transfer orderedDict to regular dictionary
                    data[id] = dict(singleData)
                    writer.writerow(data[id])

        print("writing completed")
        file.close()
        # assess_data.assess_columns_using_dataframe_and_reg(file, fieldnames)
        return data

# if the csv output file has been created, just read the output file directly and
# store the file to the data dictionary
def read_csv_output_data(fileName):
    data = {}
    with open(fileName) as file:
        reader = csv.DictReader(file)
        for row in reader:
            singleData = {}
            for (k,v) in row.items():
                singleData[k] = v
            id =row['unique_id']
            data[id] = dict(singleData)
    return data




print('read file...')
# check if the csv_output exists, if exist, read the file directly
if os.path.exists(csv_output):
    print("csv_output exists")
    data = read_csv_output_data(csv_output)
else:
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
        # {'field':'country','type': 'String','has missing' : True},
        {'field':'eaddress','type': 'String','has missing' : True},
        {'field':'domain','type': 'String','has missing' : True},
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
    print(cluster_id)
    print(cluster)
    id_set, scores = cluster
    ## cluster_d should be the whole record if it is included in the clustered_dupes
    cluster_d = [data[c] for c in id_set]

    # print("cluster_d", cluster_d)
    # canonical_rep = dedupe.canonicalize(cluster_d)
    # print("canonical_rep", canonical_rep)
    for record_id, score in zip(id_set, scores):
        # print("print...")
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            # "canonical representation" : canonical_rep,
            "confidence": score
        }
        print("cluster_membership", cluster_membership[record_id])
        # print(cluster_membership[record_id])

singleton_id = cluster_id + 1

## write output_file
with open(output_file, 'w') as f_output, open(csv_output, encoding = "ISO-8859-1") as f_input:
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
        row_id = blocks[0]
        print("row_id",row_id)
        ## make sure if the record is in the same record pairs list
        if row_id in cluster_membership:
            print("inside memebership")
            cluster_id = cluster_membership[row_id]["cluster id"]
            print("cluster_id", cluster_id)
            print("onfidence", cluster_membership[row_id]['confidence'])
            # canonical_rep = cluster_membership[row_id]["canonical representation"]
            row.insert(0, cluster_membership[row_id]['confidence'])
            row.insert(0, cluster_id)
            print("row",row)
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
