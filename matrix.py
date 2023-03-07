def board_matrix(game_state):
    board = game_state["board"]
    snakes = ['A','B','C','D','E','F','G','H']
    matrix = [[0 for col in range(board['width'])] for row in range(board['height'])]
    snakeNum = 0

    life = 1
    for seg in reversed(game_state["you"]["body"]):
        matrix[seg["x"]][seg["y"]] = snakes[snakeNum] + str(life)
        life +=1
    snakeNum+=1


    for snake in board['snakes']:
        if snake != game_state["you"]:
            life = 1
            for seg in reversed(snake["body"]):
                matrix[seg["x"]][seg["y"]] = snakes[snakeNum] + str(life)
                life +=1
            snakeNum+=1

    for food in board['food']:
        matrix[food["x"]][food["y"]] = "f"
        
    return matrix