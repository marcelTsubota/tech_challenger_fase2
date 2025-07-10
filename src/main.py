"""
main.py
Tech Challenge Fase 2 - Algoritmos Genéticos
Autor: Marcel Tsubota
Descrição: Otimização de seleção de melhorias em imóvel utilizando Algoritmos Genéticos.
"""

import os
import csv
import random
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# ================================
# PARÂMETROS DO ALGORITMO
# ================================
TAMANHO_POPULACAO = 50
NUM_GERACOES = 100
TAXA_MUTACAO = 0.01
TAXA_CROSSOVER = 0.8
ORCAMENTO_TOTAL = 50000

# ================================
# CARREGAMENTO DO DATASET
# ================================
def carregar_melhorias(nome_arquivo):
    """
    Lê o arquivo CSV com melhorias, custos e valorizações.
    Args:
        nome_arquivo (str): Caminho para o arquivo CSV.
    Returns:
        list[dict]: Lista de melhorias.
    """
    melhorias = []
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        reader.fieldnames = [campo.strip() for campo in reader.fieldnames]
        for row in reader:
            melhorias.append({
                'nome': row['nome'].strip(),
                'custo': float(row['custo'].replace(',', '.')),
                'valorizacao': float(row['valorizacao'].replace(',', '.'))
            })
    return melhorias

# ================================
# FUNÇÕES DO ALGORITMO GENÉTICO
# ================================
def inicializar_populacao(num_individuos, num_melhorias):
    """
    Cria a população inicial com indivíduos aleatórios.
    """
    return [ [random.randint(0, 1) for _ in range(num_melhorias)] for _ in range(num_individuos) ]

def avaliar_fitness(individuo, melhorias, orcamento):
    """
    Calcula o fitness do indivíduo: soma das valorizações sem ultrapassar o orçamento.
    """
    custo_total = sum(m['custo'] for m, v in zip(melhorias, individuo) if v)
    if custo_total > orcamento:
        return 0  # Penaliza se passar do orçamento
    return sum(m['valorizacao'] for m, v in zip(melhorias, individuo) if v)

def selecao_roleta(populacao, fitnesses):
    """
    Seleciona indivíduos por roleta viciada (proporcional ao fitness).
    """
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(populacao)  # Evita divisão por zero
    pick = random.uniform(0, total_fitness)
    atual = 0
    for individuo, fitness in zip(populacao, fitnesses):
        atual += fitness
        if atual > pick:
            return individuo
    return populacao[-1]

def crossover(pai1, pai2):
    """
    Realiza crossover de um ponto entre dois pais.
    """
    if random.random() < TAXA_CROSSOVER:
        ponto = random.randint(1, len(pai1)-1)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
        return filho1, filho2
    return pai1[:], pai2[:]

def mutacao(individuo):
    """
    Aplica mutação em um indivíduo.
    """
    return [1-g if random.random() < TAXA_MUTACAO else g for g in individuo]

# ================================
# LOOP PRINCIPAL DO ALGORITMO
# ================================
def algoritmo_genetico(melhorias, orcamento):
    num_melhorias = len(melhorias)
    populacao = inicializar_populacao(TAMANHO_POPULACAO, num_melhorias)
    melhor_individuo = None
    melhor_fitness = 0
    evolucao_fitness = []

    for geracao in range(NUM_GERACOES):
        fitnesses = [avaliar_fitness(i, melhorias, orcamento) for i in populacao]
        
        # Guarda o melhor fitness desta geração
        geracao_melhor_fitness = max(fitnesses)
        evolucao_fitness.append(geracao_melhor_fitness)

        # Armazena o melhor indivíduo
        for individuo, fit in zip(populacao, fitnesses):
            if fit > melhor_fitness:
                melhor_individuo = individuo[:]
                melhor_fitness = fit

        nova_populacao = []
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao_roleta(populacao, fitnesses)
            pai2 = selecao_roleta(populacao, fitnesses)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:TAMANHO_POPULACAO]
        print(f"Geração {geracao+1}: Melhor fitness = {melhor_fitness}")

    return melhor_individuo, melhor_fitness, evolucao_fitness

