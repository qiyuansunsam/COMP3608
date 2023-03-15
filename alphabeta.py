def utility(state):
   if num_in_a_row(4, state, "red") > 0 :
       return 10000
   if num_in_a_row(4, state, "yellow") > 0:
       return -10000

def evaluation(state):
  return score(state, "red") - score(state, "yellow")

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


def connect_four_ab(contents, turn, max_depth):
    dict = {
        "red" : max,
        "yellow" : min
    }
    alpha = -2**63
    beta = 2**63
    depth = max_depth
    node_count = 0
    play_col = 0
    state = contents.split(",")
    num_rows = len(state)
    num_cols = len(state[0])
    def minimax(state, player, depth, alpha, beta):
        nonlocal node_count, play_col
        node_count += 1 
    
        terminal_test = utility(state)
        if terminal_test:
            return terminal_test
        
        next_player = "red" if player == "yellow" else "yellow"
        best_score = -2**63
        scores = []
        score = 0
        if depth == 0:
            return evaluation(state)
        for col in range(num_cols):
            #check if the column is playable
            for row in range(num_rows):
                if state[row][col] == ".":
                    new_state = state.copy()
                    new_state[row] = new_state[row][:col] + player[0] + new_state[row][col+1:]
                    #print(new_state)
                    score = minimax(new_state, next_player, depth - 1, alpha, beta)
                    scores.append(score)
                    break
                
            best_score = dict[player](scores)
            if player == "red":
                alpha = max(score, alpha)
            if player == "yellow":
                beta = min(score, beta)
            if alpha >= beta:
                return score
        if depth == max_depth:
            play_col = scores.index(best_score)
        return best_score
    minimax(state, turn, depth, alpha, beta)
    return f'{play_col}\n{node_count}'

if __name__ == '__main__':
    # Example function call below, you can add your own to test the connect_four_mm function
    print(connect_four_ab(".ryyrry,.rryry.,..y.r..,..y....,.......,.......", "red", 4))