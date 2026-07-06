# estrada.py
import pygame
import random
from carro import Carro
from obstaculo import Obstaculo
from config_loader import carregar_config
from estrategia_factory import EstrategiaFactory

class Estrada:
    def __init__(self, nome_arquivo, offset_x_tela, modo_carro="suave", spawn_min=3000, spawn_max=6000):
        self.offset_x   = offset_x_tela
        self.modo_carro = modo_carro
        
        # Guardamos os tempos de spawn configurados para esta estrada específica
        self.spawn_min = spawn_min
        self.spawn_max = spawn_max

        estrada_x, estrada_largura, carros_cfg = carregar_config(nome_arquivo)
        self.estrada_x_local = estrada_x
        self.estrada_largura = estrada_largura

        self.faixas_disponiveis = sorted(list(set(c["x"] for c in carros_cfg)))

        self.carros = [
            Carro(c["x"], c["y"], c["cor"], estrategia=EstrategiaFactory.criar(modo_carro))
            for c in carros_cfg
        ]

        self.obstaculos = []
        # Define o primeiro spawn baseado no tempo customizado da estrada
        self.proximo_obstaculo_tempo = pygame.time.get_ticks() + random.randint(self.spawn_min, self.spawn_max)

        self.carro_ref = self._carro_central()
        self.zoom             = 1.0
        self.tempo_troca      = pygame.time.get_ticks()
        self.contador_batidas = 0

    def _carro_central(self):
        if not self.carros:
            return None
        ordenados = sorted(self.carros, key=lambda c: c.y)
        return ordenados[len(ordenados) // 2]

    @property
    def media_gasolina(self):
        if not self.carros:
            return 0.0
        return sum(c.gasolina_total for c in self.carros) / len(self.carros)

    @property
    def media_distancia(self):
        if not self.carros:
            return 0.0
        return sum(c.distancia_total for c in self.carros) / len(self.carros)

    def calcular_zoom(self):
        if not self.carro_ref or len(self.carros) < 2:
            self.zoom = 1.0
            return
        maior = max(abs(c.y - self.carro_ref.y) for c in self.carros)
        self.zoom = max(0.3, 1 - maior / 1500) if maior > 300 else 1.0

    def zoom_y(self, y, cy): return cy + (y - cy) * self.zoom
    def zoom_x(self, x, cx): return cx + (x - cx) * self.zoom

    def verificar_colisoes(self, tempo_atual):
        # Carro com Carro
        for c1 in self.carros:
            if c1.batido:
                continue
            for c2 in self.carros:
                if c1 is c2 or c2.batido:
                    continue
                if abs(c1.x_base - c2.x_base) >= 20:
                    continue
                if c1.get_rect().colliderect(c2.get_rect()):
                    if c1.y < c2.y:
                        c1.batido = True
                        c1.tempo_batida = tempo_atual
                        self.contador_batidas += 1
                    elif c2.y < c1.y:
                        c2.batido = True
                        c2.tempo_batida = tempo_atual
                        self.contador_batidas += 1

        # Carro com Buraco
        for c in self.carros:
            if c.batido:
                continue
            for obs in self.obstaculos:
                if abs(c.x_base - obs.x_base) < 20 and c.get_rect().colliderect(obs.get_rect()):
                    c.batido = True
                    c.tempo_batida = tempo_atual
                    self.contador_batidas += 1

    def _gerar_obstaculo(self, tempo_atual):
        if not self.carros or not self.faixas_disponiveis:
            return
            
        carro_sorteado = random.choice(self.carros)
        faixa = random.choice(self.faixas_disponiveis)
        pos_y = carro_sorteado.y + random.randint(180, 350)
        
        self.obstaculos.append(Obstaculo(faixa, pos_y))
        
        # Usa as variáveis da instância configuradas no jogo.py para agendar o próximo buraco
        self.proximo_obstaculo_tempo = tempo_atual + random.randint(self.spawn_min, self.spawn_max)

    def atualizar(self, tempo_atual):
        if tempo_atual - self.tempo_troca > 3000:
            for c in self.carros:
                c.trocar_velocidade()
            self.tempo_troca = tempo_atual

        if tempo_atual >= self.proximo_obstaculo_tempo:
            self._gerar_obstaculo(tempo_atual)

        for obs in self.obstaculos:
            obs.atualizar(tempo_atual)
        self.obstaculos = [o for o in self.obstaculos if o.ativo]

        todos_alvos = self.carros + self.obstaculos

        for c in self.carros:
            c.atualizar(tempo_atual, todos_alvos)

        self.verificar_colisoes(tempo_atual)
        self.calcular_zoom()
        self.carro_ref = self._carro_central()