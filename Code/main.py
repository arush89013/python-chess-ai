import chess
import time

# Evaluation constants
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def evaluate_board(board):
    """
    Evaluates the board state. 
    Positive favors White (Human), Negative favors Black (AI).
    """
    if board.is_checkmate():
        return -9999 if board.turn else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Recursive Minimax with Alpha-Beta Pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_ai_move(board, depth):
    """
    Finds the best move for the AI (playing as Black).
    """
    best_move = None
    best_value = float('inf')  # AI wants to minimize the score (Black)

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -float('inf'), float('inf'), True)
        board.pop()
        if board_value < best_value:
            best_value = board_value
            best_move = move
    return best_move

def play_game():
    board = chess.Board()
    print("--- Python AI Chess: You (White) vs AI (Black) ---")
    print("Enter moves in UCI format (e.g., e2e4).")

    while not board.is_game_over():
        print("\n", board)
        
        if board.turn == chess.WHITE:
            # Human Turn
            move_str = input("\nYour move (White): ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("❌ Illegal move. Try again.")
            except ValueError:
                print("⚠️ Invalid format. Use e2e4 style.")
        else:
            # AI Turn
            print("\nAI is thinking...")
            start_time = time.time()
            move = get_ai_move(board, 3)
            end_time = time.time()
            
            board.push(move)
            print(f"AI moved: {move} (calculated in {end_time - start_time:.2f}s)")

    print("\n--- GAME OVER ---")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    play_game()
