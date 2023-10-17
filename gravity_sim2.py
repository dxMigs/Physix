import pygame as pg
from itertools import combinations
import math

pg.init()

#Körper Objekt
class Body:
    def __init__(self, pos, mass, velocity, color, radius, name=""):
        #Geschwindigkeit und Position als zwei dimensionale Vektoren festlegen
        self.pos = pg.Vector2(pos) 
        self.velocity = pg.Vector2(velocity) 
        self.mass = mass
        self.color = color
        self.radius = radius
        self.name = name
        self.spur = [(pos[0], pos[1])]
        self.repetitions = 0

    #Funtkion zur Aktualisierung der Position
    def update_position(self):
        self.pos += (self.velocity*dt) / FPS
        self.repetitions += 1
        if self.name == 'rakete' and self.repetitions >= 100/dt*15:
            self.spur.append(self.pos.xy)
            self.repetitions = 0
        elif self.name != 'rakete' and self.repetitions >= 100/dt*25: 
            self.spur.append(self.pos.xy)
            self.repetitions = 0
        if not self.name == 'rakete' and len(self.spur) > 100: self.spur.pop(0)
    
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
WIDTH = 1200
HEIGHT = 900

#Farben
RED = (240, 0, 0)
BLUE = (0, 0, 240)
GREEN = (0, 240, 0)
BLACK= (0, 0, 0)
SATURN_FARBE = (209, 138, 41)
TITAN_FARBE = (255,165,0)
GREY = (130, 130, 130)
LIGHT_GREY = (170, 170, 170)

#Berechnungen pro Sekunde
FPS = 16384

#Verhältnis Konstante
VH = 0.000_000_12

#Umrechungskonste
UK = 1/math.sqrt(VH)

#Konstanten
G = 6.674*10**-11 * VH

#Uhr die die Geschwindigkeit der Simulation festlegt
clock = pg.time.Clock()
dt = 64

#Fonts
text_font = pg.font.SysFont("Arial", 25)

