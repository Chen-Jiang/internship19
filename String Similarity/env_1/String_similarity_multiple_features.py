import codecs, difflib, Levenshtein, distance
import csv

"""
try multiple fretures to see how these strings will be classified
features: address and city and country
"""

# files
test_file = "t1.csv"


with open(test_file,'r') as file:
    reader = csv.reader(file, delimiter = "\n")
    next(reader,None)
    id = 0
    city = {}
    country = {}

    # read the csv file and put all the records to the two different lists
    # then read the two list to do string similariy analysis
    for row in reader:
        arr = row[0].lower().split(',')
        add_city = arr[0] + " " + arr[1]
        add_country = add_city + " " + arr[2]
        city[id] = add_city
        country[id] = add_country
        id += 1
        # print(city[0])
        # print(city[0])


    for i in range(len(city)):
        print(i)
        for j in range(len(city)):
            if i != j:
                print(city[i] + " VS " + city[j])
                diff1 = difflib.SequenceMatcher(city[i],city[j]).ratio()
                lev1 = Levenshtein.ratio(city[i],city[j])
                sor1 = 1 - distance.sorensen(city[i],city[j])
                jac1 = 1 - distance.jaccard(city[i],city[j])

                print("combine city info: ")
                print("diff",diff1)
                print("lev",lev1)
                print("sor",sor1)
                print("jac",jac1)

    for i in range(len(country)):
        for j in range(len(country)):
            if i != j:
                print(country[i]," VS ", country[j])
                diff1 = difflib.SequenceMatcher(country[i],country[j]).ratio()
                lev1 = Levenshtein.ratio(country[i],country[j])
                sor1 = 1 - distance.sorensen(country[i],country[j])
                jac1 = 1 - distance.jaccard(country[i],country[j])

                print("combine country info: ")
                print("diff",diff1)
                print("lev",lev1)
                print("sor",sor1)
                print("jac",jac1)
