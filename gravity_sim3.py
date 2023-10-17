import pygame as pg
from itertools import combinations
import math


pg.init()

#Körper Objekt
class Body:
    def __init__(self, pos, mass, velocity, color, radius, name="", velocity_vecor_angle=0):
        #Geschwindigkeit und Position als zwei dimensionale Vektoren festlegen
        self.pos = pg.Vector2(pos) 
        self.velocity = pg.Vector2(velocity) 
        self.velocity.rotate_ip(velocity_vecor_angle)
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
        if not self.name == 'rakete' and len(self.spur) > 500/dt*500: self.spur.pop(0)
    
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
WIDTH = 1920
HEIGHT = 1080

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

#Astronomische Einheit
AE = 149597870700

#Berechnungen pro Sekunde
FPS = 16384

#Verhältnis Konstante
VH = 0.000_000_000_35

#Umrechungskonste
UK = 1/math.sqrt(VH)

#Konstanten
G = 6.674*10**-11 * VH

#Uhr die die Geschwindigkeit der Simulation festlegt
clock = pg.time.Clock()
dt = 1024

#Fonts
text_font = pg.font.SysFont("Arial", 25)

#Fenster starten
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
screen_center = (screen.get_width() // 2, screen.get_height() // 2)

#Liste der Körper anlegen
bodies = []
planets = []

#Sonne Objekt
masse_sonne = float(1.989*10**30 * VH)
radius_sonne = 8
Sonne = Body((screen_center[0], screen_center[1]), masse_sonne, (0,0), YELLOW, radius_sonne, name="sonne")
bodies.append(Sonne)
planets.append(Sonne)

#Jupiter Objekt
masse_jupiter = float(1.898*10**27 * VH)
position_jupiter = (screen_center[0], screen_center[1] - float(5.204*AE*VH))
velocity_jupiter = (math.sqrt(float(G)*(float(Sonne.mass))/float(5.204*AE*VH)), 0)
radius_jupiter = 4
Jupiter = Body(position_jupiter, masse_jupiter, velocity_jupiter, JUPITER_FARBE, radius_jupiter, name="jupiter")
bodies.append(Jupiter)
planets.append(Jupiter)

#Saturn Objekt
spawn_angle_saturn = -math.radians(82.57645)
r_saturn = float(9.582*AE*VH)
y = math.cos(spawn_angle_saturn)*r_saturn
x = math.sin(spawn_angle_saturn)*r_saturn
position_saturn = (screen_center[0] - x, screen_center[1] - y)
velocity_saturn = (math.sqrt(float(G)*(float(Sonne.mass))/float(9.582*AE*VH)),0)
masse_saturn = float(5.638*10**26 * VH)
radius_saturn = 4
Saturn = Body(position_saturn, masse_saturn, velocity_saturn, SATURN_FARBE, radius_saturn, name="saturn", velocity_vecor_angle=-math.degrees(spawn_angle_saturn))
bodies.append(Saturn)
planets.append(Saturn)

#Erde Objekt
masse_erde = float (5.972*10**24 * VH)
position_erde = (screen_center[0], screen_center[1] - float(AE*VH))
velocity_erde = (math.sqrt(float(G)*(float(Sonne.mass))/float(AE*VH)), 0)
radius_erde = 3
Erde = Body(position_erde, masse_erde, velocity_erde, EARTH_COLOR, radius_erde, name="erde")
bodies.append(Erde)
planets.append(Erde)

#Venus Objekt
masse_venus = float(4.864*10**24 * VH)
position_venus = (screen_center[0], screen_center[1] - float(0.723*AE*VH))
velocity_venus = (math.sqrt(float(G)*(float(Sonne.mass))/float(0.723*AE*VH)), 0)
radius_venus = 3
Venus = Body(position_venus, masse_venus, velocity_venus, ORANGE, radius_venus, name="venus")
bodies.append(Venus)
planets.append(Venus)

#Rakete Objekt
masse_rakete = float(3000*VH)
position_rakete = (screen_center[0], screen_center[1] - float(1.015*AE*VH))
velocity_rakete = (math.sqrt(float(G)*float(Sonne.mass)/float(1.015*AE*VH)), 0) 
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
    SP_line = pg.math.Vector2(planet.pos-Sonne.pos)
    SR_line = pg.math.Vector2(Rakete.pos-Sonne.pos)

    thada = float(SP_line.angle_to(SR_line))
    
    a = float((SP_line.length()+SR_line.length())/2)
    transfer_period = float(2*math.pi*math.sqrt(a**3/G*Sonne.mass)/2)

    a_planet = float(SP_line.length())
    planet_period = float(2*math.pi*math.sqrt(a_planet**3/G*Sonne.mass))

    alpha = float(transfer_period/planet_period * 360)
    needed_thada = float(-(180 - alpha))

    if int(needed_thada) == int(thada):
        transfer_acceleration(SP_line, SR_line, distance)

def rocket_speed(real=True):
    if real:
        real_speed = math.sqrt((float(Rakete.velocity[0]*UK))**2+(float(Rakete.velocity[1]*UK))**2)
        return real_speed
    else:
        speed = math.sqrt((float(Rakete.velocity[0]))**2+(float(Rakete.velocity[1]))**2)
        return speed
    
beschleunigt = False
def transfer_acceleration(SP_line, SR_line, distance):
    global beschleunigt
    speed = rocket_speed(real=False)
    needed_velocity = math.sqrt(float(G) * float(Sonne.mass) * ((2/(float(SR_line.length())))-(1/((SP_line.length()+float(distance*VH)+float(SR_line.length()))/2))))
    beschleunigungs_faktor = float(needed_velocity)/float(speed)
    if not beschleunigt:
        delta_v_requirement(rocket_speed(), needed_velocity*UK)
        Rakete.velocity *= beschleunigungs_faktor
        beschleunigt = True 


counter = 0
beschleunigt_2 = False
def swing_by_acceleration(planet, distance, x_acceleration, y_acceleration, delay):
    global counter, beschleunigt_2, acceleration_distance
    if round(int(get_distance_periapsis(planet)/1000), 1) == distance and not beschleunigt_2:
        counter += 1
        if counter >= delay:
            inititial_velocity = rocket_speed()
            Rakete.velocity[0] *= x_acceleration
            Rakete.velocity[1] *= y_acceleration
            acceleration_distance = round(int(get_actual_distance(Venus)/1000), 1)
            final_velocity = rocket_speed()
            delta_v_requirement(inititial_velocity, final_velocity)
            beschleunigt_2 = True

distances = dict(sonne=[], erde=[], venus=[], saturn=[], jupiter=[])
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
    time_elapsed += int(((1*dt/FPS)*UK)/4)
    seconds = time_elapsed
    minutes = seconds/60
    hours = minutes/60
    days = hours/24
    years = days/365
    return years, days, hours

def show_info():
    daten_sonne = f"{round(int(get_actual_distance(Sonne)/1000), 1)} km, {round(int(get_distance_periapsis('sonne')/1000), 1)} km, {round(int(get_distance_apoapsis('sonne')/1000), 1)} km"
    daten_erde = f"{round(int(get_actual_distance(Erde)/1000), 1)} km, {round(int(get_distance_periapsis('erde')/1000), 1)} km, {round(int(get_distance_apoapsis('erde')/1000), 1)} km"
    daten_venus = f"{round(int(get_actual_distance(Venus)/1000), 1)} km, {round(int(get_distance_periapsis('venus')/1000), 1)} km, {round(int(get_distance_apoapsis('venus')/1000), 1)} km"
    daten_jupiter = f"{round(int(get_actual_distance(Jupiter)/1000), 1)} km, {round(int(get_distance_periapsis('jupiter')/1000), 1)} km, {round(int(get_distance_apoapsis('jupiter')/1000), 1)} km"
    daten_saturn = f"{round(int(get_actual_distance(Saturn)/1000), 1)} km, {round(int(get_distance_periapsis('saturn')/1000), 1)} km, {round(int(get_distance_apoapsis('saturn')/1000), 1)} km"
    draw_text(f"Geschwindigkeit Rakete (rel.S.): {round(rocket_speed(), 1)} m/s", text_font, LIGHT_GREY , 5, 5)
    draw_text(f"Erde ΔD, Pa, Aa: {daten_erde}", text_font, LIGHT_GREY , 5, 5 + 30)
    draw_text(f"Venus ΔD, Pa, Aa:  {daten_venus}", text_font, LIGHT_GREY , 5, 5 + 30*2)
    draw_text(f"Jupiter ΔD, Pa, Aa: {daten_jupiter}", text_font, LIGHT_GREY, 5, 5 + 30*3)
    draw_text(f"Saturn ΔD, Pa, Aa: {daten_saturn}", text_font, LIGHT_GREY, 5, 5 + 30*4)
    draw_text(f"Sonne ΔD, Pa, Aa: {daten_sonne}", text_font, LIGHT_GREY, 5, 5 + 30*5)
    time_string = f"{int(zeit_vergangen()[0])} Jahre : {int(zeit_vergangen()[1])} Tage : {int(zeit_vergangen()[2])} Stunden"
    x = len(time_string)*10
    draw_text(time_string, text_font, LIGHT_GREY , WIDTH-x, 5)
    draw_text("Delta-V Anforderungen:", text_font, LIGHT_GREY, 5, 5 + 30*7)
    unpacked = ", ".join(delta_v_list)
    draw_text(unpacked, text_font, LIGHT_GREY, 5,  5 + 30*8)
    fast_forward_string = f"Zeitgeschwindigkeit: {int(dt)}"
    x2 = len(fast_forward_string)*10
    draw_text(fast_forward_string, text_font, LIGHT_GREY, WIDTH-x2, 35)
    if beschleunigt_2:
        draw_text(f"Höhe Beschleunigung Titan: {acceleration_distance} km", text_font, LIGHT_GREY, 5, 5 + 30*10)

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
    transfer_angle(Jupiter, -3780000*1000, transfer_lines=False)
    swing_by_acceleration('venus', 2910, 2.5, 2.5, 30)
    show_info()
    zeit_vergangen()
    
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

    pg.display.flip()

pg.quit()