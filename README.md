# Trabalho de POO2  curso de ciencias da computação do IFC-Blumenau.

<p align="center">
    <img width="220" height="320" alt="IF" src="https://github.com/user-attachments/assets/b3a2614e-bac5-43d1-bd4d-89f1f8fc8bf5" />
</p>

---

### Sobre o projeto: 
Simulação em Python/Pygame de duas estradas paralelas, cada uma povoada por múltiplos carros que reagem a obstáculos (buracos) e a outros veículos usando estratégias de frenagem distintas. O projeto compara, lado a lado e em tempo real, o comportamento de uma frenagem suave (gradual) contra uma frenagem reativa (baseada em resposta a mudanças bruscas do carro da frente).

### Diagrama de classes:
<img width="770" height="919" alt="diagrama_simulação" src="https://github.com/user-attachments/assets/d4a89f68-a7cb-4888-8744-8bc6556b5b46" />

### Diagrama:
- plantuml_export.puml — diagrama de classes em formato PlantUML

O projeto foi refatorado de um único arquivo monolítico para uma arquitetura multi-arquivo orientada a objetos, isolando regras de negócio (Carro, Estrada, estratégias de frenagem) da camada de apresentação (Jogo, Renderer) e da persistência de dados (logger.py, config_loader.py).

### Visão da simulação:
- A tela será dividida em 2 painéis
  - Estrada1 - frenagem suave: os carros reduzem a velocidade progressivamente conforme se aproximam de um obstáculo, calculando um fator de desaceleração baseado na distância.
  - Estrada2 - frenagem reativa: os carros só freiam bruscamente quando percebem que o carro da frente desacelerou ou quando a distância de segurança é violada, entrando em um estado de espera antes de retomar a velocidade.
- Cada estrada gera obstáculos (buracos) em intervalos configuráveis, registra colisões, consumo de combustível fictício e distância percorrida, exportando essas estatísticas periodicamente para um arquivo CSV.
- Ao final da execução (ou periodicamente, a cada 10 segundos), um arquivo dados_simulacao_AAAAMMDD_HHMMSS.csv é gerado na raiz do projeto com o histórico de colisões, consumo médio e distância média de cada estrada.

### Print do código em execução:
<img width="1872" height="1012" alt="começo da execução" src="https://github.com/user-attachments/assets/dd50bc92-e95a-4a64-8836-20d6651195ee" />

### Configurações das estradas:
- Cada estrada é descrita em um arquivo de texto simples:
```bash
estrada_x=100
estrada_largura=700

carro=130,0,0,255,0
carro=230,-30,0,0,255
...
```
- estrada_x e estrada_largura definem a posição e largura da pista
- Cada linha carro=x,y,r,g,b define a posição inicial e a cor de um carro
  
Essa abordagem mantém a configuração fora do código, facilitando testar diferentes cenários sem recompilar/editar a lógica.

A frequência de geração de buracos é definida por estrada, em jogo.py:
```bash
self.estrada1 = Estrada("config1.txt", ..., modo_carro="suave",
                        spawn_min=6000, spawn_max=8000)   # buraco a cada 6-8s

self.estrada2 = Estrada("config2.txt", ..., modo_carro="reativo",
                        spawn_min=5000, spawn_max=8000)   # buraco a cada 5-8s
```

### Funcionalidades:
- Múltiplos carros por estrada, carregados a partir de arquivos de configuração externos (config1.txt, config2.txt)
- Geração aleatória de obstáculos (buracos)
- Duas (ou mais) estratégias de frenagem plugáveis via padrão Strategy, escolhidas por uma Factory
- Detecção de colisão carro com carro e carro com obstáculo, com tempo de recuperação aleatório
- Câmera com zoom dinâmico centrada no carro de referência de cada estrada
- HUD com número de colisões, consumo médio de combustível e distância média por estrada
- Exportação periódica de estatísticas para CSV, com colunas separadas por ||| para cada estrada
  
### Video de desmonstração:
Execução e explicação no video: https://youtu.be/Q1euXE6Y_sQ

### Arquitetura:
ARQUIVO | RESPONSABILIDADE  ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ 
- main.py
  - ponto de entrada, inicializa o pygame e a classe jogo  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ 
- jogo.py
  -  classe principalㅤ ㅤ ㅤ ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrada.py
  -  gerencia carros, obstáculos, colisões, zoom e spawns  ㅤ   ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- carro.py
  -  posição, velocidade, colisçao e consumo  ㅤ ㅤ ㅤㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- obstaculo.py
  -  representa o buraco na pista ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrategia_frenagem.py
  -  hierarquia de estratégias de frenagem  ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrategia_factory.py
  -  cria a estratégia cprreta a partir de uma string  ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- config_loader.py
  -  leitura dos arquivos .txt de configuração   ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- renderer.py
  -  renderização açternativa ou desaclopada da estrada e do HUD  ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- logger.py
  -  gravação alternatica de estatísticas em CSV, desaclopada da classe jogo

### Print do arquivo das estatísticas:
<img width="797" height="360" alt="estatistica 3" src="https://github.com/user-attachments/assets/b8ab46c6-5ad1-46eb-bfc9-378d80e9cb56" />ㅤ ㅤ ㅤ  
Um detalhe sobre o número de batidas, é que quando um buraco sapwna em cima de um carro, também é considerado uma batida

### Metricas coletadas (CSV)
| Coluna | Significado |
|-------|------|
| Tempo(ms) | Tempo de simulação decorrido, em milissegundos |
| E1_batidas / E2_batidas | Número acumulado de colisões (carro-carro ou carro-buraco) em cada estrada |
| E1_gasolina_media / E2_gaolina_media | Consumo médio de combustível fictício por carro. O consumo é proporcional à velocidade, mas reduzido a 30% enquanto o carro está freando, simulando uma condução mais eficiente |
| E1_Distancia_Media / E2_Distancia_Media | Distância média percorrida pelos carros da estrada |

### Como executar:
Tenha em mente que você precisa ter:
    - python 3.10+
    - pygame2.x
    
Use
```bash
pip install pygame
```
Ou se preferir um requirements.txt:
```bash
pygame>=2.5
```
E depois usar:
```bash
python main.py
```
ou 'run' no arquivo main, caso voce use no VScode por exemplo

# Estrura das pastas:

├── main.py                  # Ponto de entrada

├── jogo.py                  # Loop principal, janela, HUD e gravação de estatísticas

├── estrada.py                # Gerencia carros, obstáculos, colisões e zoom

├── carro.py                  # Modelo do carro e delegação à estratégia de frenagem

├── obstaculo.py               # Modelo do buraco/obstáculo

├── estrategia_frenagem.py    # Hierarquia de estratégias (Strategy)

├── estrategia_factory.py     # Fábrica de estratégias (Factory Method)

├── config_loader.py          # Leitura dos arquivos .txt de configuração

├── renderer.py                # Renderização desacoplada (alternativa a jogo.py)

├── logger.py                  # Gravação de estatísticas desacoplada (alternativa a jogo.py)

├── config1.txt                # Configuração da Estrada 1 (frenagem suave)

├── config2.txt                # Configuração da Estrada 2 (frenagem reativa)

└── plantuml_export.puml       # Diagrama de classes em PlantUML
