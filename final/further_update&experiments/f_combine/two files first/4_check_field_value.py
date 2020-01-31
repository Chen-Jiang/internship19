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

            fields = ['unique_id','first_name','last_name','address_line','suburb','city','country','postcode','eaddress','domain','phone_number','origin']

            for row in reader:
                single_record = {}
                # print("row",row)
                for i in range(1,len(fields)):
                    # merge eaddress and domain to get a email field
                    if i == 8:
                        alist = []
                        dlist = []
                        emails = []
                        # eaddress
                        eaddress = row[fields[i]].strip("(").strip(")").strip(",").strip("\'")
                        if "," in eaddress:
                            alist = eaddress.split("\', \'")
                        else:
                            alist.append(eaddress)
                        # domain
                        domain = row[fields[i+1]].strip("(").strip(")").strip(",").strip("\'")
                        if "," in domain:
                            dlist = domain.split("\', \'")
                        else:
                            dlist.append(domain)

                        for p in range(len(alist)):
                            for q in range(len(dlist)):
                                emails.append(slist[p] + "@" + dlist[q])











                        email = eaddress + domain
                        single_record[header[i-1]] = email   #single_record[7] = email
                    # skip the domain to get the phone numbers
                    elif i == 9:
                        phone_number = row[fields[i+1]]
                        single_record[header[i-1]] = phone_number ##single_record[8] = email
                    # skip the phone_number
                    elif i == 10:
                        continue
                    # to transform origins from the current column to three columns
                    elif i == 11:
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
                    else:
                        single_record[header[i-1]] = row[fields[i]]
                data[index] = single_record
                print("data",data[index])
                writer.writerow(data[index])
                index += 1
        t2 = datetime.now()
        print("time needs:", t2-t1)

check_field_values(input)
