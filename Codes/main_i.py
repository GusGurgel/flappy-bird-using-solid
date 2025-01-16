# Interface Segregation

import pygame
from abc import abstractmethod
from random import uniform
import ctypes
from os.path import join

from platform import system

# Resolução de problema de tela no windows
if system() == "Windows":
	ctypes.windll.user32.SetProcessDPIAware()

# Objeto que não precisa ser desenhado
class InvisibleObject():
    def __init__(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

# Objeto genérico do jogo
class Object():
    def __init__(self, image, rect, layer):
        self.image = image
        self.rect = rect
        self.layer = layer

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, display_surface):
        if self.image != None:
            display_surface.blit(self.image, self.rect)

class MovableObject(Object):
    def __init__(self, image, rect, layer, inital_acceleration = (0, 0), do_move=False):
        super().__init__(image, rect, layer)
        self.acceleration = pygame.Vector2(*inital_acceleration)
        self.do_move = do_move

    @abstractmethod
    def update_acceleration(self, dt):
        pass

    def update(self, dt):
        # Aplicar aceleração
        if self.do_move:
            self.rect.center += self.acceleration * dt
            self.update_acceleration(dt)
        return super().update(dt)

class HorizontalMovableObject(MovableObject):
    def __init__(self, image, rect, layer, inital_acceleration=(0, 0), do_move=False):
        super().__init__(image, rect, layer, inital_acceleration, do_move)
    
    def update_acceleration(self, dt):
        keys = pygame.key.get_pressed()
        self.acceleration.x = (keys[pygame.K_d] - keys[pygame.K_a]) * 50
        super().update_acceleration(dt)

# Container de objetos
class ObjectContainer():
    def __init__(self, objects):
        self.objects = objects
    
    def update_objects(self, dt):
        for object in self.objects:
            object.update(dt)
    
    def draw_objects(self, display_surface):
        objects = filter(lambda x : type(x).__base__ in [Object, MovableObject], self.objects)
        for object in sorted(objects, key=lambda x : x.layer):
            object.draw(display_surface)

