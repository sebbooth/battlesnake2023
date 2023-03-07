import copy

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def list_subtract(lst1, lst2):
    lst3 =  [value for value in lst1 if value not in lst2]
    return lst3

def find_snake_heads(snakes):
    snake_heads = {}
    for snake in snakes:
        snake_heads[snake] = snakes[snake][0]
    return snake_heads

def find_snakes(matrix):
    snakes = {}
    for x in range(0,len(matrix)):
        for y in range(len(matrix[0])):
            try:
                if matrix[x][y][0] != 'f':
                    snakes[matrix[x][y]] = [x,y]
            except:
                pass
    sorted_snakes = [snake for snake in snakes]

    sorted_snakes.sort(key=lambda x: -int(x[1:]))

    #print(sorted_snakes)
    snakeList = {}
    for seg in sorted_snakes:
        if seg[0] not in snakeList:
            snakeList[seg[0]] = [seg]
        else:
            snakeList[seg[0]].append(seg)

    #print(snakeList)
    full_snakes = {}
    for snake in snakeList:
        full_snakes[snake] = []
        for seg in sorted_snakes:
            if seg[0] == snake:
                full_snakes[snake].append(snakes[seg])
        for n in range(1,int(snakeList[snake][-1][1:])):
            full_snakes[snake].append([])
    
    """
    snakeList = []
    for seg in sorted_snakes:
       if seg[0] not in snakeList:
          snakeList.append(seg[0])

    full_snakes = {}
    for snake in snakeList:
        full_snakes[snake] = []
        for seg in sorted_snakes:
            if seg[0] == snake:
                full_snakes[snake].append(snakes[seg])
    """
    #print(full_snakes)
    return full_snakes

def print_bfs_matrix(matrix):
    print('_'*20)

    for y in reversed(range(0,len(matrix))):
        for x in range(0,len(matrix[0])):
            if isinstance(matrix[x][y], int):
                print('{:3s}'.format(str(matrix[x][y])), end="")

            #print food green
            elif matrix[x][y] == 'f':
                print('\033[92m'+'{:3s}'.format(str(matrix[x][y])),end="\033[0m")

            #print nomans
            elif matrix[x][y][0] == 'N':
                print('\u001b[30m'+'{:3s}'.format('X'),end="\033[0m")


            #print you yellow
            elif matrix[x][y][0] == 'A':
                print('\u001b[33m'+'{:3s}'.format(str(matrix[x][y][1:])),end="\033[0m")

            # B is blue
            elif matrix[x][y][0] == 'B':
                print('\u001b[34m'+'{:3s}'.format(str(matrix[x][y][1:])),end="\033[0m")

            # C is magenta
            elif matrix[x][y][0] == 'C':
                print('\u001b[35m'+'{:3s}'.format(str(matrix[x][y][1:])),end="\033[0m")

            #print other snakes red
            else:
                print('\u001b[31m'+'{:3s}'.format(str(matrix[x][y][1:])),end="\033[0m")

        print()
        print()

def neighbours(matrix, node):
    w = len(matrix)
    h = len(matrix[0])
    nbrs = []
    if node[1]+1 < h:
        nbrs.append([node[0],node[1]+1])
    if node[1]-1 >= 0:
        nbrs.append([node[0],node[1]-1])
    if node[0]-1 >= 0:
        nbrs.append([node[0]-1,node[1]])
    if node[0]+1 < w:
        nbrs.append([node[0]+1,node[1]])
    return nbrs

def all_moves(matrix):
    snakes = find_snakes(matrix)
    heads = find_snake_heads(snakes)
    moves = {'A':[],
             'B':[],
             'C':[],
             'D':[],
             'E':[],
             'F':[],
             'G':[],
             }
    for snake in snakes:
        moves[snake] = []
        for n in neighbours(matrix,heads[snake]):
            if matrix[n[0]][n[1]] == 0 or matrix[n[0]][n[1]] == 'f':
                moves[snake].append(n)
        if len(moves[snake]) == 0:
            moves[snake].append(neighbours(matrix,heads[snake])[0])
    return moves
    
def move_combs(matrix, allMoves):
    combs = []
    snakeList = []
    snakes = find_snakes(matrix)
    if len(snakes) == 0:
        return combs

    for snake in snakes:
        snakeList.append(snake)
    
    try:
        snake = snakeList.pop()
        for move in allMoves[snake]:
            combs.append({snake:move})
    except:
        pass

    while len(snakeList) != 0:
        snake = snakeList.pop()
        newCombs = []
        for move in allMoves[snake]:
            for comb in combs:
                newcomb = copy.deepcopy(comb)
                newcomb[snake] = move
                newCombs.append(newcomb)
        combs = newCombs

    return combs

def matrix_after_moves(matrix, movesSet):
    newMat = copy.deepcopy(matrix)
    snakes = find_snakes(matrix)
    newSnakes = copy.deepcopy(snakes)
    #print(snakes)
    for snake in snakes:
        for snake2 in snakes:
            if snake!=snake2:
                if movesSet[snake] == movesSet[snake2]:
                    if len(snakes[snake]) > len(snakes[snake2]):
                        newSnakes[snake2] = []
                    elif len(snakes[snake]) < len(snakes[snake2]):
                        newSnakes[snake] = []
                    else:
                        newSnakes[snake] = []
                        newSnakes[snake] = []
        
        if len(newSnakes[snake]) != 0:
            newSnakes[snake].pop()
            newSnakes[snake].insert(0,movesSet[snake])
            if matrix[movesSet[snake][0]][movesSet[snake][1]] == 'f':
                newSnakes[snake].append([])

    for x in range(0,len(newMat)):
        for y in range(0,len(newMat[0])):
            if newMat[x][y] != 0 and newMat[x][y] != 'f':
                newMat[x][y] = 0
    
    for snake in snakes:
        if len(snake)!=0:
            life = len(newSnakes[snake])
            for seg in newSnakes[snake]:
                if len(seg)!=0:
                    newMat[seg[0]][seg[1]] = snake+str(life)                
                life -=1
                
    #print_bfs_matrix(newMat)
    return newMat

def all_children(matrix, evalSnake):
    allMoves = all_moves(matrix)
    moveCombs = move_combs(matrix, allMoves)
    
    children = {}
    for move in allMoves[evalSnake]:
        children[evalSnake+str(move)] = []

        for moveSet in moveCombs:
            if moveSet[evalSnake]==move:
                children[evalSnake+str(move)].append(matrix_after_moves(matrix,moveSet))
    
    return children

def move_to_turn(matrix, move):
    snakes = find_snakes(matrix)
    heads = find_snake_heads(snakes)

    start = heads[move[0]]
    end = [int(n) for n in move[2:-1].split(", ")]

    if start[0] != end[0]:
        if start[0] > end[0]:
            return "left"
        else:
            return "right"
    elif start[1] > end[1]:
        return "down"
    else:
        return "up"