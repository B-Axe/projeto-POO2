# carro.py
import random
import pygame

class Carro:
    DISTANCIA_FRENAGEM = 150
    DISTANCIA_SEGURA   = 110

    def __init__(self, x, y, cor, estrategia):
        self.x_base = x
        self.y      = float(y)
        self.cor    = cor
        self.estrategia = estrategia

        self.velocidade_base  = random.randint(2, 7)
        self.velocidade_atual = float(self.velocidade_base)

        self.largura = 60
        self.altura  = 100

        self.batido       = False
        self.tempo_batida = 0
        self.freando      = False

        #estatisticas acumuladas
        self.gasolina_total  = 0.0
        self.distancia_total = 0.0

    def atualizar(self, tempo_atual, alvos):
        if self.batido:
            self.velocidade_atual = 0.0 #velocidade zero enquanto estiver batido
            if tempo_atual - self.tempo_batida > 5000:
                self.batido = False
                self.velocidade_atual = float(self.velocidade_base)
            else:
                return

        self.freando = False

        self.velocidade_atual = self.estrategia.calcular_velocidade(self, tempo_atual, alvos)

        self.y += self.velocidade_atual
        self._consumir_gasolina()

    def _consumir_gasolina(self):
        if self.velocidade_atual == 0.0:
            consumo = 0.0
        elif self.freando:
            consumo = self.velocidade_atual * 0.3
        else:
            consumo = self.velocidade_atual * 1.0

        self.gasolina_total  += consumo
        self.distancia_total += self.velocidade_atual

    def trocar_velocidade(self):
        if not self.batido:
            self.velocidade_base = random.randint(2, 7)

    def get_rect(self):
        return pygame.Rect(int(self.x_base), int(self.y), self.largura, self.altura)
