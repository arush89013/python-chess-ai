import pygame
import chess
import time

# --- Configuration ---
WIDTH, HEIGHT = 512, 600  # Increased height to fit the UI bar
BOARD_HEIGHT = 512
SQ_SIZE = WIDTH // 8
COLORS = [pygame.Color("#f0d9b5"), pygame.Color("#b58863")]

# Difficulty Settings
DIFFICULTIES = {
    "EASY": 1,
    "MEDIUM": 2,
    "HARD": 3
}
current_diff = "MEDIUM"

# --- AI Logic ---
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
            max_eval = max(max_eval, minimax(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, max_eval)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            min_eval = min(min_eval, minimax(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, min_eval)
            if beta <= alpha: break
        return min_eval


# --- UI Helpers ---
IMAGES = {}


def load_assets():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for p in pieces:
        IMAGES[p] = pygame.transform.scale(pygame.image.load(f"assets/{p}.png"), (SQ_SIZE, SQ_SIZE))

    global ADDR_FONT, UI_FONT, MOVE_SOUND, CAPTURE_SOUND
    pygame.font.init()
    ADDR_FONT = pygame.font.SysFont("Arial", 11, bold=True)
    UI_FONT = pygame.font.SysFont("Arial", 18, bold=True)
    MOVE_SOUND = pygame.mixer.Sound("assets/move.wav")
    CAPTURE_SOUND = pygame.mixer.Sound("assets/capture.wav")


def draw_ui(screen):
    # Draw bottom panel
    pygame.draw.rect(screen, (40, 40, 40), pygame.Rect(0, BOARD_HEIGHT, WIDTH, 88))

    # Draw Difficulty Buttons
    x_pos = 20
    for diff in DIFFICULTIES.keys():
        color = (255, 255, 255) if diff == current_diff else (100, 100, 100)
        text_surf = UI_FONT.render(diff, True, color)
        screen.blit(text_surf, (x_pos, BOARD_HEIGHT + 30))
        # Store rects for clicking logic if needed, or just use coordinates
        x_pos += 150


def draw_game(screen, board, selected):
    for r in range(8):
        for c in range(8):
            color = COLORS[(r + c) % 2]
            rect = pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)

            sq_id = chess.square(c, 7 - r)
            addr_text = chess.square_name(sq_id)
            text_color = (139, 69, 19) if (r + c) % 2 == 0 else (245, 245, 220)
            addr_surf = ADDR_FONT.render(addr_text, True, text_color)
            screen.blit(addr_surf, (c * SQ_SIZE + 5, r * SQ_SIZE + 5))

            if selected == sq_id:
                pygame.draw.rect(screen, (255, 255, 0), rect, 3)

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            name = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
            screen.blit(IMAGES[name], (chess.square_file(sq) * SQ_SIZE, (7 - chess.square_rank(sq)) * SQ_SIZE))


def main():
    global current_diff
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI - Difficulty Select")
    load_assets()

    board = chess.Board()
    selected_sq = None
    running = True
    ai_thinking_start = None

    while running:
        # AI Turn
        if not board.is_game_over() and board.turn == chess.BLACK:
            if ai_thinking_start is None: ai_thinking_start = time.time()
            if time.time() - ai_thinking_start >= 1.0:
                # Use the DEPTH from our current difficulty
                depth = DIFFICULTIES[current_diff]
                best_move = None;
                best_val = float('inf')
                for move in board.legal_moves:
                    board.push(move)
                    val = minimax(board, depth, -float('inf'), float('inf'), True)
                    board.pop()
                    if val < best_val: best_val, best_move = val, move
                if best_move:
                    if board.is_capture(best_move):
                        CAPTURE_SOUND.play()
                    else:
                        MOVE_SOUND.play()
                    board.push(best_move)
                ai_thinking_start = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check if click is in the UI Bar (Difficulty Selection)
                if pos[1] > BOARD_HEIGHT:
                    if 20 <= pos[0] <= 120:
                        current_diff = "EASY"
                    elif 170 <= pos[0] <= 270:
                        current_diff = "MEDIUM"
                    elif 320 <= pos[0] <= 420:
                        current_diff = "HARD"

                # Board Clicks
                elif not board.is_game_over() and board.turn == chess.WHITE:
                    sq = chess.square(pos[0] // SQ_SIZE, 7 - (pos[1] // SQ_SIZE))
                    if selected_sq is None:
                        if board.piece_at(sq): selected_sq = sq
                    else:
                        move = chess.Move(selected_sq, sq)
                        if move in board.legal_moves:
                            if board.is_capture(move):
                                CAPTURE_SOUND.play()
                            else:
                                MOVE_SOUND.play()
                            board.push(move)
                        selected_sq = None

        screen.fill((0, 0, 0))
        draw_game(screen, board, selected_sq)
        draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
