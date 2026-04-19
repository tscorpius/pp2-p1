import pygame                                                                                                                           
import random                                                                                                                           
                                                                                                                                        
pygame.init()                                                                                                                           
                                                                                                                                    
WIDTH = 600
HEIGHT = 600                                                                                                                            
CELL = 20                                                                                                                               
                                                                                                                                        
screen = pygame.display.set_mode((WIDTH, HEIGHT))                                                                                       
pygame.display.set_caption("Snake")                                                                                                     
                                                                                                                                        
WHITE = (255, 255, 255)                                                                                                                 
BLACK = (0, 0, 0)                                                                                                                       
GREEN = (50, 200, 50)                                                                                                                   
DARK_GREEN = (30, 150, 30)                                                                                                              
RED = (220, 50, 50)                                                                                                                     
YELLOW = (255, 220, 0)                                                                                                                  
GRAY = (200, 200, 200)                                                                                                                  
                                                                                                                                        
font = pygame.font.SysFont(None, 36)                                                                                                    
small_font = pygame.font.SysFont(None, 24)                                                                                              
                                                                                                                                        
def random_food(snake):                                                                                                                 
    while True:                                                                                                                         
        x = random.randint(0, WIDTH // CELL - 1) * CELL                                                                                 
        y = random.randint(0, HEIGHT // CELL - 1) * CELL                                                                                
        if (x, y) not in snake:                                                                                                         
            return (x, y)                                                                                                               
                                                                                                                                        
def reset():                                                                                                                            
    snake = [(WIDTH // 2, HEIGHT // 2)]                                                                                                 
    direction = (CELL, 0)                                                                                                               
    food = random_food(snake)                                                                                                           
    score = 0                                                                                                                           
    level = 1                                                                                                                           
    speed = 8                                                                                                                           
    return snake, direction, food, score, level, speed                                                                                  
                                                                                                                                        
snake, direction, food, score, level, speed = reset()                                                                                   
clock = pygame.time.Clock()                                                                                                             
game_over = False                                                                                                                       
move_timer = 0                                                                                                                          
                                                                                                                                        
running = True                                                                                                                          
while running:                                                                                                                        
    clock.tick(60)
    move_timer += 1                                                                                                                     
                                                                                                                                        
    for event in pygame.event.get():                                                                                                    
        if event.type == pygame.QUIT:                                                                                                   
            running = False                                                                                                             
                                                                                                                                        
        if event.type == pygame.KEYDOWN:                                                                                                
            if game_over:                                                                                                               
                if event.key == pygame.K_r:                                                                                             
                    snake, direction, food, score, level, speed = reset()                                                               
                    game_over = False                                                                                                   
                    move_timer = 0                                                                                                      
            else:                                                                                                                       
                if event.key == pygame.K_UP and direction != (0, CELL):                                                                 
                    direction = (0, -CELL)                                                                                              
                if event.key == pygame.K_DOWN and direction != (0, -CELL):                                                              
                    direction = (0, CELL)                                                                                               
                if event.key == pygame.K_LEFT and direction != (CELL, 0):                                                               
                    direction = (-CELL, 0)                                                                                              
                if event.key == pygame.K_RIGHT and direction != (-CELL, 0):                                                             
                    direction = (CELL, 0)                                                                                               
                                                                                                                                        
    if not game_over and move_timer >= 60 // speed:                                                                                     
        move_timer = 0                                                                                                                  
                                                                                                                                        
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])                                                                 
                                                                                                                                    
        # Проверка границ
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:                                                         
            game_over = True                                                                                                            
        elif head in snake:                                                                                                             
            game_over = True                                                                                                            
        else:                                                                                                                           
            snake.insert(0, head)                                                                                                       
                                                                                                                                        
            if head == food:                                                                                                            
                score += 1                                                                                                              
                food = random_food(snake)                                                                                               
                                                                                                                                        
                # Уровни                                                                                                                
                if score % 3 == 0:                                                                                                      
                    level += 1                                                                                                          
                    speed += 2                                                                                                          
            else:                                                                                                                       
                snake.pop()                                                                                                             
                                                                                                                                        
    # Рисование                                                                                                                         
    screen.fill(BLACK)                                                                                                                  
                                                                                                                                        
    # Сетка                                                                                                                             
    for x in range(0, WIDTH, CELL):                                                                                                     
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))                                                                     
    for y in range(0, HEIGHT, CELL):                                                                                                  
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))

    # Еда
    pygame.draw.rect(screen, RED, (*food, CELL, CELL), border_radius=5)

    # Змейка
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (*segment, CELL, CELL), border_radius=4)
                                                                                                                                        
    # Счёт и уровень                                                                                                                    
    score_text = font.render(f"Score: {score}", True, WHITE)                                                                            
    level_text = font.render(f"Level: {level}", True, YELLOW)                                                                           
    screen.blit(score_text, (10, 10))                                                                                                   
    screen.blit(level_text, (WIDTH - 120, 10))                                                                                          
                                                                                                                                        
    if game_over:                                                                                                                       
        over_text = font.render("GAME OVER", True, RED)                                                                                 
        restart_text = small_font.render("Press R to restart", True, WHITE)                                                             
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 30))                                             
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))                                       
                                                                                                                                        
    pygame.display.flip()                                                                                                               
                                                                                                                                        
pygame.quit()