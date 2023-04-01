import time, sys
def utility(state):
   if num_in_a_row(4, state, "red") > 0 :
       return 10000
   if num_in_a_row(4, state, "yellow") > 0:
       return -10000

def evaluation(state, row, col):
  return score(state, "red") - score(state, "yellow")
"""
def score2(state, player, row, col):
    score = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    consecitive = 0
    while start_row < 6 and start_col < 7:
        if state[start_row][start_col] == player[0]:
            consecitive += 1
            if consecitive > 1:
                score += 10**consecitive
        else:
            consecitive = 0
        start_col += 1
        start_row += 1

    start_row = row + min(5 - row, col)
    start_col = col - min(5 - row, col)
    consecitive = 0
    while start_row >= 0 and start_col < 7:
        if state[start_row][start_col] == player[0]:
            consecitive += 1
            if consecitive > 1:
                score += 10**consecitive
        else:
            consecitive = 0
        start_col += 1
        start_row -= 1
    
    for i in range(7):
        if state[row][i] == player[0]:
            consecitive += 1
            if consecitive > 1:
                score += 10**consecitive
        else:
            consecitive = 0

    for i in range(6):
        if state[i][col] == player[0]:
            consecitive += 1
            if consecitive > 1:
                score += 10**consecitive
        else:
            consecitive = 0

    return score
"""
def score(state, player):
  three_in_a_row = num_in_a_row(3, state, player) 
  two_in_a_row = num_in_a_row(2, state, player) - 2 * three_in_a_row 
  return state.count(player[0]) + \
      10 * two_in_a_row + \
      100 * three_in_a_row
      
def num_in_a_row(count, state, player):
    p = player[0]
    num_rows = len(state)
    num_cols = len(state[0])
    num = 0
    
    # Check rows for consecutive pieces
    for row in range(num_rows):
        for col in range(num_cols - count + 1):
            if state[row][col:col+count] == p*count:
                num += 1
    
    # Check columns for consecutive pieces
    for col in range(num_cols):
        for row in range(num_rows - count + 1):
            if [state[row + i][col] for i in range(count)] == [p]*count:
                num += 1
    
    # Check diagonals for consecutive pieces
    for row in range(num_rows - count + 1):
        for col in range(num_cols - count + 1):
            if [state[row+i][col+i] for i in range(count)] == [p]*count:
                num += 1
            if [state[row+i][col+count-i-1] for i in range(count)] == [p]*count:
                num += 1
    
    return num


def connect_four(contents, turn):
    dict = {
        "red" : max,
        "yellow" : min
    }
    order = [3, 4, 2, 5, 1, 6, 0]
    max_depth = 6
    alpha = -2**63
    beta = 2**63
    depth = max_depth
    node_count = 0
    play_col = 0
    state = contents.split(",")
    def minimax(state, player, depth, alpha, beta, row, col):
        nonlocal node_count, play_col
    
        terminal_test = utility(state)
        if terminal_test:
            return terminal_test
        node_count += 1 
        
        next_player = "red" if player == "yellow" else "yellow"
        scores = []
        score = 0
        if depth == 0:
            return evaluation(state, row, col)
        
        col = 3
        #check if the column is playable
        for row in range(6):
            if state[row][col] == ".":
                new_state = state.copy()
                new_state[row] = new_state[row][:col] + player[0] + new_state[row][col+1:]
                #print(new_state)
                score = minimax(new_state, next_player, depth - 1, alpha, beta, row, col)
                scores.append(score)
                break
            
        if player == "red":
            alpha = max(score, alpha)
        if player == "yellow":
            beta = min(score, beta)
        if alpha >= beta:
            return score
        
        for increment in range(1,4):
            col = 3 + increment
            #check if the column is playable
            for row in range(6):
                if state[row][col] == ".":
                    new_state = state.copy()
                    new_state[row] = new_state[row][:col] + player[0] + new_state[row][col+1:]
                    #print(new_state)
                    score = minimax(new_state, next_player, depth - 1, alpha, beta, row, col)
                    scores.append(score)
                    break
                
            if player == "red":
                alpha = max(score, alpha)
            if player == "yellow":
                beta = min(score, beta)
            if alpha >= beta:
                return score
            
            col = 3 - increment
            #check if the column is playable
            for row in range(6):
                if state[row][col] == ".":
                    new_state = state.copy()
                    new_state[row] = new_state[row][:col] + player[0] + new_state[row][col+1:]
                    #print(new_state)
                    score = minimax(new_state, next_player, depth - 1, alpha, beta, row, col)
                    scores.append(score)
                    break
                
            if player == "red":
                alpha = max(score, alpha)
            if player == "yellow":
                beta = min(score, beta)
            if alpha >= beta:
                return score
                 
        best_score = dict[player](scores)
        if depth == max_depth:
            play_col = order[scores.index(best_score)]
        return best_score
    minimax(state, turn, depth, alpha, beta, 0, 0)
    return f'{play_col}\n{node_count}'

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # You can modify these values to test your code
        board = '.......,.......,.......,.......,.......,.......'
        #board = '.ryyrry,.rryry.,..y.r..,..y....,.......,.......'
        player = 'red'
    else:
        board = sys.argv[1]
        player = sys.argv[2]
    s = time.time()
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four(board, player))
    e = time.time()
    print(e - s)