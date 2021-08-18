#import sys
import random
import math
import data_generator as dg
import time

sequences_list = ["aaabcd", "aabadc", "cdabba", "dcbbab", "dbaabc", "cbbbad"] #lista de sequências bem simples, apenas para permitir a execução dos algoritmos
initial_order = list(range(0, len(sequences_list))) #lista de ordenação de índices ordenada sequencialmente, também apenas para permitir a execução
#sequences_list = dg.get_data("samples.txt")
'''
sigma = 0.09
t_max = 100
t_min = 0.0005
'''
t_min = 0.1
t_max = 1000000000
max_iter = 500
max_time = 20

def overlay(seq1, seq2): #calcula a quantidade de caracteres que podem ser sobrepostos, do final da sequencia 1 com o começo da sequência 2
    '''
    exemplo: (aaa, aab) -> aa -> count = 2
    '''
    seq1_len = len(seq1) - 1
    if len(seq2) >= len(seq1):
        seq2_len = len(seq1) - 1 #se a seq2 for maior, igualamos o comprimento; se for igual, tanto faz qual comprimento usar
    elif len(seq2) < len(seq1):
        seq2_len = len(seq2) - 1 #se a seq2 for menor, utilizamos o próprio comprimento de seq2

    count = 0
    while count == 0 and seq2_len > -1:
        aux = seq1_len #para não perder o comprimento da seq1 e evitar o calculo de len()

        for i in range(seq2_len, -1, -1):
            if seq1[aux] == seq2[i]: #char igual, incrementa o contador de sobreposição e decrementa o contador de char de seq1
                count += 1
                aux -= 1
            else: #a sobreposição não funcionou, contador é zerado para a próxima iteração
                count = 0
                break
        
        seq2_len -= 1
        
    return count

def common_supersequence(seq1, seq2): #calcula a supersequência comum a duas sequências
    '''
    exemplo: (aaa, aab) -> overlay_count = 2 -> aaa + aab[2:3] -> aaab
    '''
    overlay_count = overlay(seq1, seq2) #calculamos a quantidade de sobreposição possível na sequência
    supersequence = seq1 + seq2[overlay_count:len(seq2)] #retornamos a string que concatena as sequências, desconsiderando os char iniciais da seq2, envolvidos na sobreposição
    return supersequence

def common_supersequence_list(order): #calcula a supersequência comum para sequências em uma lista ordenada
    '''
    exemplo: (aaa, aab, abb) -> (aaab, abb) -> aaabb
    '''
    overlay_seq = sequences_list[order[0]]
    for j in range(1, len(order)):
        overlay_seq = common_supersequence(overlay_seq, sequences_list[order[j]])
    return overlay_seq


#busca local do simulated annealing (não criei função específica para isso, então apenas comentei o "while" do algoritmo, para que seja executada uma iteração apenas)

def find_random_neighboor(indexes_order): #encontra uma sequência vizinha, alterando a posição dos índices usados para formar a supersequência
    rand_sequence = random.randint(0, len(indexes_order) - 2) #vizinho será obtido alterando a posição de uma sequência com outra sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    new_order = [] + indexes_order
    new_order[rand_sequence] = indexes_order[rand_sequence + 1]
    new_order[rand_sequence + 1] = indexes_order[rand_sequence]

    return common_supersequence_list(new_order), new_order

def simulated_annealing(initial_sequence, initial_indexes_order): #verifica vizinhos com perturbação nos índices que compõe a supersequência atual, caminhando pelo espaço de busca
    t = t_max
    #best_sequence, best_indexes_order = greedy_algorithm() #solução gerada pelo algoritmo guloso que resolve o problema
    #random_heuristic() #solução inicial gerada por uma heurística aleatória
    best_sequence, best_indexes_order = initial_sequence, initial_indexes_order
    global_best_length = len(best_sequence)
    global_best_sequence = best_sequence
    global_best_indexes_order = best_indexes_order
    noimprove_count = 0
    start_time = time.time()

    #while(t > t_min):
    neighboor_sequence, neighboor_indexes_order = find_random_neighboor(best_indexes_order)
    fitness = len(neighboor_sequence) - len(best_sequence)
    probability_coeficient = random.uniform(0.0, 1.0)
    decision_coeficient = math.exp(-fitness/t)

    if fitness <= 0 or (fitness > 0 and probability_coeficient <= decision_coeficient):
        best_sequence, best_indexes_order = neighboor_sequence, neighboor_indexes_order
        if(global_best_length > len(best_sequence)):
            global_best_length = len(best_sequence)
            global_best_sequence = best_sequence
            global_best_indexes_order = best_indexes_order
            #print("improve_iter:", noimprove_count)
            noimprove_count = 0
        else:
            noimprove_count += 1
    else:
        noimprove_count += 1
    t = t * 0.999

    if noimprove_count == 5000:
        t += noimprove_count
        best_sequence, best_indexes_order = initial_sequence, initial_indexes_order
        noimprove_count = 0
    

        #print("noimprove_iter:", noimprove_count)
        #running_time = time.time() - start_time

        #if running_time > max_time:
            #print("running_time:", running_time)
            #break
        #t = t * random.uniform(0.8, 0.99)
        #t = t * (math.exp((random.uniform(0.1, 0.9) * -t)/sigma)) 
        
    return global_best_sequence, global_best_indexes_order


#busca local do grasp
def find_grasp_neighboor_sequence(indexes_order): #encontra a melhor sequência vizinha, modificando os índices dois a dois
    best_indexes_order = [] + indexes_order #lista ordenada de índices da solução inicial
    best_length = len(common_supersequence_list(best_indexes_order)) #comprimento da supersequência associada a lista ordenada de índices da solução inicial

    for i in range(0, len(indexes_order) - 1):
        modified_indexes_order = [] + best_indexes_order
        modified_indexes_order[i] = best_indexes_order[i + 1] #trocamos o índice i de modified_indexes_order pelo índice i+1
        modified_indexes_order[i + 1] = best_indexes_order[i]

        new_sequence = common_supersequence_list(modified_indexes_order)
        new_length = len(new_sequence)

        if new_length < best_length:
            best_indexes_order = modified_indexes_order
            best_length = new_length

    return common_supersequence_list(best_indexes_order), best_indexes_order

def grasp_localsearch(grasp_initial, grasp_initial_order): #verifica se os vizinhos são melhores que a solução inicial
    best_length = len(grasp_initial)
    best_sequence = grasp_initial
    best_indexes_order = grasp_initial_order

    best_neighboor_sequence, best_neighboor_order = find_grasp_neighboor_sequence(grasp_initial_order) #verifica entre os vizinhos qual o melhor
    best_neighboor_length = len(best_neighboor_sequence)

    if best_length > best_neighboor_length: #se o melhor vizinho tiver comprimento menor que a solução inicial, atualiza
        best_length = best_neighboor_length
        best_sequence = best_neighboor_sequence
        best_indexes_order = best_neighboor_order

    return best_sequence, best_indexes_order

if __name__ == "__main__":
    initial_sequence = common_supersequence_list(initial_order)

    sa_local_sequence, sa_local_order = simulated_annealing(initial_sequence, initial_order) #sa1: start: greedy
    grasp_local_sequence, grasp_local_order = grasp_localsearch(initial_sequence, initial_order)
    
    print("simple_initial_solution_length: \t", len(initial_sequence))
    print(initial_sequence)
    print()

    print("sa_local_length \t\t\t", len(sa_local_sequence))
    print(sa_local_sequence)
    print()

    print("grasp_local_length \t\t\t", len(grasp_local_sequence))
    print(grasp_local_sequence)