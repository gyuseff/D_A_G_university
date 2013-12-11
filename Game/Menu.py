import pygame
pygame.init()  
class GameMenu():  #para un menu de TODAS LAS OPCIONES que se quieran, solo se deben agregar a la lista jiji
    def __init__(self, screen, items,resolution, bg_color=(0,0,0), font=None, font_size=90,font_color_off=(255,255,255),font_color_on=(255,0,0)):
        self.resolution=resolution
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color_off
        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color_off)
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
            self.items.append([item, label, (width, height), (posx, posy)])
    def run(self):
        choosi=1
        while True:
            self.screen.blit(pygame.transform.scale(pygame.image.load('Images/Others/menu_chafa.png').convert(), self.resolution),(0,0))
            for name, label, (width, height), (posx, posy) in self.items:
                    self.screen.blit(label, (posx, posy))       #Display basico
            for event in pygame.event.get():                   #QUe ocurre con las teclas
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if choosi==1:
                        choosi=len(self.items)
                    else:
                        choosi-=1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if choosi==len(self.items):
                        choosi=1
                    else:
                        choosi+=1 
                if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                    pass
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    pass
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return choosi  #Retorna el valor de la opcion elegida
            for man in range(len(self.items)):       #Genera la lista y colorea la opcion que esta siendo seleccionada
                self.items[man][1]=self.font.render(str(self.items[man][0]), 1, (255,255,255))
            self.items[choosi-1][1]=self.font.render(str(self.items[choosi-1][0]), 1, (0,229,38)) 
            pygame.display.flip()   