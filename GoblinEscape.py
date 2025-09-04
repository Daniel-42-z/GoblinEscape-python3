import pygame, sys, math

# Game constants
base_width = 1024
base_height = 720
radius = 300.0

# Game variables
goblin = 0.0
boatx = 0.1 
boaty = 0.0
bspeed = 1.0
gspeeds = [3.5, 4.0, 4.2, 4.4, 4.6]
gspeed_ix = 0
speed_mult = 3.0
clicking = False
with_hint = False
progressive = True
speed = 4.0
scale = 1.0  # New scale variable

# Calculated dimensions based on scale
width = int(base_width * scale)
height = int(base_height * scale)

# UI Classes
class Toggle:
    def __init__(self, x, y, width, height, initial_value, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.label = label
        self.font = pygame.font.Font(None, 20)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value
                return True
        return False
    
    def draw(self, surface):
        # Draw toggle background
        color = (50, 200, 50) if self.value else (200, 50, 50)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Draw toggle text
        text = "ON" if self.value else "OFF"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))

class ScaleToggle:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = pygame.font.Font(None, 20)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, surface):
        global scale
        # Draw toggle background
        color = (100, 100, 200)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Draw scale text
        scale_text = "1x" if scale == 1.0 else "0.5x"
        text_surface = self.font.render(scale_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_value, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_value
        self.label = label
        self.dragging = False
        self.font = pygame.font.Font(None, 20)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
            return True
        return False
    
    def update_value(self, mouse_x):
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(relative_x, self.rect.width))
        ratio = relative_x / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        self.value = round(self.value, 1)
    
    def draw(self, surface):
        # Draw slider track
        pygame.draw.rect(surface, (100, 100, 100), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        # Draw slider handle
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 2, 10, self.rect.height + 4)
        pygame.draw.rect(surface, (255, 255, 255), handle_rect)
        
        # Draw label and value
        label_text = f"{self.label}: {self.value}"
        label_surface = self.font.render(label_text, True, (255, 255, 255))
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))

def updateScale():
    global width, height, window
    width = int(base_width * scale)
    height = int(base_height * scale)
    window = pygame.display.set_mode((width, height))

def getCurrentGoblinSpeed():
    if progressive:
        return gspeeds[gspeed_ix]
    else:
        return speed

def restart():
    global goblin, boatx, boaty, clicking
    goblin = 0.0
    boatx = 0.1 
    boaty = 0.0
    clicking = False

# Initialize pygame FIRST
pygame.init()
window = pygame.display.set_mode((width, height))

# NOW create UI elements after pygame is initialized
hint_toggle = Toggle(20, 20, 60, 25, with_hint, "Show Hint")
progressive_toggle = Toggle(20, 70, 60, 25, progressive, "Progressive")
speed_slider = Slider(20, 120, 120, 15, 3.2, 4.6, speed, "Speed")
scale_toggle = ScaleToggle(20, 170, 60, 25, "Scale")  # New scale toggle

def clear():
    current_speed = getCurrentGoblinSpeed()
    radius_mult = bspeed / current_speed
    window.fill((0,80,0))
    pygame.draw.circle(window, (0,0,128), (int(width/2), int(height/2)), int(radius*scale*1.00), 0)
    if with_hint:
        pygame.draw.circle(window, (200,200,200), (int(width/2), int(height/2)), int(radius*scale*radius_mult), 1)

