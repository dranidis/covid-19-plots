# call with
#
# python3.5 read.py --c Spain Italy Germany Greece UK --f ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv
#

import sys
import csv
import argparse
import matplotlib.pyplot as plt

label = ['Cases per mil', 'Deaths per mil', 'Recovered per mil']
maxDim = len(label)


def printCountry(country):
    if countryReported[country]:
        print('{country},{casesReported},{deathsReported},{recoveredReported}'.format(country=country,
            casesReported=casesReported[country], deathsReported=deathsReported[country], recoveredReported=recoveredReported[country]), end = ",")
    else:
        print('{country},,,,'.format(country=country), end = "")


def processCountry(country):
    if countryReported[country]:
        yValue=[casesReported[country],
            deathsReported[country], recoveredReported[country]]

    for i in range(maxDim):
        if countryReported[country]:
            if yValue[i] != '':
                yValues[i][country].append(
                    int(yValue[i]) / population[country])
            else:
                # use previous value
                lastValue=yValues[i][country][-1]
                yValues[i][country].append(lastValue)
        else:
            yValues[i][country].append(0)


def plotGraph(daysBefore):

    for i in range(maxDim):
        plt.subplot(maxDim, 1, i+1)

        plt.xlabel('Date')
        plt.ylabel(label[i])

        # plt.title('Title')
        plt.xticks(xValues, xTicks, rotation = 'vertical')

        maxX=len(xValues)
        if daysBefore != 0:
            # daysBefore = len(xValues)
            minX=maxX - daysBefore  # 30 days before
            plt.xlim([minX, maxX])
        if maxY != 0:
            plt.ylim([0, maxY])

        for country in countries:
            plt.plot(xValues, yValues[i][country], 'o-')

    plt.legend(countries, loc = 'upper left')
    plt.show()

#
# PROGRAM
#
CLI=argparse.ArgumentParser()
CLI.add_argument("--c",
                 nargs = "*",
                 type = str,
                 default = ['Italy', 'Spain', 'Greece'])
CLI.add_argument("--f", nargs = "*", type=str, default=[])
CLI.add_argument("--days", nargs = "?", type=int, default=0)
CLI.add_argument("--maxY", nargs = "?", type=int, default=0)
args= CLI.parse_args()

countries= args.c
countries.sort()

daysBefore= int(args.days)
print(daysBefore)
maxY= args.maxY

# print(countries)
files= args.f
# print(files)

#
# Initialize countries
#
countryReported= dict()
casesReported= dict()
deathsReported= dict()
recoveredReported= dict()
population= dict()
population['Greece']= 11
population['Italy']= 61
population['UK']= 66
population['Germany']= 83
population['Spain']= 46
population['Turkey']= 80
population['France']= 67
population['Sweden']= 10
population['Netherlands']= 17
population['Austria']= 9
population['Belgium']= 11
population['Portugal']= 11


#
# for plotting
#
xValues= []
yValues= [dict(), dict(), dict()]
for i in range(maxDim):
    # yValues[i] = dict()
    for country in countries:
        yValues[i][country]= []

xTicks= []


xValue= 0
# print(sys.argv)
for filename in files:
    date= filename[-14:-9]  # keep only the MM-DD from the file name
    xValues.append(xValue)
    xTicks.append(date)
    xValue += 1

    print('{date}'.format(date=date), end = ",")
    with open(filename) as csvfile:
        for country in countries:
            # print(c)
            countryReported[country]= False

        # print(countryReported)

        spamreader= csv.reader(csvfile)

        header= True
        for row in spamreader:
            if header:
                # print(row)
                colindex= 0
                for col in row:
                    # if col in ['Last_Update', 'Last Update']:
                    #     dateIndex = colindex
                    if "Country" in col:
                        countryIndex= colindex
                    if "Province" in col:
                        provinceIndex= colindex
                    if "Confirmed" in col:
                        confirmedIndex= colindex
                    if "Deaths" in col:
                        deathsIndex= colindex
                    if "Recovered" in col:
                        recoveredIndex= colindex

                    colindex += 1
                header= False
                continue
            # print(row)

            # handle strange case of UK
            if row[provinceIndex] == 'United Kingdom':
                row[provinceIndex]= 'UK'

            if row[countryIndex] == 'United Kingdom':
                row[countryIndex]= 'UK'

            if row[provinceIndex] == '':
                country= row[countryIndex]
            else:
                country= row[provinceIndex]

            if country in countries:
                countryReported[country]= True
                casesReported[country]= row[confirmedIndex]
                deathsReported[country]= row[deathsIndex]
                recoveredReported[country]= row[recoveredIndex]

            # rowindex += 1

        for country in countries:
            printCountry(country)
            processCountry(country)

    print()  # end the csv

plotGraph(daysBefore)
