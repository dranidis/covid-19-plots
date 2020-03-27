# call with
#
# python3.5 read.py --c Spain Italy Germany Greece UK --f ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv
#

import sys
import csv
import argparse
import matplotlib.pyplot as plt


countryReported = dict()
casesReported = dict()
deathsReported = dict()
population = dict()

xValues = []
yValues = dict()

xTicks = []
greece = []
population['Greece'] = 11
population['Italy'] = 61
population['UK'] = 66
population['Germany'] = 83
population['Spain'] = 46

def printCountry(country):

    if countryReported[country]:
        yValues[country].append( int(casesReported[country]) / population[country])
    else:
        yValues[country].append(0)

    if countryReported[country]:
    #     print(f'{country},{casesReported[country]},{deathsReported[country]}',
    #           end=",")
    # else:
    #     print(f'{country},,,', end="")

        print('{country},{casesReported},{deathsReported}'.format(country=country, casesReported=casesReported[country],deathsReported=deathsReported[country]), end=",")
    else:
        print('{country},,,'.format(country=country), end="")





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


for country in countries:
    yValues[country] = []



xValue = 0
#print(sys.argv)
for filename in files:
    date = filename[-14:-9] # keep only the MM-DD from the file name
    xValues.append(xValue)
    xTicks.append(date)
    xValue += 1

    print('{date}'.format(date=date), end=",")
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
    print(greece)

# plt.plot([73,73,89,99,99,190,228,331,387,418,418,495,530,624,695,743,821,892])

plt.xlabel('Date')
plt.ylabel('Reported cases per mil')
plt.title('Title')
plt.xticks(xValues, xTicks)
plt.plot(xValues, yValues['Greece'], 'r--')
plt.plot(xValues, yValues['UK'], 'g--')
plt.plot(xValues, yValues['Germany'], 'b--')
plt.plot(xValues, yValues['Italy'], 'g^')
plt.plot(xValues, yValues['Spain'], 'b^')
plt.show()    



