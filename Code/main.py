import pygame
import chess
import time

# --- Configuration ---
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
COLORS = [pygame.Color("#eeeed2"), pygame.Color("#769656")]

# --- AI Logic ---
PIECE_VALUES = {chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30, 
                chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900}

def evaluate_board(board):
    if board.is_checkmate(): return -9999 if board.turn else 9999
    if board.is_stalemate(): return 0
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

# --- UI & Sound Helpers ---
IMAGES = {}
def load_assets():
    # Load Piece Images
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load(f"assets/{p}.png"), (SQ_SIZE, SQ_SIZE))
    
    # Load ONLY Move/Capture Sounds
    global MOVE_SOUND, CAPTURE_SOUND
    MOVE_SOUND = pygame.mixer.Sound("assets/move.wav")
    CAPTURE_SOUND = pygame.mixer.Sound("assets/capture.wav")

def play_move_sound(board, move):
    if board.is_capture(move): CAPTURE_SOUND.play()
    else: MOVE_SOUND.play()

def draw_end_screen(screen, text):
    # Dark semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Victory/Loss Text
    font = pygame.font.SysFont("Arial", 40, bold=True)
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 20)))
    
    # Restart Prompt
    sub_font = pygame.font.SysFont("Arial", 20)
    sub_surf = sub_font.render("Press 'R' to Restart", True, (200, 200, 200))
    screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))

def draw_game(screen, board, selected):
    for r in range(8):
        for c in range(8):
            color = COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if selected == chess.square(c, 7-r):
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            name = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            screen.blit(IMAGES[name], (chess.square_file(sq)*SQ_SIZE, (7-chess.square_rank(sq))*SQ_SIZE))

# --- Main Logic ---
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python AI Chess")
    load_assets()
    
    board = chess.Board()
    selected_sq = None
    running = True

    while running:
        # 1. AI Turn (Black)
        if not board.is_game_over() and board.turn == chess.BLACK:
            best_move = None
            best_val = float('inf')
            for move in board.legal_moves:
                board.push(move)
                val = minimax(board, 2, -float('inf'), float('inf'), True)
                board.pop()
                if val < best_val:
                    best_val, best_move = val, move
            if best_move:
                play_move_sound(board, best_move)
                board.push(best_move)

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not board.is_game_over():
                if board.turn == chess.WHITE:
                    pos = pygame.mouse.get_pos()
                    sq = chess.square(pos[0]//SQ_SIZE, 7 - (pos[1]//SQ_SIZE))
                    if selected_sq is None:
                        if board.piece_at(sq): selected_sq = sq
                    else:
                        move = chess.Move(selected_sq, sq)
                        if move in board.legal_moves:
                            play_move_sound(board, move)
                            board.push(move)
                        selected_sq = None
            
            # Restart logic remains
            if event.type == pygame.KEYDOWN and board.is_game_over():
                if event.key == pygame.K_r:
                    board.reset()

        # 3. Drawing
        draw_game(screen, board, selected_sq)
        
        if board.is_game_over():
            res = board.result()
            msg = "White Wins!" if res == "1-0" else "Black Wins!" if res == "0-1" else "Draw!"
            draw_end_screen(screen, msg)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
