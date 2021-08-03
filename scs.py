#import sys
import random
import math
import data_generator as dg

#sequences_list = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
sequences_list = dg.get_data("samples.txt")

def overlay(sequence_1, sequence_2): #calcula a quantidade de caracteres que podem ser sobrepostos, do final da sequencia 1 com o começo da sequência 2
    '''
    exemplo: (aaa, aab) -> aa -> count = 2
    '''
    seq1_len = len(sequence_1) - 1
    if len(sequence_2) >= len(sequence_1):
        seq2_len = len(sequence_1) - 1 #se a seq2 for maior, igualamos o comprimento; se for igual, tanto faz qual comprimento usar
    elif len(sequence_2) < len(sequence_1):
        seq2_len = len(sequence_2) - 1 #se a seq2 for menor, utilizamos o próprio comprimento de seq2

    count = 0
    while count == 0 and seq2_len > -1:
        aux = seq1_len #para não perder o comprimento da seq1 e evitar o calculo de len()

        for i in range(seq2_len, -1, -1):
            if sequence_1[aux] == sequence_2[i]: #char igual, incrementa o contador de sobreposição e decrementa o contador de char de seq1
                count += 1
                aux -= 1
            else: #a sobreposição não funcionou, contador é zerado para a próxima iteração
                count = 0
                break
        
        seq2_len -= 1
        
    return count

def common_supersequence(sequence_1, sequence_2): #calcula a supersequência comum a duas sequências
    '''
    exemplo: (aaa, aab) -> overlay_count = 2 -> aaa + aab[2:3] -> aaab
    '''
    overlay_count = overlay(sequence_1, sequence_2) #calculamos a quantidade de sobreposição possível na sequência
    supersequence = sequence_1 + sequence_2[overlay_count:len(sequence_2)] #retornamos a string que concatena as sequências, desconsiderando os char iniciais da seq2, envolvidos na sobreposição
    return supersequence

def common_supersequence_list(order): #calcula a supersequência comum para sequências em uma lista ordenada
    '''
    exemplo: (aaa, aab, abb) -> (aaab, abb) -> aaabb
    '''
    overlay_seq = sequences_list[order[0]]
    for j in range(1, len(order)):
        overlay_seq = common_supersequence(overlay_seq, sequences_list[order[j]])
    return overlay_seq

def greedy_algorithm(): #encontra solução escolhendo as primeiras sequências com maior sobreposição
    heuristic_set_index = list(range(0, len(sequences_list)))

    while len(heuristic_set_index) > 1:
        max_overlay = -1
        max_overlay_set = []
        heuristic_set_value = []

        for i in heuristic_set_index: #verificamos a lista de índices de seq; ao final, teremos uma lista com as sequências e não seus indíces
            if(isinstance(i, list)): #se o índice for uma lista de índices de seq
                heuristic_set_value.append(common_supersequence_list(i))
            else:
                heuristic_set_value.append(sequences_list[i])

        for i in range(0, len(heuristic_set_value)): #buscamos as sequências com maior sobreposição
            for j in range(0, len(heuristic_set_value)):
                if(i == j):
                    continue

                overlay_count = overlay(heuristic_set_value[i], heuristic_set_value[j])

                if(max_overlay < overlay_count):
                    max_overlay = overlay_count
                    max_overlay_set = [[i, j]]

        superseq = []
        toremove = []
        for i in max_overlay_set[0]:
            aux = heuristic_set_index[i]
            if isinstance(aux, int):
                superseq += [aux]
            else:
                superseq += aux
            toremove.append(aux)
        for i in toremove:
            heuristic_set_index.remove(i)
            
        heuristic_set_index.append(superseq)

    overlay_seq = common_supersequence_list(heuristic_set_index[0])

    return overlay_seq, heuristic_set_index[0]

def random_heuristic():
    order = []
    
    while(len(order) < len(sequences_list)):
        new_seq = random.randint(0, len(sequences_list) - 1)
        if new_seq not in order:
            order.append(new_seq)
    
    return common_supersequence_list(order), order

def find_random_neighboor_sequence(sequence_order):
    rand_sequence = random.randint(0, len(sequence_order) - 2) #vizinho será obtido alterando a posição de uma sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    new_order = [] + sequence_order
    new_order[rand_sequence] = sequence_order[rand_sequence + 1]
    new_order[rand_sequence + 1] = sequence_order[rand_sequence]

    return common_supersequence_list(new_order), new_order

def simulated_annealing(t_min, t_max):
    t = t_max
    #best_sequence, best_order = greedy_algorithm(sequences_list)
    best_sequence, best_order = random_heuristic()
    #print("greedy_length: ", len(best_sequence))
    #print(best_sequence)
    
    better_length = len(best_sequence)
    better_sequence = best_sequence
    better_order = best_order
    count_equal = 0

    while(t > t_min):
        neighboor_sequence, neighboor_order = find_random_neighboor_sequence(best_order)
        fitness = len(neighboor_sequence) - len(best_sequence)
        probability_coeficient = random.uniform(0.0, 1.0)
        decision_coeficient = math.exp(-fitness/t)
        count_equal += 1

        if fitness <= 0 or (fitness > 0 and probability_coeficient <= decision_coeficient):
            best_sequence, best_order = neighboor_sequence, neighboor_order
            if(better_length > len(best_sequence)):
                #print(count_equal)
                count_equal = 0
                better_length = len(best_sequence)
                better_sequence = best_sequence
                better_order = best_order

        t = t * 0.99
        #t = t * random.uniform(0.8, 0.99)
        #t = t * (math.exp((random.uniform(0.1, 0.9) * -t)/sigma)) 
    #print("better_length: ", better)
    return better_sequence, better_order

