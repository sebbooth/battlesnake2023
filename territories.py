import copy
from matOps import * 

def territories(matrix):
    layer = 0
    noMansLand = {}

    mat = copy.deepcopy(matrix)
    territories = {}
    heads = find_snake_heads(find_snakes(matrix))
    for snake in heads:
       territories[snake] = {layer:[heads[snake]]}
    #print(territories)

    layerSize = 0
    for snake in territories:
        layerSize += len(territories[snake][layer])  

    while layerSize != 0:
        layer+=1
        for snake in territories:
            territories[snake][layer] = []
            for node in territories[snake][layer-1]:
                for nbr in neighbours(mat,node):
                    if mat[nbr[0]][nbr[1]] == 'f':
                        mat[nbr[0]][nbr[1]] = 0

                    if mat[nbr[0]][nbr[1]] == 0:
                        if nbr not in territories[snake][layer]:
                            territories[snake][layer].append(nbr)
                    
                    elif mat[nbr[0]][nbr[1]][1] != "T":
                        if int(mat[nbr[0]][nbr[1]][1:]) <= layer:
                            if nbr not in territories[snake][layer]:
                                territories[snake][layer].append(nbr)

        noMansLand[layer] = []
        for snake1 in territories:
            for snake2 in territories:
                if snake1 != snake2:
                    noMansLand[layer] += intersection(territories[snake1][layer],territories[snake2][layer])
                    territories[snake1][layer] = list_subtract(territories[snake1][layer], noMansLand[layer])
                    territories[snake2][layer] = list_subtract(territories[snake2][layer], noMansLand[layer])

        #print(noMansLand)
        for n in noMansLand[layer]:
            mat[n[0]][n[1]] = "N99"
        
        for snake in territories:
            for n in territories[snake][layer]:
                mat[n[0]][n[1]] = snake+"T"+str(layer)
        
        layerSize = 0
        for snake in territories:
            layerSize += len(territories[snake][layer]) 
        
        #print(layer)
        #print_bfs_matrix(mat)

    """
    for snake in territories:
        print(snake)
        for layer in territories[snake]:
            if len(territories[snake][layer]) != 0:
                print(layer)
                #print(snake, str(layer),str(len(territories[snake][layer])))
                print(territories[snake][layer])
    """
    terr_sizes = {}
    for snake in territories:
        terr_size = 0
        for layer in territories[snake]:
            terr_size += len(territories[snake][layer])
        terr_sizes[snake] = terr_size
    
    #print_bfs_matrix(mat)

    return terr_sizes
                    
    

