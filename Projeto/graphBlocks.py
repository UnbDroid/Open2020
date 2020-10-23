import sys
import copy




# matrix = [
#    ['R', 0],
#    ['G', 0],
#    ['W', 1],
#    ['B', 2],
#    ['Y', 2]
# ]
matrix = [
    ['R', 0],
    ['W', 1],   
    ['G', 7],
    ['B', 4]
]

delivery_locals = {'R': [74], 'Y': [73, 75], 'B': [72, 76], 'G': [71, 77], 'W': [14]}
stock_locals = {0: 32, 1: 33, 2: 42, 3:43, 4: 35, 5: 36, 6: 45, 7: 46}
blockPoints = {'W': 750, 'R': 100, 'Y': 100, 'B': 100, 'G': 100}
initialPosition = 11

n = len(matrix)+1
print(n)
all_sets = []
g = {}
p = []

def BlockDistances(start, end):
    path = 14 #maximum path
    option = 0
    count = -1
    if (type(end) == int):
        path = abs(int(start/10) -  int(end/10)) + abs((start % 10) - (end % 10))
    else:
        for i in range(len(end)):
            count += 1
            possiblePlaces = end[i]       
            newpath = abs(int(start/10) -  int(possiblePlaces/10)) + abs((start % 10) - (possiblePlaces % 10))
            if (newpath < path):
                path = newpath
                option = count
    print(start, end, path)
    return path, option
        


def createGraphBlocks(matrix):
    graphBlocks = []
    for i in range(len(matrix)+1):
        aux = []
        for j in range(len(matrix)+1):
            aux.append(0)
        graphBlocks.append(aux)
    for i in range(len(matrix)):
        path, ignore = BlockDistances(initialPosition, stock_locals[matrix[i][1]])
        graphBlocks[0][i+1] = float(path)/blockPoints[matrix[i][0]]
        path, ignore = BlockDistances(stock_locals[matrix[i][1]], delivery_locals[matrix[i][0]])
        graphBlocks[i+1][0] = float(path)/blockPoints[matrix[i][0]]
    for i in range(len(matrix)):
        leaveBlock, localLeft = BlockDistances(stock_locals[matrix[i][1]], delivery_locals[matrix[i][0]])
        for k in range(len(matrix)):
            if (i != k): 
                nextBlock, ignore = BlockDistances(delivery_locals[matrix[i][0]][localLeft], stock_locals[matrix[k][1]])
                totalpath = leaveBlock + nextBlock

                graphBlocks[i+1][k+1] = float(totalpath)/blockPoints[matrix[i][0]]
    
    print(graphBlocks)
    return graphBlocks

def get_path(matrix):
    for x in range(1, n):
        g[x + 1, ()] = matrix[x][0]
    rest = (2,)
    for i in range(3, len(matrix) + 1):
        rest = rest + (i,)
    print(rest)
        
    #rest = (2,3,4, 5, 6)
    get_minimum(1, rest, matrix)
    order = [1]

    #print('\n\nSolution to TSP: {1, ', '')
    solution = p.pop()
    #print(int(solution[1][0]))
    order.append(int(solution[1][0]))
    for x in range(n - 2):
        for new_solution in p:
            if tuple(solution[1]) == new_solution[0]:
                solution = new_solution
                #print(int(solution[1][0]))
                order.append(int(solution[1][0]))
                break
    #print('1}')
    print(order)
    return


def get_minimum(k, a, matrix):
    if (k, a) in g:
        # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
        return g[k, a]

    values = []
    all_min = []
    for j in a:
        set_a = copy.deepcopy(list(a))
        set_a.remove(j)
        all_min.append([j, tuple(set_a)])
        result = get_minimum(j, tuple(set_a), matrix)
        values.append(matrix[k-1][j-1] + result)

    # get minimun value from set as optimal solution for
    g[k, a] = min(values)
    p.append(((k, a), all_min[values.index(g[k, a])]))

    return g[k, a]


get_path(createGraphBlocks(matrix))

#print(blockPoints['W'])