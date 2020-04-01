# Initialize countries
#
# allCountries = ['Greece','Italy','UK','Germany','Spain','Turkey','France','Sweden','Netherlands','Austria','Belgium','Portugal','Switzerland']
allCountries = ['US', 'Switzerland', 'Ireland', 'Denmark', 'Norway', 'Iran', 'China', 'Greece', 'Italy', 'UK', 'Germany',
                'Spain', 'Turkey', 'France', 'Sweden', 'Netherlands', 'Austria', 'Belgium', 'Portugal',  'Japan', 'South Korea', 'Kosovo']

countries = allCountries

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
population['Kosovo'] = 1.8

label = ['Cases', 'Deaths', 'Recovered', 'Active']
maxDim = len(label)

yValues = [dict(), dict(), dict(), dict()]
for i in range(maxDim):
    # yValues[i] = dict()
    for country in countries:
        yValues[i][country] = []