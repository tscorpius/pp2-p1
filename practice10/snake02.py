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
ORANGE = (255, 165, 0)                                                                                                                  
CYAN = (0, 255, 255)                                                                                                                    
                                                                                                                                        
font = pygame.font.SysFont(None, 36)                                                                                                    
small_font = pygame.font.SysFont(None, 24)                                                                                              
                                                                                                                                        
def random_pos(snake):                                                                                                                  
    while True:                                                                                                                         
        x = random.randint(0, WIDTH // CELL - 1) * CELL                                                                                 
        y = random.randint(0, HEIGHT // CELL - 1) * CELL                                                                                
        if (x, y) not in snake:                                                                                                         
            return (x, y)                                                                                                               
                                                                                                                                        
def new_food(snake):                                                                                                                    
    pos = random_pos(snake)                                                                                                             
    weight = random.choices([1, 3, 5], weights=[60, 30, 10])[0]                                                                         
    timer = pygame.time.get_ticks()                                                                                                     
    return {"pos": pos, "weight": weight, "born": timer}                                                                                
                                                                                                                                        
def reset():                                                                                                                            
    snake = [(WIDTH // 2, HEIGHT // 2)]                                                                                                 
    direction = (CELL, 0)                                                                                                               
    food = new_food(snake)                                                                                                              
    score = 0                                                                                                                           
    level = 1                                                                                                                           
    speed = 8                                                                                                                           
    return snake, direction, food, score, level, speed                                                                                  
                                                                                                                                        
snake, direction, food, score, level, speed = reset()                                                                                   
clock = pygame.time.Clock()                                                                                                             
game_over = False                                                                                                                       
move_timer = 0                                                                                                                          
FOOD_LIFETIME = 5000                                                                                                                    
                                                                                                                                        
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
                                                                                                                                        
    if not game_over:                                                                                                                   
        # Еда исчезает через 5 секунд                                                                                                   
        now = pygame.time.get_ticks()                                                                                                   
        if now - food["born"] > FOOD_LIFETIME:                                                                                          
            food = new_food(snake)                                                                                                      
                                                                                                                                        
        if move_timer >= 60 // speed:                                                                                                   
            move_timer = 0                                                                                                              
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])                                                             
                                                                                                                                        
            if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:                                                     
                game_over = True                                                                                                        
            elif head in snake:                                                                                                         
                game_over = True                                                                                                        
            else:                                                                                                                       
                snake.insert(0, head)                                                                                                   
                                                                                                                                        
                if head == food["pos"]:                                                                                               
                    score += food["weight"]                                                                                             
                    food = new_food(snake)                                                                                              
                                                                                                                                        
                    if score % 5 == 0:                                                                                                  
                        level += 1                                                                                                      
                        speed += 2                                                                                                      
                else:                                                                                                                   
                    snake.pop()                                                                                                         
                                                                                                                                        
    # Рисование                                                                                                                         
    screen.fill(BLACK)                                                                                                                  
                                                                                                                                        
    for x in range(0, WIDTH, CELL):                                                                                                     
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))                                                                     
    for y in range(0, HEIGHT, CELL):                                                                                                    
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))                                                                      
                                                                                                                                        
    # Цвет еды зависит от веса                                                                                                          
    if food["weight"] == 1:                                                                                                             
        food_color = RED                                                                                                                
    elif food["weight"] == 3:                                                                                                           
        food_color = ORANGE                                                                                                             
    else:                                                                                                                               
        food_color = CYAN                                                                                                               
                                                                                                                                        
    # Таймер еды — мигает когда скоро исчезнет                                                                                          
    now = pygame.time.get_ticks()                                                                                                       
    time_left = FOOD_LIFETIME - (now - food["born"])                                                                                    
    if time_left < 2000 and (now // 300) % 2 == 0:                                                                                      
        food_color = WHITE                                                                                                              
                                                                                                                                        
    pygame.draw.rect(screen, food_color, (*food["pos"], CELL, CELL), border_radius=5)                                                   
    weight_label = small_font.render(str(food["weight"]), True, BLACK)                                                                  
    screen.blit(weight_label, (food["pos"][0] + 3, food["pos"][1] + 3))                                                                 
                                                                                                                                        
    for i, segment in enumerate(snake):                                                                                                 
        color = GREEN if i == 0 else DARK_GREEN                                                                                         
        pygame.draw.rect(screen, color, (*segment, CELL, CELL), border_radius=4)                                                        
                                                                                                                                        
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