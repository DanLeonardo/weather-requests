#!/usr/bin/python3

import sys
import requests
import argparse
import config

# By city Name
# -q City
# -q City,Country

# By city ID
# -id cityID

# By Coord
# -coord lat long

# By Zip Code
# -zip zipCode

# Metric
# -u celsius

def parse_arguments():
    ag = argparse.ArgumentParser()

    ag.add_argument('-q', '--city', help='City to get weather from')
    ag.add_argument('-z', '--zip', help='ZIP Code to get weather from')
    ag.add_argument('-g', '--coord', nargs=2, help='Latitude and Longitude to get weather from')
    ag.add_argument('-u', '--units', help='Standard, Metric, or Imperial units to be displayed')

    args = vars(ag.parse_args())
    return args

def display_weather(data, args):
    print('display')
    if 'name' in data:
        print(data['name'])

    if 'weather' in data:
        weather = data['weather'][0]
        print(weather['description'].capitalize())

    if 'main' in data:
        main = data['main']

        print('Temperature: %s' % main['temp'])
        print('Feels Like: %s' % main['feels_like'])

        print('Pressure: %s' % main['pressure'])
        print('Humidity: %s' % main['humidity'])
        print('Low: %s' % main['temp_min'])
        print('High: %s' % main['temp_max'])

    if 'wind' in data:
        wind = data['wind']
        wind_speed = wind['speed']
        wind_deg = wind['deg']

    if 'rain' in data:
        rain = data['rain']
        print('Rain:')

        if '1h' in rain:
            print('Last Hour: %s' % rain['1h'])
        if '3h' in rain:
            print('Last 3 Hours: %s' % rain['3h'])

    if 'snow' in data:
        snow = data['snow']
        print('Snow:')

        if '1h' in snow:
            print('Last Hour: %s' % snow['1h'])
        if '3h' in snow:
            print('Last 3 Hours: %s' % snow['3h'])

if __name__ == '__main__':
    # Read API config information from config file
    API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    API_KEY = config.API_KEY

    # Load default parameters into params
    # Params will be sent as the GET request
    params = {'APPID': API_KEY}
    for key, value in config.PARAM_DEFAULTS.items():
        params[key] = value

    # Populate params with command line arguments
    args = parse_arguments()
    for arg, value in args.items():
        if not value:
            continue

        if arg == 'city':
            params['q'] = value
        elif arg == 'zip':
            params['zip'] = value
        elif arg == 'coord':
            params['lat'] = value[0]
            params['lon'] = value[1]
        elif arg == 'units':
            if value.lower() != 'kelvin' and value.lower() != 'celsius' and value.lower() != 'imperial':
                print('Error: Unit "%s" is not supported!' % value)
                print('Continuing with default %s.' % params['units'].capitalize())
            else:
                params['units'] = value.lower()

    print('Getting weather from ', end='')
    if 'q' in params:
        print('%s.' % params['q'])
    elif 'zip' in params:
        print('zip %s.' % params['zip'])
    elif set(('lat', 'lon')) <= set(params):
        print('(%s, %s).' % (params['lat'], params['lon']))
    else:
        print('error nowhere')

    r = requests.get(url=API_URL, params=params)
    data = r.json()
    display_weather(data, None)
