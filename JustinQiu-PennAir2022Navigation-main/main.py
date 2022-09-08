import json
from geopy import distance

# Load all the data
dataCoordinates = json.load(open('data/coords.json')).get('waypoints')
coordinates = []
for point in dataCoordinates: coordinates.append((point['latitude'], point['longitude'], point['altitude']))

# Calculate distance between two coordinates
def dis(c1, c2):
    lat1, long1, height1 = c1
    lat2, long2, height2 = c2
    return ((distance.distance((lat1, long1), (lat2, long2)).feet ** 2) + (abs(height1 - height2) ** 2)) ** 0.5

# Create array of coordinate distances
distances = [[dis(coord1, coord2) for coord2 in coordinates] for coord1 in coordinates]

# Travelling salesman with dynamic programming
# Note: Memos heavily adapted from https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/

def TSPSol(n, distValues):
    # Memo with bitmask for every possible set for every starting point
    memo = [[-1]*(1 << n) for _ in range(n)]

    def TSP(cur, mask, path):
        if mask == 0: return (distValues[cur][0], path + [0])  # Base case; nothing left to visit
        if memo[cur][mask] != -1: return (memo[cur][mask][0], memo[cur][mask][1]) # Read from memo

        minDist = 10**9
        minPath = []
        for j in range(1, n):
            if (mask & (1 << j)) != 0 and j != cur:
                temp = TSP(j, mask & (~(1 << j)), path + [j]) # Recursive call for path between remaining cities
                if temp[0] + distValues[cur][j] < minDist:
                    minDist = temp[0] + distValues[cur][j]
                    minPath = temp[1]
                
        memo[cur][mask] = (minDist, minPath) # Write to memo
        return (minDist, minPath)

    temp = TSP(0, (1 << (n))-2, [])
    
    print("The cost of most efficient tour = " + str(temp[0]))
    print("The path of the most efficient tour = " + str([0] + temp[1]))

TSPSol(14, distances)