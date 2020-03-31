import sys
import csv
import argparse
import matplotlib.pyplot as plt
import code
import numpy as np

from matplotlib.animation import FuncAnimation


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


def plotGraph(daysBefore=0):
    numOfPlots = len([s for s in skip if not s])
    if numOfPlots == 0:
        print('No plots to draw.')
        return

    fig, ax = plt.subplots(numOfPlots, 1)

    plotNr = 0
    for i in range(maxDim):
        if skip[i]:
            continue
        # plt.subplot(numOfPlots, 1, plotNr)

        if numOfPlots == 1:
            axes = ax
        else:
            axes = ax[plotNr]

        if logY:
            axes.set_yscale('log')

        axes.set_xlabel('Date')
        plotLabel = label[i]

        if perMillion:
            plotLabel += ' per million'

        axes.set_ylabel(plotLabel)

        # plt.title('Title')
        axes.set_xticks(xValues)
        axes.set_xticklabels(xTicks)
        axes.tick_params(axis='x')
        # plt.xticks(xValues, xTicks,  rotation='vertical')

        axes.grid(True)

        maxX = len(xValues)
        if daysBefore != 0:
            minX = maxX - daysBefore  # 30 days before
            axes.set_xlim([minX, maxX])
        if maxY[i] != 0:
            axes.set_ylim([0, maxY[i]])

        for country in countries:
            if perMillion:
                ys = list(
                    map(lambda y: y/population[country], yValues[i][country]))
            else:
                ys = yValues[i][country]
            axes.plot(xValues, ys, color=color[country],
                      marker=marker[country])

        plotNr += 1

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


def checkData():
    print("Fixing inconsistent data for cases and deaths")
    for i in range(maxDim-1):  # last dim is active (calculated)
        print('\t--------------------------------------')
        print("\tChecking ", i)
        print('\t--------------------------------------')
        for country in countries:
            previous = 0
            index = 0
            for date in xTicks:
                current = int(yValues[i][country][index])
                if current < previous:
                    print('\t', date, country, i, previous, current, end='')
                    if i == 0 and country == 'Japan' and date == '01-23':
                        print('\t===> Correcting value to 2')
                        yValues[i][country][index] = 2
                    if i == 0 and country == 'Japan' and date == '02-07':
                        print('\t===> Correcting previous value to 25')
                        yValues[i][country][index-1] = 25
                    if i == 0 and country == 'Japan' and date == '03-16':
                        print('\t===> Correcting value to 839')
                        yValues[i][country][index] = 839
                    if i == 1 and country == 'Japan' and date == '03-10':
                        print('\t===> Correcting previous value to 10')
                        yValues[i][country][index-1] = 10
                previous = current
                index += 1


#
# PROGRAM
#

label = ['Cases', 'Deaths', 'Recovered', 'Active']

maxDim = len(label)

# Initialize countries
#
# allCountries = ['Greece','Italy','UK','Germany','Spain','Turkey','France','Sweden','Netherlands','Austria','Belgium','Portugal','Switzerland']
allCountries = ['US', 'Switzerland', 'Ireland', 'Denmark', 'Norway', 'Iran', 'China', 'Greece', 'Italy', 'UK', 'Germany',
                'Spain', 'Turkey', 'France', 'Sweden', 'Netherlands', 'Austria', 'Belgium', 'Portugal',  'Japan', 'South Korea']

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
population['South Korea'] = 51

color = dict()
marker = dict()

colors = ['b', 'g', 'r', 'c', 'm', 'k', 'y']
markers = ['s', 'o', '^', 'v', '<', '>', 'p', '*', 'd']
markerNr = 0
colorNr = 0
for country in allCountries:
    marker[country] = markers[markerNr]
    color[country] = colors[colorNr]
    markerNr = (markerNr + 1) % len(markers)
    colorNr = (colorNr + 1) % len(colors)
    # if markerNr == len(markers):
    #     markerNr = 0
    # if colorNr == len(colors):
    #     colorNr = 0

