import pygame
import ctypes
from os.path import join
from random import uniform

from platform import system

if system() == "Windows":
	ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        # [ iniciando pygame ]
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

        # [ propriedades ]
        self.running = True
        self.clock = pygame.Clock()
        self.gravity = 3
        self.started = False
        self.score_added = False
        self.score = 0

        # [ objetos ]

        # plano de fundo
        self.background_image = pygame.image.load(join("images", "bg.png"))
        self.background_rect = self.background_image.get_frect()
        self.background_speed = 40
        self.background_color = "skyblue"

        # pássaro
        self.bird_images = [
            pygame.image.load(join("images", "bird_1.png")),
            pygame.image.load(join("images", "bird_2.png"))
        ]
        self.bird_image_index = 0
        self.bird_rect = self.bird_images[0].get_frect(center=(15, (self.sub_display_rect.h/2)-5))
        self.bird_acceleration = pygame.Vector2(0, 0)
        self.bird_max_vertical_acceleration = 200
        self.bird_jump_coldown = 0.25
        self.bird_jump_force = 100
        self.bird_clock = self.bird_jump_coldown

        # canos
        self.pipes_speed = 60
        self.pipes_dist_range = (80, 90)
        self.pipes_position_offset_range = (-30, 30)
        self.pipe_1_image = pygame.image.load(join("images", "pipe_1.png"))
        self.pipe_2_image = pygame.image.load(join("images", "pipe_2.png"))

        distance_pipes = uniform(*self.pipes_dist_range)/2
        offset = uniform(*self.pipes_position_offset_range)

        pos = (self.sub_display_rect.w, self.sub_display_rect.h+distance_pipes+offset)
        self.pipe_1_rect = self.pipe_1_image.get_frect(bottomleft=pos)
        pos = (self.sub_display_rect.w, -distance_pipes+offset)
        self.pipe_2_rect = self.pipe_2_image.get_frect(topleft=pos)

        # score text
        self.font = pygame.font.SysFont("ProggyClean Nerd Font Propo", 16)
        self.score_color = "#eeeeee"
        self.score_text_surface = self.font.render(f"score: {self.score}", False, self.score_color)

    # mover o plano de fundo
    def move_background(self, dt):
        self.background_rect.centerx -= self.background_speed * dt
        if self.background_rect.left < -(2*self.sub_display_rect.w):
            self.background_rect.topleft = (0, 0)
    
    # mover o pássaro
    def move_bird(self, dt):
        # Aplicando gravidade
        self.bird_acceleration.y += self.gravity
        self.bird_clock += dt

        if self.bird_acceleration.y >= self.bird_max_vertical_acceleration:
            self.bird_acceleration.y = self.bird_max_vertical_acceleration
        elif self.bird_acceleration.y < -self.bird_max_vertical_acceleration:
            self.bird_acceleration.y = -self.bird_max_vertical_acceleration
        
        # Aplicando pulo
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            if self.bird_clock >= self.bird_jump_coldown:
                self.bird_acceleration.y = 0
                self.bird_acceleration.y -= self.bird_jump_force
                self.bird_clock = 0
        
        # Matar pássaro se sair da tela
        if self.bird_rect.top > self.sub_display_rect.bottom + 20:
            self.reset_game()
            return
        
        if self.bird_rect.bottom < self.sub_display_rect.top - 20:
            self.reset_game()
            return

        self.bird_rect.center += self.bird_acceleration * dt
    
    # mover canos
    def move_pipes(self, dt):
        if not self.score_added and self.pipe_1_rect.centerx < self.bird_rect.centerx:
            self.score += 1
            self.score_text_surface = self.font.render(f"score: {self.score}", False, self.score_color)
            self.score_added = True

        if self.pipe_1_rect.right < 0:
            distance_pipes = uniform(*self.pipes_dist_range)/2
            offset = uniform(*self.pipes_position_offset_range)

            pos = (self.sub_display_rect.w+10, self.sub_display_rect.h+distance_pipes+offset)
            self.pipe_1_rect.bottomleft = pos
            pos = (self.sub_display_rect.w+10, -distance_pipes+offset)
            self.pipe_2_rect.topleft = pos

            self.score_added = False

        self.pipe_1_rect.centerx -= self.pipes_speed * dt
        self.pipe_2_rect.centerx -= self.pipes_speed * dt

    # animar o pássaro
    def animate_bird(self):
        self.bird_image_index = 0 if self.bird_acceleration.y < 0 else 1
    
    # resolver colisões
    def handle_collision(self):
        if self.bird_rect.colliderect(self.pipe_1_rect)\
        or self.bird_rect.colliderect(self.pipe_2_rect):
            self.reset_game()
    
    # resetar o jogo
    def reset_game(self):
        self.started = False
        self.score = 0
        self.score_added = False

        # resetar pássaro
        self.bird_acceleration.y = 0
        self.bird_image_index = 0
        self.bird_rect.center=(15, (self.sub_display_rect.h/2)-5)

        # resetar canos
        distance_pipes = uniform(*self.pipes_dist_range)/2
        offset = uniform(*self.pipes_position_offset_range)
        pos = (self.sub_display_rect.w+10, self.sub_display_rect.h+distance_pipes+offset)
        self.pipe_1_rect.bottomleft = pos
        pos = (self.sub_display_rect.w+10, -distance_pipes+offset)
        self.pipe_2_rect.topleft = pos
    
    # resolver os eventos
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False

    # atualizar jogo
    def update(self, dt):
        if not self.started and (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
            self.started = True
            self.score_text_surface = self.font.render(f"score: {self.score}", False, self.score_color)
        if not self.started:
            return
        self.move_background(dt)
        self.move_pipes(dt)
        self.animate_bird()
        self.handle_collision()
        self.move_bird(dt)

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


        # desnhar plano de fundo
        self.sub_display_surface.blit(self.background_image, 
                                        self.background_rect)

        # desenhar pássaro
        self.sub_display_surface.blit(self.bird_images[self.bird_image_index],
                                      self.bird_rect)

        # desenhar canos
        self.sub_display_surface.blit(self.pipe_1_image,
                                      self.pipe_1_rect)
        
        self.sub_display_surface.blit(self.pipe_2_image,
                                      self.pipe_2_rect)

        self.sub_display_surface.blit(self.score_text_surface)

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