#Fenster starten
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen_center = (screen.get_width() // 2, screen.get_height() // 2)

#Liste der Körper anlegen
bodies = []
planets = []

#Saturn Objekt
masse_saturn = float(5.638*10**26 * VH)
radius_saturn = 7
Saturn = Body((screen_center[0], screen_center[1]), masse_saturn, (0,0), SATURN_FARBE, radius_saturn, name="saturn")
bodies.append(Saturn)
planets.append(Saturn)

#Titan Objekt
masse_titan = float(1.345*10**23 * VH)
position_titan = (screen_center[0], screen_center[1] - float(1_221_000_000*VH))
velocity_titan = (math.sqrt(float(G)*(float(Saturn.mass))/float(1_221_000_000*VH)), 0)
radius_titan = 4
Titan = Body(position_titan, masse_titan, velocity_titan, TITAN_FARBE, radius_titan, name="titan")
bodies.append(Titan)
planets.append(Titan)

#Iapetus Objekt
masse_iapetus = float(1.81*10**21 * VH)
position_iapetus = (screen_center[0], screen_center[1] - float(3_561_000_000*VH))
velocity_iapetus = (math.sqrt(float(G)*(float(Saturn.mass))/float(3_561_000_000*VH)), 0)
radius_iapetus = 4
Iapetus = Body(position_iapetus, masse_iapetus, velocity_iapetus, GREY, radius_iapetus, name="iapetus")
bodies.append(Iapetus)
planets.append(Iapetus)

#Rhea Objekt
masse_rhea = float(2.3*10**21 * VH)
position_rhea = (screen_center[0], screen_center[1] - float(527_000_000*VH))
velocity_rhea = (math.sqrt(float(G)*(float(Saturn.mass))/float(527_000_000*VH)), 0)
radius_rhea = 4
Rhea = Body(position_rhea, masse_rhea, velocity_rhea, GREY, radius_rhea, name="rhea")
bodies.append(Rhea)
planets.append(Rhea)

#Rakete Objekt
masse_rakete = float(3000 * VH)
position_rakete = (screen_center[0], screen_center[1] - float(100_000_000*VH))
velocity_rakete = (math.sqrt(float(G)*float(masse_saturn)/float(100_000_000*VH)), 0) 
radius_rakete = 2
Rakete = Body(position_rakete, masse_rakete, velocity_rakete, GREEN, radius_rakete, name = "rakete")
bodies.append(Rakete)

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

#Berechung des Transfer-Winkels "Thada"
def transfer_angle(planet, distance, transfer_lines = True):
    global SP_line
    if transfer_lines == True:
        pg.draw.line(screen, GREEN, Saturn.pos, planet.pos,2)
        pg.draw.line(screen, GREEN, Saturn.pos, Rakete.pos,2)
    SP_line = pg.math.Vector2(planet.pos-Saturn.pos)
    SR_line = pg.math.Vector2(Rakete.pos-Saturn.pos)

    thada = SP_line.angle_to(SR_line)
    
    a = (SP_line.length()+SR_line.length())/2
    transfer_period = 2*math.pi*math.sqrt(a**3/G*Saturn.mass)/2

    a_planet = SP_line.length()
    planet_period = 2*math.pi*math.sqrt(a_planet**3/G*Saturn.mass)

    alpha = transfer_period/planet_period * 360
    needed_thada = -(180 - alpha)

    if round(needed_thada, 0) == round(thada, 0):
        transfer_beschleunigen(SP_line, SR_line, distance)

def rocket_speed(real=True):
    if real:
        real_speed = math.sqrt((float(Rakete.velocity[0]*UK))**2+(float(Rakete.velocity[1]*UK))**2)
        return real_speed
    else:
        speed = math.sqrt((float(Rakete.velocity[0]))**2+(float(Rakete.velocity[1]))**2)
        return speed
    
beschleunigt = False
def transfer_beschleunigen(SP_line, SR_line, distance):
    global beschleunigt
    speed = rocket_speed(real=False)
    needed_velocity = math.sqrt(float(G) * float(Saturn.mass) * ((2/(float(SR_line.length())))-(1/((SP_line.length()+float(distance*VH)+float(SR_line.length()))/2))))
    beschleunigungs_faktor = float(needed_velocity)/float(speed)
    if not beschleunigt:
        delta_v_requirement(rocket_speed(), needed_velocity*UK)
        Rakete.velocity *= beschleunigungs_faktor
        beschleunigt = True 


counter = 0
beschleunigt_2 = False
def titan_beschleunigen(x_acceleration, y_acceleration, delay):
    global counter, beschleunigt_2, acceleration_distance
    if round(int(get_distance_periapsis('titan')/1000), 1) == 2662 and not beschleunigt_2:
        counter += 1
        if counter >= delay:
            inititial_velocity = rocket_speed()
            Rakete.velocity[0] *= x_acceleration
            Rakete.velocity[1] *= y_acceleration
            acceleration_distance = round(int(get_actual_distance(Titan)/1000), 1)
            final_velocity = rocket_speed()
            delta_v_requirement(inititial_velocity, final_velocity)
            beschleunigt_2 = True

distances = dict(titan=[], rhea=[], iapetus=[], saturn=[])
def save_distances():
    global distances
    for planet in planets:
        rocket_pos = pg.math.Vector2(Rakete.pos)
        planet_pos = pg.math.Vector2(planet.pos)
        distance = pg.math.Vector2.distance_to(rocket_pos, planet_pos)/VH
        distances[planet.name].append(distance)
        for distance in distances[planet.name]:
            if distance != get_distance_periapsis(planet.name) and distance != get_distance_apoapsis(planet.name):
                distances[planet.name].remove(distance) 

def get_distance_periapsis(planet_name):
    periapsis = min(distances[planet_name])
    return periapsis
    
def get_distance_apoapsis(planet_name):
    apoapsis = max(distances[planet_name])
    return apoapsis

def get_actual_distance(planet):
    rocket_pos = pg.math.Vector2(Rakete.pos)
    planet_pos = pg.math.Vector2(planet.pos)
    distance = pg.math.Vector2.distance_to(rocket_pos, planet_pos)/VH
    return distance
        
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

time_elapsed = 0
def zeit_vergangen():
    global time_elapsed
    time_elapsed += ((1*dt/FPS)*UK)/4
    seconds = time_elapsed
    minutes = seconds/60
    hours = time_elapsed/3600
    days = time_elapsed/86400 
    return days, hours, minutes
    
def show_info():
    daten_titan = f"{round(int(get_actual_distance(Titan)/1000), 1)} km, {round(int(get_distance_periapsis('titan')/1000), 1)} km, {round(int(get_distance_apoapsis('titan')/1000), 1)} km"
    daten_rhea = f"{round(int(get_actual_distance(Rhea)/1000), 1)} km, {round(int(get_distance_periapsis('rhea')/1000), 1)} km, {round(int(get_distance_apoapsis('rhea')/1000), 1)} km"
    daten_saturn = f"{round(int(get_actual_distance(Saturn)/1000), 1)} km, {round(int(get_distance_periapsis('saturn')/1000), 1)} km, {round(int(get_distance_apoapsis('saturn')/1000), 1)} km"
    draw_text(f"Geschwindigkeit Rakete: {round(rocket_speed(), 1)} m/s", text_font, LIGHT_GREY , 5, 5)
    draw_text(f"Titan ΔD, Pa, Aa: {daten_titan}", text_font, LIGHT_GREY , 5, 35)
    draw_text(f"Rhea ΔD, Pa, Aa:  {daten_rhea}", text_font, LIGHT_GREY , 5, 65)
    draw_text(f"Saturn ΔD, Pa, Aa: {daten_saturn}", text_font, LIGHT_GREY, 5, 95)
    time_string = f"{int(zeit_vergangen()[0])} Tage : {int(zeit_vergangen()[1])} Stunden : {int(zeit_vergangen()[2])} Minuten"
    x = len(time_string)*10
    draw_text(time_string, text_font, LIGHT_GREY , WIDTH-x, 5)
    draw_text("Delta-V Anforderungen:", text_font, LIGHT_GREY, 5, 155)
    unpacked = ", ".join(delta_v_list)
    draw_text(unpacked, text_font, LIGHT_GREY, 5, 185)
    fast_forward_string = f"Zeitgeschwindigkeit: {int(dt)}"
    x2 = len(fast_forward_string)*10
    draw_text(fast_forward_string, text_font, LIGHT_GREY, WIDTH-x2, 35)
    if beschleunigt_2:
        draw_text(f"Höhe Beschleunigung Titan: {acceleration_distance} km", text_font, LIGHT_GREY, 5, 245)

#Eine Liste mit Delta-V Anforderungen
delta_v_list = []
def delta_v_requirement(inititial_velocity, final_velocity):
    global delta_v_list
    delta_v = final_velocity - inititial_velocity
    delta_v_list.append(str(round(delta_v,1))+" m/s")

#Simulationsschleife
running = True
while running:
    clock.tick(FPS)
    update_screen()
    gravitation_function()
    save_distances()
    rocket_speed()
    transfer_angle(Titan, -3_000_000, transfer_lines=False)
    titan_beschleunigen(2.5, 2.5, 30)
    show_info()
    zeit_vergangen()
    
    for event in pg.event.get():
        if event.type == pg.QUIT: running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if dt != 2048:
                    dt *= 2
            if event.key == pg.K_LEFT:
                if dt > 1:
                    dt /= 2

    
                
    
    pg.display.flip()