# Plano de fundo
class Background(MovableObject):
    def __init__(self):
        image = pygame.image.load(join("images", "bg.png"))
        rect = image.get_frect()
        layer = 0

        self.do_move = False
        super().__init__(image, rect, layer, (-40, 0))
    
    # Resetar posicão do plano de fundo
    def reset_position(self):
        if self.rect.left < -200:
            self.rect.topleft = (0, 0)
    
    # Começar o mover quando clickar
    def start_move_on_click(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.do_move = True
    
    # Resetar background
    def reset(self):
        self.rect.topleft = (0, 0)
        self.do_move = False

    def update(self, dt):
        super().update(dt)
        self.start_move_on_click()
        self.reset_position()

# Pássaro
class Bird(MovableObject):
    def __init__(self):
        self.gravity = 3
        self.bird_image_index = 0
        self.bird_max_vertical_acceleration = 200
        self.bird_jump_coldown = 0.25
        self.bird_jump_force = 100
        self.bird_clock = self.bird_jump_coldown

        self.bird_images = [
            pygame.image.load(join("images", "bird_1.png")),
            pygame.image.load(join("images", "bird_2.png"))
        ]
        
        image = self.bird_images[self.bird_image_index]
        rect = image.get_frect(center=(14, 65))
        layer = 1

        super().__init__(image, rect, layer)

    def update_acceleration(self, dt):
        # Aplicando gravidade
        self.acceleration.y += self.gravity
        self.bird_clock += dt

        if self.acceleration.y >= self.bird_max_vertical_acceleration:
            self.acceleration.y = self.bird_max_vertical_acceleration
        elif self.acceleration.y < -self.bird_max_vertical_acceleration:
            self.acceleration.y = -self.bird_max_vertical_acceleration

        # Aplicando pulo
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            if self.bird_clock >= self.bird_jump_coldown:
                self.acceleration.y = 0
                self.acceleration.y -= self.bird_jump_force
                self.bird_clock = 0
        
        super().update_acceleration(dt)
    
    def start_move_on_click(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.do_move = True

    def reset(self):
        self.do_move = False
        self.rect.center = (14, 65)
        self.bird_image_index = 0
        self.acceleration = pygame.Vector2(0, 0)

    def animate(self):
        if self.acceleration.y <= 0:
            self.image = self.bird_images[0]
        else:
            self.image = self.bird_images[1]
    
    def update(self, dt):
        super().update(dt)
        self.start_move_on_click()
        self.animate()

# Canos
class DoublePipe(Object):
    def __init__(self):
        self.image1 = self.pipe_1_image = pygame.image.load(join("images", "pipe_1.png"))
        self.image2 = self.pipe_2_image = pygame.image.load(join("images", "pipe_2.png"))
        self.rect1 = self.pipe_1_image.get_frect()
        self.rect2 = self.pipe_2_image.get_frect()

        self.pipes_speed = 60
        self.pipes_dist_range = (80, 90)
        self.pipes_position_offset_range = (-30, 30)
        self.do_move = False

        super().__init__(None, None, 1)
        self.reset()

    def draw(self, display_surface):
        display_surface.blit(self.image1, self.rect1)
        display_surface.blit(self.image2, self.rect2)
    
    def reset(self):
        distance_pipes = uniform(*self.pipes_dist_range)/2
        offset = uniform(*self.pipes_position_offset_range)

        self.rect1.bottomleft = (105, 140+distance_pipes+offset)
        self.rect2.topleft = (105, -distance_pipes+offset)

        self.do_move = False
    
    def move(self, dt):
        if self.rect1.right < 0:
            self.reset()

        self.rect1.centerx -= self.pipes_speed * dt
        self.rect2.centerx -= self.pipes_speed * dt
    
    def update(self, dt):
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.do_move = True

        if self.do_move:
            self.move(dt)

class Death(InvisibleObject):
    def __init__(self, bird, double_pipe, kill_operation):
        self.bird = bird
        self.double_pipe = double_pipe
        self.kill_operation = kill_operation
    
    # Matar pássaro quando colidir com cano
    def kill_by_collision(self):
        if self.bird.rect.colliderect(self.double_pipe.rect1)\
        or self.bird.rect.colliderect(self.double_pipe.rect2):
            self.kill_operation()
    
    # Matar pássaro quando sair do mapa
    def kill_by_out_of_bounds(self):
        if self.bird.rect.bottom < -10:
            self.kill_operation()
        elif self.bird.rect.top > 150:
            self.kill_operation()

    def update(self, dt):
        self.kill_by_collision()
        self.kill_by_out_of_bounds()

class Score(Object):
    def __init__(self):
        self.font = pygame.font.SysFont("ProggyClean Nerd Font Propo", 16)
        self.score = 0
        image = self.font.render(f"score {self.score}", False, "white")
        rect = image.get_frect()

        super().__init__(image, rect, 1)
    
    def add_score(self):
        self.score += 1
        self.image = self.font.render(f"score {self.score}", False, "white")
        self.rect = self.image.get_frect()
    
    def reset(self):
        self.score = 0
        self.image = self.font.render(f"score {self.score}", False, "white")

class ScoreObserver(InvisibleObject):
    def __init__(self, bird, pipes, score):
        self.bird = bird
        self.pipes = pipes
        self.score = score

        self.score_added = True
    
    def update(self, _):
        if self.bird.rect.centerx > self.pipes.rect1.centerx:
            self.score_added = False
        else:
            if not self.score_added:
                self.score.add_score()
                self.score_added = True

class Game:
    def __init__(self):
        # inicar pygame
        pygame.init()

        # crinado superfície principal
        self.display_surface = pygame.display.set_mode(
            (500, 700),
            vsync=1
        )
        self.display_rect = self.display_surface.get_frect()

        # criando superfície de pintura
        self.sub_display_surface = pygame.surface.Surface(
            (100, 140),
            pygame.SRCALPHA
        )
        self.sub_display_rect = self.sub_display_surface.get_frect()

        # mudando título
        pygame.display.set_caption("Flappy Bird Clone")

        # propriedades
        self.running = True
        self.starte = False
        self.clock = pygame.Clock()
        self.background_color = "skyblue"

        # objetos
        self.bird = Bird()
        self.background = Background()
        self.double_pipe = DoublePipe()
        self.death = Death(self.bird, self.double_pipe, self.reset)
        self.score = Score()
        self.score_observer = ScoreObserver(self.bird, self.double_pipe, self.score)

        self.objects_container = ObjectContainer([
            self.bird,
            self.background,
            self.double_pipe,
            self.death,
            self.score,
            self.score_observer
        ])

    def reset(self):
        self.double_pipe.reset()
        self.bird.reset()
        self.background.reset()
        self.score.reset()
        self.score_observer.score_added = True
    
    # resolver os eventos
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False

    # atualizar jogo
    def update(self, dt):
        self.objects_container.update_objects(dt)

    # desenhar objetos
    def draw(self):
        # desenhar superfície de desenho
        self.display_surface.blit(
            pygame.transform.scale(
                self.sub_display_surface,
                (self.display_rect.w, self.display_rect.h)
            )
        )

        # limpar superfície
        self.sub_display_surface.fill(self.background_color)

        self.objects_container.draw_objects(self.sub_display_surface)

        # flip the screen buffer
        pygame.display.update()  
    
    # iniciar jogo
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        # Quit services
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()