def find_grasp_neighboor_sequence(sequence_order):
    #rand_sequence = random.randint(0, len(sequence_order) - 2) #vizinho será obtido alterando a posição de uma sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    order_1 = [] + sequence_order
    cur_length = common_supersequence_list(order_1)
    for i in range(0, len(sequence_order) - 1):
        order_2 = [] + order_1
        order_2[i] = order_1[i + 1]
        order_2[i + 1] = order_1[i]

        new_length = common_supersequence_list(order_2)

        if new_length < cur_length:
            order_1 = order_2
            cur_length = new_length

    return common_supersequence_list(order_1), order_1

def grasp_construction():
    grasp_sequences = [] + sequences_list
    max_overlay = -1
    constructed_solution = []

    for i in range(0, len(grasp_sequences)): #buscamos as sequências com maior sobreposição
        for j in range(0, len(grasp_sequences)):
            if(i == j):
                continue

            overlay_count = overlay(grasp_sequences[i], grasp_sequences[j])

            if(max_overlay < overlay_count):
                max_overlay = overlay_count
                max_overlay_seq = [[i, j]]
            elif(max_overlay == overlay_count):
                max_overlay_seq.append([i, j])

    choosed = random.randint(0, len(max_overlay_seq) - 1)
    cur_seq, next_seq = max_overlay_seq[choosed]
    constructed_solution.append(cur_seq)
    constructed_solution.append(next_seq)
    
    while(len(constructed_solution) < len(sequences_list)):
        max_overlay = -1

        for j in range(0, len(grasp_sequences)): #buscamos as sequências com maior sobreposição
            if next_seq == j or j in constructed_solution:
                continue

            overlay_count = overlay(sequences_list[next_seq], grasp_sequences[j])
            #print(overlay_count)

            if(max_overlay < overlay_count):
                max_overlay = overlay_count
                max_overlay_seq = [[j]]
            elif(max_overlay == overlay_count):
                max_overlay_seq.append([j])

        choosed = random.randint(0, len(max_overlay_seq) - 1)
        next_seq = max_overlay_seq[choosed][0]
        constructed_solution.append(next_seq)
        #print(constructed_solution)
        
    return common_supersequence_list(constructed_solution), constructed_solution

def grasp_localsearch(grasp_initial, grasp_initial_order):
    #grasp_initial, grasp_initial_order = grasp_construction(sequences_list)
    best_solution = len(grasp_initial)
    best_sequence = grasp_initial
    best_order = grasp_initial_order
    best_neighboor_solution = best_solution

    #print("grasp_local: ", best_solution, best_sequence, best_order)

    while(best_solution < best_neighboor_solution):
        best_neighboor_sequence, best_neighboor_order = find_grasp_neighboor_sequence(grasp_initial_order)
        best_neighboor_solution = len(best_neighboor_sequence)

        if best_solution > best_neighboor_solution:
            best_solution = best_neighboor_solution
            best_sequence = best_neighboor_sequence
            best_order = best_neighboor_order

    #print("grasp_local: ", best_solution, best_sequence, best_order)
    return best_sequence, best_order

def grasp(max_iter):
    #print(best_order)
    grasp_initial, grasp_initial_order = grasp_construction()
    #print("grasp_iter: ", grasp_initial, grasp_initial_order)
    best_sequence, best_order = grasp_localsearch(grasp_initial, grasp_initial_order)
    best_length = len(best_sequence)

    for i in range(0, max_iter):
        #print("i: ", i)
        #a = input()
        grasp_initial, grasp_initial_order = grasp_construction()
        #print("grasp_iter: ", grasp_initial, grasp_initial_order)
        new_sequence, new_order = grasp_localsearch(grasp_initial, grasp_initial_order)
        new_length = len(new_sequence)
        
        if(best_length > new_length):
            best_length = new_length
            best_sequence = new_sequence
            best_order = new_order
    #print("grasp_local: ", best_length, best_sequence, best_order)
    return best_sequence, best_order

if __name__ == "__main__":
    '''
    sigma = 0.09
    t_max = 100
    t_min = 0.0005
    '''
    t_min = 0.1
    t_max = 1000000000
    max_iter = 500

    #print(grasp_construction(sequences_list))
    solution1, order1 = greedy_algorithm()
    solution2, order2 = simulated_annealing(t_min, t_max)
    solution3, order3 = grasp(max_iter)

    print("greedy: ", len(solution1))
    print(solution1)

    print("sa: ", len(solution2))
    print(solution2)

    print("grasp: ", len(solution3))
    print(solution3)