import pygame, sys, random, math
from pygame.locals import *


#############################################################################

def rezize(image,resolution):
    return  pygame.transform.scale(pygame.image.load(image).convert(), resolution)

###############################################################################

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

############################################################################

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/v.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)
    def update(self):
        pass
    
#################################################################################################
      
class Fondo(pygame.sprite.Sprite):
    def __init__(self,imagen,left,top,resolution):
        self.image = rezize(imagen, resolution)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    
    def mov(self,PJ,keys,time,fondo2,resolution):

        if PJ.rect.x >= resolution[0]/2 and keys[K_RIGHT] and not PJ.choque:
            self.rect.left -= 0.5 * time
        if self.rect.left < 0 and keys[K_RIGHT] and PJ.rect.right == resolution[0]/2:
            fondo2.rect.left = self.rect.right

#############################################################################

class Camera(object):
    def __init__(self, camera_func, resolution):
        self.camera_func = camera_func
        self.state = Rect(0, 0, resolution[0], resolution[1])

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target,resolution):
        self.state = self.camera_func(self.state, target.rect,resolution)

def simple_camera(camera, target_rect,resolution):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+resolution[0]/2, -t+resolution[1]/2, w, h)

def complex_camera(camera, target_rect,resolution):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+(resolution[0]/2), -t+resolution[1]/2, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-resolution[0]), l)   # stop scrolling at the right edge
    t = max(-(camera.height-resolution[1]), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)

##################################################################################

class Burbuja(pygame.sprite.Sprite):
    def __init__(self, posx, posy, resolution):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/bb_1.png')
        self.rect =  Rect(posx, posy, 70, 66)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.vivo = True
        self.speed = 3
        self.proyectil = Proyectil(self)
        
    def update(self, pj, time, platforms,oils,resolution):
        """Movimiento de Personaje y colisiones"""
        if self.vivo:
            #if self.rect.top <= 0:
            #    self.rect.top = 0
            #    self.speed *= -1 
            #if self.rect.bottom >= resolution[1]:
            #    self.rect.bottom = resolution[1]
            #    self.speed *= -1 
            r = random.randint(0,1)
            if r == 1 and self.proyectil.wait:
                self.proyectil.wait = False 
            vx, vy = self.velocidad(pj) 

            for p in platforms:
                if pygame.sprite.collide_rect(self, p):
                    self.speed *= -1
                    self.rect.centery += self.speed

            for o in oils:
                if pygame.sprite.collide_circle(self, o):
                    self.speed *= -1
                    self.rect.centery += self.speed
                    
            self.proyectil.update(pj, time, self, vx, vy, platforms, oils,resolution) 

            self.rect.centery += self.speed
            
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
    
    def velocidad(self, pj):
        x1 = pj.rect.centerx - self.rect.centerx
        y1 = pj.rect.centery - self.rect.centery
        norm = math.sqrt(x1**2 + y1**2)
        x2 = x1/norm
        y2 = y1/norm
        return x2, y2
    
    def muerte(self):
        self.vivo = False
        self.image = pygame.image.load('Images/Others/vacio.png')

#########################################################################
     
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,burbuja):
        pygame.sprite.Sprite.__init__(self)
        self.wait = True
        self.image = pygame.image.load('Images/Others/vacio.png')
        self.rect = Rect(burbuja.rect.centerx, burbuja.rect.centery, 30, 28)
        self.rect.centerx = burbuja.rect.centerx
        self.rect.centery = burbuja.rect.centery
        self.speed = 10
        
    def update(self, pj, time, burbuja, vx, vy,platforms,oils,resolution):
        if self.wait:
            self.rect.centery = burbuja.rect.centery
            self.rect.centerx = burbuja.rect.centerx
        if not self.wait:
            self.image = pygame.image.load('Images/Others/bb_p.png')
            self.rect.centerx += vx*self.speed
            self.rect.centery += vy*self.speed
            for p in platforms:
                if pygame.sprite.collide_rect(self, p):
                    self.desaparicion(burbuja)
            for o in oils:
                if pygame.sprite.collide_rect(self, o):
                    self.desaparicion(burbuja)
            if not burbuja.vivo or self.rect.left <= 0 or self.rect.top <= 0 or self.rect.bottom >= resolution[1]:
                self.desaparicion(burbuja)
    
    def desaparicion(self, burbuja):
        self.wait = True
        self.image = pygame.image.load("Images/Others/vacio.png")

###################################################################################
              
