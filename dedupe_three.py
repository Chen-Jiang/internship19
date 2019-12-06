## this is to use dedupe to analyse data

from collections import defaultdict
from collections import OrderedDict
from future.builtins import next

import os
import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode

## files
# input_file = 'experian_fibre.csv'
input_file = 'experian_matrix.csv'
# input_file = 'experian_neighbourly.csv'
# input_file = 'copy.csv'
output_file = 'csvFormat_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'

## according to the dedupe examples, adjust our original csv files to a standard csv format file, and write to a new csv file
## preprocess the format of data
def preProcessFile(fileName, revise_format_file):

    # read the original file, change the format and write to the new file
    with open(revise_format_file,'a') as file:
        data = {}
        # according to different input file, run differnt nethod about reading file
        if n1 == 'experian_fibre':
            ## set new csv file's headers (all the headers from the original files)
            fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
            with open(fileName, encoding = "ISO-8859-1") as f:
                reader = csv.DictReader(f, delimiter="\n")
                read_fibre_file(reader, writer, data)

        elif n1 == 'experian_matrix':
            ## set new csv file's headers (all the headers from the original files)
            fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','dob','email','phone_1','phone_2','phone_3']
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
            with open(fileName, encoding = "ISO-8859-1") as f:
                reader = csv.DictReader(f, delimiter=",", lineterminator=",")
                # all_records = {}
                try(reader,writer,data)
                # read_fibre_file(reader, writer, data)

        elif n1 == 'experian_neighbourly':
            ## set new csv file's headers (all the headers from the original files)
            fieldnames = ['unique_id','first_name','last_name','address_line','suburb_name','city','postcode','email','phone_home','phone_mobile']
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
            with open(fileName, encoding = "ISO-8859-1") as f:
                reader = csv.DictReader(f, delimiter="\n")
                read_fibre_file(reader, writer, data)

        print("writing completed")
        file.close()
        return data

def try(reader,writer,data):

    for row in reader:
        print("new row")

        for (k,v) in row.items():
            record_pair = []
            values = v.split("|")
            v_len = len(values)
            k_len = 0

            if k != None:
                keys = k.split("|")
                k_len = len(keys)

            # situation 1: all the values have been extracted successfully
            if v_len == k_len:
                record_pair.append(v)
            # situation2: just several values are extracted
            else:
                # when the length of values is less than keys', just check and
                # revise it again and again
                if len(values) < k_len:
                    # situation1: have None as keys
                    if None in row:
                        print("has NONE")
                        print(row[None])
                        v += str(row[None]).strip("['").strip("']")
                        values = v.split("|")

                    if len(values) < k_len:
                        # read the next line to get more information
                        next_record = next(reader)
                        for (k1,v1) in next_record.items():
                            if "\n" in v1:
                                print("has ")
                                last, current = v1.split("\n")
                                v += last
                    # situation2: has \n in the value
                    elif "\\n" in v:
                        re1, re2 = v.split("\\n")
                        record_pair.append(re1)
                        record_pair.append(re2)
                # situation3: has None and \n in the value








            # put all the valid key-value pairs to dictionary
            for item in record_pair:
                values = item.split("|")
                i = 0
                while i < len(keys):
                    singleData[keys[i].strip("\"")] = values[i].lower().strip("\"")
                    i += 1
                ## add the single record to data dictionary, key is the unique_id of the records, and the value is all the contents
                id = int(singleData["unique_id"])
                ## transfer orderedDict to regular dictionary
                data[id] = dict(singleData)
                # print(data[id])
                writer.writerow(data[id])



# this method is to delete all the special punctuations in the value contexts, also
# make sure that each element of the dictionary will be a valid record
# return a dictionary which contains all the records in the original file
def process_line(reader,writer,data):
    all_records = {}
    id = 0
    count = 0

    for row in reader:
        singledata = {}
        count += 1
        print("new row")
        print(row)


        for (k,v) in row.items():
            record_pair = []
            singleData = {}
            # print(k)

            if k != None:
                # print(row)
                keys = k.split("|")
                values = v.split("|")

            # there are several situations that the number of keys and the number
            # of values is different, one is one record accounts for more than one cell
            # in the csv file; another is there is special punctuation marks in
            # one record , such as \n
                if len(keys) != len(values):
                    print("len(keys)", len(keys))
                    print("len(values)", len(values))

                # some records accounts for several cells in the csv file,
                # this is to extract the full contents of a single record
                    if None in row:
                        print("NONE")
                        print(row[None])
                        v += str(row[None]).strip("['").strip("']")
                        record_pair.append(v)
                        # print("v",type(v))
                        # records has None and \n at the same time
                        if "\\n" in v:
                            print("ok")
                            re1, re2 = v.split("\\n")
                            print("re1", re1)
                            print("re2", re2)
                            record_pair.append(re1)
                            record_pair.append(re2)
                            print("new values")

                    else:
                    # get the next line
                        next_record = next(reader)
                    # print("NEXT!!!!!!!",next_record)
                        for (k1,v1) in next_record.items():
                            if "\n" in v1:
                                print("has ")
                                last, current = v1.split("\n")
                                v += last
                                record_pair.append(v)
                                print("v", v)
                # if keys and values are the same length, just add the record to
                # dictionary
                else:
                    record_pair.append(v)



                for item in record_pair:
                    values = item.split("|")
                    i = 0
                    while i < len(keys):
                        singleData[keys[i].strip("\"")] = values[i].lower().strip("\"")
                        i += 1
                    ## add the single record to data dictionary, key is the unique_id of the records, and the value is all the contents
                    id = int(singleData["unique_id"])
                    ## transfer orderedDict to regular dictionary
                    data[id] = dict(singleData)
                    # print(data[id])
                    writer.writerow(data[id])

        print("end")
    print("total count", count)
    return data









def read_fibre_file(reader,writer,data):
        ## create a dictionary: data to store all the records
        # data = {}
        for row in reader:
            for (k,v) in row.items():
                # print(row)
                # print(k)
                ## create a dictionry to store the single records
                singleData = {}

                if k != None:
                ## split keys and values to a list, then match every key-value pair to a dictionary
                    keys = k.split("|")
                    values = v.split("|")

                    # if keys' and values' length is not thw same, try to add values to those empty fields (why this happenes????)
                    if len(keys) != len(values):
                        print(row)
                        print(k)
                        print(v)
                        v += str(row[None])
                        values = v.split("|")

                    # print(row[None])
                    print("len(keys)", len(keys))
                    print("len(values)", len(values))

                    i = 0
                    ## to delete all the ",,," at the end of each row, len(keys)-1
                    while i < len(keys)-1:
                        if not values[i].strip("\"").strip("-").strip():
                            values[i] = "null"
                        else:
                            if "," not in values[i]:
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
                    # print(data[id])
                    writer.writerow(data[id])

# def read_matrix_file(reader, writer, data):



## read the adjusted csv file and create a dictionary of recoreds
def readData(fileName):
    data = {}
    with open(fileName) as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
    return data

print('read file...')
n1, n2 = input_file.split(".")
# create a new file, and store the new formatted file
revise_format_file = n1 + '_csvFormat.csv'
data = preProcessFile(input_file, revise_format_file)

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
with open(output_file, 'w') as f_output, open(revise_format_file, encoding = "ISO-8859-1") as f_input:
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
