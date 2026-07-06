# renderer.py
import pygame

class Renderer:
    VERDE    = (40, 160, 40)
    CINZA    = (70, 70, 70)
    BRANCO   = (255, 255, 255)
    VERMELHO = (255, 0, 0)
    PRETO    = (0, 0, 0)
    AMARELO  = (255, 255, 0)
    LARANJA  = (255, 140, 0)

    def __init__(self, largura_slot, altura_tela):
        self.LARGURA_SLOT = largura_slot
        self.ALTURA_TELA = altura_tela
        self.fonte = pygame.font.SysFont("monospace", 13)
        self.fonte_hud = pygame.font.SysFont("monospace", 18, bold=True)

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

        # Desenhar os obstáculos ativos
        for obs in estrada.obstaculos:
            base_y = cy - (obs.y - estrada.carro_ref.y)
            tela_y = estrada.zoom_y(base_y, cy)
            tela_x = estrada.zoom_x(obs.x_base, cx)
            
            larg = int(obs.largura * estrada.zoom)
            alt = int(obs.altura * estrada.zoom)
            # Desenha um retângulo escuro com borda laranja de atenção
            pygame.draw.rect(superficie, obs.cor, (int(tela_x), int(tela_y), larg, alt))
            pygame.draw.rect(superficie, self.LARANJA, (int(tela_x), int(tela_y), larg, alt), max(1, int(2 * estrada.zoom)))

        # Desenhar os carros
        for carro in estrada.carros:
            base_y = cy - (carro.y - estrada.carro_ref.y)
            tela_y = estrada.zoom_y(base_y, cy)
            tela_x = estrada.zoom_x(carro.x_base, cx)
            self._desenhar_carro(superficie, carro, tela_x, tela_y, estrada.zoom)

    def _desenhar_carro(self, surf, carro, x, y, zoom):
        larg = int(60 * zoom)
        alt  = int(100 * zoom)
        cor  = self.VERMELHO if carro.batido else carro.cor

        pygame.draw.rect(surf, cor, (int(x), int(y), larg, alt))

        for rx in (10, 50):
            pygame.draw.circle(surf, self.PRETO,
                (int(x + rx * zoom), int(y + 90 * zoom)), int(10 * zoom))

        for fx in (15, 45):
            pygame.draw.circle(surf, self.AMARELO,
                (int(x + fx * zoom), int(y + 10 * zoom)), int(5 * zoom))

        if carro.freando and not carro.batido:
            fy = int(y + alt - int(8 * zoom))
            for bx in (5, 40):
                pygame.draw.rect(surf, self.VERMELHO,
                    (int(x + bx * zoom), fy, int(15 * zoom), int(6 * zoom)))

        txt = self.fonte.render(f"{carro.velocidade_atual:.1f}", True, self.BRANCO)
        surf.blit(txt, (int(x + 5 * zoom), int(y) - 16))

    def desenhar_hud(self, tela, estrada1, estrada2):
        configs = [
            (estrada1, "Estrada 1 (frenagem suave)",   8),
            (estrada2, "Estrada 2 (frenagem reativa)", self.LARGURA_SLOT + 8),
        ]

        for estrada, label, x_tela in configs:
            linhas = [
                (f"{label} - Batidas: {estrada.contador_batidas}", (255, 80,  80)),
                (f"Média gasolina:  {estrada.media_gasolina:.1f}", (255, 200, 50)),
                (f"Média distância: {estrada.media_distancia:.0f}", (100, 220, 255)),
                (f"Obstáculos em pista: {len(estrada.obstaculos)}", (255, 140, 0))
            ]

            renderizadas = [
                self.fonte_hud.render(texto, True, cor)
                for texto, cor in linhas
            ]

            w = max(r.get_width() for r in renderizadas) + 8
            h = sum(r.get_height() for r in renderizadas) + 4 + len(renderizadas) * 2
            pygame.draw.rect(tela, self.PRETO, (x_tela, 8, w, h))

            y_cur = 11
            for surf_linha in renderizadas:
                tela.blit(surf_linha, (x_tela + 4, y_cur))
                y_cur += surf_linha.get_height() + 2
