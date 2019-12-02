import csv
import codecs
import Levenshtein, distance


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
    with open(same_file,'w', newline = '\n') as output:
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
    num_of_valid_predict = 0
    correct_rate = 0
    #  read the same_record to a dictionary
    with open(fileName,'r') as file:
        print("same")
        reader = csv.DictReader(file)

        # there are two situations: two same records and multiple records
        # create a single dictionry for every similar records block
        id = 0
        for row in reader:
            all_data[id] = dict(row)
            id += 1
        print(len(all_data))

        for r1 in all_data:
            # print(111)
            index  = 0
            same_record = {}
            same_record[index] = all_data[r1]
            for r2 in all_data:
                if r1 != r2:
                    if all_data[r1]['Cluster ID'] == all_data[r2]['Cluster ID']:
                        index += 1
                        same_record[index] = all_data[r2]
            # till now, similar record blocks has been found, and every block is
            # stored in a dictionary
            # we can compare different fields now
            # return the num of records which are classified correctly
            # use string metrics and the similarity rate is more than 0.5
            num_of_valid_predict += compare_same_records(same_record)
        # calculate the ratio of records correctly classified among all records
        # which was classified as "similiar"
        # has bug!!!!!!!
        correct_rate = num_of_valid_predict/len(all_data)
        print("correct_rate", correct_rate)

# used when similiar record blocks are identified, the input is a dictionary of
# one block of same records
def compare_same_records(all_same_records):

    num_of_valid_predict = 0

    # setting up all the fields into a block
    fields = ['first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']

    # setting weightes for different fields manually
    field_weights = {
    fields[0]:0.7,
    fields[1]:0.7,
    fields[2]:0.7,
    fields[3]:0.6,
    fields[4]:0.6,
    fields[5]:0.6,
    fields[6]:0.6,
    fields[7]:0.9,
    fields[8]:0.9,
    fields[9]:0.9,
    fields[10]:0.8
    }

    total_score = 8

    # calculate the similarity between the two contents using the single feature
    # comparison method, and times the weights to get the final similarity score
    # of the two records
    lev1 = 0
    lev2 = 0
    sor1 = 0
    sor2 = 0
    jac1 = 0
    jac2 = 0
    for i in range(11):
        field = []
        for record in all_same_records:
            name = all_same_records[record][fields[i]]
            # print(name)
            if name != "" and name != "null":
                print(all_same_records[record][fields[i]])
                field.append(all_same_records[record][fields[i]])
        print("a", len(field))

        # apply the String_similarity_single_feature to the single field
        # if there are only two same records:
        if len(field) == 2:
            # use String metric to calculate the similarity between two Strings
            lev0 = Levenshtein.ratio(field[0],field[1])
            sor0 = 1 - distance.sorensen(field[0],field[1])
            jac0 = 1 - distance.jaccard(field[0],field[1])
            print("lev0", lev0)
            print("sor0", sor0)
            print("jac0", jac0)

            # let the similarity times the weight of different fields
            lev1 = lev0 * field_weights[fields[i]]
            sor1 = sor0 * field_weights[fields[i]]
            jac1 = jac0 * field_weights[fields[i]]
            print("lev1", lev1)
            print("sor1", sor1)
            print("jac1", jac1)

            # calculate the sum of the every similarity
            lev2 += lev1
            sor2 += sor1
            jac2 += jac1
            print("lev2", lev2)
            print("sor2", sor2)
            print("jac2", jac2)
        # if there are more than two same records:
        # elif len(field) > 2:

    # use the sum be divided by the total sum to get the final result
    # see sum/total as the possibility of correct
    lev_ave = lev2/8
    sor_ave = sor2/8
    jac_ave = jac2/8
    print("lev_ave", lev_ave)
    print("sor_ave", sor_ave)
    print("jac_ave", jac_ave)

    if lev_ave > 0.5 and sor_ave > 0.5 and jac_ave > 0.5:
        print("len(field)", len(all_same_records))
        num_of_valid_predict += len(all_same_records)
        # print(num_of_valid_predict)
    print("num_of_valid_predict", num_of_valid_predict)
    return num_of_valid_predict



# when a user write down these information, it is possible that the contexts
# will be different in some degree, so just regular expression may not be sufficient
# String metric analysis may be used
# maybe two methods: 1. combine different fields; 2. analyze field by field
# different matching result will get different marks or weights? How to set?


extract_same_records(input_file)
