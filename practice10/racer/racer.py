import pygame                                                                                                                           
import random                                                                                                                           
                                                                                                                                        
pygame.init()                                                                                                                           
                                                                                                                                        
WIDTH = 400                                                                                                                             
HEIGHT = 600                                                                                                                            
screen = pygame.display.set_mode((WIDTH, HEIGHT))                                                                                     
pygame.display.set_caption("Racer")
                                                                                                                                        
WHITE = (255, 255, 255)                                                                                                                 
BLACK = (0, 0, 0)                                                                                                                       
RED = (220, 50, 50)                                                                                                                     
GRAY = (100, 100, 100)                                                                                                                  
DARK_GRAY = (50, 50, 50)                                                                                                                
YELLOW = (255, 220, 0)                                                                                                                  
                                                                                                                                        
font = pygame.font.SysFont(None, 36)                                                                                                    
small_font = pygame.font.SysFont(None, 24)                                                                                              
                                                                                                                                        
# Игрок                                                                                                                                 
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 120, 50, 80)                                                                             
player_speed = 5                                                                                                                        
                                                                                                                                        
# Враги                                                                                                                                 
enemies = []                                                                                                                            
enemy_speed = 4                                                                                                                         
spawn_timer = 0                                                                                                                         
                                                                                                                                        
# Монеты                                                                                                                                
coins = []                                                                                                                              
coin_timer = 0                                                                                                                        
coin_count = 0                                                                                                                          
                                                                                                                                        
# Дорога                                                                                                                                
road_lines = [i * 100 for i in range(7)]                                                                                                
road_speed = 4                                                                                                                          
                                                                                                                                        
score = 0                                                                                                                               
clock = pygame.time.Clock()                                                                                                             
running = True                                                                                                                          
game_over = False                                                                                                                       
                                                                                                                                        
while running:                                                                                                                          
    clock.tick(60)                                                                                                                    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                                                                                   
            running = False                                                                                                             
        if game_over and event.type == pygame.KEYDOWN:                                                                                  
            if event.key == pygame.K_r:                                                                                                 
                # Перезапуск                                                                                                            
                enemies.clear()                                                                                                         
                coins.clear()                                                                                                           
                score = 0                                                                                                               
                coin_count = 0                                                                                                          
                enemy_speed = 4                                                                                                         
                game_over = False                                                                                                       
                                                                                                                                        
    if not game_over:                                                                                                                   
        # Движение игрока                                                                                                             
        keys = pygame.key.get_pressed()                                                                                                 
        if keys[pygame.K_LEFT] and player.left > 80:                                                                                    
            player.x -= player_speed                                                                                                    
        if keys[pygame.K_RIGHT] and player.right < WIDTH - 80:                                                                          
            player.x += player_speed                                                                                                    
                                                                                                                                        
        # Дорожная разметка                                                                                                             
        road_speed = 4 + score // 5                                                                                                     
        for i in range(len(road_lines)):                                                                                                
            road_lines[i] += road_speed                                                                                                 
            if road_lines[i] > HEIGHT:                                                                                                  
                road_lines[i] = -100                                                                                                    
                                                                                                                                        
        # Спавн врагов                                                                                                                  
        spawn_timer += 1                                                                                                                
        if spawn_timer > 60:                                                                                                            
            x = random.randint(85, WIDTH - 135)                                                                                         
            enemies.append(pygame.Rect(x, -80, 50, 80))                                                                                 
            spawn_timer = 0                                                                                                             
                                                                                                                                        
        # Движение врагов                                                                                                               
        enemy_speed = 4 + score // 5                                                                                                    
        for enemy in enemies[:]:                                                                                                      
            enemy.y += enemy_speed                                                                                                      
            if enemy.y > HEIGHT:                                                                                                        
                enemies.remove(enemy)                                                                                                   
                score += 1                                                                                                              
            if enemy.colliderect(player):                                                                                               
                game_over = True                                                                                                        
                                                                                                                                        
        # Спавн монет                                                                                                                   
        coin_timer += 1                                                                                                                 
        if coin_timer > 90:                                                                                                           
            x = random.randint(85, WIDTH - 115)
            coins.append(pygame.Rect(x, -30, 25, 25))
            coin_timer = 0                                                                                                              
                                                                                                                                        
        # Движение монет                                                                                                                
        for coin in coins[:]:                                                                                                           
            coin.y += road_speed                                                                                                        
            if coin.y > HEIGHT:                                                                                                       
                coins.remove(coin)
            if coin.colliderect(player):                                                                                                
                coins.remove(coin)                                                                                                      
                coin_count += 1                                                                                                         
                                                                                                                                        
    # Рисование                                                                                                                         
    screen.fill(DARK_GRAY)                                                                                                              
                                                                                                                                        
    # Дорога                                                                                                                            
    pygame.draw.rect(screen, GRAY, (75, 0, WIDTH - 150, HEIGHT))                                                                        
    for y in road_lines:                                                                                                                
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 60))                                                                    
                                                                                                                                        
    # Монеты                                                                                                                            
    for coin in coins:                                                                                                                  
        pygame.draw.ellipse(screen, YELLOW, coin)                                                                                       
                                                                                                                                        
    # Враги                                                                                                                             
    for enemy in enemies:                                                                                                               
        pygame.draw.rect(screen, RED, enemy, border_radius=6)                                                                           
                                                                                                                                        
    # Игрок                                                                                                                             
    pygame.draw.rect(screen, (50, 150, 255), player, border_radius=6)                                                                   
                                                                                                                                        
    # Счёт и монеты                                                                                                                     
    score_text = font.render(f"Score: {score}", True, WHITE)                                                                            
    coin_text = font.render(f"Coins: {coin_count}", True, YELLOW)                                                                       
    screen.blit(score_text, (10, 10))                                                                                                   
    screen.blit(coin_text, (WIDTH - 130, 10))                                                                                           
                                                                                                                                        
    if game_over:                                                                                                                       
        over_text = font.render("GAME OVER", True, RED)                                                                                 
        restart_text = small_font.render("Press R to restart", True, WHITE)                                                             
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 30))                                             
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))                                       
                                                                                                                                        
    pygame.display.flip()                                                                                                               
                                                                                                                                        
pygame.quit() 