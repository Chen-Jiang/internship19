'''

After getting the final dudepe result of the three files, check the field values:
complete the emails and the origins transform into three columns

The input is final_combined_result.csv
The output is revised_final_combined_result.csv

'''

import csv
from datetime import datetime

input = "final_combined_result.csv"
output_file = "revised_final_combined_result.csv"

def check_field_values(file):

    data = {}
    index = 0

    with open(output_file, 'a') as output:

        t1 = datetime.now()
        print("start time:", t1)

        header = ['first_name','last_name','address_line','suburb','city','country','postcode','email','phone_number','in_fibre','in_neighbourly','in_matrix_home']
        writer = csv.DictWriter(output, fieldnames=header, extrasaction='ignore')
        writer.writeheader()

        with open(file, encoding = 'ISO-8859-1') as input:
            reader = csv.DictReader(input, delimiter=",", lineterminator=",")

            fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','email','eaddress','domain','phone_number','origin']

            for row in reader:
                single_record = {}
                # print("row",row)
                for i in range(1,len(fields)):   #[1,12]

                    if i <= 8:
                        single_record[header[i-1]] = row[fields[i]]
                    elif i == 9 or i == 10:
                        continue
                    elif i == 11:
                        single_record[header[i-3]] = row[fields[i]]
                    elif i == 12:
                        list = []  # to contain the origin values
                        origins = row[fields[i]]   #get a String ('fibre',) or ('fibre','matrix_homesub')
                        origins = origins.strip("(").strip(")").strip(",").strip("\'")   #fibre or  fibre', 'matrix_homesub
                        if "," in origins:
                            list = origins.split("\', \'")   # [fibre,matrix_homesub]
                        else:
                            list.append(origins)

                        # 9: in_fibre; 10:in_neighbourly; 11:in_matrix_home
                        origin_dict = {}
                        origin_dict['fibre'] = 9
                        origin_dict['neighbourly'] = 10
                        origin_dict['matrix_homesub'] = 11

                        for n in range(len(list)):
                            ele = list[n]
                            if ele in origin_dict:
                                single_record[header[origin_dict[ele]]] = "Yes"

                data[index] = single_record
                # print("data",data[index])
                writer.writerow(data[index])
                index += 1
        t2 = datetime.now()
        print("time needs:", t2-t1)

check_field_values(input)
