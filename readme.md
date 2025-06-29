# Gerenciador de Memória Virtual - Simulador

## Descrição do Projeto

Este projeto é uma simulação de um **gerenciador de memória virtual com paginação**, como ocorre em sistemas operacionais reais. Ele permite acompanhar o funcionamento do gerenciamento de memória enquanto processos são criados, executados, bloqueados e finalizados.

Entre as funcionalidades implementadas estão:

- Controle da memória principal e secundária.
- Uso de tabela de páginas para cada processo, com bits de presença (P), modificação (M) e endereço real do quadro.
- Uso de uma TLB (Translation Lookaside Buffer) para acelerar a tradução de endereços.
- Políticas de substituição de páginas quando a memória principal está cheia.

## Funcionalidades

- **Alocação dinâmica de quadros para páginas quando processos acessam novos endereços.**
- **TLB associativa para simular acessos rápidos a mapeamentos recentes.**
- **Faltas de página quando uma página não está na memória principal.**
- **Substituição de páginas quando necessário, de acordo com a política escolhida.**
- **Gestão das filas de prontos e bloqueados, com suporte a operações de I/O.**
- **Exibição detalhada das estruturas durante a execução (MP, MS, TLB, tabelas de páginas, estados dos processos).**

## Políticas de substituição de páginas

O sistema implementa duas políticas possíveis:

- **Relógio (Clock)**: percorre os quadros em ordem. O critério é:

  - Primeiro procura páginas com **U = 0 e M = 0** (não usadas e não modificadas).
  - Se não encontrar, zera U das páginas com U = 1 e continua o ciclo.
  - Se a página a ser substituída tiver M = 1, ela é salva na memória secundária antes da substituição.

- **LRU (Least Recently Used)**: substitui a página que não é usada há mais tempo.  
  _(Implementação opcional no projeto)_

## O que o simulador demonstra

- Alocação e liberação de quadros.
- TLB hit e miss.
- Faltas de página e carregamento de página da MS.
- Substituição de página usando Relógio (com U e M).
- Estado dos processos e movimentação entre filas.
- Salvamento de páginas modificadas na MS.
