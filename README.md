[diagrama_classes_simulacao_transito.html](https://github.com/user-attachments/files/29765856/diagrama_classes_simulacao_transito.html)# Trabalho de POO2  curso de ciencias da computação do IFC-Blumenau.ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ<img width="220" height="320" alt="IF" src="https://github.com/user-attachments/assets/b3a2614e-bac5-43d1-bd4d-89f1f8fc8bf5" />
### Sobre o projeto: 
Simulação em Python/Pygame de duas estradas paralelas, cada uma povoada por múltiplos carros que reagem a obstáculos (buracos) e a outros veículos usando estratégias de frenagem distintas. O projeto compara, lado a lado e em tempo real, o comportamento de uma frenagem suave (gradual) contra uma frenagem reativa (baseada em resposta a mudanças bruscas do carro da frente).
# Diagrama de classe:
[Uploa<div id="cd"></div>
<script type="module">
import mermaid from 'https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs';
const dark = matchMedia('(prefers-color-scheme: dark)').matches;
await document.fonts.ready;
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  fontFamily: '"Anthropic Sans", sans-serif',
  themeVariables: {
    darkMode: dark,
    fontSize: '13px',
    fontFamily: '"Anthropic Sans", sans-serif',
    lineColor: dark ? '#9c9a92' : '#73726c',
    textColor: dark ? '#c2c0b6' : '#3d3d3a',
  },
});
const def = `classDiagram
  class Jogo {
    +tela
    +estrada1
    +estrada2
    +rodar()
    +desenhar_estrada()
    +desenhar_hud()
  }
  class Estrada {
    +carros
    +obstaculos
    +modo_carro
    +contador_batidas
    +atualizar()
    +verificar_colisoes()
    +media_gasolina
    +media_distancia
  }
  class Carro {
    +x_base
    +y
    +cor
    +velocidade_atual
    +batido
    +gasolina_total
    +distancia_total
    +atualizar()
  }
  class Obstaculo {
    +x_base
    +y
    +ativo
    +atualizar()
  }
  class EstrategiaFactory {
    +criar(modo) EstrategiaFrenagem
  }
  class EstrategiaFrenagem {
    <<abstract>>
    +calcular_velocidade()
  }
  class EstrategiaSuave
  class EstrategiaReativa
  class EstrategiaLivre
  class Renderer {
    +desenhar_estrada()
    +desenhar_hud()
  }
  class LoggerEstatisticas {
    +gravar()
  }
  class config_loader {
    <<module>>
    +carregar_config()
  }

  Jogo "1" *-- "2" Estrada
  Estrada "1" *-- "many" Carro
  Estrada "1" *-- "many" Obstaculo
  Estrada ..> EstrategiaFactory : usa
  Estrada ..> config_loader : usa
  EstrategiaFactory ..> EstrategiaFrenagem : cria
  Carro "1" o-- "1" EstrategiaFrenagem : usa
  EstrategiaFrenagem <|-- EstrategiaSuave
  EstrategiaFrenagem <|-- EstrategiaReativa
  EstrategiaFrenagem <|-- EstrategiaLivre
  Renderer ..> Estrada : renderiza
  LoggerEstatisticas ..> Estrada : registra
`;
const { svg } = await mermaid.render('cd-svg', def);
document.getElementById('cd').innerHTML = svg;
document.querySelectorAll('#cd svg .classGroup rect').forEach(r => r.setAttribute('rx', '8'));
</script>
ding diagrama_classes_simulacao_transito.html…]()


### Print do código em execução:
<img width="1872" height="1012" alt="começo da execução" src="https://github.com/user-attachments/assets/dd50bc92-e95a-4a64-8836-20d6651195ee" />

### Print do arquivo das estatísticas:
<img width="851" height="206" alt="035e54fd-9840-4d7c-870f-2059895c2ffc" src="https://github.com/user-attachments/assets/5784a263-03dd-47ff-949d-647b5da9abc8" />
