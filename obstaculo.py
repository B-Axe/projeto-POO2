# obstaculo.py
import random
import pygame

class Obstaculo:
    # O buraco dura entre 2s e 3s antes de sumir
    DURACAO_MINIMA = 2000
    DURACAO_MAXIMA = 3000

    def __init__(self, x, y):
        self.x_base = x
        self.y = float(y)
        self.largura = 50
        self.altura = 35
        self.cor = (25, 25, 25)
        
        self.tempo_criacao = pygame.time.get_ticks()
        self.duracao = random.randint(self.DURACAO_MINIMA, self.DURACAO_MAXIMA)
        self.ativo = True

    def atualizar(self, tempo_atual):
        if tempo_atual - self.tempo_criacao >= self.duracao:
            self.ativo = False

    @property
    def velocidad_atual(self):
        return 0.0 

    @property
    def velocidade_atual(self):
        return 0.0

    def get_rect(self):
        return pygame.Rect(int(self.x_base), int(self.y), self.largura, self.altura)