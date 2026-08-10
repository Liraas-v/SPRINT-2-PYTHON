<div align="center">

![FIAP](https://img.shields.io/badge/FIAP-2026-ED1C24?style=flat)
![Sprint](https://img.shields.io/badge/Sprint-2-ED1C24?style=flat)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python)

</div>

---

## Sobre o Projeto

O **JoviLens** é uma aplicação Python desenvolvida como parte do **FIAP x JOVI Challenge 2026**, projeto acadêmico da Sprint 2 do curso de tecnologia da FIAP. O sistema simula um assistente de câmera inteligente com foco educacional, permitindo que estudantes registrem e organizem materiais de aula capturados em sala.

O projeto apresenta três funcionalidades principais: **detecção de cena** (que analisa descrições do usuário para sugerir modos fotográficos ideais), **tradução de texto** (simulando tradução em tempo real com base em um dicionário embutido) e **modo aula** (que organiza capturas de lousa e caderno por disciplina e professor, exportando os registros como arquivos `.txt`).

Todo o sistema é operado via interface de menu no terminal, com feedback visual através de barras de progresso em ASCII e tabelas formatadas, demonstrando na prática os fundamentos de programação estruturada em Python.

---

## Objetivo de Aprendizado

Este projeto exercita os seguintes conceitos de Python:

- **Funções** — modularização com mais de 12 funções definidas, separando responsabilidades de interface, lógica e persistência
- **Estruturas de dados** — uso de listas e dicionários para armazenar histórico de capturas, regras de detecção e mapeamento de traduções
- **Controle de fluxo** — condicionais (`if/elif/else`) e laços `while` para navegação contínua em menus e validação de entradas
- **Manipulação de strings** — `.lower()`, `.split()`, `.strip()` e substituição para normalizar e processar texto
- **Leitura e escrita de arquivos** — exportação de sessões de aula como arquivos `.txt` usando `open()` com modo de escrita
- **Variáveis globais** — manutenção de estado da aplicação entre chamadas de função
- **Interface de terminal** — construção de menus interativos, barras de progresso e cabeçalhos em ASCII art
- **Validação de entradas** — verificação de strings vazias, comprimento mínimo e intervalos numéricos

---

## Tech Stack

[![Skills](https://skillicons.dev/icons?i=python)](https://skillicons.dev)

> Nenhuma dependência externa — apenas a biblioteca padrão do Python 3.

---

## Como Rodar

```bash
git clone https://github.com/Liraas-v/SPRINT-2-PYTHON
cd SPRINT-2-PYTHON

python JOVILENS.PY
```

---

## Estrutura do Projeto

```
SPRINT-2-PYTHON/
├── JOVILENS.PY          # Script principal — lógica completa da aplicação
├── aula_Historia_1.txt  # Exemplo de exportação: aula de História (gerado pelo app)
└── aula_Quimica_1.txt   # Exemplo de exportação: aula de Química (gerado pelo app)
```

---
