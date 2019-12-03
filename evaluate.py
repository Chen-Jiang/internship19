import csv
import codecs
import Levenshtein, distance


"""
This is to evaluate the performance of active learning algorithm
by checking if the result should be the same user

# when a user write down these information, it is possible that the contexts
# will be different in some degree, so just regular expression may not be sufficient
# String metric analysis may be used
# maybe two methods:
# 1. combine different fields;
# 2. analyze field by field, different matching result will get different marks or weights


# calculate the ratio of records pairs correctly classified out of all
# records pairs which was classified as "similiar"

"""


## files

# the input_file is the output_file from dedupe.py, changed the file name
input_file = 'result1_output.csv'
settings_file = 'csvFormat_learned_settings'
training_file = 'csvFormat_training.json'
same_file = 'same_records_from_learning.csv'
test_file = 'test.csv'


# extract all the records which are labeled "same user" and save to another csv file
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
    num_of_pairs = 0
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
        total_count = len(all_data)
        print("len(all_data)", total_count)

        # store all the same records to avoid compare twice
        # store as a dictionary so that easy to search
        same_records_id = {}

        # find all the same blocks among all the records, and compare them
        for r1 in all_data:
            if r1 not in same_records_id.keys():
                same_records_id[r1] = r1
                index  = 0
                same_record = {}
                same_record[index] = all_data[r1]
                for r2 in all_data:
                    if r1 != r2:
                        if all_data[r1]['Cluster ID'] == all_data[r2]['Cluster ID']:
                            index += 1
                            same_record[index] = all_data[r2]
                            same_records_id[r2] = r2
                if len(same_record) == 2:
                    num_of_pairs += int(1)
                else:
                    a = len(same_record)
                    num_of_pairs += int((a * (a-1))/2)
                # till now, similar record blocks has been found, and every block is stored in a dictionary, can be compared now
                # return the num of records which are classified correctly
                # (use string metrics and the similarity rate is more than 0.5)
                num_of_valid_predict += compare_same_records(same_record)
                print("num_of_valid_predict1", num_of_valid_predict)

        # calculate the ratio of records pairs correctly classified out of all
        # records pairs which was classified as "similiar"
        print("len(all_data)", total_count)
        print("total compare pairs", num_of_pairs)
        correct_rate = num_of_valid_predict/num_of_pairs
        print("correct_pair_rate", correct_rate)

# used when similiar record blocks are identified, the input is a dictionary of
# one block of same records
def compare_same_records(all_same_records):
    # setting up all the fields into a block
    fields = ['first_name','last_name','address_line','suburb','city','postcode','country','email','phone_main','phone_mobile','phone_fax']

    # setting weightes for different fields manually
    # how to revise the weights so that correct preferences during active learning learning precess?
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

    # if there are only two same records in the block:
    if len(all_same_records) == 2:
        # return 0
        return compare_two_records(all_same_records, fields, field_weights)
    # if there are more than 2 same records in the block:
    else:
        return compare_more_than_two_records(all_same_records,fields, field_weights)

# calculate the similarity between the two contents using the single feature
# comparison method, and times the weights to get the final similarity score
# of the two records
def compare_two_records(all_same_records,fields, field_weights):

    print("start comparing two.....")
    print(len(all_same_records))
    for re in all_same_records:
        print(all_same_records[re])

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
            field.append(all_same_records[record][fields[i]])

        # apply the String_similarity_single_feature to the single field
        # let the similarity times the weight of different fields
        # those with empty and "null" seen as 0 similarity
        if field[0] != "" and field[0] != "null" and field[1] != "" and field[1] != "null":
            lev1 += (Levenshtein.ratio(field[0],field[1])) * field_weights[fields[i]]
            sor1 += (1 - distance.sorensen(field[0],field[1])) * field_weights[fields[i]]
            jac1 += (1 - distance.jaccard(field[0],field[1])) * field_weights[fields[i]]

# use the sum be divided by the total sum to get the final result
# see sum/total as the possibility of correct
    lev_ave = lev1/8
    sor_ave = sor1/8
    jac_ave = jac1/8
    final_score = (lev_ave + sor_ave + jac_ave)/3
    print("final_score", final_score)

    # can try other threshold
    # use three methods and average the three results
    # if lev_ave > 0.5 and sor_ave > 0.5 and jac_ave > 0.5:
    if final_score > 0.5:
        return 1
    else:
        return 0

def compare_more_than_two_records(all_same_records,fields, field_weights):

    print("start comparing more than 2 records....")
    total = len(all_same_records)
    print(total)
    total_combinations = (total * (total-1))/2

    num_of_valid_predict = 0

    # record the number of blocks correctly classified
    num_of_correct_sub_blocks = 0

    result = []

    for i in range(total):
        for j in range(total):
            # compare ith and jth records in the block every time
            if i < j:
                lev1 = 0
                lev2 = 0
                sor1 = 0
                sor2 = 0
                jac1 = 0
                jac2 = 0
                for s in range(11):
                    field = []
                    field.append(all_same_records[i][fields[s]])
                    field.append(all_same_records[j][fields[s]])
                    # apply the String_similarity_single_feature to the single field
                    # let the similarity times the weight of different fields
                    # those with empty and "null" seen as 0 similarity
                    if field[0] != "" and field[0] != "null" and field[1] != "" and field[1] != "null":
                        lev1 += (Levenshtein.ratio(field[0],field[1])) * field_weights[fields[i]]
                        sor1 += (1 - distance.sorensen(field[0],field[1])) * field_weights[fields[i]]
                        jac1 += (1 - distance.jaccard(field[0],field[1])) * field_weights[fields[i]]

                # use the sum be divided by the total sum to get the final result
                # see sum/total as the possibility of correct
                lev_ave = lev1/8
                sor_ave = sor1/8
                jac_ave = jac1/8
                final_score = (lev_ave + sor_ave + jac_ave)/3

                result.append(final_score)

                # if lev_ave > 0.5 or sor_ave > 0.5 or jac_ave > 0.5:
                # combine the three results coming from three methods
                if final_score > 0.5:
                    num_of_correct_sub_blocks += 1
                    print("more than 0.5 small block result...")
                    print(all_same_records[i])
                    print(all_same_records[j])
                    print("final_score", final_score)
                else:
                    print("less than 0.5 small block result...")
                    print(all_same_records[i])
                    print(all_same_records[j])
                    print("final_score", final_score)
    print("num_of_correct_classified", num_of_correct_sub_blocks)
    for a in result:
        print("final_score: ", a)

    return num_of_correct_sub_blocks


extract_same_records(input_file)
