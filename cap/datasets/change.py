import csv
import random
lists = ['Q1','Q2','Q3','Q4']
i = 0
with open ('storage_clean.csv') as csv_file:
    csv_reader = csv.reader(csv_file, dialect='excel')

    with open('storage_clean_new.csv','w') as new_file:
        csv_writer = csv.writer(new_file, dialect='excel')

        for line in csv_reader:
            if i == 0:
                line.append("LAUNCHED")
                i+=1
            else:
                val = random.choice(lists) +' '+ str(random.randint(2000,2015))
                line.append(val.strip())
                print(line)
            csv_writer.writerow(line)