# Gerenciador de Memória Virtual - Simulador

## Descrição do Projeto

Este projeto é uma simulação de um **gerenciador de memória virtual com paginação**, como ocorre em sistemas operacionais reais. Ele permite acompanhar o funcionamento do gerenciamento de memória enquanto processos são criados, executados, bloqueados e finalizados.

Entre as funcionalidades implementadas estão:

- Controle da memória principal e secundária.
- Uso de tabela de páginas para cada processo, com bits de presença (P), modificação (M) e endereço real do quadro.
- Uso de uma TLB.
- Políticas de substituição de páginas quando a memória principal está cheia.

## Funcionalidades

- **Alocação dinâmica de quadros para páginas quando processos acessam novos endereços.**
- **TLB associativa para simular acessos rápidos a mapeamentos recentes.**
- **Faltas de página quando uma página não está na memória principal.**
- **Substituição de páginas quando necessário, de acordo com a política escolhida.**
- **Gestão das filas de prontos e bloqueados, com suporte a operações de I/O.**
- **Exibição detalhada das estruturas durante a execução (MP, MS, TLB, tabelas de páginas, estados dos processos).**

## Políticas de substituição de páginas

O sistema implementa duas políticas possíveis: Relógio e LRU.

## O que o simulador demonstra

- Alocação e liberação de quadros.
- TLB hit e miss.
- Faltas de página e carregamento de página da MS.
- Substituição de página usando Relógio.
- Substituição de página usando LRU.
- Estado dos processos e movimentação entre filas.
- Salvamento de páginas modificadas na MS.

## O que é impresso na tela após cada instrução:

- Atual processo executando.
- TLB.
- Tabela contendo o id do Processo e o seu número de páginas.
- Tabela de página de cada processo.
- Estado de cada processo.
- Filas de processos pronto e bloqueado.
- Memória principal.
- Memória secundária.
- Instrução seguinte a ser executada.

## Decisões de projeto

- Um processo só vai para o estado bloqueado após um I/O.
- Desconsideramos o tempo de alocação da memória secundária para a memória principal devido a uma falta de página como motivo para bloquear um processo.

## Como usar

- Ir até o diretorio do projeto.
- Executar no terminal: python main.py
- Escolher a configuração do sistema.
- Escolher a política de substituição.
- Escolher o arquivo de entrada desejado.
- Acompanhar a execução das instruções apertando enter.

Obs: caso deseje incluir mais um arquivo, insira ele na pasta "componentes\entradas".

## Sugestão de teste

- Escolher configuração 2 e entrada1.
- Escolher configuração 2 e entrada2.
- Escolher configuração 4 e entrada3.
- Escolher configuração 3 e entrada4.

A configuração 1 não é boa para perceber todos os aspectos do simulador, mas pode ser executada com qualquer entrada, por ter um tamanho de página e MP muito grande para as entradas.

A entrada_errada serve para mostrar que o simulador não aceita instruções sem a devida formatação.
