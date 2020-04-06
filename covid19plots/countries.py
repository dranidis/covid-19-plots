import csv
import numpy as np

# Initialize countries
#
allCountries = ['US', 'Switzerland', 'Ireland', 'Denmark', 'Norway', 'Iran', 'China', 'Greece', 'Italy', 'UK', 'Germany',
                'Spain', 'Turkey', 'France', 'Sweden', 'Netherlands', 'Austria', 'Belgium', 'Portugal',  'Japan', 'South Korea', 'Canada', 'Romania']

countries = allCountries

#
# Initialize data collections for reading from file
#
countryReported = dict()
casesReported = dict()
deathsReported = dict()
recoveredReported = dict()

# population = dict()
# population['US'] = 372
# population['Ireland'] = 5
# population['Denmark'] = 6
# population['Norway'] = 5
# population['China'] = 1340
# population['Iran'] = 81
# population['Greece'] = 11
# population['Italy'] = 61
# population['UK'] = 66
# population['Germany'] = 83
# population['Spain'] = 46
# population['Turkey'] = 80
# population['France'] = 67
# population['Sweden'] = 10
# population['Netherlands'] = 17
# population['Austria'] = 9
# population['Belgium'] = 11
# population['Portugal'] = 11
# population['Switzerland'] = 8.5
# population['Japan'] = 127
# population['South Korea'] = 51
# population['Canada'] = 37
# population['Romania'] = 19
# population['Hubei'] = 58.5

population = {'Portugal': 10.374822, 'Ireland': 6.378, 'Austria': 8.725931, 'Denmark': 5.717014, 'Germany': 81.7709, 'Iran': 79.3699, 'Spain': 46.438422, 'South Korea': 25.281, 'UK': 65.11, 'Canada': 36.155487, 'Turkey': 78.741053, 'Japan': 126.96, 'Netherlands': 17.0198, 'Greece': 10.858018, 'Sweden': 9.894888, 'Norway': 5.223256, 'Romania': 19.861408, 'Belgium': 11.319511, 'Italy': 60.665551, 'France': 66.71, 'Switzerland': 8.3416, 'China': 1377.422166, 'US': 323.947}

label = ['Cases', 'Deaths', 'Recovered', 'Active']
maxDim = len(label)

xValues = []
xTicks = []
yValues = [dict(), dict(), dict(), dict()]

for i in range(maxDim):
    for country in countries:
        yValues[i][country] = []


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


def readFiles(files):
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

                if row[provinceIndex] == '' or row[countryIndex] in ['US', 'Canada', 'China']:
                    country = row[countryIndex]
                else:
                    country = row[provinceIndex]

                if country in countries:
                    processRow(country, row[confirmedIndex],
                               row[deathsIndex], row[recoveredIndex])

                # extra call for 'Hubei'
                if 'Hubei' in countries and row[provinceIndex] == 'Hubei':
                    processRow('Hubei', row[confirmedIndex],
                               row[deathsIndex], row[recoveredIndex])

            for country in countries:
                processCountry(country)


def readUpdateFile():
    filename = 'update.csv'
    print('Reading', filename, 'for recent data')
    updated = dict()
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile)
        xValues.append(xValues[-1] + 1)
        xTicks.append('new')

        header = False
        for row in spamreader:
            if header:
                header = False
                continue
            country = row[0]
            totalCases = row[1]
            totalDeaths = row[3]
            totalRec = row[5]

            if totalDeaths != '':
                totalDeaths = int(totalDeaths)
            else:
                totalDeaths = np.nan
            if totalCases != '':
                totalCases = int(totalCases)
            else:
                totalCases = np.nan
            if totalRec != '':
                totalRec = int(totalRec)
            else:
                totalRec = np.nan

            if country == 'USA':
                country = 'US'
            if country == 'S. Korea':
                country = 'South Korea'

            updated[country] = (totalCases, totalDeaths, totalRec, totalCases - totalDeaths - totalRec)

        countries = []
        for country in allCountries:
            if country in updated.keys():
                print('Updating ', country)
                (tc, td, tr, ta) = updated[country]
                print(tc, td, tr, ta)
                yValues[0][country].append(tc)
                yValues[1][country].append(td)
                yValues[2][country].append(tr)
                yValues[3][country].append(ta)
                countries.append(country)
            else:
                print('Not updated:', country)
    print("\n>>>\n", flush=True)


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
    print("\n>>>\n", flush=True)