class Slime(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Others/slime.png')
        self.rect = Rect(posx, posy, 39, 34)
        self.rect.centerx = posx
        self.rect.centery = posy
        self.speed = 0.1
        self.vivo = True
        self.right = False
        self.left = True
    
    def update(self, pj, time,platforms,oils):
        if self.vivo:
            #if pj.rect.centerx - self.rect.centerx > 0:
            #    self.right = True
            #    self.left = False
            #if pj.rect.centerx - self.rect.centerx < 0:
            #    self.left = True
            #    self.right = False
            for p in platforms:
                if pygame.sprite.collide_rect(self,p):
                    self.speed *= -1
                    self.rect.centerx += self.speed
            for o in oils:
                if pygame.sprite.collide_rect(self, o):
                    self.speed *= -1
                    self.rect.centerx += self.speed
            self.rect.centerx += self.speed
            if pygame.sprite.collide_rect(pj, self) and pj.attacking:
                self.muerte()
    def muerte(self):
            self.vivo = False
            self.image = pygame.image.load('Images/Others/vacio.png')
        
####################################################################################
      
class PJ(Entity,pygame.sprite.Sprite):
    def __init__(self, position,sprites):
        Entity.__init__(self)
        self.sheet = pygame.image.load(sprites)
        self.sheet.set_clip(pygame.Rect(6, 52, 30, 50))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.xvel=0
        self.yvel=0
        self.onGround=False
        self.attacking = False
        self.frame = 0
        self.alt=position[1]
        #stick
        self.right_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.left_states={ 0: (6, 52, 30, 50),
                           1: (49, 52, 30, 50),
                           2: (86, 52, 30, 50),
                           3: (123, 52, 35, 50),
                           4: (167, 52, 35, 50),
                           5: (215, 52, 30, 50)}
        self.upright_states={ 0: (16, 216, 32, 45),
                              1: (59, 216, 32, 45),
                              2: (103, 216, 32, 45),
                              3: (145, 216, 32, 45)}
        self.attackright_states={0: (24, 372, 43, 53),
                                 #1: (68, 372, 60, 53),
                                 #2: (132, 372, 60, 53),
                                 1: (195, 372, 60, 53),
                                 2: (255, 372, 60, 53)}
        #woman
        self.left_states={0:(518,203,39,60),
                           1:(553,203,39,60),
                           2:(587,203,39,60),
                           3:(624,203,39,60),
                           4:(660,203,37,60),
                           5:(691,203,39,60)}
        self.right_states={0:(724,203,39,60),
                           1:(758,203,37,60),
                           2:(790,203,39,60),
                           3:(827,203,39,60),
                           4:(863,203,39,60),
                           5:(900,203,39,60)}
        self.upleft_states={0:(274,452,39,60),
                           1:(320,452,39,60),
                           2:(362,452,39,60),
                           3:(410,452,39,60),
                           4:(454,452,37,60),
                           5:(492,452,39,60),
                           6:(534,452,39,60),
                           7:(570,452,39,60),
                           8:(602,452,39,60),
                           9:(640,452,39,60),
                           10:(683,452,39,60)}
        self.upright_states={0:(728,452,39,60),
                           1:(770,452,39,60),
                           2:(810,452,39,60),
                           3:(849,452,39,60),
                           4:(882,452,37,60),
                           5:(920,452,39,60),
                           6:(962,452,39,60),
                           7:(1003,452,39,60),
                           8:(1048,452,39,60),
                           9:(1093,452,39,60),
                           10:(1135,452,39,60)}
        
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect


    def update(self, up,right, left,attack,platforms):
        if attack:
            self.clip(self.attackright_states)
            self.attacking = True
        if self.rect.y==self.alt-10:
            self.onGround=True
        if up:
            if self.onGround:
                self.yvel=-30
            else:
                pass
        if right and self.onGround:
            if not attack:
                self.clip(self.right_states)
            self.xvel= 5
            if attack:
                self.clip(self.attackright_states)
        if left and self.onGround:
            self.clip(self.left_states)
            self.xvel= -5
        if not self.onGround:
            
            self.yvel+=5
            
            if self.yvel<-4:
                self.clip(self.upright_states[0])
            elif self.yvel<-1:
                self.clip(self.upright_states[1])
            elif self.yvel<2:
                self.clip(self.upright_states[2])
            elif self.yvel<4:
                self.clip(self.upright_states[3])
            elif self.yvel<7:
                self.clip(self.upright_states[4])
            elif self.yvel<10:
                self.clip(self.upright_states[5])
            elif self.yvel<12:
                self.clip(self.upright_states[6])
            elif self.yvel<13:
                self.clip(self.upright_states[7])
            elif self.yvel<20:
                self.clip(self.upright_states[7])
            elif self.yvel<23:
                self.clip(self.upright_states[8])
            if self.yvel>30:
                self.clip(self.upright_states[10])
                self.yvel=30
                
        if not (right or left):
            self.xvel=0
        if self.onGround and self.xvel==0 and not attack:
            self.clip(self.right_states[0])
        self.rect.x+=self.xvel
        self.collide(self.xvel,0,platforms,attack)
        self.rect.y+=self.yvel
        self.onGround=False
        self.collide(0, self.yvel , platforms,attack)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
    def reset(self,x,y):
        self.x = x
        self.y = y

        self.rect.center = (self.x, self.y,attack)
        
    def muerte_proyectil(self, enemigo):
        if pygame.sprite.collide_rect(self, enemigo.proyectil): 
            self.vivo = False
            self.image = pygame.image.load("Images/Others/vacio.png")
    
    def muerte_toque(self, enemigo):
        if pygame.sprite.collide_rect(self, enemigo):
            self.vivo = False
            self.image = pygame.image.load("Images/Others/vacio.png")
            
    def muerte_oil(self, oils):
        for o in oils:
            if pygame.sprite.collide_rect(self, o):
                self.vivo = False
                self.image = pygame.image.load("Images/Others/vacio.png")

    def collide(self, xvel, yvel, platforms,attack):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Platform) and not attack:
                    self.clip(self.right_states[0])
                    self.choque=True
                elif isinstance(p, Platform) and attack:
                    self.clip(self.attackright_states[0])
                    self.choque=True
                if isinstance(p, Water) and not attack:
                    self.clip(self.right_states[0])
                elif isinstance(p, Water) and attack:
                    self.clip(self.attackright_states[0])
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                        self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0        
        
    def handle_event(self,key,platforms):
        right=up=left=attack=False
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        if key[pygame.K_RIGHT]:
            right=True
        if key[pygame.K_UP]:
            up=True
        if key[pygame.K_LEFT]:
            left=True
        if key[pygame.K_k]:
            attack=True

        self.update(up,right,left,attack,platforms)

