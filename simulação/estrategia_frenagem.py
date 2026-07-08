# estrategia_frenagem.py
from abc import ABC, abstractmethod

class EstrategiaFrenagem(ABC):
    @abstractmethod
    def calcular_velocidade(self, carro, tempo_atual, alvos) -> float:
        pass

    def _obter_alvo_a_frente(self, carro, alvos):
        ALCANCE = carro.DISTANCIA_FRENAGEM + carro.altura + 20
        candidato, menor = None, float("inf")

        for outro in alvos:
            if outro is carro:
                continue

            if hasattr(outro, 'ativo') and not outro.ativo:
                continue
                
            if abs(outro.x_base - carro.x_base) >= 20:
                continue
                
            dist = outro.y - (carro.y + carro.altura)
            if 0 <= dist < ALCANCE and dist < menor:
                menor, candidato = dist, outro

        return candidato


class EstrategiaLivre(EstrategiaFrenagem):
    def calcular_velocidade(self, carro, tempo_atual, alvos) -> float:
        return float(carro.velocidade_base)


class EstrategiaSuave(EstrategiaFrenagem):
    def calcular_velocidade(self, carro, tempo_atual, alvos) -> float:
        frente = self._obter_alvo_a_frente(carro, alvos)

        if frente is not None:
            dist = frente.y - (carro.y + carro.altura)

            if dist < carro.DISTANCIA_FRENAGEM:
                carro.freando = True

                if dist <= carro.DISTANCIA_SEGURA:
                    vel_alvo = max(0.0, frente.velocidade_atual)
                else:
                    fator = (dist - carro.DISTANCIA_SEGURA) / (
                        carro.DISTANCIA_FRENAGEM - carro.DISTANCIA_SEGURA
                    )
                    vel_alvo = max(
                        0.0,
                        frente.velocidade_atual
                        + fator * (carro.velocidade_base - frente.velocidade_atual),
                    )

                if carro.velocidade_atual > vel_alvo:
                    return max(vel_alvo, carro.velocidade_atual - 0.3)
                else:
                    return min(vel_alvo, carro.velocidade_atual + 0.15)

        return min(float(carro.velocidade_base), carro.velocidade_atual + 0.15)


class EstrategiaReativa(EstrategiaFrenagem):
    def __init__(self):
        self.vel_frente_anterior = None
        self.esperando = False
        self.tempo_espera = 0

    def calcular_velocidade(self, carro, tempo_atual, alvos) -> float:
        frente = self._obter_alvo_a_frente(carro, alvos)

        if self.esperando:
            if tempo_atual - self.tempo_espera >= 1000:
                self.esperando = False
                self.vel_frente_anterior = None
            else:
                carro.freando = True
                return 0.0

        if frente is None:
            self.vel_frente_anterior = None
            return min(float(carro.velocidade_base), carro.velocidade_atual + 0.15)

        vel_frente_agora = frente.velocidade_atual
        dist = frente.y - (carro.y + carro.altura)

        frente_reduziu = (
            self.vel_frente_anterior is not None
            and vel_frente_agora < self.vel_frente_anterior - 0.5
        )

        if frente_reduziu or dist < carro.DISTANCIA_SEGURA:
            carro.freando = True
            nova_vel = max(0.0, carro.velocidade_atual - 1.5)

            if nova_vel == 0.0 and not self.esperando:
                self.esperando = True
                self.tempo_espera = tempo_atual
            return nova_vel

        elif dist < carro.DISTANCIA_FRENAGEM:
            carro.freando = True
            return min(float(carro.velocidade_base), max(0.0, vel_frente_agora))

        self.vel_frente_anterior = vel_frente_agora
        return min(float(carro.velocidade_base), carro.velocidade_atual + 0.15)
