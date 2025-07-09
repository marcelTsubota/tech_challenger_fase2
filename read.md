# Tech Challenge FIAP – Algoritmos Genéticos em Reformas de Apartamentos

## Resumo do Projeto

Este projeto utiliza Algoritmos Genéticos (AG) para planejar reformas internas em apartamentos residenciais, otimizando a escolha de melhorias com o objetivo de maximizar a valorização do imóvel para revenda, respeitando um orçamento limitado.

## Objetivo

Dado um conjunto de possíveis melhorias (ex: troca de pisos, pintura, móveis planejados), o algoritmo seleciona a combinação ótima de reformas para cada apartamento, considerando:

- Tamanho do imóvel (m²)
- Tipo de reforma (econômica, padrão, alto padrão)
- Custos e valorização estimados de cada melhoria

## Estrutura do Projeto

TCF2/
├── venv/ # Ambiente virtual Python
├── requirements.txt # Bibliotecas necessárias
├── main.py # Script principal com Algoritmo Genético
├── melhorias.csv # Lista de melhorias, custos e valorizações (opcional)
└── README.md # Este arquivo de descrição

## Como rodar o projeto

1. **Clone o repositório** ou copie os arquivos para uma pasta local.
2. **Crie e ative o ambiente virtual:**
   ```
   python -m venv venv
   source venv/Scripts/activate    # (Git Bash/VS Code/Windows)
   ```
3. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```
4. **Rode o script principal:**
   ```
   python main.py
   ```

## Sobre os Dados

Os custos e valorizações das melhorias podem ser simulados ou baseados em dados reais do mercado. A tabela `melhorias.csv` (opcional) pode ser editada conforme o cenário.

## Resultados

O projeto compara a solução do AG com métodos aleatórios e estratégias simples (ganância). Os resultados são apresentados em gráficos e tabelas.

## Entrega

- Código-fonte
- Documentação completa
- Vídeo explicativo mostrando o funcionamento e análise dos resultados

---

_Projeto desenvolvido para a Fase 2 do curso Inteligência Artificial para Desenvolvedores – FIAP._
