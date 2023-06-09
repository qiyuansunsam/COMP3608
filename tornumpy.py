import time, sys, joblib
import numpy as np

#memory = joblib.Memory(location='./cache', verbose=0)

def evaluation(state, player, row, col):
    
    start = time.time()
    score1 = score2(state, player, row, col) if player == 1 else -score2(state, player, row, col)
    end = time.time()
    print(end - start)
    return score1

#cached_evaluation = memory.cache(evaluation)

def score2(state, player, row, col):
    def update_score(consecutive, score):
        score += 10 ** consecutive
        if consecutive == 4:
            return 10000, True
        return score, False

    score = 0
    consecutive = 0
    directions = [
        (1, 1, row - min(row, col), col - min(row, col)),
        (-1, 1, row + min(5 - row, col), col - min(5 - row, col)),
        (0, 1, row, 0),
        (1, 0, 0, col),
    ]


    for dr, dc, r_start, c_start in directions:
        r, c = r_start, c_start
        consecutive = 0
        while 0 <= r < 6 and 0 <= c < 7:
            if state[r][c] == player:
                consecutive += 1
                score, done = update_score(consecutive, score)
                if done:
                    return score
            else:
                consecutive = 0
            r += dr
            c += dc

    return score



def connect_four(contents, turn):
    dict = {
        1 : max,
        2 : min
    }
    #order of going form middle
    order = [3, 2, 4, 1, 5, 0, 6]

    max_depth = 2
    alpha = -2**63
    beta = 2**63
    depth = max_depth
    node_count = 0
    play_col = 0
    state = contents.split(",")
    turn = 1 if player == "red" else 2

    def map_element(element):
        if element == '.':
            return 0
        elif element == 'r':
            return 1
        elif element == 'y':
            return 2
    
    # Split the input string by ',' and create a NumPy array
    rows = contents.split(",")
    input_array = np.array([list(row) for row in rows])

    # Vectorize the mapping function
    vectorized_map = np.vectorize(map_element)

    # Apply the mapping function to the input array
    state = vectorized_map(input_array)

    node_count = 0
    def minimax(state, player, depth, alpha, beta, row, col):
        nonlocal play_col, node_count
        next_player = 1 if player == 2 else 2

        terminal_test = evaluation(state, next_player, row, col)
        if abs(terminal_test) == 10000:
            return terminal_test
        node_count += 1
        scores = []
        cols = []
        score = 0
        if depth == 0:
            return evaluation(state, player, row, col)
        
        for col in order:
            #check if the column is playable
            for row in range(6):
                if state[row][col] == 0:
                    
                    new_state = state.copy()
                    new_state[row][col] = player
                    #print(new_state)
                    score = minimax(new_state, next_player, depth - 1, alpha, beta, row, col)
                    scores.append(score)
                    cols.append(col)
                    break
            
            
            if player == 1 and score:
                alpha = max(score, alpha)
            if player == 2 and score:
                beta = min(score, beta)
            if alpha >= beta:
                return score
        
        #please do make better of determining the move, I cant think of any, those I tried bugged horribly...
        best_score = dict[player](scores)
        if depth == max_depth:
            index = scores.index(best_score)
            while state[5][cols[index]] != 0 and index < 7:
                index += 1
            play_col = cols[index]
        return best_score
    minimax(state, turn, depth, alpha, beta, 0, 0)
    #print(score2('...rrrr,.......,.......,.......,.......,.......'.split(","), "red", 0, 6))
    print(node_count)
    return play_col

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        #board = '...r...,...y...,.......,.......,.......,.......'
        board = '.ryyrry,.rryry.,..yrrr.,..yyy..,.......,.......'
        #board = 'r.ryr..,r.ryy..,r.ryr..,y.yry..,..ryr..,..yy...'
        player = 'red'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    s = time.time()
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four(board, player))
    e = time.time()
    print(e - s)