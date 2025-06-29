# REGRAS DE KATA IMPLEMENTADAS NO SISTEMA

## Regras Oficiais WKF (World Karate Federation) para Kata

### Sistema de Pontuação:
- 5 juízes avaliam cada kata
- Remove-se a maior e menor nota
- Soma-se as 3 notas restantes
- Pontuação mínima para avançar: 5.0 pontos

### Sistema de Classificação por Número de Atletas:

#### Eliminatórias:
- **≤ 4 atletas**: Todos vão direto para a final
- **5-8 atletas**: Top 4 vão para a final
- **9-16 atletas**: Top 8 vão para a semifinal
- **> 16 atletas**: Top 16 vão para a próxima fase

#### Semifinal:
- Top 4 atletas vão para a final

#### Final:
- Top 3 atletas vão para o pódio (1º, 2º, 3º lugar)

### Critérios de Eliminação:
1. **Pontuação insuficiente**: Atletas com menos de 5.0 pontos são eliminados
2. **Classificação**: Apenas os melhores colocados avançam conforme as regras acima
3. **Empate**: Em caso de empate, considera-se a maior nota individual

### Configurações Ajustáveis:
- **Pontuação mínima**: Pode ser alterada no arquivo `views.py` (linha ~790)
- **Número de classificados**: Segue automaticamente as regras oficiais

### Como Funciona:
1. Atletas competem nas eliminatórias
2. Sistema calcula automaticamente quantos passam
3. Aplica critério de pontuação mínima
4. Classifica os melhores para a próxima fase
5. Processo se repete até a final

## Exemplo Prático:

### Com 12 atletas:
- **Eliminatórias**: Top 8 passam para semifinal
- **Semifinal**: Top 4 passam para final  
- **Final**: Top 3 vão para o pódio

### Com 6 atletas:
- **Eliminatórias**: Top 4 passam direto para final
- **Final**: Top 3 vão para o pódio

## Observações:
- O sistema agora segue as regras oficiais de Kata
- Não avança mais "todo mundo" indiscriminadamente
- Mantém a integridade competitiva da modalidade
- Respeita os padrões internacionais de karatê
