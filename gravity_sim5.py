import pygame as pg
from itertools import combinations
import math


pg.init()

#Körper Objekt
class Body:
    def __init__(self, pos, mass, velocity, color, radius, velocity_vecor_angle=0):
        #Geschwindigkeit und Position als zwei dimensionale Vektoren festlegen
        self.pos = pg.Vector2(pos) 
        self.velocity = pg.Vector2(velocity) 
        self.velocity.rotate_ip(velocity_vecor_angle)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.spur = [(pos[0], pos[1])]
        self.repetitions = 0

    #Funtkion zur Aktualisierung der Position
    def update_position(self):
        self.pos += (self.velocity*dt) / FPS
        self.repetitions += 1
        if self.repetitions >= 2500/dt: 
            self.spur.append(self.pos.xy)
            self.repetitions = 0
        if len(self.spur) > dt/5: self.spur.pop(0)
    
    def gravitation(self, other):
        #Distanz zwischen zwei Körper
        self.distance = pg.math.Vector2.distance_to(self.pos, other.pos) 
        #Richtung der Kraft als Normalvektor
        self.direction = pg.math.Vector2.normalize(other.pos - self.pos)
        #Berechnung der Gravitationskraft 
        f = G * (self.mass * other.mass) / self.distance**2
        #Berechnung der Geschwindigkeit
        self.velocity += (((f * self.direction)/self.mass)* dt) /FPS
        other.velocity += (((f * -self.direction)/other.mass)* dt) /FPS

#Fenster Einstellungen
WIDTH = 1700
HEIGHT = 800

#Farben
RED = (240, 0, 0)
BLUE = (0, 0, 240)
GREEN = (0, 240, 0)
BLACK= (0, 0, 0)
SATURN_FARBE = (209, 138, 41)
TITAN_FARBE = (255,165,0)
GREY = (130, 130, 130)
LIGHT_GREY = (170, 170, 170)
YELLOW = (235,235,0)
JUPITER_FARBE = (230, 201, 178)
ORANGE = (255,165,0)
EARTH_COLOR = (0,191,255)

#Berechnungen pro Sekunde
FPS = 16384

#Uhr die die Geschwindigkeit der Simulation festlegt
clock = pg.time.Clock()
dt = 512

#Fonts
text_font = pg.font.SysFont("Arial", 25)

#Gravitationskonstante
G = 3

#Weitere Variable
clicking = False

#Fenster starten
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen_center = (screen.get_width() // 2, screen.get_height() // 2)

#Liste der Körper anlegen
bodies = []

#Sonne Objekt
masse_sonne = 200
radius_sonne = 8
Sonne = Body((screen_center[0], screen_center[1]), masse_sonne, (0,0), YELLOW, radius_sonne)
bodies.append(Sonne)

#Funktion für Aktualisierung des Fensters
def update_screen():
    #Hintergrundfarbe
    screen.fill(BLACK)
    #Für jeden Körper in der Körper Liste 
    for body in bodies:
        if len(body.spur) > 2:
            pg.draw.lines(screen, BLUE, False, body.spur,2)
        #"Zeichne" Körper auf dem Fenster
        pg.draw.circle(screen, body.color, body.pos, body.radius)
        #"Aktualisiere Position" Funktion aufrufen
        body.update_position()
        
#Funktion zuständig für die Gravitation
def gravitation_function():
    for b1, b2 in combinations(bodies, 2):
        b1.gravitation(b2)

def on_button_up(pos1, pos2):
    vector1 = pg.math.Vector2(pos1)
    vector2 = pg.math.Vector2(pos2)
    length = vector1.distance_to(vector2)
    velocity = (length/100, 0)
    x = pos2[0] - pos1[0]
    y = pos2[1] - pos1[1]
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    spawn_body(pos2, velocity, angle-180)


def spawn_body(pos, velocity, angle):
    masse = 1
    radius = 4
    body_object = Body(pos, masse, velocity, GREY, radius, velocity_vecor_angle=angle)
    bodies.append(body_object)


#Simulationsschleife
running = True
while running:
    clock.tick(FPS)
    update_screen()
    gravitation_function()
    
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if dt != FPS:
                    dt *= 2
            elif event.key == pg.K_LEFT:
                if dt > 1:
                    dt /= 2
            elif event.key == pg.K_ESCAPE:
                running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
                pos1 = pg.mouse.get_pos()

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
                pos2 = pg.mouse.get_pos()
                on_button_up(pos1, pos2)

    if clicking:
        mid_pos = pg.mouse.get_pos()
        pg.draw.line(screen, GREY, pos1, mid_pos)


    pg.display.flip()

pg.quit()