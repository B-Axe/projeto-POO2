# jogo.py
# Classe principal: janela, renderização, HUD e gravação de estatísticas

import pygame
import csv
from datetime import datetime
from estrada import Estrada


class Jogo:

    LARGURA_SLOT = 750
    LARGURA_TELA = LARGURA_SLOT * 2
    ALTURA_TELA  = 800

    VERDE    = (40, 160, 40)
    CINZA    = (70, 70, 70)
    BRANCO   = (255, 255, 255)
    VERMELHO = (255, 0, 0)
    PRETO    = (0, 0, 0)
    AMARELO  = (255, 255, 0)

    def __init__(self):

        self.tela = pygame.display.set_mode((self.LARGURA_TELA, self.ALTURA_TELA))
        pygame.display.set_caption("Simulação de Trânsito com Obstáculos (Buracos)")

        self.clock     = pygame.time.Clock()
        self.fonte     = pygame.font.SysFont("monospace", 13)
        self.fonte_hud = pygame.font.SysFont("monospace", 18, bold=True)

        # CONFIGURAÇÃO DOS TEMPOS DE SPAWN AQUI:
        # estrada 1: frenagem suave - buracos a cada 1.5s a 3s (1500ms a 3000ms)
        self.estrada1 = Estrada("config1.txt", offset_x_tela=0, modo_carro="suave", 
                                spawn_min=1500, spawn_max=3000)
                                
        # estrada 2: frenagem reativa - buracos a cada 5s a 8s (5000ms a 8000ms)
        self.estrada2 = Estrada("config2.txt", offset_x_tela=self.LARGURA_SLOT, modo_carro="reativo", 
                                spawn_min=5000, spawn_max=8000)

        self.estradas = [self.estrada1, self.estrada2]

        self.ultimo_registro    = 0
        self.intervalo_registro = 10000  # grava estatísticas a cada 10 segundos

        self.nome_arquivo_csv = f"dados_simulacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self._inicializar_csv()

    # --------------------------------------------------
    def _inicializar_csv(self):
        with open(self.nome_arquivo_csv, mode="w", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([
                "Tempo(ms)", 
                "E1_Batidas", "E1_Gasolina_Media", "E1_Distancia_Media",
                "E2_Batidas", "E2_Gasolina_Media", "E2_Distancia_Media"
            ])

    # --------------------------------------------------
    def _gravar_estatisticas(self, tempo_atual):
        with open(self.nome_arquivo_csv, mode="a", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([
                tempo_atual,
                self.estrada1.contador_batidas,
                f"{self.estrada1.media_gasolina:.2f}",
                f"{self.estrada1.media_distancia:.1f}",
                f"||| {self.estrada2.contador_batidas}",
                f"{self.estrada2.media_gasolina:.2f}",
                f"{self.estrada2.media_distancia:.1f}",
            ])

    # --------------------------------------------------
    def rodar(self):

        surfs = [
            pygame.Surface((self.LARGURA_SLOT, self.ALTURA_TELA))
            for _ in self.estradas
        ]

        rodando = True
        while rodando:

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    rodando = False

            tempo_atual = pygame.time.get_ticks()

            for estrada in self.estradas:
                estrada.atualizar(tempo_atual)

            if tempo_atual - self.ultimo_registro >= self.intervalo_registro:
                self._gravar_estatisticas(tempo_atual)
                self.ultimo_registro = tempo_atual

            self.tela.fill(self.VERDE)

            for estrada, surf in zip(self.estradas, surfs):
                self.desenhar_estrada(estrada, surf)
                self.tela.blit(surf, (estrada.offset_x, 0))

            pygame.draw.line(self.tela, self.PRETO,
                (self.LARGURA_SLOT, 0), (self.LARGURA_SLOT, self.ALTURA_TELA), 3)

            self.desenhar_hud()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    # --------------------------------------------------
    def desenhar_estrada(self, estrada, superficie):

        W, H = self.LARGURA_SLOT, self.ALTURA_TELA
        superficie.fill(self.VERDE)

        if not estrada.carro_ref:
            return

        cy, cx = H // 2, W // 2

        ex = estrada.zoom_x(estrada.estrada_x_local, cx)
        ew = estrada.estrada_largura * estrada.zoom
        pygame.draw.rect(superficie, self.CINZA, (int(ex), 0, int(ew), H))

        NUM_FAIXAS = 7
        lf = estrada.estrada_largura / NUM_FAIXAS
        for f in range(1, NUM_FAIXAS):
            xl = estrada.zoom_x(estrada.estrada_x_local + f * lf, cx)
            for i in range(-H * 2, H * 2, 80):
                ym = i + (estrada.carro_ref.y % 80)
                yt = estrada.zoom_y(ym, cy)
                pygame.draw.rect(superficie, self.BRANCO,
                    (int(xl), int(yt), int(8 * estrada.zoom), int(40 * estrada.zoom)))

        # === DESENHAR OS BURACOS (OBSTÁCULOS) ===
        for obs in estrada.obstaculos:
            base_y = cy - (obs.y - estrada.carro_ref.y)
            tela_y = estrada.zoom_y(base_y, cy)
            tela_x = estrada.zoom_x(obs.x_base, cx)
            larg = int(obs.largura * estrada.zoom)
            alt = int(obs.altura * estrada.zoom)
            
            # Desenha o fundo escuro elíptico do buraco
            pygame.draw.ellipse(superficie, obs.cor, (int(tela_x), int(tela_y), larg, alt))
            # Desenha uma borda amarela ao redor para sinalização visual
            pygame.draw.ellipse(superficie, (255, 235, 0), (int(tela_x), int(tela_y), larg, alt), max(1, int(2 * estrada.zoom)))

        # Desenhar os carros
        for carro in estrada.carros:
            base_y = cy - (carro.y - estrada.carro_ref.y)
            tela_y = estrada.zoom_y(base_y, cy)
            tela_x = estrada.zoom_x(carro.x_base, cx)
            self._desenhar_carro(superficie, carro, tela_x, tela_y, "%s" % carro.velocidade_atual, estrada.zoom)

    # --------------------------------------------------
    def _desenhar_carro(self, surf, carro, x, y, texto, zoom):

        larg = int(carro.largura * zoom)
        alt  = int(carro.altura * zoom)

        # Se o carro estiver acidentado, ele fica obrigatoriamente Vermelho
        cor = self.VERMELHO if carro.batido else carro.cor
        pygame.draw.rect(surf, cor, (int(x), int(y), larg, alt))

        # rodas traseiras
        for rx in (10, 50):
            pygame.draw.circle(surf, self.PRETO,
                (int(x + rx * zoom), int(y + 90 * zoom)), int(10 * zoom))

        # faróis
        for fx in (15, 45):
            pygame.draw.circle(surf, self.AMARELO,
                (int(x + fx * zoom), int(y + 10 * zoom)), int(5 * zoom))

        # luzes de freio
        if carro.freando and not carro.batido:
            fy = int(y + alt - int(8 * zoom))
            for bx in (5, 40):
                pygame.draw.rect(surf, self.VERMELHO,
                    (int(x + bx * zoom), fy, int(15 * zoom), int(6 * zoom)))

        # texto da velocidade
        v_float = float(texto)
        txt = self.fonte.render(f"{v_float:.1f}", True, self.BRANCO)
        surf.blit(txt, (int(x + 5 * zoom), int(y) - 16))

    # --------------------------------------------------
    def desenhar_hud(self):

        configs = [
            (self.estrada1, "Estrada 1 (frenagem suave)",   8),
            (self.estrada2, "Estrada 2 (frenagem reativa)", self.LARGURA_SLOT + 8),
        ]

        for estrada, label, x_tela in configs:

            linhas = [
                (f"{label} - Batidas: {estrada.contador_batidas}", (255, 80,  80)),
                (f"Média gasolina:  {estrada.media_gasolina:.1f}", (255, 200, 50)),
                (f"Média distância: {estrada.media_distancia:.0f}", (100, 220, 255)),
                (f"Buracos activos: {len(estrada.obstaculos)}", (255, 140, 0))
            ]

            renderizadas = [
                self.fonte_hud.render(texto, True, cor)
                for texto, cor in linhas
            ]

            w = max(r.get_width() for r in renderizadas) + 8
            h = sum(r.get_height() for r in renderizadas) + 4 + len(renderizadas) * 2

            pygame.draw.rect(self.tela, self.PRETO, (x_tela, 8, w, h))

            y_cur = 11
            for surf_linha in renderizadas:
                self.tela.blit(surf_linha, (x_tela + 4, y_cur))
                y_cur += surf_linha.get_height() + 2
