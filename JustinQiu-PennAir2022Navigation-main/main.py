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
# Note: Heavily adapted from https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/ (didn't want to reinvent the wheel with memos)
# Changes include: adapted for problem, included path tracking, changed to 0-index

def TSPSol(n, distValues):
    # Memo with bitmask for every possible set for every starting point
    memo = [[-1]*(1 << n) for _ in range(n)]

    def TSP(cur, mask, path):
        if mask == ((1 << cur) | 1): return (distValues[1][cur], path + [cur])  # Base case
        if memo[cur][mask] != -1: return (memo[cur][mask][0], memo[cur][mask][1]) # Read from memo

        minDist = 10**9
        minPath = []
        for j in range(0, n):
            if (mask & (1 << j)) != 0 and j != cur and j != 0:
                temp = TSP(j, mask & (~(1 << cur)), path + [cur]) # Recursive call for path between remaining cities
                if temp[0] + distances[j][cur] < minDist:
                    minDist = temp[0] + distances[j][cur]
                    minPath = temp[1]
                
        memo[cur][mask] = (minDist, minPath) # Write to memo
        return (minDist, minPath)

    ans = 10**9
    ansPath = []
    for i in range(0, n):
        if ans > TSP(i, (1 << (n))-1, [])[0] + distValues[i][1]:
            ans = TSP(i, (1 << (n))-1, [])[0] + distValues[i][1]
            ansPath =  TSP(i, (1 << (n))-1, [])[1] + [i]
    
    print("The cost of most efficient tour = " + str(ans))
    print("The path of the most efficient tour = " + str(ansPath))

TSPSol(14, distances)