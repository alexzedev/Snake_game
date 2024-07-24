import pygame
import random

# Pygame initialization
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Window settings
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake by alexzedev")

# Game settings
BLOCK_SIZE = 20
SPEED = 7

clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2)]
        self.direction = "RIGHT"

    def move(self):
        x, y = self.body[0]
        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        # Wall traversal support
        x = x % WIDTH
        y = y % HEIGHT

        self.body.insert(0, (x, y))

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self):
        for block in self.body:
            pygame.draw.rect(window, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        return (x, y)

    def draw(self):
        pygame.draw.rect(window, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def game_over():
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over! Press R to Restart", True, WHITE)
    window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()

        # Food collision check
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.randomize_position()
            score += 1

        # Checking for collisions with your own body
        if snake.body[0] in snake.body[1:]:
            game_over()
            return

        # Removing the last segment if the snake has not eaten the food
        if len(snake.body) > score + 1:
            snake.body.pop()

        window.fill(BLACK)
        snake.draw()
        food.draw()

        # Displaying the result
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, WHITE)
        window.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    while True:
        main()