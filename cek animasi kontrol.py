from ursina import *

Texture_list = [
    "grass",
    "noise",
    "vignette", 
    "brick",
    "test_tileset",
    "radial_gradient",
    "white_cube"
]

def input (key):
    if key == "space":
        cube.color = color.random_color()
    if key == "alt":
        cube.texture = random.choice(Texture_list)
    if key == "right arrow" :
        cube.rotation_x +=40
    if key == "up arrow" :
        cube.rotation_y +=10
    if key == "down arrow" :
        cube.rotation_z -=10
    if key == "left mouse down" :
        cube.scale *=1.1
    if key == "right mouse down" :
        cube.scale *=0.9




def update() : 
    global speed
    if held_keys['a']:
        cube.x -= time.dt * speed 
    if held_keys['d']:
        cube.x += time.dt * speed 
    if held_keys['w']:
        cube.y += time.dt * speed 
    if held_keys['s']:
        cube.y -= time.dt * speed 
    if held_keys['escape']:
       application.quit()
    
app = Ursina()

speed = 5

cube = Entity (
    model = "cube",
    texture = "grass",
    position = (0,0,0)
)

app.run()

