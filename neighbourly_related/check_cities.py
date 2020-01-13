import csv

input = "experian_neighbourly_csvFormat.csv"

def check_city(input):

    fieldnames = ['unique_id','first_name','last_name','address_line','suburb_name','city','postcode','email','phone_number']
    city_list = {}

    with open(input, encoding = "ISO-8859-1") as f:

        reader = csv.DictReader(f, delimiter=",", lineterminator=",")

        for row in reader:
            if row['city'] not in city_list:
                city_list[row['city']] = 1
            else:
                city_list[row['city']] += 1

        for (k,v) in city_list:
            print(k,v)

check_city(input)
