import sys
import argparse
import code

from covid19plots import plots as p
from covid19plots import countries as c

def run():
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

    CLI.add_argument('-p', '--plot', action='store_true',
                    help='time plots of cases/deaths/recoveries/active. Choose plots to skip with the --skip flag')
    CLI.add_argument('-t', '--totalsGraph', action='store_true',
                    help='new n numbers in last d days/total numbers. Choose which numbers to plot with the --number flag and how many days with the -d flag.')
    CLI.add_argument('-a', '--animate', action='store_true',
                    help='animate new numbers/total numbers. Choose which numbers to plot with the --number flag')
    CLI.add_argument('-w', '--week', action='store_true', 
                    help='Plot last days sum vs total. Although the flag is named week any number of days can be set with -r')

    CLI.add_argument('-d', '--days', nargs='?', type=int, default=0,
                    help='number of days to plot before today. By default plots start from the beginning of data collection.')
    CLI.add_argument('--maxY', nargs=4, type=int, default=[0, 0, 0, 0],
                    help='y axes limits for time plots')
    CLI.add_argument('-l', '--logY', action='store_true',
                    help='use log scale for the Y axes of time plots')
    CLI.add_argument('-i', '--interactive', action='store_true',
                    help='open interactive python console after parsing the files')
    CLI.add_argument('--csv', action='store_true', help='generate CSV output')


    CLI.add_argument('-n', '--number', nargs='?', type=int, default=1,
                    help='number to animate 0:cases, 1:deaths, 2:recovered, 3:active')
    CLI.add_argument('-s', '--savetofile', nargs='?', type=str,
                    help='file to save the animation')
    CLI.add_argument('-m', '--million', action='store_true',
                    help='in plots divide values by country population in millions')
    CLI.add_argument('--draw', nargs=4, default=['1','1','0','0'],
                    help='boolean (True|False) whether the specific time plot will be drawn. Plots: Cases, Deaths, Recovered, Active')
    CLI.add_argument('-r', '--runningTotal', nargs='?', type=int, default=7,
                    help='number of days to calculate running totals (in animation/last days sum vs total)')          
    args = CLI.parse_args()

    c.countries = args.country
    c.countries.sort()

    p.maxY = args.maxY
    p.skip = [not ts.lower() in ['true', 't', '1']  for ts in args.draw]
    p.perMillion = args.million
    p.logY = args.logY
    p.savetofile = args.savetofile
    p.timePeriod = int(args.runningTotal)

    #
    # START-UP
    #
    c.readFiles(args.files)
    c.checkData()

    if args.plot:
        p.plotGraph(int(args.days))

    if args.animate:
        p.animate(args.number, int(args.days))

    if args.csv:
        c.generateCSV()

    if args.week:
        p.lastDaysSumVsTotal(args.number)

    if args.totalsGraph:
        p.totalsGraph(args.number, int(args.days))

    if args.interactive:
        code.interact(local=globals())


