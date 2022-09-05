from cmath import pi
import json
from geopy import distance
import matplotlib.pyplot as plt

# Load all the data
dataFlyCoordinates = json.load(open('data/coords.json')).get('flyZones')[0]['boundaryPoints']
flyCoordinates = []
dataCoordinates = json.load(open('data/coords.json')).get('waypoints')
coordinates = []
for point in dataCoordinates: coordinates.append([point['latitude'], point['longitude']])

# Find min latitude and min longitude
minLat = 10**9
minLong = 10**9
for flyPoint in dataFlyCoordinates:
    minLat = min(minLat, flyPoint['latitude'])
    minLong = min(minLong, flyPoint['longitude'])

# Plot points with corrected distance
for coordinate in coordinates:
    plt.plot(distance.distance(coordinate, (coordinate[0], minLong)).feet, 
    distance.distance(coordinate, (minLat, coordinate[1])).feet, 'ro', 
    label = coordinates.index(coordinate)) 

plt.legend()
plt.show()