#
# CLI arguments
#
CLI = argparse.ArgumentParser(description='Plot graphs for the COVID-19')
CLI.add_argument('-c', '--country',
                 nargs='*',
                 type=str,
                 default=allCountries,
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

countries = args.country
countries.sort()
daysBefore = int(args.days)
maxY = args.maxY
skip = args.skip


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


# countries=['US','Italy','China','Spain','Germany','France','Iran','UK']
# countries=['Turkey','Portugal','Norway','Greece', 'Ireland', 'Denmark']
# countries=['Turkey','Italy','Germany','Greece', 'UK', 'Spain']
# countries=['Japan', 'China', 'Greece']
# countries=['Greece', 'Turkey', 'UK', 'Italy', 'Spain']

# cases = yValues[0]['Greece']
#  dcases = [ cases[i+1]/cases[i] if cases[i] != 0 else 0  for i in range(len(cases)-1)]

def changeVector(cases):
    return [cases[i+1]/cases[i] if cases[i] != 0 else 1 for i in range(len(cases)-1)]


def newCases(cases):
    dcases = [cases[i+1] - cases[i] for i in range(len(cases)-1)]
    dcases.insert(0, 0)
    return dcases


def countryNewCases(country, i):
    return newCases(yValues[i][country])


def countryChange(country, i):
    return changeVector(yValues[i][country])


def runningTotal(cases, days):
    total = []
    numbers = len(cases) - days + 1
    for d in range(numbers):
        t = 0
        for i in range(days):
            t += cases[d + i]
        total.append(t)

    return total


timePeriod = 7


def newInPeriodTotalPairs(country, cdra):
    lastTime = timePeriod
    totalNewCasesLastTime = runningTotal(
        countryNewCases(country, cdra), lastTime)
    totalCases = yValues[cdra][country][lastTime-1:]
    pairs = [(i, j)
             for i, j in zip(totalNewCasesLastTime, totalCases) if j > 0]
    return pairs


# cdra = 1 # cases:0 , deaths:1, rec: 2, act: 3
def scatterGraph(cdra):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # for country in ['China', 'Italy', 'Spain', 'Greece',  'Germany', 'US', 'UK']:

    xlabel = ['Total cases', 'Total Deaths',
              'Total recoveries', 'Total active']
    daysLabel = ' in last ' + str(timePeriod) + ' days'
    ylabel = ['New cases' + daysLabel, 'New deaths' + daysLabel,
              'New recoveries' + daysLabel, 'New active' + daysLabel]

    lastTime = timePeriod
    for country in countries:
        totalNewCasesLastTime = runningTotal(
            countryNewCases(country, cdra), lastTime)
        totalCases = yValues[cdra][country][lastTime-1:]

        pairs = [(i, j) for i, j in zip(
            totalNewCasesLastTime, totalCases) if i > 0 and j > 0]
        new = [i for i, j in pairs]
        tot = [j for i, j in pairs]

        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(xlabel[cdra])
        plt.ylabel(ylabel[cdra])
        plt.grid(True)

        ax1.plot(tot, new, color=color[country],
                 marker=marker[country], label=country)

    plt.legend(loc='upper left')
    plt.show()


def initAnimatedScatterGraph(cdra, line, annotation):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # for country in ['China', 'Italy', 'Spain', 'Greece',  'Germany', 'US', 'UK']:

    xlabel = ['Total cases', 'Total Deaths',
              'Total recoveries', 'Total active']
    daysLabel = ' in last ' + str(timePeriod) + ' days'
    ylabel = ['New cases' + daysLabel, 'New deaths' + daysLabel,
              'New recoveries' + daysLabel, 'New active' + daysLabel]

    for country in countries:
        new = []
        tot = []

        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel(xlabel[cdra])
        plt.ylabel(ylabel[cdra])
        plt.grid(True)

        plt.xlim(1, 1000000)
        plt.ylim(1, 10000)
        if cdra in [0, 2, 3]:
            plt.ylim(1, 1000000)
        else:
            plt.xlim(1, 100000)

        line[country], = ax1.plot(tot, new, color=color[country],
                                  marker=marker[country], label=country)

        annotation[country] = ax1.annotate(
            country, xy=(0.1, 0.1), xytext=(0.1, 0.1)
        )
    plt.legend(loc='upper left')
    dateText = ax1.text(1000, 10, '-----', fontsize=36,
                        bbox=dict(facecolor='red', alpha=0.5))

    return fig, line, annotation, dateText


def animation_frame(i, line, cdra, annotation, dateText):
    lastTime = timePeriod

    toValue = timePeriod + i
    date = xTicks[toValue-1]

    dateText.set_text(date)

    for country in countries:
        partialYValues = yValues[cdra][country][0:toValue]

        totalNewCasesLastTime = runningTotal(
            newCases(partialYValues), lastTime)
        totalCases = partialYValues[lastTime-1:]

        pairs = [(i, j) for i, j in zip(
            totalNewCasesLastTime, totalCases) if i > 0 and j > 0]
        new = [i for i, j in pairs]
        tot = [j for i, j in pairs]

        line[country].set_xdata(tot)
        line[country].set_ydata(new)

        if len(tot) > 0:
            anx = tot[-1]
            any = new[-1]
        else:  # outside the visible area
            anx = 0.1
            any = 0.1
        annotation[country].set_position((anx*1.2, any/1.1))
        annotation[country].xy = (anx, any)

    return line, annotation, dateText,


def animate(cdra, speed=500, repeat=False):
    line = dict()
    annotation = dict()
    fig, line, annotation, dateText = initAnimatedScatterGraph(
        cdra, line, annotation)
    passlines = line
    animation = FuncAnimation(fig, func=animation_frame, fargs=(
        passlines, cdra, annotation, dateText), frames=len(xTicks)-timePeriod+1, interval=speed, repeat=repeat, blit=False)
    plt.show()


#
# START-UP
#
readFiles()
checkData()

if args.animate:
    animate(args.number)

if printCSV:
    generateCSV()

if args.plot:
    plotGraph(daysBefore)

if interactiveMode:
    code.interact(local=locals())
