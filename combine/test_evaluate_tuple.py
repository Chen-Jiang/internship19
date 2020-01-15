'''

This is to evaluate the performance of dedupe_join_files
the major difference between this evaluation and others lies that almost all the fields' type are Set

input is combined_output.csv
output will be the accurate rate from this training shown on the terminal

'''

import Levenshtein, distance

def set_up_instances():

    # set up test cases
    dict1 = {}
    dict2 = {}
    dict3 = {}
    phone1 = []
    phone2 = []
    phone3 = []

    m1 = "12345"
    m2 = "98761"
    m3 = "60952"

    phone1.append(m1)
    phone2.append(m2)
    phone2.append(m3)
    phone3.append(m2)

    dict1['phone'] = tuple(i for i in phone1)
    dict2['phone'] = tuple(i for i in phone2)
    dict3['phone'] = tuple(i for i in phone3)

    score_12 = compare_set(dict1, dict2)
    score_23 = compare_set(dict2, dict3)


def compare_set(d1, d2):

    lev = 0
    sor = 0
    jac = 0

    score = 0
    need_break = True

    # v1 & v2 is tuple, and the elements of v1, v2 is String, which is decided by m1, m2, m3
    v1 = d1['phone']
    v2 = d2['phone']

    print(v1, v2)

    for i in range(len(v1)):  #2
        if need_break:
            for j in range(len(v2)):   #1
                lev += Levenshtein.ratio(v1[i],v2[j])
                sor += 1 - distance.sorensen(v1[i],v2[j])
                jac += 1 - distance.jaccard(v1[i],v2[j])

                aver = (lev+sor+jac)/3

                if aver == 1:
                    score = aver
                    need_break = False
                    break

                if aver < 1 and aver > score:
                    score = aver
        else:
            break

    print("final score:", score)


set_up_instances()
