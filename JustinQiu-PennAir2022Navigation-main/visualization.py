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
    newX = distance.distance(coordinate, (coordinate[0], minLong)).feet
    newY = distance.distance(coordinate, (minLat, coordinate[1])).feet
    plt.plot(newX, newY, 'rv')
    plt.annotate(coordinates.index(coordinate), xy = (newX-20, newY+100))

plt.title('Plot for Adjusted Waypoints')
plt.ylabel('Adjusted Y Coordinate (feet)', fontsize = 15) 
plt.xlabel('Adjusted X Coordinate (feet)', fontsize = 15) 
plt.show()