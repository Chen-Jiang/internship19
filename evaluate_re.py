import re

'''
try to use different check method: using regular expression to calculate the
similarity between different fields in different records
There is a difficult part: how to represent the different similarity according to
different regular expression result?
'''

# using regular expression to compare blocks with only two records
def compare_two_records_with_re(all_same_records,fields,field_weights):

    print("start comparing with regular expression...")

    compare_score = 0
    num_of_correctly_classified_pair = 0

    # loop all the fields
    for i in range(11):
        field = []
        for j in all_same_records:
            if i == 7:
                if "@" in all_same_records[j][fields[i]]:
                    # to avoid different email domains
                    email_name, domain = all_same_records[j][fields[i]].split("@")
                    print("email_name", email_name)
                    field.append(email_name)
                else:
                    field.append(all_same_records[j][fields[i]])
            else:
                field.append(all_same_records[j][fields[i]])

        # find the shorter text
        smaller = min(len(field[0]),len(field[1]))
        if len(field[0]) == smaller:
            a = 0
            b = 1
        elif len(field[1]) == smaller:
            a = 1
            b = 0

        # when comparing, both the text needs to be NOT empty and NOT null
        # if is empty  or null, do not contribute to the final_score
        if field[a] != "" and field[a] != "null" and field[b] != "" and field[b] != "null":
            # let the shorter text to fit longer text
            # first try match mathod and if the short one suits the longer one,
            match_result = re.match(re.escape(field[a]),field[b])
            if match_result:
                # if the contexts in this field suits totally, then has full score
                match_score = 1
                compare_score += match_score * field_weights[fields[i]]
                # print("part compare_score", compare_score)

            # when the two texts do not fit, try search method, if can be found,
            # give some marks according to the degree of fitness
            else:
                search_result = re.search(re.escape(field[a]),field[b])
                if search_result:
                    # use the ration of occurrence of one word to another word as the score
                    search_score = (float(len(field[a])/len(field[b]))) * field_weights[fields[i]]
                    compare_score += search_score
                    # print("part compare_score", compare_score)

    compare_score /= 6.9
    # print("compare_score", compare_score)

    if compare_score > 0.5:
        num_of_correctly_classified_pair = 1
    else:
        num_of_correctly_classified_pair = 0
        print("less than 0.5", compare_score)
        print(all_same_records[0])
        print(all_same_records[1])
        print()


    return num_of_correctly_classified_pair


# using regular expression to compare blocks with more than two records
def compare_more_than_two_records_with_re(all_same_records,fields,field_weights):

    print("start comparing more than two records with regular expression...")

    compare_score = 0
    num_of_correctly_classified_pair = 0

    for i in range(len(all_same_records)):
        for j in range(len(all_same_records)):
            if i != j:
                for m in range(11):
                    field = []
                    if m == 7:
                        print(all_same_records[i][fields[m]])
                        print(all_same_records[j][fields[m]])
                        if "@" in all_same_records[i][fields[m]] and "@" in all_same_records[j][fields[m]]:
                            print(1)
                            email_name_i, domain_i = all_same_records[i][fields[m]].split("@")
                            email_name_j, domain_j = all_same_records[j][fields[m]].split("@")
                            field.append(email_name_i)
                            field.append(email_name_j)
                            print(email_name_i)
                            print(email_name_j)
                        else:
                            field.append(all_same_records[i][fields[m]])
                            field.append(all_same_records[j][fields[m]])
                        print("email",field[0])
                        print("email",field[1])
                    else:
                        field.append(all_same_records[i][fields[m]])
                        field.append(all_same_records[j][fields[m]])

                    print("len(field[0]",field[0])
                    print("len(field[1]",field[1])
                    # find the shorter text
                    smaller = min(len(field[0]),len(field[1]))
                    if len(field[0]) == smaller:
                        a = 0
                        b = 1
                    elif len(field[1]) == smaller:
                        a = 1
                        b = 0
                        # when comparing, both the text needs to be NOT empty and NOT null
                        # if is empty  or null, do not contribute to the final_score
                    if field[a] != "" and field[a] != "null" and field[b] != "" and field[b] != "null":
                        # try match method firstly
                        match_result = re.match(re.escape(field[a]), field[b])
                        # if match_result exists, then score is 1
                        if match_result:
                            match_score = 1 * field_weights[fields[m]]
                            compare_score += match_score
                        # if match_result does not exist, then try search method to figure
                        # out the similarity
                        else:
                            search_result = re.search(re.escape(field[a]),field[b])
                            if search_result:
                                search_score = (float(len(field[a])/len(field[b]))) * field_weights[fields[m]]
                                compare_score += search_score
                # calculate the average score of the comparing
                compare_score /= 6.9

                if compare_score > 0.5:
                    num_of_correctly_classified_pair += 1
                else:
                    print("less than 0.5", compare_score)
                    print(all_same_records[i])
                    print(all_same_records[j])
                    print()

    return num_of_correctly_classified_pair
