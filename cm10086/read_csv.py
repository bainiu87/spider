# -*- coding: utf-8 -*-
import csv
csvfile = file('data.csv', 'rb')
reader = csv.reader(csvfile)
a=0
for line in reader:
    a+=1
    print a

csvfile.close()
