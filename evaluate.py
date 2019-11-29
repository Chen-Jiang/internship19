import csv

"""
This is to evaluate the performance of active learning algorithm
by checking if the result should be the same user
"""


## files
# input_file = 'experian_fibre.csv'
# input_file = 'copy.csv'
input_file = 'result1_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'
same_file = 'same_records_from_learning.csv'
test_file = 'test.csv'


# extract all the records which are labeled "same user" and save to another file
def extract_same_records(fileName):
    with open(same_file,'a', newline = '\n') as output:
        fieldnames = ['Cluster ID','confidence_score','unique_id','first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        data = {}

        with open(fileName,'r') as file:
            # if add "delimeter" within the DictReader, row['first_name'] can not be read
            reader = csv.DictReader(file)

            for row in reader:
                score = row['confidence_score']
                # all therecords' confidence_score is a string, no matter has contents or not
                # if score exists
                if score:
                    id = row['unique_id']
                    data[id] = dict(row)
                    writer.writerow(data[id])

    gather_same_records(same_file)


# choose fields which can be compared
# first_name, last_name, address_line, city, postcode, country, email, phone_main, phone_mobile
def gather_same_records(fileName):

    all_data = {}
    exist_id = []
    #  read the same_record to a dictionary
    with open(fileName,'r') as file:
        print("same")
        reader = csv.DictReader(file)
        # there are two situations: two same records and multiple records
        # create a single dictionry for every same records block
        same_record = {}
        for row in reader:
            all_data[row['unique_id']] = dict(row)

            # if not id in exist_id:
            #     exist_id.append(id)
            #     same_record = dict(row)
            # else:
        print(len(all_data))

    




# def compare_same_records():




# when a user write down these information, it is possible that the contexts
# will be different in some degree, so just regular expression may not be sufficient
# String metric analysis may be used
# maybe two methods: 1. combine different fields; 2. analyze field by field
# different matching result will get different marks or weights? How to set?


extract_same_records(input_file)
