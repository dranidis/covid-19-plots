import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import util
import countries as c

figsizeX, figsizeY = (13, 9)

savetofile = ''

skip = [False, False, False, False]
logY = False
perMillion = False
maxY = [0, 0, 0, 0]
timePeriod = 7

color = dict()
marker = dict()

colors = ['b', 'g', 'r', 'c', 'm', 'k', 'y']
markers = ['s', 'o', '^', 'v', '<', '>', 'p', '*', 'd']
markerNr = 0
colorNr = 0


extraFramesAtTheEnd = 10

for country in c.allCountries:
    marker[country] = markers[markerNr]
    color[country] = colors[colorNr]
    markerNr = (markerNr + 1) % len(markers)
    colorNr = (colorNr + 1) % len(colors)

def plotGraph(daysBefore=0):
    numOfPlots = len([s for s in skip if not s])
    if numOfPlots == 0:
        print('No plots to draw.')
        return

    fig, ax = plt.subplots(numOfPlots, 1, figsize=(figsizeX, figsizeY))

    plotNr = 0
    for i in range(c.maxDim):
        if skip[i]:
            continue

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
        axes.set_xticks(c.xValues)
        axes.set_xticklabels(c.xTicks, rotation = 90)
        axes.tick_params(axis='x')
        # plt.xticks(xValues, xTicks,  rotation='vertical')

        axes.grid(True)

        maxX = len(c.xValues)
        if daysBefore != 0:
            minX = maxX - daysBefore  
            axes.set_xlim([minX, maxX])
        if maxY[i] != 0:
            axes.set_ylim([0, maxY[i]])

        for country in c.countries:
            ys = [v/div(country) for v in c.yValues[i][country]]
            axes.plot(c.xValues, ys, color=color[country],
                      marker=marker[country])

        plotNr += 1

    if len(c.countries) > 5:
        plt.legend(c.countries, loc='upper left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(c.countries, loc='upper left', fontsize='small', ncol=1)

    plt.show()

def div(country):
    if perMillion:
        return c.population[country]
    return 1

# cdra = 1 # cases:0 , deaths:1, rec: 2, act: 3
def totalsGraph(cdra, daysBefore=0):
    line = dict()
    annotation = dict()
    fig, line, annotation, dateText = initAnimatedScatterGraph(
        cdra, line, annotation)

    if daysBefore == 0:
        frames = len(c.xTicks) - timePeriod + 1
    else:
        frames = daysBefore

    animation_frame(frames-1, line, cdra, annotation, dateText, daysBefore)
    plt.show()

def initAnimatedScatterGraph(cdra, line, annotation):
    fig = plt.figure(figsize=(figsizeX, figsizeY))
    ax1 = fig.add_subplot(111)

    xlabel = ['Total ' + str(l) for l in c.label]
    daysLabel = ' in last ' + str(timePeriod) + ' days'
    ylabel = ['New ' + str(l) + daysLabel for l in c.label]

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
    # plt.legend(loc='upper left')
    dateText = ax1.text(1000, 10, '-----', fontsize=36,
                        bbox=dict(facecolor='red', alpha=0.5))

    return fig, line, annotation, dateText


def animation_frame(i, line, cdra, annotation, dateText, daysBefore):
    if daysBefore == 0:
        frames = len(c.xTicks) - timePeriod + 1
    else:
        frames = daysBefore

    if i >= frames:
        i = frames - 1

    fromValue, toValue = util.getFromTo(
        len(c.xTicks), timePeriod, daysBefore, i)

    date = c.xTicks[toValue-1]

    dateText.set_text(date)

    for country in c.countries:
        partialYValues = c.yValues[cdra][country][0:toValue]

        totalNewCasesLastTime = util.runningTotal(
            util.newCases(partialYValues), timePeriod)[fromValue:]
        totalCases = partialYValues[timePeriod-1:][fromValue:]

        pairs = [(i, j) for i, j in zip(
            totalNewCasesLastTime, totalCases) if i > 0 and j > 0]
        new = [i/div(country) for i, j in pairs]
        tot = [j/div(country) for i, j in pairs]

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


def animate(cdra, daysBefore=0, speed=500, repeat=False):
    line = dict()
    annotation = dict()
    fig, line, annotation, dateText = initAnimatedScatterGraph(
        cdra, line, annotation)
    passlines = line

    if daysBefore == 0:
        frames = len(c.xTicks) - timePeriod + 1
    else:
        frames = daysBefore

    frames += extraFramesAtTheEnd
    animation = FuncAnimation(fig, func=animation_frame,
                              fargs=(passlines, cdra, annotation,
                                     dateText, daysBefore),
                              frames=frames,
                              interval=speed, repeat=repeat, blit=False)

    if savetofile:
        animation.save(savetofile, writer='imagemagick', fps=1)
        print('Saved animation to file: ', savetofile)
    else:
        plt.show()


def lastDaysSumVsTotal(cdra):
    past = len(c.xTicks) - timePeriod

    fig = plt.figure(figsize=(figsizeX, figsizeY))
    ax1 = fig.add_subplot(111)

    for country in c.countries:
        s = [j/i if i > 0 else np.nan for i, j in zip(
            c.yValues[cdra][country][-past:],
            util.runningTotal(util.newCases(c.yValues[cdra][country]), timePeriod)[-past:])]
        plt.plot(s, color=color[country],
                 marker=marker[country])

        annotation = ax1.annotate(
            country, xy=(len(s), s[-1]), xytext=(len(s), s[-1])
        )

    if len(c.countries) > 5:
        plt.legend(c.countries, loc='lower left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(c.countries, loc='lower left', fontsize='small', ncol=1)
    plt.ylabel('Last '+ str(timePeriod) + ' days ' + c.label[cdra] + ' / Total ' + c.label[cdra])

    ax1.set_xticks(c.xValues)
    ax1.set_xticklabels(c.xTicks[timePeriod:], rotation = 90)
    ax1.tick_params(axis='x')
    ax1.grid(True)
    plt.show()
