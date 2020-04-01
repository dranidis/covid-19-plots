import sys
import csv
import argparse
import code
import numpy as np


import plots
import countries as c

def processCountry(country):
    cases = 0
    deaths = 0
    recovered = 0
    activeCases = 0

    if countryReported[country]:
        cases = casesReported[country]
        deaths = deathsReported[country]
        recovered = recoveredReported[country]
        if deaths > 0 or recovered > 0:
            activeCases = cases - deaths - recovered

    yValue = [cases, deaths, recovered, activeCases]

    for i in range(c.maxDim):
        if yValue[i] != 0:
            c.yValues[i][country].append(yValue[i])
        elif len(c.yValues[i][country]) > 0:
            # use previous value
            lastValue = c.yValues[i][country][-1]
            c.yValues[i][country].append(lastValue)
        else:
            c.yValues[i][country].append(0)



def readFiles():
    xValue = 0
    for filename in files:
        date = filename[-14:-9]  # keep only the MM-DD from the file name
        plots.xValues.append(xValue)
        plots.xTicks.append(date)
        xValue += 1

        with open(filename) as csvfile:
            for country in c.countries:
                countryReported[country] = False

            spamreader = csv.reader(csvfile)

            header = True
            for row in spamreader:
                if header:
                    colindex = 0
                    for col in row:
                        # if col in ['Last_Update', 'Last Update']:
                        #     dateIndex = colindex
                        if 'Country' in col:
                            countryIndex = colindex
                        if 'Province' in col:
                            provinceIndex = colindex
                        if 'Confirmed' in col:
                            confirmedIndex = colindex
                        if 'Deaths' in col:
                            deathsIndex = colindex
                        if 'Recovered' in col:
                            recoveredIndex = colindex

                        colindex += 1
                    header = False
                    continue

                if row[countryIndex] == 'Mainland China':
                    row[countryIndex] = 'China'

                # handle strange case of UK
                if row[provinceIndex] == 'United Kingdom':
                    row[provinceIndex] = 'UK'

                if row[countryIndex] == 'United Kingdom':
                    row[countryIndex] = 'UK'

                if row[provinceIndex] == '' or 'China' in row[countryIndex] or 'US' == row[countryIndex]:
                    country = row[countryIndex]
                else:
                    country = row[provinceIndex]

                if country in c.countries:
                    processRow(country, row[confirmedIndex],
                               row[deathsIndex], row[recoveredIndex])

            for country in c.countries:
                processCountry(country)


def processRow(country, cases, deaths, recovered):
    c = 0
    d = 0
    r = 0
    if len(cases) > 0 and int(cases) > 0:
        c = int(cases)
    if len(deaths) > 0 and int(deaths) > 0:
        d = int(deaths)
    if len(recovered) > 0 and int(recovered) > 0:
        r = int(recovered)

    if countryReported[country]:
        # already processed once in this file
        casesReported[country] += c
        deathsReported[country] += d
        recoveredReported[country] += r
    else:
        casesReported[country] = c
        deathsReported[country] = d
        recoveredReported[country] = r

    countryReported[country] = True


def generateCSV():
    index = 0
    for date in plots.xTicks:
        print(date, end=',')
        for country in c.countries:
            print(country, end=',')
            for i in range(c.maxDim):
                print(c.yValues[i][country][index], end=',')
        print()
        index += 1


def checkData():
    print("Fixing inconsistent data for cases and deaths")
    for i in range(c.maxDim-1):  # last dim is active (calculated)
        print('\t--------------------------------------')
        print("\tChecking ", i)
        print('\t--------------------------------------')
        for country in c.countries:
            previous = 0
            index = 0
            for date in plots.xTicks:
                current = int(c.yValues[i][country][index])
                if current < previous:
                    print('\t', date, country, i, previous, current, end='')
                    if i == 0 and country == 'Japan' and date == '01-23':
                        print('\t===> Correcting value to 2')
                        c.yValues[i][country][index] = 2
                    if i == 0 and country == 'Japan' and date == '02-07':
                        print('\t===> Correcting previous value to 25')
                        c.yValues[i][country][index-1] = 25
                    if i == 0 and country == 'Japan' and date == '03-16':
                        print('\t===> Correcting value to 839')
                        c.yValues[i][country][index] = 839
                    if i == 1 and country == 'Japan' and date == '03-10':
                        print('\t===> Correcting previous value to 10')
                        c.yValues[i][country][index-1] = 10
                previous = current
                index += 1


