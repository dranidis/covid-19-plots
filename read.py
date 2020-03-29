# call with
#
# python3.5 read.py --c Spain Italy Germany Greece UK --f ../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/*.csv
#

import sys
import csv
import argparse
import matplotlib.pyplot as plt
import code


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

    for i in range(maxDim):
        if yValue[i] != 0:
            yValues[i][country].append(yValue[i])
        elif len(yValues[i][country]) > 0:
            # use previous value
            lastValue = yValues[i][country][-1]
            yValues[i][country].append(lastValue)
        else:
            yValues[i][country].append(0)


def plotGraph(daysBefore = 0):
    numOfPlots = len([s for s in skip if not s])

    plotNr = 0
    for i in range(maxDim):
        if skip[i]:
            continue
        else:
            plotNr += 1

        plt.subplot(numOfPlots, 1, plotNr)

        if logY:
            plt.yscale('log')

        plt.xlabel('Date')
        plotLabel = label[i]

        if perMillion:
            plotLabel += ' per million'

        plt.ylabel(plotLabel)

        # plt.title('Title')
        plt.xticks(xValues, xTicks, rotation='vertical')

        maxX = len(xValues)
        if daysBefore != 0:
            minX = maxX - daysBefore  # 30 days before
            plt.xlim([minX, maxX])
        if maxY[i] != 0:
            plt.ylim([0, maxY[i]])

        for country in countries:
            if perMillion:
                ys = list(
                    map(lambda y: y/population[country], yValues[i][country]))
            else:
                ys = yValues[i][country]
            plt.plot(xValues, ys, 'o-')

    if len(countries) > 5:
        plt.legend(countries, loc='upper left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(countries, loc='upper left', fontsize='small', ncol=1)

    plt.show()


def readFiles():
    xValue = 0
    for filename in files:
        date = filename[-14:-9]  # keep only the MM-DD from the file name
        xValues.append(xValue)
        xTicks.append(date)
        xValue += 1

        with open(filename) as csvfile:
            for country in countries:
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

                if country in countries:
                    processRow(country, row[confirmedIndex],
                               row[deathsIndex], row[recoveredIndex])

            for country in countries:
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
    for date in xTicks:
        print(date, end=',')
        for country in countries:
            print(country, end=',')
            for i in range(maxDim):
                print(yValues[i][country][index], end=',')
        print()
        index += 1


#
# PROGRAM
#

label = ['Cases', 'Deaths', 'Recovered', 'Active']

maxDim = len(label)

# Initialize countries
#
# allCountries = ['Greece','Italy','UK','Germany','Spain','Turkey','France','Sweden','Netherlands','Austria','Belgium','Portugal','Switzerland']
allCountries = ['Japan', 'Ireland', 'Denmark', 'Norway', 'US', 'Iran', 'China', 'Greece', 'Italy', 'UK', 'Germany',
                'Spain', 'Turkey', 'France', 'Sweden', 'Netherlands', 'Austria', 'Belgium', 'Portugal', 'Switzerland']

population = dict()
population['US'] = 372
population['Ireland'] = 5
population['Denmark'] = 6
population['Norway'] = 5
population['China'] = 1340
population['Iran'] = 81
population['Greece'] = 11
population['Italy'] = 61
population['UK'] = 66
population['Germany'] = 83
population['Spain'] = 46
population['Turkey'] = 80
population['France'] = 67
population['Sweden'] = 10
population['Netherlands'] = 17
population['Austria'] = 9
population['Belgium'] = 11
population['Portugal'] = 11
population['Switzerland'] = 8.5
population['Japan'] = 127

#
CLI = argparse.ArgumentParser(description='Plot graphs for the COVID-19')
CLI.add_argument('-c', '--country',
                 nargs='*',
                 type=str,
                 default=allCountries)
CLI.add_argument('files', nargs='+', type=str)
CLI.add_argument('-d', '--days', nargs='?', type=int, default=0, help='number of days to plot before today. By default plots start from the beginning of data collection.')
CLI.add_argument('--maxY', nargs=4, type=int, default=[0,0,0,0])
CLI.add_argument('-l', '--logY', action='store_true', help='use log scale for the Y axes')
CLI.add_argument('-i', '--interactive', action='store_true', help='open interactive python console after parsing the files')
CLI.add_argument('--csv', action='store_true', help='generate CSV output')
CLI.add_argument('-m', '--million', action='store_true', help='divide values by country population in millions')
CLI.add_argument('--skip', nargs=4, default=[False, False, True, False], help='boolean (True|False) whether the specific plot will be drawn. Plots: Cases, Deaths, Recovered, Active')
args = CLI.parse_args()

countries = args.country
countries.sort()
daysBefore = int(args.days)
maxY = args.maxY
skip = args.skip

if len(maxY) != 4:
    print('maxY should receive 4 values')
    sys.exit(-1)

logY = args.logY
interactiveMode = args.interactive
files = args.files
printCSV = args.csv
perMillion = args.million

#
# Initialize data collections for reading from file
#
countryReported = dict()
casesReported = dict()
deathsReported = dict()
recoveredReported = dict()


#
# for plotting
#
xValues = []
yValues = [dict(), dict(), dict(), dict()]
for i in range(maxDim):
    # yValues[i] = dict()
    for country in countries:
        yValues[i][country] = []
xTicks = []


readFiles()

if printCSV:
    generateCSV()

if interactiveMode:
    code.interact(local=locals())
else:
    plotGraph(daysBefore)

# total = dict()
# for country in countries:
#     total[country] = []
#     for x in xValues:
#         total[country].append(yValues[0][country][x] + yValues[1][country][x]  + yValues[2][country][x] )

# countries=['US','Italy','China','Spain','Germany','France','Iran','UK']
# countries=['Turkey','Portugal','Norway','Greece', 'Ireland', 'Denmark']
# countries=['Turkey','Italy','Germany','Greece', 'Turkey', 'UK', 'Spain']
# countries=['Japan', 'China']
