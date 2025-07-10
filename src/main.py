import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

# ------------------------
# CONFIGURAÇÕES DO PROJETO
# ------------------------

# Parâmetros do apartamento e reforma
tamanho_m2 = 70
custo_por_m2 = 800  # padrão médio
orcamento_total = tamanho_m2 * custo_por_m2

# Lista de melhorias simuladas (nome, custo, valorizacao)
melhorias = [
    {"nome": "Pintura geral",                 "custo": 5000,  "valorizacao": 7000},
    {"nome": "Troca de pisos",                "custo": 12000, "valorizacao": 15000},
    {"nome": "Reforma do banheiro",           "custo": 8000,  "valorizacao": 11000},
    {"nome": "Iluminação LED",                "custo": 3000,  "valorizacao": 5000},
    {"nome": "Móveis planejados na cozinha",  "custo": 9000,  "valorizacao": 12000},
    {"nome": "Troca de portas",               "custo": 4000,  "valorizacao": 4500},
    {"nome": "Ar condicionado split",         "custo": 5000,  "valorizacao": 6000},
    {"nome": "Gesso/sanca",                   "custo": 3500,  "valorizacao": 4000},
    {"nome": "Automação básica",              "custo": 7000,  "valorizacao": 8000},
    {"nome": "Novo revestimento (cozinha)",   "custo": 6000,  "valorizacao": 7500},
]

# -------------------------
# FUNÇÃO DE FITNESS
# -------------------------

def fitness(individuo, melhorias, orcamento_total):
    custo_total = sum([m['custo'] for i, m in enumerate(melhorias) if individuo[i] == 1])
    valor_total = sum([m['valorizacao'] for i, m in enumerate(melhorias) if individuo[i] == 1])
    if custo_total > orcamento_total:
        return 0
    return valor_total

# -------------------------
# OPERAÇÕES DO AG
# -------------------------

def inicializar_populacao(n_individuos, n_melhorias):
    return [np.random.randint(2, size=n_melhorias) for _ in range(n_individuos)]

def selecao_roleta(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        # Todas as soluções são inválidas, sorteia qualquer indivíduo
        return random.choice(populacao)
    pick = random.uniform(0, total_fitness)
    atual = 0
    for ind, fit in zip(populacao, fitnesses):
        atual += fit
        if atual >= pick:
            return ind
    return populacao[-1]

def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
    filho2 = np.concatenate((pai2[:ponto], pai1[ponto:]))
    return filho1, filho2

def mutacao(individuo, taxa_mutacao=0.05):
    novo = individuo.copy()
    for i in range(len(novo)):
        if random.random() < taxa_mutacao:
            novo[i] = 1 - novo[i]
    return novo

# -------------------------
# EXECUÇÃO DO ALGORITMO GENÉTICO
# -------------------------

def algoritmo_genetico(melhorias, orcamento_total, n_geracoes=100, n_individuos=40, taxa_mutacao=0.08):
    n_melhorias = len(melhorias)
    populacao = inicializar_populacao(n_individuos, n_melhorias)
    historico_melhor_fitness = []
    melhor_solucao = None
    melhor_fitness = -1

    for geracao in range(n_geracoes):
        fitnesses = [fitness(ind, melhorias, orcamento_total) for ind in populacao]
        max_fit = max(fitnesses)
        historico_melhor_fitness.append(max_fit)

        if max_fit > melhor_fitness:
            melhor_fitness = max_fit
            melhor_solucao = populacao[fitnesses.index(max_fit)].copy()

        nova_populacao = []

        # Gera nova população (elitismo: mantém o melhor da geração anterior)
        nova_populacao.append(melhor_solucao)
        while len(nova_populacao) < n_individuos:
            pai1 = selecao_roleta(populacao, fitnesses)
            pai2 = selecao_roleta(populacao, fitnesses)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        populacao = nova_populacao[:n_individuos]

    return melhor_solucao, melhor_fitness, historico_melhor_fitness

# -------------------------
# EXECUTA E MOSTRA RESULTADO
# -------------------------

if __name__ == "__main__":
    melhor_solucao, melhor_fitness, historico = algoritmo_genetico(
        melhorias, orcamento_total, n_geracoes=80, n_individuos=40, taxa_mutacao=0.10
    )

    print("Orçamento disponível: R$", orcamento_total)
    print("Melhor plano de reforma encontrado:")
    custo_total = 0
    for i, gene in enumerate(melhor_solucao):
        if gene == 1:
            print(f"- {melhorias[i]['nome']} (Custo: R${melhorias[i]['custo']}, Valorização: R${melhorias[i]['valorizacao']})")
            custo_total += melhorias[i]['custo']
    print(f"Total gasto: R${custo_total}")
    print(f"Valorização total estimada: R${melhor_fitness}")

    # Plota evolução do fitness
    plt.plot(historico)
    plt.xlabel("Geração")
    plt.ylabel("Melhor Fitness")
    plt.title("Evolução do Algoritmo Genético")
    plt.show()
