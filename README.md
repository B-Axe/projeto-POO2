# Trabalho de POO2  curso de ciencias da computação do IFC-Blumenau.ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ<img width="220" height="320" alt="IF" src="https://github.com/user-attachments/assets/b3a2614e-bac5-43d1-bd4d-89f1f8fc8bf5" />
### Sobre o projeto: 
Simulação em Python/Pygame de duas estradas paralelas, cada uma povoada por múltiplos carros que reagem a obstáculos (buracos) e a outros veículos usando estratégias de frenagem distintas. O projeto compara, lado a lado e em tempo real, o comportamento de uma frenagem suave (gradual) contra uma frenagem reativa (baseada em resposta a mudanças bruscas do carro da frente).

### Print do código em execução:
<img width="1872" height="1012" alt="começo da execução" src="https://github.com/user-attachments/assets/dd50bc92-e95a-4a64-8836-20d6651195ee" />

### Funcionalidades:
- Múltiplos carros por estrada, carregados a partir de arquivos de configuração externos (config1.txt, config2.txt)
- Geração aleatória de obstáculos (buracos)
- Duas (ou mais) estratégias de frenagem plugáveis via padrão Strategy, escolhidas por uma Factory
- Detecção de colisão carro com carro e carro com obstáculo, com tempo de recuperação aleatório
- Câmera com zoom dinâmico centrada no carro de referência de cada estrada
- HUD com número de colisões, consumo médio de combustível e distância média por estrada
- Exportação periódica de estatísticas para CSV, com colunas separadas por ||| para cada estrada
  
### Arquitetura:
ARQUIVO | RESPONSABILIDADE  ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ 
- main.py | ponto de entrada, inicializa o pygame e a classe jogo  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ 
- jogo.py | classe principalㅤ ㅤ ㅤ ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrada.py | gerencia carros, obstáculos, colisões, zoom e spawns  ㅤ   ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- carro.py | posição, velocidade, colisçao e consumo  ㅤ ㅤ ㅤㅤ ㅤ ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- obstaculo.py | representa o buraco na pista ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrategia_frenagem.py | hierarquia de estratégias de frenagem  ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- estrategia_factory.py | cria a estratégia cprreta a partir de uma string  ㅤㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- config_loader.py | leitura dos arquivos .txt de configuração   ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- renderer.py | renderização açternativa ou desaclopada da estrada e do HUD  ㅤ  ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ 
- logger.py | gravação alternatica de estatísticas em CSV, desaclopada da classe jogo

### Print do arquivo das estatísticas:
<img width="851" height="206" alt="035e54fd-9840-4d7c-870f-2059895c2ffc" src="https://github.com/user-attachments/assets/5784a263-03dd-47ff-949d-647b5da9abc8" />
