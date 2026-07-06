# logger.py
import csv
from datetime import datetime

class LoggerEstatisticas:
    def __init__(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.arquivo_csv = f"estatisticas_{ts}.csv"
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        with open(self.arquivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "tempo_s",
                "e1_batidas", " e1_media_gasolina", " e1_media_distancia",
                " ||| ", " e2_batidas", " e2_media_gasolina", " e2_media_distancia",
            ])

    def gravar(self, tempo_ms, estrada1, estrada2):
        with open(self.arquivo_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                f"{tempo_ms / 1000:.1f}",
                f"||| {estrada1.contador_batidas}",
                f"{estrada1.media_gasolina:.2f}",
                f"{estrada1.media_distancia:.1f}",
                f"||| {estrada2.contador_batidas}",
                f"{estrada2.media_gasolina:.2f}",
                f"{estrada2.media_distancia:.1f}",
            ])
