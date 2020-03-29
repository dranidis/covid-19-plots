# COVID-19 plots based on daily reports by Johns Hopkins CSSE

## Run the script

Minimum command line options:
```
python3.5 read.py <path of csse_covid_19_daily_reports>/*.csv
```

## Help
```
python3.5 read.py -h
```

Output:
```
usage: read.py [-h] [-c [COUNTRY [COUNTRY ...]]] [-d [DAYS]]
               [--maxY MAXY MAXY MAXY MAXY] [-l] [-i] [--csv] [-m]
               [--skip SKIP SKIP SKIP SKIP]
               files [files ...]

Plot graphs for the COVID-19

positional arguments:
  files

optional arguments:
  -h, --help            show this help message and exit
  -c [COUNTRY [COUNTRY ...]], --country [COUNTRY [COUNTRY ...]]
  -d [DAYS], --days [DAYS]
                        number of days to plot before today. By default plots
                        start from the beginning of data collection.
  --maxY MAXY MAXY MAXY MAXY
  -l, --logY            use log scale for the Y axes
  -i, --interactive     open interactive python console after parsing the
                        files
  --csv                 generate CSV output
  -m, --million         divide values by country population in millions
  --skip SKIP SKIP SKIP SKIP
                        boolean (True|False) whether the specific plot will be
                        drawn. Plots: Cases, Deaths, Recovered, Active
```

## Interactive mode

In interactive mode:

Plot graphs
```
plotGraph()
```
or with days
```
plotGraph(20)
```


