## this is to use dedupe to analyse data

from collections import defaultdict
from future.builtins import next

import os
import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode

## files
input_file = 'copy.csv'
output_file = 'copy_output.csv'
settings_file = 'copy_learned_settings'
training_file = 'copy_training.json'

## according to the dedupe examples, adjust our original csv files to a standard csv format file, and write to a new csv file
## preprocess the format of data
def preProcessFile(fileName):
    with open('csvFormat.csv','a', newline='') as file:
        ## set new csv file's headers (all the headers from the original files)
        fieldnames = ['unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        ## read original csv file, and read every row to a dictionary then write every dictionary to the new csv file
        with open(fileName, newline='') as file:
            reader = csv.DictReader(file, delimiter="\n")
            for row in reader:
                for (k,v) in row.items():
                    data = {}
                    ## split keys and values to a list, then match every key-value pair to a dictionary
                    keys = k.split("|")
                    values = v.split("|")
                    ## to delete all the ",,," at the end of each row
                    i = 0
                    while i < len(keys)-1:
                        if "," not in values[i]:
                            ## delete all the "" of the words
                            data[keys[i].strip("\"")] = values[i].strip("\"")
                            i += 1
                        ## some contents are written in a single cell
                        ## separate different contents
                        else:
                            contents = values[i].split(",")
                            for j in range(len(contents)):
                                ## delete all the "" of the words
                                data[keys[i].strip("\"")] = contents[j].strip("\"")
                                i = i + 1
                    writer.writerow(data)

        print("writing completed")
        file.close()
        readData('csvFormat.csv')

## read the adjusted csv file and create a dictionary of recoreds
def readData(fileName):
    data = {}
    with open(fileName) as file:
        reader = csv.DictReader(file)
        for row in reader:
            #print(row)
    return data

print('read file...')
#readFile(input_file)
preProcessFile(input_file)
