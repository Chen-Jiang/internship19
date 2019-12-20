'''
this file is used to read neighbourly_file to extract data from file and use active learning

ideas about how to extract data from matrix file (the same as reading matrix_file):
1. deal with "\n" firstly: separate records like that firstly
2. deal with has the same marks with delimiter
3. deal with the records who has less fields

'''

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
input_file = 'experian_neighbourly.csv'
output_file = 'csvFormat_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'

## according to the dedupe examples, adjust our original csv files to a standard csv format file, and write to a new csv file
## preprocess the format of data
def preProcessFile(fileName, revise_format_file):

    # read the original file, change the format and write to the new file
    with open(revise_format_file,'a') as file:
        data = {}

        original_fieldnames = ['unique_id','first_name','last_name','address_line','suburb_name','city','postcode','email','phone_home','phone_mobile']
        original_fieldnames_len = len(original_fieldnames)
        ## set new csv file's headers (all the headers from the original files)
        fieldnames = ['unique_id','first_name','last_name','address_line','suburb_name','city','postcode','email','phone_number']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
        with open(fileName, encoding = "ISO-8859-1") as f:
            reader = csv.DictReader(f, delimiter=",", lineterminator=",")
            # all_records = {}
            data = read_neighbourly_file(reader,writer,data,fieldnames,original_fieldnames_len)

        print("writing completed")
        assess_data.assess_columns_using_dataframe_and_reg(file,fieldnames)
        file.close()
        return data

