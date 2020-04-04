import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from covid19plots import util
from covid19plots import countries as c

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

def getXValues():
    return c.xValues

#
# Plots to draw
#
def plotGraph(daysBefore=0):
    plotGraphFunc(getXValues, getYValues, getYLabel, daysBefore)

def lastDaysSumVsDays(daysBefore=0):
    plotGraphFunc(getXValues, getYAvgNew, getYLabelAvgNew, daysBefore)

def lastDaysSumVsTotal(daysBefore=0):
    plotGraphFunc(getXValues, getY, getYLabelW, daysBefore)

#
# Data functions for Y axis
#
def getYValues(i, country):
    return [v/div(country) if v > 0 else np.nan for v in c.yValues[i][country]]    

def getYAvgNew(i, country):
    return [v/div(country) if v > 0 else np.nan for v in util.runningAvgN(util.newCases(
                c.yValues[i][country]), timePeriod)]

def getY(i, country):
    return [j/i if i > 0 else np.nan for i, j in zip(
            c.yValues[i][country],
            util.runningTotalN(util.newCases(c.yValues[i][country]), timePeriod))]

#
# Labelling functions for Y axis
#
def getYLabel(i):
    plotLabel = c.label[i]
    if perMillion:
        plotLabel += ' per million'
    return plotLabel

def getYLabelAvgNew(i):
    plotLabel = 'Last '+ str(timePeriod) + ' days ' + c.label[i]
    if perMillion:
        plotLabel += ' per million'    
    return plotLabel + ' / ' + str(timePeriod) + ' days '

def getYLabelW(i):
    plotLabel = 'Last '+ str(timePeriod) + ' days ' + c.label[i] + ' / Total ' + c.label[i]
    return plotLabel

#
# General function for time-plots
#
def plotGraphFunc(getXValues, getYValues, getYLabel, daysBefore):

    numOfPlots = len([s for s in skip if not s])
    if numOfPlots == 0:
        print('No plots to draw.')
        return

    fig, ax = plt.subplots(numOfPlots, 1, figsize=(figsizeX, figsizeY))

    plotNr = 0
    for i in [i for s,i in zip(skip, range(c.maxDim)) if not s]:
        if numOfPlots == 1:
            axes = ax
        else:
            axes = ax[plotNr]

        if logY:
            axes.set_yscale('log')

        axes.set_xlabel('Date')
        
        plotLabel = getYLabel(i)

        axes.set_ylabel(plotLabel)

        axes.set_xticks(c.xValues)
        axes.set_xticklabels(c.xTicks, rotation = 90)
        axes.tick_params(axis='x')

        axes.grid(True)

        maxX = len(c.xValues)
        if daysBefore != 0:
            minX = maxX - daysBefore  
            axes.set_xlim([minX, maxX])
        if maxY[i] != 0:
            axes.set_ylim([0, maxY[i]])

        for country in c.countries:
            xs = getXValues()
            ys = getYValues(i, country)
            axes.plot(xs, ys, color=color[country],
                      marker=marker[country])
            annotation = axes.annotate(
                country, xy=(xs[-1], ys[-1]), xytext=(xs[-1]+0.1, ys[-1])
            )

        plotNr += 1

    addLegends()
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
    daysLabel = ' per day (in last ' + str(timePeriod) + ' days)'
    ylabel = ['Average ' + str(l) + daysLabel for l in c.label]

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

        pairs = [(i/timePeriod, j) for i, j in zip(
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


def addLegends():
    if len(c.countries) > 5:
        plt.legend(c.countries, loc='upper left', fontsize='xx-small', ncol=2)
    else:
        plt.legend(c.countries, loc='upper left', ncol=1)    