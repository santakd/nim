import pygame
from pygame.locals import *
import time
import logging
import sys
import math
import random

# ========================= Logging =========================
logging.basicConfig(filename='nimgame.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

nodes = 0

# ========================= Minimax with Alpha-Beta =========================
def minimax(piles, maximizing, alpha, beta):
    global nodes
    nodes += 1
    total = sum(piles)
    
    if total == 0:
        return 1 if maximizing else -1   # Player who took last stick loses
    
    if maximizing:
        best_val = -math.inf
        for row in range(3):
            for num in range(1, piles[row] + 1):
                new_piles = piles[:]
                new_piles[row] -= num
                val = minimax(new_piles, False, alpha, beta)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if alpha >= beta:
                    return best_val
        return best_val
    else:
        best_val = math.inf
        for row in range(3):
            for num in range(1, piles[row] + 1):
                new_piles = piles[:]
                new_piles[row] -= num
                val = minimax(new_piles, True, alpha, beta)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if alpha >= beta:
                    return best_val
        return best_val

def get_ai_move(piles, difficulty):
    global nodes
    nodes = 0
    start = time.time()
    
    all_moves = []
    for row in range(3):
        for num in range(1, piles[row] + 1):
            all_moves.append((row, num))
    
    if not all_moves:
        return None
    
    move_to_val = {}
    best_val = -math.inf
    best_moves = []
    
    if difficulty != 'easy':
        for move in all_moves:
            row, num = move
            new_piles = piles[:]
            new_piles[row] -= num
            val = minimax(new_piles, False, -math.inf, math.inf)
            move_to_val[move] = val
            if val > best_val:
                best_val = val
                best_moves = [move]
            elif val == best_val:
                best_moves.append(move)
    
    random_move = random.choice(all_moves)
    
    if difficulty == 'easy':
        move = random_move
        new_piles_temp = piles[:]
        new_piles_temp[move[0]] -= move[1]
        val = minimax(new_piles_temp, False, -math.inf, math.inf)
    elif difficulty == 'medium':
        if random.random() < 0.3:
            move = random_move
        else:
            move = random.choice(best_moves)
        val = move_to_val[move]
    else:  # hard
        move = random.choice(best_moves)
        val = move_to_val[move]
    
    end = time.time()
    logging.info(f"AI Move (Difficulty: {difficulty}, Player: {current_player}) → Row {move[0]+1}, Remove {move[1]} | "
                 f"Value: {val} | Nodes: {nodes} | Time: {end-start:.4f}s")
    return move

# ========================= PyGame Setup =========================
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Misère Nim")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)
tiny_font = pygame.font.SysFont(None, 24)  # For longer messages

WHITE = (245, 245, 245)
BLACK = (11, 11, 11)
BLUE = (22, 22, 245)
GREEN = (22, 245, 22)
RED = (245, 22, 22)
GRAY = (180, 180, 180)

# ========================= Helper Functions =========================
def player_name(p):
    if p == 1:
        return player1_name
    else:
        return player2_name

def is_human_turn():
    return ((current_player == 1 and player1_is_human) or 
            (current_player == 2 and player2_is_human))

def draw_board(piles, message=""):
    screen.fill(WHITE)
    row_y = [120, 240, 360]  # Moved up to give more space at bottom
    initial_counts = [3, 5, 7]
    
    # Draw scores
    score_text1 = small_font.render(f"{player1_name} Wins: {player1_wins}", True, BLACK)
    screen.blit(score_text1, (60, 30))
    score_text2 = small_font.render(f"{player2_name} Wins: {player2_wins}", True, BLACK)
    screen.blit(score_text2, (500, 30))
    
    for r in range(3):
        text = small_font.render(f"Row {r+1}: {piles[r]}/{initial_counts[r]}", True, BLACK)
        screen.blit(text, (60, row_y[r] - 35))
        for i in range(piles[r]):
            x = 220 + i * 60  # Increased spacing for clarity
            color = GREEN if r == selected_row and i in selected_set else BLUE
            pygame.draw.rect(screen, color, (x, row_y[r] - 35, 48, 85))
    
    # Draw message in two lines if needed, using smaller font
    if message:
        lines = message.split(' → ')
        if len(lines) > 1:
            msg_surf1 = small_font.render(lines[0], True, RED)
            screen.blit(msg_surf1, (60, 420))
            msg_surf2 = tiny_font.render(' → ' + lines[1], True, RED)
            screen.blit(msg_surf2, (60, 455))
        else:
            msg_surf = small_font.render(message, True, RED)
            screen.blit(msg_surf, (60, 440))
    
    if is_human_turn() and not game_over:
        btn_color = GREEN if len(selected_set) > 0 else GRAY
        pygame.draw.rect(screen, btn_color, remove_rect)
        remove_text = small_font.render("Remove", True, BLACK)
        screen.blit(remove_text, (remove_rect.x + 20, remove_rect.y + 15))
    
    if game_over:
        # Draw buttons lower to avoid overlap
        pygame.draw.rect(screen, GREEN, restart_rect)
        restart_text = small_font.render("Play Again", True, BLACK)
        screen.blit(restart_text, (restart_rect.x + 20, restart_rect.y + 15))
        
        pygame.draw.rect(screen, GREEN, change_mode_rect)
        change_text = small_font.render("Change Mode", True, BLACK)
        screen.blit(change_text, (change_mode_rect.x + 20, change_mode_rect.y + 15))
        
        pygame.draw.rect(screen, GREEN, quit_rect)
        quit_text = small_font.render("Quit", True, BLACK)
        screen.blit(quit_text, (quit_rect.x + 20, quit_rect.y + 15))
    
    pygame.display.flip()

def draw_menu():
    screen.fill(WHITE)
    title = font.render("Choose Game Mode", True, BLACK)
    screen.blit(title, (220, 80))
    
    # Button 1: Human vs AI
    pygame.draw.rect(screen, GREEN, (120, 180, 180, 110))
    screen.blit(small_font.render("Human vs AI", True, BLACK), (140, 220))
    
    # Button 2: Human vs Human
    pygame.draw.rect(screen, GREEN, (340, 180, 180, 110))
    screen.blit(small_font.render("Hotseat", True, BLACK), (380, 220))
    
    # Button 3: AI vs AI
    pygame.draw.rect(screen, GREEN, (560, 180, 180, 110))
    screen.blit(small_font.render("AI vs AI", True, BLACK), (590, 220))
    
    pygame.display.flip()

def draw_difficulty_menu():
    screen.fill(WHITE)
    title = font.render("Choose AI Difficulty", True, BLACK)
    screen.blit(title, (200, 80))
    
    # Button 1: Easy
    pygame.draw.rect(screen, GREEN, (120, 180, 180, 110))
    screen.blit(small_font.render("Easy", True, BLACK), (170, 220))
    
    # Button 2: Medium
    pygame.draw.rect(screen, GREEN, (340, 180, 180, 110))
    screen.blit(small_font.render("Medium", True, BLACK), (370, 220))
    
    # Button 3: Hard
    pygame.draw.rect(screen, GREEN, (560, 180, 180, 110))
    screen.blit(small_font.render("Hard", True, BLACK), (600, 220))
    
    pygame.display.flip()

# ========================= Initialization =========================
player1_wins = 0
player2_wins = 0

restart_rect = pygame.Rect(100, 500, 150, 50)  # Adjusted positions
change_mode_rect = pygame.Rect(280, 500, 200, 50)
quit_rect = pygame.Rect(510, 500, 100, 50)
remove_rect = pygame.Rect(600, 420, 150, 50)

selected_row = -1
selected_set = set()

just_started = True
human_turn_start = None

# ========================= Main Loop =========================
running = True
mode_selection = True
difficulty_selection = False
difficulty = 'hard'  # Default
player1_is_human = True
player2_is_human = True
player1_name = "Player 1"
player2_name = "Player 2"
piles = [3, 5, 7]
current_player = 1
game_over = False
message = ""

while running:
    clock.tick(30)

    if mode_selection:
        draw_menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 120 <= mx <= 300 and 180 <= my <= 290:          # Human vs AI
                    player1_is_human = True
                    player2_is_human = False
                    player1_name = "Human"
                    player2_name = "AI"
                    mode_selection = False
                    difficulty_selection = True
                elif 340 <= mx <= 520 and 180 <= my <= 290:        # Human vs Human
                    player1_is_human = True
                    player2_is_human = True
                    player1_name = "Player 1"
                    player2_name = "Player 2"
                    mode_selection = False
                    difficulty_selection = False
                elif 560 <= mx <= 740 and 180 <= my <= 290:        # AI vs AI
                    player1_is_human = False
                    player2_is_human = False
                    player1_name = "AI 1"
                    player2_name = "AI 2"
                    mode_selection = False
                    difficulty_selection = True
        continue

    if difficulty_selection:
        draw_difficulty_menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 120 <= mx <= 300 and 180 <= my <= 290:          # Easy
                    difficulty = 'easy'
                    difficulty_selection = False
                elif 340 <= mx <= 520 and 180 <= my <= 290:        # Medium
                    difficulty = 'medium'
                    difficulty_selection = False
                elif 560 <= mx <= 740 and 180 <= my <= 290:        # Hard
                    difficulty = 'hard'
                    difficulty_selection = False
        continue

    if just_started:
        diff_log = difficulty if not player1_is_human or not player2_is_human else 'N/A'
        logging.info(f"New game started: Mode - {player1_name} vs {player2_name}, Difficulty: {diff_log}")
        just_started = False

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN and not game_over:
            mx, my = event.pos
            if is_human_turn():
                # Check if click on remove button
                if remove_rect.collidepoint(mx, my) and len(selected_set) > 0:
                    num_remove = len(selected_set)
                    player = current_player
                    piles[selected_row] -= num_remove
                    total = sum(piles)
                    time_taken = time.time() - human_turn_start
                    if total == 0:
                        winner = 3 - current_player
                        message = f"{player_name(current_player)} took the last stick! {player_name(winner)} wins!"
                        if winner == 1:
                            player1_wins += 1
                        else:
                            player2_wins += 1
                        game_over = True
                        logging.info(f"Game ended, Winner: {player_name(winner)}")
                    else:
                        current_player = 3 - current_player
                    # Log human move
                    logging.info(f"Human Move (Player: {player}) → Row {selected_row+1}, Remove {num_remove} | "
                                 f"Value: N/A | Nodes: N/A | Time: {time_taken:.4f}s")
                    human_turn_start = None
                    selected_set.clear()
                    selected_row = -1
                    continue
                
                # Check if click on stick
                row_y = [120, 240, 360]
                clicked_row = -1
                clicked_index = -1
                for r in range(3):
                    if piles[r] > 0 and row_y[r]-60 < my < row_y[r]+80 and 220 < mx < 220 + piles[r]*60:
                        index = (mx - 220) // 60
                        if 0 <= index < piles[r]:
                            clicked_row = r
                            clicked_index = index
                            break
                
                if clicked_row != -1:
                    if selected_row != -1 and selected_row != clicked_row:
                        selected_set.clear()
                    selected_row = clicked_row
                    if clicked_index in selected_set:
                        selected_set.remove(clicked_index)
                    else:
                        selected_set.add(clicked_index)

        elif event.type == MOUSEBUTTONDOWN and game_over:
            mx, my = event.pos
            if restart_rect.collidepoint(mx, my):
                piles = [3, 5, 7]
                current_player = 1
                game_over = False
                message = ""
                selected_row = -1
                selected_set.clear()
                just_started = True
                human_turn_start = None
            elif change_mode_rect.collidepoint(mx, my):
                mode_selection = True
                just_started = True
                human_turn_start = None
            elif quit_rect.collidepoint(mx, my):
                running = False

    if game_over:
        draw_board(piles, message)
        continue

    if not game_over and is_human_turn() and human_turn_start is None:
        human_turn_start = time.time()

    # AI Turn?
    is_ai_turn = ((current_player == 1 and not player1_is_human) or 
                  (current_player == 2 and not player2_is_human))

    if is_ai_turn:
        message = f"{player_name(current_player)} (AI) thinking..."
        draw_board(piles, message)
        pygame.display.flip()
        
        row, num = get_ai_move(piles, difficulty)
        piles[row] -= num
        total = sum(piles)
        
        if total == 0:
            winner = 3 - current_player
            message = f"{player_name(current_player)} took the last stick! {player_name(winner)} wins!"
            if winner == 1:
                player1_wins += 1
            else:
                player2_wins += 1
            game_over = True
            logging.info(f"Game ended, Winner: {player_name(winner)}")
        else:
            current_player = 3 - current_player
        
        time.sleep(0.75)          # Delay for AI vs AI mode
        continue

    # Human Turn
    message = f"{player_name(current_player)}'s turn → Select sticks in a row, then click Remove"
    draw_board(piles, message)

pygame.quit()
sys.exit()