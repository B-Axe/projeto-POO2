# estrategia_factory.py
from estrategia_frenagem import EstrategiaSuave, EstrategiaReativa, EstrategiaLivre

class EstrategiaFactory:
    @staticmethod
    def criar(modo: str):
        if modo == "reativo":
            return EstrategiaReativa()
        elif modo == "livre":
            return EstrategiaLivre()
        return EstrategiaSuave()