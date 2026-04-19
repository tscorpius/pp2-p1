import pygame                                                                                                          
import datetime                                                                                                        
                                                                                                                        
pygame.init()                                                                                                          
                                                                                                                        
WIDTH = 600                                                                                                            
HEIGHT = 600                                                                                                         
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
                                                                                                                        
CENTER = (WIDTH // 2, HEIGHT // 2)                                                                                     
                                                                                                                        
clock_img = pygame.image.load("/Users/zere/Desktop/labs/practice9/mickeys_clock/clock.png")                            
clock_img = pygame.transform.scale(clock_img, (500, 500))                                                              
clock_rect = clock_img.get_rect(center=CENTER)                                                                         
                                                                                                                        
hour_img = pygame.image.load("/Users/zere/Desktop/labs/practice9/mickeys_clock/hour.png")                              
hour_img = pygame.transform.scale(hour_img, (180, 500))                                                                
                                                                                                                        
minute_img = pygame.image.load("/Users/zere/Desktop/labs/practice9/mickeys_clock/minute.png")                          
minute_img = pygame.transform.scale(minute_img, (180, 500))                                                            
                                                                                                                        
def rotate_hand(image, angle):                                                                                         
    rotated = pygame.transform.rotate(image, -angle)                                                                   
    rect = rotated.get_rect(center=CENTER)                                                                             
    return rotated, rect                                                                                               
                                                                                                                        
clock = pygame.time.Clock()                                                                                            
                                                                                                                        
running = True                                                                                                       
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                                                                                            
                                                                                                                        
    now = datetime.datetime.now()                                                                                      
    minutes = now.minute                                                                                               
    seconds = now.second                                                                                               
                                                                                                                    
    minute_angle = (minutes / 60) * 360 - 90
    second_angle = (seconds / 60) * 360 - 90                                                                           
                                                                                                                        
    screen.fill((255, 255, 255))                                                                                       
    screen.blit(clock_img, clock_rect)                                                                                 
                                                                                                                        
    min_rotated, min_rect = rotate_hand(minute_img, minute_angle)                                                      
    sec_rotated, sec_rect = rotate_hand(hour_img, second_angle)                                                        
                                                                                                                        
    screen.blit(min_rotated, min_rect)                                                                                 
    screen.blit(sec_rotated, sec_rect)                                                                                 
                                                                                                                        
    pygame.display.flip()                                                                                              
    clock.tick(60)                                                                                                     
                                                                                                                        
pygame.quit()  