import pygame
import chess
import time

# --- Configuration ---
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
COLORS = [pygame.Color("#eeeed2"), pygame.Color("#769656")] # Classic Lichess colors

# --- AI Logic (Minimax + Alpha-Beta) ---
PIECE_VALUES = {chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30, 
                chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900}

def evaluate_board(board):
    if board.is_checkmate(): return -9999 if board.turn else 9999
    score = 0
    for pt, val in PIECE_VALUES.items():
        score += len(board.pieces(pt, chess.WHITE)) * val
        score -= len(board.pieces(pt, chess.BLACK)) * val
    return score

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over(): return evaluate_board(board)
    if maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            max_eval = max(max_eval, minimax(board, depth-1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, max_eval)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            min_eval = min(min_eval, minimax(board, depth-1, alpha, beta, True))
            board.pop()
            beta = min(beta, min_eval)
            if beta <= alpha: break
        return min_eval

# --- UI Logic ---
IMAGES = {}

def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for p in pieces:
        # Note: Ensure these files exist in your 'assets' folder!
        try:
            IMAGES[p] = pygame.transform.scale(
                pygame.image.load(f"assets/{p}.png"), (SQ_SIZE, SQ_SIZE))
        except:
            IMAGES[p] = None # Fallback if images are missing

def draw_game_state(screen, board, selected_sq):
    # 1. Draw Board
    for r in range(8):
        for c in range(8):
            color = COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            # Highlight selection
            if selected_sq == chess.square(c, 7-r):
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

    # 2. Draw Pieces
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            color_prefix = 'w' if piece.color == chess.WHITE else 'b'
            piece_name = color_prefix + piece.symbol().upper()
            if IMAGES.get(piece_name):
                # Convert chess square to screen coordinates
                c, r = chess.square_file(sq), 7 - chess.square_rank(sq)
                screen.blit(IMAGES[piece_name], (c*SQ_SIZE, r*SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    load_images()
    board = chess.Board()
    selected_sq = None
    running = True

    while running:
        # Check for AI Turn (Black)
        if not board.is_game_over() and board.turn == chess.BLACK:
            best_val = float('inf')
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                val = minimax(board, 2, -float('inf'), float('inf'), True)
                board.pop()
                if val < best_val:
                    best_val = val
                    best_move = move
            board.push(best_move)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                location = pygame.mouse.get_pos()
                col, row = location[0] // SQ_SIZE, 7 - (location[1] // SQ_SIZE)
                sq = chess.square(col, row)

                if selected_sq is None:
                    if board.piece_at(sq): selected_sq = sq
                else:
                    move = chess.Move(selected_sq, sq)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_sq = None

        draw_game_state(screen, board, selected_sq)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