def exibir_solucao(individuo, melhorias):
    print("\nMelhor combinação de melhorias encontrada:")
    custo_total = 0
    valorizacao_total = 0
    for gene, melhoria in zip(individuo, melhorias):
        if gene:
            print(f"- {melhoria['nome']} (Custo: {melhoria['custo']}, Valorização: {melhoria['valorizacao']})")
            custo_total += melhoria['custo']
            valorizacao_total += melhoria['valorizacao']
    print(f"\nCusto total: {custo_total}")
    print(f"Valorização total: {valorizacao_total}")

# ================================
# GRÁFICO DE EVOLUÇÃO DO FITNESS
# ================================
""" def plotar_evolucao_fitness(evolucao_fitness):
    plt.figure(figsize=(12, 6))
    plt.plot(
        range(1, len(evolucao_fitness)+1),
        evolucao_fitness,
        marker='o',
        linestyle='-',
        linewidth=2,
        markersize=6,
        label='Melhor Fitness'
    )
    plt.title('Evolução do Melhor Fitness por Geração', fontsize=16, fontweight='bold')
    plt.xlabel('Geração', fontsize=13)
    plt.ylabel('Melhor Fitness', fontsize=13)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('resultados/evolucao_fitness.png', dpi=150)
    plt.show() """

def plotar_evolucao_fitness(evolucao_fitness, nome_projeto='Tech Challenge Fase 2'):
    # Garante que a pasta resultados existe
    os.makedirs('resultados', exist_ok=True)
    
    # Gera nome de arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    nome_arquivo_base = f"resultados/evolucao_fitness_{timestamp}"
    
    plt.figure(figsize=(13, 7))
    
    # Escolha de cor personalizada (azul escuro, pode trocar)
    cor_principal = "#005caa"
    
    # Linha principal e pontos
    plt.plot(
        range(1, len(evolucao_fitness)+1),
        evolucao_fitness,
        marker='o',
        linestyle='-',
        linewidth=2.5,
        markersize=7,
        label='Melhor Fitness',
        color=cor_principal
    )
    
    # Linha de tendência suavizada (média móvel)
    if len(evolucao_fitness) > 5:
        janela = 5
        media_movel = np.convolve(evolucao_fitness, np.ones(janela)/janela, mode='valid')
        plt.plot(range(janela, len(evolucao_fitness)+1), media_movel,
                 label='Média Móvel (5 gerações)', linestyle='--', color='#f28500', linewidth=2)
    
    # Gráfico mais visual
    plt.title(f'Evolução do Melhor Fitness por Geração\n{nome_projeto}', fontsize=17, fontweight='bold', color='#222')
    plt.xlabel('Geração', fontsize=14, fontweight='bold')
    plt.ylabel('Melhor Fitness', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(visible=True, linestyle=':', alpha=0.55)
    plt.legend(fontsize=13, loc='best', frameon=True, shadow=True)
    
    # Caixa ao redor do gráfico
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_linewidth(1.2)
    plt.gca().spines['bottom'].set_linewidth(1.2)
    
    # Marca d'água
    plt.figtext(0.99, 0.01, 'Tech Challenge Fase 2 - FIAP', fontsize=11, color='#aaa',
                ha='right', va='bottom', alpha=0.8)
    
    # Encontrar o índice do valor máximo e mínimo
    idx_max = np.argmax(evolucao_fitness)
    idx_min = np.argmin(evolucao_fitness)

    # Anotar o valor máximo no gráfico
    plt.annotate(f'Máx: {max(evolucao_fitness):.2f}',
                xy=(idx_max + 1, evolucao_fitness[idx_max]),
                xytext=(-60, -30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=12, color='green', fontweight='bold')

    # Anotar o valor mínimo no gráfico
    plt.annotate(f'Mín: {min(evolucao_fitness):.2f}',
                xy=(idx_min + 1, evolucao_fitness[idx_min]),
                xytext=(20, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=12, color='red', fontweight='bold')
    
    plt.tight_layout()
    # Salva em PNG e PDF
    plt.savefig(f"{nome_arquivo_base}.png", dpi=180)
    plt.savefig(f"{nome_arquivo_base}.pdf")
    plt.show()
    
# ================================
# EXECUÇÃO PRINCIPAL
# ================================
def main():
    melhorias = carregar_melhorias('../melhorias.csv')
    melhor_individuo, melhor_fitness, evolucao_fitness = algoritmo_genetico(melhorias, ORCAMENTO_TOTAL)
    exibir_solucao(melhor_individuo, melhorias)    
    plotar_evolucao_fitness(evolucao_fitness)

if __name__ == "__main__":
    main()
