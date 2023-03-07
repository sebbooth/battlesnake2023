from matOps import *
from territories import *

def eval_matrix(matrix, evalSnake):
    
    terr = territories(matrix)
    if evalSnake not in terr:
        return float('-inf')
    numSnakes = 0
    tot = 0
    for snake in terr:
        if snake != evalSnake:
            numSnakes += 1
            tot += terr[evalSnake] / terr[snake]
    if numSnakes == 0:
        return float('inf')
    return tot/numSnakes


def minimax_matrix(children, evalSnake, depth, maxMin=float('-inf'), minMax=float('inf')):
  minChildren = []

  for move in children:
    minEval = float('inf')
    if depth == 1:
      for child in children[move]:
        eval = eval_matrix(child, evalSnake)
        if eval<=minEval:
          minEval = eval
          minChildren = [val for val in minChildren if val[0] != move]
          minChildren.append([move, eval, copy.deepcopy(child)])
          
          maxMin = max([val[1] for val in minChildren])
          minMax = min(minMax, eval)
          if minMax <= maxMin:
            continue
          
          if minEval == float('-inf'):
            break
  
    else:
      for child in children[move]:
        childChildren = all_children(child, evalSnake)

        try:
            eval = minimax_matrix(childChildren, evalSnake, depth-1, maxMin, minMax)[0][1]
        except:
            #print(print_bfs_matrix(child))
            eval = float('-inf')

        if eval<=minEval:
          minEval = eval
          minChildren = [val for val in minChildren if val[0] != move]
          minChildren.append([move, eval, copy.deepcopy(child)])

          maxMin = max([val[1] for val in minChildren])
          minMax = min(minMax, eval)
          if minMax <= maxMin:
            continue
          
          if minEval == float('-inf'):
            break
  
  minChildren.sort(key=lambda x: -x[1])
  return minChildren