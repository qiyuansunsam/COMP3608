import sys, time
evaluation_cache = {}
def evaluation(state, player, row, col):
    cache_key = (tuple(state), player, row, col)
    if cache_key not in evaluation_cache:
        evaluation_cache[cache_key] = score2(state, player, row, col) if player == "red" else -score2(state, player, row, col)
    return evaluation_cache[cache_key]

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
            if state[r][c] == player[0]:
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
        "red" : max,
        "yellow" : min
    }
    #order of going form middle
    order = [3, 2, 4, 1, 5, 0, 6]

    max_depth = 7
    alpha = -2**63
    beta = 2**63
    depth = max_depth
    node_count = 0
    play_col = 0
    state = contents.split(",")
    def minimax(state, player, depth, alpha, beta, row, col):
        nonlocal play_col
        next_player = "red" if player == "yellow" else "yellow"

        terminal_test = evaluation(state, next_player, row, col)
        if abs(terminal_test) == 10000:
            return terminal_test
        
        scores = []
        cols = []
        score = 0
        if depth == 0:
            return evaluation(state, player, row, col)
        
        for col in order:
            #check if the column is playable
            for row in range(6):
                if state[row][col] == ".":
                    new_state = state.copy()
                    new_state[row] = new_state[row][:col] + player[0] + new_state[row][col+1:]
                    #print(new_state)
                    score = minimax(new_state, next_player, depth - 1, alpha, beta, row, col)
                    scores.append(score)
                    cols.append(col)
                    break
            if player == "red" and score:
                alpha = max(score, alpha)
            if player == "yellow" and score:
                beta = min(score, beta)
            if alpha >= beta:
                return score
        
        #please do make better of determining the move, I cant think of any, those I tried bugged horribly...
        best_score = dict[player](scores)
        if depth == max_depth:
            index = scores.index(best_score)
            while state[5][cols[index]] != "." and index < 7:
                index += 1
            play_col = cols[index]
        return best_score
    minimax(state, turn, depth, alpha, beta, 0, 0)
    #print(score2('...rrrr,.......,.......,.......,.......,.......'.split(","), "red", 0, 6))
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