#############################################################################
    
class Oil(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/oil.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass
    
#############################################################################
    
class Valdosa(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/v.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass
    
#############################################################################
    
class Water(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("Images/Others/w.png")
        self.image.convert()
        self.rect = Rect(x, y, 18, 18)

    def update(self):
        pass

#################################################################################
    
def velocidad(pj, burbuja):
    x1 = pj.rect.centerx - burbuja.rect.centerx
    y1 = pj.rect.centery - burbuja.rect.centery
    norm = math.sqrt(x1**2 + y1**2)
    x2 = x1/norm
    y2 = y1/norm
    return x2, y2

###############################################################################

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("Images/Others/times.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
    
#####################################################################   

def main(resolution,sprites):

    fondo='Images/Others/fondo1.png' 
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    fondo1=Fondo('Images/Others/fondo1.png',0,0,resolution)
    fondo2=Fondo('Images/Others/fondo2.png',fondo1.rect.right,0,resolution)
    fondo3=Fondo('Images/Others/fondo3.png',fondo2.rect.right,0,resolution)
    
    x=y=0
    f= file("Maps/1_1.txt")
    level = f.readlines()
    platforms=[]
    burbujas = []
    slimes = []
    oils = []
    val=[]
    wat=[]
    
    entities=pygame.sprite.Group()
    for row in level:
        for col in row:
            if col =="p":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col =="b":
                b = Burbuja(x,y,resolution)
                burbujas.append(b)
                entities.add(b)
                entities.add(b.proyectil)
            if col =="s":
                s = Slime(x,y)
                slimes.append(s)
                entities.add(s)
            if col == "o":
                o = Oil(x,y)
                oils.append(o)
                entities.add(o)
            if col == "w":
                w = Water(x,y)
                wat.append(w)
                entities.add(w)
            if col == "v":
                v = Valdosa(x,y)
                val.append(v)
                entities.add(v)
            if col == "1":
                player = PJ((x,y),sprites)
                
            x += 18
        y += 18
        x = 0
    total_level_width  = len(level[0])*35
    total_level_height = len(level)*35
    camera = Camera(complex_camera, (total_level_width, total_level_height))
    entities.add(player)


    while True:
        
        time=clock.tick(60)
        key=pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                sys.exit()
        if fondo1.rect.right>=0:
            fondo1.mov(player,key,time,fondo2,resolution)
        if fondo1.rect.right<=0:
            fondo1.rect.left=fondo3.rect.right

        if fondo2.rect.right>=0:
            fondo2.mov(player,key,time,fondo3,resolution)
        if fondo2.rect.right<=0:
            fondo2.rect.left=fondo1.rect.right

        if fondo3.rect.right>=0:
            fondo3.mov(player,key,time,fondo1,resolution)
        if fondo3.rect.right<=0:
            fondo3.rect.left=fondo2.rect.right

        for b in burbujas:
            b.update(player, time, platforms, oils,resolution)
            player.muerte_proyectil(b)
            player.muerte_toque(b)
        for s in slimes:
            s.update(player, time, platforms, oils)
            player.muerte_toque(s)
            
        player.attacking = False
        player.muerte_oil(oils)
        
        player.handle_event(key,platforms)
        camera.update(player,resolution)
        background=pygame.image.load(fondo).convert()
        screen.blit(background,(0,0))
        screen.blit(fondo1.image,(fondo1.rect.left,fondo1.rect.top))
        screen.blit(fondo2.image,(fondo2.rect.left,fondo2.rect.top))
        screen.blit(fondo3.image,(fondo3.rect.left,fondo3.rect.top))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
     
        pygame.display.flip()
        clock.tick(30)
    return 0


