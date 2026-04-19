import pygame                                                                                                                         
                                                                                                                                          
pygame.init()                                                                                                                           
                                                                                                                                          
WIDTH = 600                                                                                                                             
HEIGHT = 600                                                                                                                            
screen = pygame.display.set_mode((WIDTH, HEIGHT))                                                                                     
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x = WIDTH // 2
y = HEIGHT // 2                                                                                                                         
RADIUS = 25                                                                                                                             
STEP = 20                                                                                                                               
                                                                                                                                          
clock = pygame.time.Clock()                                                                                                             
                                                                                                                                        
running = True
while running:
    for event in pygame.event.get():                                                                                                    
        if event.type == pygame.QUIT:                                                                                                   
            running = False                                                                                                             
                                                                                                                                          
        if event.type == pygame.KEYDOWN:                                                                                                
            if event.key == pygame.K_UP and y - RADIUS - STEP >= 0:                                                                     
                 y -= STEP                                                                                                               
            if event.key == pygame.K_DOWN and y + RADIUS + STEP <= HEIGHT:                                                              
                y += STEP                                                                                                               
            if event.key == pygame.K_LEFT and x - RADIUS - STEP >= 0:                                                                   
                x -= STEP                                                                                                               
            if event.key == pygame.K_RIGHT and x + RADIUS + STEP <= WIDTH:                                                              
                x += STEP                                                                                                               
                                                                                                                                          
    screen.fill(WHITE)                                                                                                                  
    pygame.draw.circle(screen, RED, (x, y), RADIUS)                                                                                   
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
