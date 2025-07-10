"""
main.py
Tech Challenge Fase 2 - Algoritmos Genéticos
Autor: [Seu Nome ou Grupo]
Descrição: Otimização de seleção de melhorias em imóvel utilizando Algoritmos Genéticos.
"""

import random
import csv

# ================================
# PARÂMETROS DO ALGORITMO
# ================================
TAMANHO_POPULACAO = 50
NUM_GERACOES = 100
TAXA_MUTACAO = 0.01
TAXA_CROSSOVER = 0.8
ORCAMENTO_TOTAL = 30000  # Exemplo de orçamento

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
        reader = csv.DictReader(csvfile)
        for row in reader:
            melhorias.append({
                'nome': row['melhoria'],
                'custo': float(row['custo']),
                'valorizacao': float(row['valorizacao'])
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
        return pai1[:ponto] + pai2[ponto:]
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

    for geracao in range(NUM_GERACOES):
        fitnesses = [avaliar_fitness(i, melhorias, orcamento) for i in populacao]

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

    return melhor_individuo, melhor_fitness

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
# EXECUÇÃO PRINCIPAL
# ================================
def main():
    melhorias = carregar_melhorias('../melhorias.csv')
    melhor_individuo, melhor_fitness = algoritmo_genetico(melhorias, ORCAMENTO_TOTAL)
    exibir_solucao(melhor_individuo, melhorias)

if __name__ == "__main__":
    main()
