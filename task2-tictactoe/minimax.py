from game import check_winner, is_draw, get_empty_cells

def minimax(board, depth, is_maximizing):
    # Base cases — game khatam hua?
    if check_winner(board, "O"):   # AI jeeta
        return 10 - depth
    if check_winner(board, "X"):   # Human jeeta
        return depth - 10
    if is_draw(board):             # Draw
        return 0

    if is_maximizing:
        # AI ki turn — best (maximum) score dhundo
        best_score = -1000
        for (i, j) in get_empty_cells(board):
            board[i][j] = "O"
            score = minimax(board, depth + 1, False)
            board[i][j] = " "
            best_score = max(best_score, score)
        return best_score
    else:
        # Human ki turn — worst (minimum) score dhundo
        best_score = 1000
        for (i, j) in get_empty_cells(board):
            board[i][j] = "X"
            score = minimax(board, depth + 1, True)
            board[i][j] = " "
            best_score = min(best_score, score)
        return best_score

def best_move(board):
    best_score = -1000
    move = None
    for (i, j) in get_empty_cells(board):
        board[i][j] = "O"
        score = minimax(board, 0, False)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move