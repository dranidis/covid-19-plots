# call with
#
# python3.7 read.py --c Spain Italy Germany Greece UK --f ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv
#

import sys
import csv
import argparse

def printCountry(country):
    if countryReported[country]:
        print(f'{country},{casesReported[country]},{deathsReported[country]}',
              end=",")
    else:
        print(f'{country},,,', end="")





CLI = argparse.ArgumentParser()
CLI.add_argument("--c",
                 nargs="*",
                 type=str,
                 default=['Italy', 'Spain', 'Greece'])
CLI.add_argument("--f", nargs="*", type=str, default=[])
args = CLI.parse_args()

countries = args.c
countries.sort()

# print(countries)
files = args.f
# print(files)

countryReported = dict()
casesReported = dict()
deathsReported = dict()

#print(sys.argv)
for filename in files:
    date = filename[-14:-9] # keep only the MM-DD from the file name
    print(f'{date}', end=",")
    with open(filename) as csvfile:
        for country in countries:
            # print(c)
            countryReported[country] = False

        # print(countryReported)

        spamreader = csv.reader(csvfile)

        header = True
        for row in spamreader:
            if header:
                # print(row)
                colindex = 0
                for col in row:
                    # if col in ['Last_Update', 'Last Update']:
                    #     dateIndex = colindex
                    if "Country" in col:
                        countryIndex = colindex
                    if "Province" in col:
                        provinceIndex = colindex
                    if "Confirmed" in col:
                        confirmedIndex = colindex
                    if "Deaths" in col:
                        deathsIndex = colindex

                    colindex += 1
                header = False
                continue
            # print(row)

            # handle strange case of UK
            if row[provinceIndex] == 'United Kingdom':
                row[provinceIndex] = 'UK'

            if row[countryIndex] == 'United Kingdom':
                row[countryIndex] = 'UK'

            if row[provinceIndex] == '':
                country = row[countryIndex]
            else:
                country = row[provinceIndex]

            if country in countries:
                countryReported[country] = True
                casesReported[country] = row[confirmedIndex]
                deathsReported[country] = row[deathsIndex]

            # rowindex += 1

        for country in countries:
            printCountry(country)

    print()


