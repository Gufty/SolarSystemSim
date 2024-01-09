import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1000,1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a sort of canvas
pygame.display.set_caption("Solar System Sim") #this is like the title of the app, similar to HTMLs title

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARKGREY = (80,78,81)

FONT = pygame.font.SysFont("comicsans", 16)
class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit =[]
        self.sun = False
        self.distanceToSun = 0
        
        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updatedPoints = []
            for point in self.orbit:
                x,y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updatedPoints.append((x,y))
            pygame.draw.lines(win, self.color, False, updatedPoints, 2)
        
        pygame.draw.circle(win, self.color, (x,y), self.radius)
        
        if not self.sun:
            distanceText = FONT.render(f"{round(self.distanceToSun / 1000), 1}km", 1, WHITE)
            win.blit(distanceText, (x - distanceText.get_width() / 2,y - distanceText.get_height() / 2))
        
    
    def attraction(self, other):
        otherX, otherY = other.x, other.y
        distanceX = otherX - self.x
        distanceY = otherY - self.y
        distance = math.sqrt(distanceX ** 2 + distanceY **2)
        if other.sun:
            self.distanceToSun = distance
        force = self.G * self.mass * other.mass / distance **2
        theta = math.atan2(distanceY, distanceX)
        forceX = math.cos(theta) * force
        forceY = math.sin(theta) * force
        return forceX, forceY
    
    def updatePosition(self, planets):
        totalFX = totalFY = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            totalFX += fx
            totalFY += fy
        
        self.x_vel += totalFX / self.mass * self.TIMESTEP
        self.y_vel += totalFY / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        

def main(): #this is basically a inf loop we need to run our code constantly to ensure our window doesnt close instantly after running it.
    run = True
    clock = pygame.time.Clock() #regulates framerate
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 **30)
    sun.sun = True
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(.387 * Planet.AU, 0, 8, DARKGREY, .330 * 10**24)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    while run: #inf while loop
        clock.tick(60) #max "fps"
        WIN.fill((0,0,0))
        for event in pygame.event.get(): #for any event that the user does, wheter that be a keystroke or mouse click, check it
            if event.type == pygame.QUIT: #if the user clicks on the x on the window
                run = False #run is set to false to exit the inf while loop
                
        for planet in planets:
            planet.updatePosition(planets)
            planet.draw(WIN)
        
        pygame.display.update()
    pygame.quit() #stops the program
    
main()