def read_neighbourly_file(reader,writer,data,fieldnames,original_fieldnames_len):
    keys = fieldnames
    k_len = original_fieldnames_len  #10
    count = 0

    # read line by line
    for row in reader:
        # print("row", row)
        singleData = {}
        records = []
        values = []
        vs = ""

        # step1: extract records contents
        # get all the values of this record and make sure the format of the values
        # is the same, like: |"xxxxxx"|"XXXXXX"|"xxxxxXXXXX"|
        for (k,v) in row.items():
            # add the values to a string vs
            if isinstance(v,str):
                vs += v

            if isinstance(v,list):
                for i in range(len(v)):
                    if v[i].startswith("|") and "\n" not in v[i]:
                        vs += "\"" + v[i][0] + "\"" + v[i][1:]
                    else:
                        vs += v[i]

        # step2: process different format of records tofind all the valid field values then write to records array
        # first deal with records with \n, like this situation:
        # 3323622|"PHILIP & GLENDA"|"MCDONNELL & STEWART"|"30 MILLSTREAM DRIVE"|"NORTHWOOD"|"CHRISTCHURCH 8051"|"8051"|"NEW ZEALAND"|
        # |"GLENDASTEWART25@HOTMAIL.CO|||\n3323623"|"KEVIN"|"HENRY"|"268 MARSDEN ROAD"||"GREYMOUTH 7805"|"7805"|"NEW ZEALAND"|||||
        # if there is \n in the records, separate them firstly
        if "\n" in vs:
            print("has \\n:",vs)
            first_record, second_record = vs.split("\n")
            print("first_record",first_record)
            print("second_record",second_record)
            records.append(first_record.split("|"))
            records.append(second_record.split("|"))
        # another type: do not have \n in the record
        else:
            values = vs.split("|")
            # if there is such extra | situation in the record
            if len(values) > k_len:
                # find any records who has extra "|" in the field contents
                # like this format: |"|XXXXX|XXXXX|"|, which will affect the result
                # separated by "|"
                f2 = re.finditer("(\|){1}\"[^\"]*\|[^\"]*?\"",vs)
                # replace all the extra | to other contents; then split the records according to |;
                # after splitting, replace the replaced contents to | again
                for item in f2:
                    print("item",item.group(0))    # |"gillandbarry|@xnet.co.nz"
                    # remove the normal |, so only extra | is remained
                    item_new = item.group(0).strip("|")      # "gillandbarry|@xnet.co.nz"
                    # replace | to (this is a replacement)
                    item_new = re.sub("\|","(this is a replacement)",item_new)  # "gillandbarry(this is a replacement)@xnet.co.nz"
                    # replace "gillandbarry|@xnet.co.nz" to "gillandbarry(this is a replacement)@xnet.co.nz"
                    # and update vs
                    vs = vs.replace(item.group(0).strip("|"),item_new)
                print("new vs:", vs)
                # split vs according to "|", after aplitting, replace back
                values = vs.split("|")
                for i in range(len(values)):
                    if "(this is a replacement)" in values[i]:
                        values[i] = values[i].replace("(this is a replacement)", "|")

            # revise all the format of the element in the value array
            for i in range(len(values)):
                values[i] = values[i].lower().strip("\"")


            v_len = len(values)
            # all the values are extracted, add this record to records array
            # this is record is DONE!!!
            if v_len == k_len:
                records.append(values)
            else:
                if v_len > k_len:
                    print("Still more than",row)

                elif v_len < k_len:
                    print("values", values)
                    # if values' length is less than keys' length, we extract the next record
                    # to see if there is any remaining part of the last record
                    # then, the next row will be skipped in the loop
                    next_record = next(reader)
                    print("next record::", next_record)
                    current = ""
                    for (k1,v1) in next_record.items():

                        # values can be a String, like this format:
                        # 'unique_id|"first_name"|"last_name"|"address_line"|"suburb"|"city"|"postcode"|"country"|"dob"|"email"|"phone_1"|"phone_2"|"phone_3"',
                        # '|||\n3381810"||"FAWCETT"|"14 ARATAKI ROAD"||"HAVELOCK NORTH 4130"|"4130"|"NEW ZEALAND"|||||'
                        if isinstance(v1, str):

                            if "\n" in v1:
                                # last is the last one's remaining part
                                # current is the next record's contents
                                last, current = v1.split("\n")
                                print("last:",last)
                                print("current", current)
                                vs += last
                                last_fields = vs.split("|")
                                print("last_fields", last_fields)
                                # add the next_record's contents to the former values array
                                # add the two records to the special records
                                records.append(last_fields)
                        # when key = None, the value is a list
                        if isinstance(v1, list):
                            print("enter")
                            for ele in v1:
                                current += ele
                            print("current123",current)

                    # when finishes loop, add current record to records
                    current_field = current.split("|")
                    records.append(current_field)

        # step3: get element from records array and write to new file
        # if the row is valid without any processing, the len(records) = 1;
        # other situations like combvine two records in a single row, the len(records) = 2
        for element in records:
            i = 0
            while i < k_len:  # i<10
                if i == k_len-2:     # i = 8,phone_home field
                    phone_number = []
                    j = i
                    while j < k_len:
                        while "+64" in element[j] or "-" in element[j] or "(" in element[j] or ")" in element[j] or " " in element[j]:
                            element[j] = element[j].replace("+64","")
                            element[j] = element[j].replace("-","")
                            element[j] = element[j].replace("(","")
                            element[j] = element[j].replace(")","")
                            element[j] = element[j].replace(" ","")
                        if element[j]:
                            # only store different phone numbers
                            if element[j] not in phone_number:
                                phone_number.append(element[j])
                        j += 1
                    if len(phone_number) > 0:
                        singleData[keys[i].strip("\"")] = tuple(i for i in phone_number)
                    else:
                        singleData[keys[i].strip("\"")] = "null"
                    break


                else:
                    if not element[i].strip("\"").strip():
                        singleData[keys[i].strip("\"")] = "null"
                    else:
                        singleData[keys[i].strip("\"")] = element[i].lower().strip("\"")
                    i += 1

            ## add the single record to data dictionary, key is the unique_id of the records, and the value is all the contents
            id = int(singleData["unique_id"].strip("\""))
            ## transfer orderedDict to regular dictionary
            data[id] = dict(singleData)
            # print(data[id])
            writer.writerow(data[id])
            count += 1
    print(count)
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
        {'field':'suburb_name','type': 'String','has missing' : True},
        {'field':'city','type': 'String','has missing' : True},
        {'field':'postcode','type': 'Exact','has missing' : True},
        {'field':'email','type': 'String','has missing' : True},
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
with open(output_file, 'w') as f_output, open(revise_format_file, encoding = "ISO-8859-1") as f_input:
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
