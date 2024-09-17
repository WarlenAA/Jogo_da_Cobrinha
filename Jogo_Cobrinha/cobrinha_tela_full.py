import pygame
import random

# Inicialização do Pygame
pygame.init()

# Obter informações sobre a tela
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

# Definição das cores utilizadas no jogo
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configuração da janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Jogo da Cobrinha")

# Velocidade da cobrinha
SNAKE_SPEED = 10

# Tamanho dos blocos da cobrinha e da comida
BLOCK_SIZE = 20

# Fonte para exibir a pontuação
font = pygame.font.SysFont(None, 32)

# Função para desenhar a cobrinha
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(window, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

# Função para desenhar a comida
def draw_food(food):
    pygame.draw.rect(window, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

# Função para exibir a pontuação
def show_score(score):
    text = font.render(f"Pontuação: {score}", True, WHITE)
    window.blit(text, (10, 10))

# Função para exibir a mensagem de game over
def show_game_over():
    message = font.render("Game Over", True, WHITE)
    message_rect = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    window.blit(message, message_rect)

# Função para exibir os botões de dificuldade
def show_difficulty_buttons():
    # Botão "Fácil"
    pygame.draw.rect(window, WHITE, (WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 30))
    text = font.render("Fácil", True, BLACK)
    window.blit(text, (WIDTH / 2 - 60, HEIGHT / 2 - 45))

    # Botão "Médio"
    pygame.draw.rect(window, WHITE, (WIDTH / 2 - 100, HEIGHT / 2, 200, 30))
    text = font.render("Médio", True, BLACK)
    window.blit(text, (WIDTH / 2 - 60, HEIGHT / 2 + 5))

    # Botão "Difícil"
    pygame.draw.rect(window, WHITE, (WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 30))
    text = font.render("Difícil", True, BLACK)
    window.blit(text, (WIDTH / 2 - 60, HEIGHT / 2 + 55))

# Função para exibir o botão de jogar novamente
def show_play_again_button():
    pygame.draw.rect(window, WHITE, (WIDTH / 2 - 120, HEIGHT / 2 + 30, 240, 30))
    text = font.render("Jogar novamente?", True, BLACK)
    window.blit(text, (WIDTH / 2 - 110, HEIGHT / 2 + 35))

    # Botão "Sim"
    pygame.draw.rect(window, WHITE, (WIDTH / 2 - 100, HEIGHT / 2 + 70, 80, 30))
    text = font.render("Sim", True, BLACK)
    window.blit(text, (WIDTH / 2 - 90, HEIGHT / 2 + 75))

    # Botão "Não"
    pygame.draw.rect(window, WHITE, (WIDTH / 2 + 20, HEIGHT / 2 + 70, 80, 30))
    text = font.render("Não", True, BLACK)
    window.blit(text, (WIDTH / 2 + 30, HEIGHT / 2 + 75))

# Função principal do jogo
def game_loop():
    # Posição inicial da cobrinha
    x = WIDTH / 2
    y = HEIGHT / 2

    # Velocidade inicial da cobrinha
    dx = 0
    dy = 0

    # Lista de segmentos da cobrinha
    snake = []
    snake_length = 1

    # Posição inicial da comida
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Variáveis para controlar o estado do jogo
    game_over = False
    score = 0

    # Dificuldade do jogo (escolhida na interface)
    difficulty = None

    # Loop para aguardar a escolha da dificuldade na interface
    while not difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 + 100:
                    if HEIGHT / 2 - 50 <= mouse_pos[1] <= HEIGHT / 2 - 20:
                        difficulty = "fácil"
                    elif HEIGHT / 2 <= mouse_pos[1] <= HEIGHT / 2 + 30:
                        difficulty = "médio"
                    elif HEIGHT / 2 + 50 <= mouse_pos[1] <= HEIGHT / 2 + 80:
                        difficulty = "difícil"

        window.fill(BLACK)
        show_difficulty_buttons()
        pygame.display.update()

    # Definição da velocidade do jogo de acordo com a dificuldade escolhida
    if difficulty == "fácil":
        SNAKE_SPEED = 10
    elif difficulty == "médio":
        SNAKE_SPEED = 20
    elif difficulty == "difícil":
        SNAKE_SPEED = 30

    # Loop principal do jogo
    while not game_over:
        # Verificação de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy != BLOCK_SIZE:
                    dx = 0
                    dy = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and dy != -BLOCK_SIZE:
                    dx = 0
                    dy = BLOCK_SIZE
                elif event.key == pygame.K_LEFT and dx != BLOCK_SIZE:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx != -BLOCK_SIZE:
                    dx = BLOCK_SIZE
                    dy = 0

        # Atualização da posição da cobrinha
        x += dx
        y += dy

        # Verificação de colisão da cobrinha com a parede
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_over = True

        # Limpeza da tela
        window.fill(BLACK)

        # Desenho da comida
        draw_food((food_x, food_y))

        # Atualização da posição da cobrinha
        snake.append((x, y))
        if len(snake) > snake_length:
            del snake[0]

        # Verificação de colisão da cobrinha com a comida
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 1

        # Verificação de colisão da cobrinha com o próprio corpo
        if any(segment == (x, y) for segment in snake[:-1]):
            game_over = True

        # Desenho da cobrinha
        draw_snake(snake)

        # Exibição da pontuação
        show_score(score)

        # Atualização da janela do jogo
        pygame.display.update()

        # Definição da velocidade do jogo
        pygame.time.Clock().tick(SNAKE_SPEED)

    # Loop para aguardar a escolha de jogar novamente
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y or event.key == pygame.K_s:
                    return True
                elif event.key == pygame.K_n:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH / 2 - 100 <= mouse_pos[0] <= WIDTH / 2 - 20:
                    if HEIGHT / 2 + 70 <= mouse_pos[1] <= HEIGHT / 2 + 100:
                        return True
                elif WIDTH / 2 + 20 <= mouse_pos[0] <= WIDTH / 2 + 100:
                    if HEIGHT / 2 + 70 <= mouse_pos[1] <= HEIGHT / 2 + 100:
                        return False

        window.fill(BLACK)
        show_game_over()
        show_play_again_button()
        pygame.display.update()

# Início do jogo
game_running = True
while game_running:
    game_running = game_loop()