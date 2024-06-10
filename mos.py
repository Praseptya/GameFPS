from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from math import atan2, degrees

app = Ursina()


# Menambahkan objek 2.5D yang terlihat dari kedua sisi==================================

class Object2_5D(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.front = Entity(parent=self, model='quad', texture='char1.png', scale=(3, 3), double_sided=True)
        self.position = (5, 1.5, 0)
        self.message_index = 0
        self.current_text = None 
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        direction = camera.world_position - self.world_position
        angle = atan2(direction.x, direction.z)
        self.rotation_y = degrees(angle)

    def input(self, key):
        if key == 'e' and distance(self.world_position, camera.world_position) < 4:
            self.show_message()

    def show_message(self):
        if self.current_text:
            destroy(self.current_text)
        
        messages = [
            'Cobalah tembak semua target',
            'Gampang kok, tinggal klik aja mouse kiri',
             'ish jangan ganggu mulu ih',
            'coba tambahin fitur atau object lainnya',
            'soon tba'

        ]
        
        message = messages[self.message_index]
        self.current_text = Text(
            text=message,
            origin=(0, 0),
            position=(0, 0.3),
            color=color.yellow
        )
        self.current_text.fade_out(duration=3)
        
        self.message_index = (self.message_index + 1) % len(messages)

object_2_5d = Object2_5D()

# 1. field

# Menambahkan banyak kursi dalam baris dan kolom
rows = 4      # jumlah baris
cols = 4  # jumlah kolom
chair_texture = load_texture('school chair texture.png')
for i in range(rows):
    for j in range(cols):
        kursi = Entity(model='school chair.obj', scale=0.4, texture=chair_texture, collider='box', x=-6 + j * 4, z=5 + i * 3)
        
ground = Entity(model='plane', scale=(100,1,100), color=color.white.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
barrier = Entity(model='cube', scale=(20,2,0.5), color=color.orange, collider='box', x=0, z=2)
dinding1 = Entity(model='cube', scale=(20,12,1), color=color.white, texture = 'dinding texture.jpeg',collider='box', x=0, z=-2)
papan_tulis = Entity (model = 'cube', scale=(8,4,0.5), color = color.white, texture = '200w.gif', collider='mesh', x= 0,y= 3, z= 21)
papan_tulis2 = Entity (model = 'cube', scale=(10,5,0.5), color = color.white, texture = 'sky.jpg', collider='mesh', x= 0,y= 3, z= -1.5)
papan_tulis3 = Entity (model = 'cube', scale=(6,3,0.5), color = color.white, texture = 'sky.jpg', collider='mesh', x= 9.7,y= 3, z= 12, rotation_y=90)
papan_tulis4 = Entity (model = 'cube', scale=(6,3,0.5), color = color.white, texture = 'sky.jpg', collider='mesh', x= 9.7,y= 3, z= 5, rotation_y=90)
dinding2 = Entity(model='cube', scale=(20,12,1), color=color.white, texture = 'dinding texture.jpeg',collider='box', x=0, z=22)
dinding3 = Entity(model='cube', scale=(24,12,1), color=color.white, texture = 'dinding texture.jpeg',collider='box', x=-10, z=10, rotation_y=90)
dinding4 = Entity(model='cube', scale=(24,12,1), color=color.white,texture = 'dinding texture.jpeg', collider='box', x=10, z=10, rotation_y=90)

# 2. entitas
peluru = []
moving_targets = []

# Load target textures
target_textures = [load_texture('botol.jpg'), load_texture('sky.jpg'), load_texture('smoke.jpg')]

# 3. target placement
for i in range(6):
    x = random.randrange(-9, 9, 2)
    y = random.randrange(1, 6, 1)
    z = random.randrange(3, 21, 2)
    texture = random.choice(target_textures)
    moving_target = Entity(model='cube', color=color.white, texture=texture, scale=(1,1,0.1), dx=0.05, position=(x,y,z), collider='box')
    moving_targets.append(moving_target)

# 4. pistol
pistol = Entity(parent=camera, model='pistol.obj', scale=0.1, rotation=(90,30,50) ,position=(1, -0.5, 1.5), collider='box')

# 5. player
player = FirstPersonController(model='cube', y=0, origin_y=-.5)
player.pistol = pistol

# 6. interact peluru
def shoot():
    bullet = Entity(parent=pistol, model='cube', scale=0.3, color=color.black, collider='box')
    bullet.world_parent = scene
    bullet.position = player.pistol.world_position + player.pistol.forward * -2.3
    bullet.look_at(bullet.position + camera.forward)
    peluru.append(bullet)
    pistol.blink(color.white)
        
# Interval untuk menembak secara terus menerus
shoot_interval = 0.1
shoot_timer = 0

def input(key):
    if key == 'left mouse down':
        shoot()
        
        

# 7. Interact object (klo di hit ilang)
def update():
    global shoot_timer

    if held_keys['left mouse']:
        shoot_timer -= time.dt
        if shoot_timer <= 0:
            shoot()
            shoot_timer = shoot_interval

    for m in moving_targets:
        m.x += m.dx
        if m.x > 9:
            m.x = 9
            m.dx *= -1
        if m.x < -9:
            m.x = -9
            m.dx *= -1

    if held_keys['escape']:
        application.quit()
   
    global peluru
    if len(peluru) > 0:
        for b in peluru:
            b.position += b.forward * time.dt * 500
            hit_info = b.intersects()
            if hit_info.hit:
                if hit_info.entity in moving_targets:
                    moving_targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    destroy(b)
                    peluru.remove(b)
                    if len(moving_targets) == 0:
                        message = Text(text='YOU WON', scale=2, origin=(0,0), background=True, color=color.blue)
                        if held_keys['escape']:
                            application.quit()

app.run()
