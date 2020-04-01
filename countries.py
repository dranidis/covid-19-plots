import csv

# Initialize countries
#
allCountries = ['US', 'Switzerland', 'Ireland', 'Denmark', 'Norway', 'Iran', 'China', 'Greece', 'Italy', 'UK', 'Germany',
                'Spain', 'Turkey', 'France', 'Sweden', 'Netherlands', 'Austria', 'Belgium', 'Portugal',  'Japan', 'South Korea', 'Canada']

countries = allCountries

#
# Initialize data collections for reading from file
#
countryReported = dict()
casesReported = dict()
deathsReported = dict()
recoveredReported = dict()

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
population['Canada'] = 37

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

                if row[provinceIndex] == '' or row[countryIndex] in ['US','Canada','China']:
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

