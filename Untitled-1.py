from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Initialize the Ursina app
app = Ursina()

# Load textures
chair_texture = load_texture('school chair texture.png')

# Create multiple chairs in a grid pattern
rows = 4      # Number of rows
cols = 4      # Number of columns
for i in range(rows):
    for j in range(cols):
        kursi = Entity(model='school chair.obj', scale=0.4, texture=chair_texture, collider='box', x=-6 + j * 4, z=5 + i * 3)

# Add one chair in front of the papan_tulis
additional_chair = Entity(model='school chair.obj', scale=0.4, texture=chair_texture, collider='box', x=0, z=18, y=0)

# Add a beamer on top of the additional chair
beamer = Entity(model='Beamer_timco.fbx', scale=0.05, position=(0, 1.2, 18))

# Create the ground
ground = Entity(model='plane', scale=(100,1,100), color=color.white.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')

# Create walls and barriers
barrier = Entity(model='cube', scale=(20,2,0.5), color=color.orange, collider='box', x=0, z=2)
dinding1 = Entity(model='cube', scale=(20,12,1), color=color.white, texture='dinding texture.jpeg', collider='box', x=0, z=-2)
dinding2 = Entity(model='cube', scale=(20,12,1), color=color.white, texture='dinding texture.jpeg', collider='box', x=0, z=22)
dinding3 = Entity(model='cube', scale=(24,12,1), color=color.white, texture='dinding texture.jpeg', collider='box', x=-10, z=10, rotation_y=90)
dinding4 = Entity(model='cube', scale=(24,12,1), color=color.white, texture='dinding texture.jpeg', collider='box', x=10, z=10, rotation_y=90)

# Create papan_tulis for each dinding
papan_tulis1 = Entity(model='cube', scale=(8,4,0.5), color=color.white, texture='200w.gif', collider='mesh', x=0, y=3, z=21)
papan_tulis2 = Entity(model='cube', scale=(8,4,0.5), color=color.white, texture='200w.gif', collider='mesh', x=0, y=3, z=33)
papan_tulis3 = Entity(model='cube', scale=(8,4,0.5), color=color.white, texture='200w.gif', collider='mesh', x=-10, y=3, z=10, rotation_y=90)
papan_tulis4 = Entity(model='cube', scale=(8,4,0.5), color=color.white, texture='200w.gif', collider='mesh', x=10, y=3, z=10, rotation_y=90)

# Create a door on the right wall
door = Entity(model='cube', scale=(2,4,0.1), color=color.brown, collider='box', x=10, y=2, z=5, rotation_y=90)

# Create the ceiling
ceiling = Entity(model='cube', scale=(20,1,24), color=color.white, texture='dinding texture.jpeg', collider='box', x=0, y=6, z=10)

# Initialize lists for bullets and moving targets
bullets = []
moving_targets = []

# Create moving targets at random positions
for i in range(6):
    x = random.randrange(-9, 9, 2)
    y = random.randrange(1, 6, 1)
    z = random.randrange(3, 21, 2)
    moving_target = Entity(model='cube', color=color.white, texture='botol.jpg', scale=(1,1,0.1), dx=0.05, position=(x,y,z), collider='box')
    moving_targets.append(moving_target)

# Create a pistol entity attached to the camera
pistol = Entity(parent=camera, model='cube', color=color.gray, origin_y=-0.5, scale=(0.5,0.5,2), position=(2,-1,2.5), collider='box')

# Create a player with first-person controls
player = FirstPersonController(model='cube', y=0, origin_y=-.5)
player.pistol = pistol

# Handle input events
def input(key):
    global bullets
    if key == 'left mouse down' and player.pistol:
        bullet = Entity(parent=pistol, model='cube', scale=.1, position=(0,0.5,0), speed=3, color=color.black, collider='box')
        bullets.append(bullet)
        pistol.blink(color.white)
        bullet.world_parent = scene

# Update the game state
def update():
    for m in moving_targets:
        m.x += m.dx
        if m.x > 9:
            m.x = 9
            m.dx *= -1
        if m.x < -9:
            m.x = -9
            m.dx *= -1

    global bullets
    if len(bullets) > 0:
        for b in bullets:
            b.position += b.forward * 8
            hit_info = b.intersects()
            if hit_info.hit:
                if hit_info.entity in moving_targets:
                    moving_targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    if len(moving_targets) == 0:
                        message = Text(text='YOU WON', scale=2, origin=(0,0), background=True, color=color.blue)
                        application.pause()
            if b.z > 100 or b.z < -100 or b.x > 100 or b.x < -100:  # Bullet out of bounds check
                destroy(b)
                bullets.remove(b)

# Run the Ursina app
app.run()
