import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import util
import countries as c

skip = [False, False, False, False]
logY = False
perMillion = False
maxY = [0,0,0,0]
timePeriod = 7

xValues = []
xTicks = []

color = dict()
marker = dict()

colors = ['b', 'g', 'r', 'c', 'm', 'k', 'y']
markers = ['s', 'o', '^', 'v', '<', '>', 'p', '*', 'd']
markerNr = 0
colorNr = 0

for country in c.allCountries:
    marker[country] = markers[markerNr]
    color[country] = colors[colorNr]
    markerNr = (markerNr + 1) % len(markers)
    colorNr = (colorNr + 1) % len(colors)
    # if markerNr == len(markers):
    #     markerNr = 0
    # if colorNr == len(colors):
    #     colorNr = 0

def plotGraph(daysBefore=0):
    numOfPlots = len([s for s in skip if not s])
    if numOfPlots == 0:
        print('No plots to draw.')
        return

    fig, ax = plt.subplots(numOfPlots, 1)

    plotNr = 0
    for i in range(c.maxDim):
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
        plotLabel = c.label[i]

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

        for country in c.countries:
            if perMillion:
                ys = list(
                    map(lambda y: y/c.population[country], c.yValues[i][country]))
            else:
                ys = c.yValues[i][country]
            axes.plot(xValues, ys, color=color[country],
                      marker=marker[country])

        plotNr += 1

    if len(c.countries) > 5:
        plt.legend(c.countries, loc='upper left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(c.countries, loc='upper left', fontsize='small', ncol=1)

    plt.show()

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
    for country in c.countries:
        totalNewCasesLastTime = util.runningTotal(
            util.countryNewCases(country, cdra), lastTime)
        totalCases = c.yValues[cdra][country][lastTime-1:]

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

    for country in c.countries:
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
    toValue = timePeriod + i
    date = xTicks[toValue-1]

    dateText.set_text(date)

    for country in c.countries:
        partialYValues = c.yValues[cdra][country][0:toValue]

        totalNewCasesLastTime = util.runningTotal(
            util.newCases(partialYValues), timePeriod)
        totalCases = partialYValues[timePeriod-1:]

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
    animation = FuncAnimation(fig, func=animation_frame,
                              fargs=(passlines, cdra, annotation, dateText),
                              frames=len(xTicks)-timePeriod+1,
                              interval=speed, repeat=repeat, blit=False)

    # animation.save('im.mp4')
    plt.show()




def lastWeekVsTotal():
    past = len(xTicks) - timePeriod
    for country in c.countries:
        s = [j/i if i > 0 else np.nan for i, j in zip(
            c.yValues[1][country][-past:], 
            util.runningTotal(util.newCases(c.yValues[1][country]), 7)[-past:])]
        plt.plot(s, color=color[country],
                 marker=marker[country])
    if len(c.countries) > 5:
        plt.legend(c.countries, loc='lower left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(c.countries, loc='lower left', fontsize='small', ncol=1)
    plt.ylabel('Last week deaths/Total deaths')
    plt.show()