def redraw(draw_text=False,win=False):
    clear()
    pygame.draw.circle(window, (255,255,255), (int(width/2 + boatx*scale),int(height/2 + boaty*scale)), max(1, int(6*scale)), 2)
    pygame.draw.circle(window, (255,0,0), (int(width/2 + radius*scale*math.cos(goblin)),int(height/2 + radius*scale*math.sin(goblin))), max(1, int(6*scale)), 0)
    
    if draw_text:
        font_size = max(36, int(72*scale))
        font = pygame.font.Font(None, font_size)
        if win:
            text = font.render("Escaped!", 1, (255, 255, 255))
        else:
            text = font.render("You Were Eaten", 1, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = window.get_rect().centerx
        textpos.centery = height/2
        window.blit(text, textpos)
    
    # Draw speed info
    font_size = max(24, int(48*scale))
    font = pygame.font.Font(None, font_size)
    current_speed = getCurrentGoblinSpeed()
    mode_text = " (Progressive)" if progressive else " (Constant)"
    text = font.render("Goblin Speed: " + str(current_speed) + mode_text, 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = width/2
    textpos.centery = height - int(20*scale)
    window.blit(text, textpos)
    
    # Draw UI elements
    hint_toggle.draw(window)
    progressive_toggle.draw(window)
    scale_toggle.draw(window)  # Draw the new scale toggle
    if not progressive:  # Only show speed slider in constant mode
        speed_slider.draw(window)
        
    pygame.display.flip()

def updateGoblin():
    global goblin
    gspeed = getCurrentGoblinSpeed()
    newang = math.atan2(boaty, boatx)
    diff = newang - goblin
    if diff < math.pi: diff += math.pi*2.0
    if diff > math.pi: diff -= math.pi*2.0
    if abs(diff)*radius <= gspeed * speed_mult:
        goblin = newang
    else:
        goblin += gspeed * speed_mult / radius if diff > 0.0 else -gspeed * speed_mult / radius
    if goblin < math.pi: goblin += math.pi*2.0
    if goblin > math.pi: goblin -= math.pi*2.0

def moveBoat(x,y):
    global boatx, boaty
    dx = x - boatx
    dy = y - boaty
    mag = math.sqrt(dx*dx + dy*dy)
    if mag <= bspeed * speed_mult:
        boatx = x
        boaty = y
    else:
        boatx += bspeed * speed_mult * dx/mag
        boaty += bspeed * speed_mult * dy/mag 

def detectWin():
    global gspeed_ix
    if boatx*boatx + boaty*boaty > radius*radius:
        diff = math.atan2(boaty, boatx) - goblin
        if diff < math.pi: diff += math.pi*2.0
        if diff > math.pi: diff -= math.pi*2.0
        while True:
            is_win = abs(diff) > 0.000001
            redraw(True, is_win)
            events = [event.type for event in pygame.event.get()]
            if pygame.QUIT in events: 
                pygame.quit()
                sys.exit(0)
            elif pygame.MOUSEBUTTONDOWN in events:
                restart()
                if is_win and progressive:  # Only increment if progressive mode
                    gspeed_ix += 1
                break

clock = pygame.time.Clock()
clear()

while True:
    events = pygame.event.get()
    for event in events: 
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit(0)
        
        # Handle UI events first
        ui_handled = False
        ui_handled |= hint_toggle.handle_event(event)
        ui_handled |= progressive_toggle.handle_event(event)
        if not progressive:
            ui_handled |= speed_slider.handle_event(event)
        
        # Handle scale toggle
        if scale_toggle.handle_event(event):
            scale = 0.5 if scale == 1.0 else 1.0  # Toggle between 1.0 and 0.5
            updateScale()
            ui_handled = True
        
        # Update global variables from UI
        with_hint = hint_toggle.value
        progressive = progressive_toggle.value
        if not progressive:
            speed = speed_slider.value
        
        # Only handle game controls if UI didn't handle the event
        if not ui_handled and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right click
                restart()
    
    # Handle mouse button state for boat movement
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse is not over UI elements
        if not (hint_toggle.rect.collidepoint(mouse_pos) or 
                progressive_toggle.rect.collidepoint(mouse_pos) or 
                scale_toggle.rect.collidepoint(mouse_pos) or
                (not progressive and speed_slider.rect.collidepoint(mouse_pos))):
            clicking = True
            x, y = mouse_pos
            moveBoat((x - width/2)/scale, (y - height/2)/scale)  # Scale mouse coordinates
    else:
        clicking = False
    
    updateGoblin()
    detectWin()
    redraw()
    clock.tick(60)