#
# PROGRAM
#



#
# CLI arguments
#
CLI = argparse.ArgumentParser(description='Plot graphs for the COVID-19')
CLI.add_argument('-c', '--country',
                 nargs='*',
                 type=str,
                 default=c.allCountries,
                 help='countries to present in plots')
CLI.add_argument('files', nargs='+', type=str,
                 help='csv files to read from')
CLI.add_argument('-d', '--days', nargs='?', type=int, default=0,
                 help='number of days to plot before today. By default plots start from the beginning of data collection.')
CLI.add_argument('--maxY', nargs=4, type=int, default=[0, 0, 0, 0],
                 help='y axes limits for time plots')
CLI.add_argument('-l', '--logY', action='store_true',
                 help='use log scale for the Y axes of time plots')
CLI.add_argument('-i', '--interactive', action='store_true',
                 help='open interactive python console after parsing the files')
CLI.add_argument('--csv', action='store_true', help='generate CSV output')
CLI.add_argument('-p', '--plot', action='store_true',
                 help='time plots of cases/deaths/recoveries/active. Choose plots to skip with the --skip flag')
CLI.add_argument('-a', '--animate', action='store_true',
                 help='animate new numbers/total numbers. Choose which numbers to plot with the --number flag')
CLI.add_argument('-n', '--number', nargs='?', type=int, default=1,
                 help='number to animate 0:cases, 1:deaths, 2:recovered, 3:active')
CLI.add_argument('-m', '--million', action='store_true',
                 help='in plots divide values by country population in millions')
CLI.add_argument('--skip', nargs=4, default=[False, False, True, False],
                 help='boolean (True|False) whether the specific time plot will be drawn. Plots: Cases, Deaths, Recovered, Active')
args = CLI.parse_args()

c.countries = args.country
c.countries.sort()

plots.maxY = args.maxY
plots.skip = args.skip
plots.perMillion = args.million
plots.logY = args.logY

interactiveMode = args.interactive
daysBefore = int(args.days)
files = args.files
printCSV = args.csv

#
# Initialize data collections for reading from file
#
countryReported = dict()
casesReported = dict()
deathsReported = dict()
recoveredReported = dict()


# countries=['US','Italy','China','Spain','Germany','France','Iran','UK']
# countries=['Turkey','Portugal','Norway','Greece', 'Ireland', 'Denmark']
# countries=['Turkey','Italy','Germany','Greece', 'UK', 'Spain']
# countries=['Japan', 'China', 'Greece']
# countries=['Greece', 'Turkey', 'UK', 'Italy', 'Spain']

# cases = yValues[0]['Greece']
#  dcases = [ cases[i+1]/cases[i] if cases[i] != 0 else 0  for i in range(len(cases)-1)]



# def changeVector(cases):
#     return [cases[i+1]/cases[i] if cases[i] != 0 else 1 for i in range(len(cases)-1)]



# def countryNewCases(country, i):
#     return util.newCases(yValues[i][country])


# # def countryChange(country, i):
# #     return changeVector(yValues[i][country])




# def newInPeriodTotalPairs(country, cdra):
#     lastTime = plots.timePeriod
#     totalNewCasesLastTime = util.runningTotal(
#         countryNewCases(country, cdra), lastTime)
#     totalCases = yValues[cdra][country][lastTime-1:]
#     pairs = [(i, j)
#              for i, j in zip(totalNewCasesLastTime, totalCases) if j > 0]
#     return pairs




#
# START-UP
#
readFiles()
checkData()

if args.animate:
    plots.animate(args.number)

if printCSV:
    generateCSV()

if args.plot:
    plots.plotGraph(daysBefore)

if interactiveMode:
    code.interact(local=locals())
