import pygame                                                                                                                           
                                                                                                                                        
pygame.init()                                                                                                                           
                                                                                                                                        
WIDTH = 800                                                                                                                             
HEIGHT = 600                                                                                                                            
screen = pygame.display.set_mode((WIDTH, HEIGHT))                                                                                       
pygame.display.set_caption("Paint")                                                                                                     
                                                                                                                                    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)                                                                                                                       
GRAY = (200, 200, 200)                                                                                                                  
                                                                                                                                        
# Цвета для выбора                                                                                                                      
COLORS = [                                                                                                                              
    (0, 0, 0), (255, 255, 255), (255, 0, 0),                                                                                            
    (0, 255, 0), (0, 0, 255), (255, 255, 0),                                                                                            
    (255, 165, 0), (128, 0, 128), (0, 255, 255),                                                                                        
    (255, 192, 203)                                                                                                                     
]                                                                                                                                       
                                                                                                                                        
current_color = BLACK                                                                                                                   
current_tool = "pencil"                                                                                                                 
drawing = False                                                                                                                         
start_pos = None                                                                                                                        
                                                                                                                                        
canvas = pygame.Surface((WIDTH, HEIGHT - 80))                                                                                           
canvas.fill(WHITE)                                                                                                                      
                                                                                                                                        
font = pygame.font.SysFont(None, 24)                                                                                                    
                                                                                                                                        
def draw_toolbar():                                                                                                                     
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 80))                                                                                   
                                                                                                                                        
    # Цвета                                                                                                                             
    for i, color in enumerate(COLORS):                                                                                                  
        rect = pygame.Rect(10 + i * 45, 10, 35, 35)                                                                                     
        pygame.draw.rect(screen, color, rect)                                                                                           
        pygame.draw.rect(screen, BLACK, rect, 2)                                                                                        
        if color == current_color:                                                                                                      
            pygame.draw.rect(screen, BLACK, rect, 4)                                                                                    
                                                                                                                                        
    # Инструменты                                                                                                                       
    tools = ["pencil", "rect", "circle", "eraser", "square", "rtriangle", "etriangle", "rhombus"]                                       
    for i, tool in enumerate(tools):                                                                                                    
        rect = pygame.Rect(10 + i * 80, 50, 70, 25)                                                                                     
        color = (150, 150, 255) if tool == current_tool else GRAY                                                                       
        pygame.draw.rect(screen, color, rect)                                                                                           
        pygame.draw.rect(screen, BLACK, rect, 1)                                                                                        
        label = font.render(tool, True, BLACK)                                                                                          
        screen.blit(label, (rect.x + 5, rect.y + 5))                                                                                    
                                                                                                                                        
clock = pygame.time.Clock()                                                                                                             
running = True                                                                                                                          
                                                                                                                                        
while running:                                                                                                                          
    for event in pygame.event.get():                                                                                                    
        if event.type == pygame.QUIT:                                                                                                   
            running = False                                                                                                             
                                                                                                                                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos                                                                                                            
                                                                                                                                        
            # Выбор цвета                                                                                                               
            if y < 45:                                                                                                                  
                for i, color in enumerate(COLORS):                                                                                      
                    rect = pygame.Rect(10 + i * 45, 10, 35, 35)                                                                         
                    if rect.collidepoint(x, y):                                                                                         
                        current_color = color                                                                                           
                                                                                                                                        
            # Выбор инструмента                                                                                                         
            elif y < 80:                                                                                                                
                tools = ["pencil", "rect", "circle", "eraser", "square", "rtriangle", "etriangle", "rhombus"]                           
                for i, tool in enumerate(tools):                                                                                        
                    rect = pygame.Rect(10 + i * 80, 50, 70, 25)                                                                         
                    if rect.collidepoint(x, y):                                                                                         
                        current_tool = tool                                                                                             
                                                                                                                                        
            else:                                                                                                                       
                drawing = True                                                                                                        
                start_pos = (x, y - 80)                                                                                                 
                                                                                                                                        
        if event.type == pygame.MOUSEBUTTONUP:                                                                                          
            if drawing and start_pos:                                                                                                   
                x, y = event.pos                                                                                                        
                end_pos = (x, y - 80)                                                                                                   
                w = end_pos[0] - start_pos[0]                                                                                           
                h = end_pos[1] - start_pos[1]                                                                                           
                                                                                                                                        
                if current_tool == "rect":                                                                                              
                    pygame.draw.rect(canvas, current_color, (*start_pos, w, h), 2)                                                      
                                                                                                                                        
                elif current_tool == "circle":                                                                                          
                    cx = (start_pos[0] + end_pos[0]) // 2                                                                               
                    cy = (start_pos[1] + end_pos[1]) // 2                                                                               
                    r = max(abs(w), abs(h)) // 2                                                                                        
                    pygame.draw.circle(canvas, current_color, (cx, cy), r, 2)                                                           
                                                                                                                                        
                elif current_tool == "square":                                                                                          
                    side = min(abs(w), abs(h))                                                                                          
                    pygame.draw.rect(canvas, current_color, (*start_pos, side, side), 2)                                                
                                                                                                                                        
                elif current_tool == "rtriangle":                                                                                       
                    p1 = start_pos                                                                                                      
                    p2 = (start_pos[0], end_pos[1])                                                                                     
                    p3 = end_pos                                                                                                        
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3], 2)                                                         
                                                                                                                                        
                elif current_tool == "etriangle":                                                                                       
                    side = abs(w)                                                                                                       
                    p1 = (start_pos[0] + side // 2, start_pos[1])                                                                       
                    p2 = (start_pos[0], start_pos[1] + side)                                                                            
                    p3 = (start_pos[0] + side, start_pos[1] + side)                                                                     
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3], 2)                                                         
                                                                                                                                        
                elif current_tool == "rhombus":                                                                                         
                    cx = (start_pos[0] + end_pos[0]) // 2                                                                               
                    cy = (start_pos[1] + end_pos[1]) // 2                                                                               
                    p1 = (cx, start_pos[1])                                                                                             
                    p2 = (end_pos[0], cy)                                                                                               
                    p3 = (cx, end_pos[1])                                                                                               
                    p4 = (start_pos[0], cy)                                                                                             
                    pygame.draw.polygon(canvas, current_color, [p1, p2, p3, p4], 2)                                                     
                                                                                                                                        
            drawing = False                                                                                                             
            start_pos = None                                                                                                            
                                                                                                                                        
        if event.type == pygame.MOUSEMOTION:                                                                                            
            if drawing and current_tool in ["pencil", "eraser"]:                                                                        
                x, y = event.pos                                                                                                        
                color = WHITE if current_tool == "eraser" else current_color                                                            
                pygame.draw.circle(canvas, color, (x, y - 80), 5)                                                                       
                                                                                                                                        
    screen.fill(GRAY)                                                                                                                   
    draw_toolbar()                                                                                                                      
    screen.blit(canvas, (0, 80))                                                                                                        
                                                                                                                                        
    pygame.display.flip()                                                                                                               
    clock.tick(60)                                                                                                                      
                                                                                                                                        
pygame.quit()