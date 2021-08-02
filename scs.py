#import sys
import random
import math

def get_data(data_file):
    data_file = open(data_file, "r")
    sequences_set = data_file.readlines()
    length_count = 0
    for i in range(0, len(sequences_set)):
        sequences_set[i] = sequences_set[i].replace("\n", "")
        length_count += len(sequences_set[i])
    #print("total_length:", length_count)
    data_file.close()
    return sequences_set

def common_supersequence(sequence_1, sequence_2):
    overlay_count = overlay(sequence_1, sequence_2) #calculamos a quantidade de sobreposição possível na sequência
    return sequence_1 + sequence_2[overlay_count:len(sequence_2)] #retornamos a string que concatena as sequências, desconsiderando os char iniciais da seq2, envolvidos na sobreposição

def common_supersequence_list(sequences_set, order):
    overlay_seq = sequences_set[order[0]]
    for j in range(1, len(order)):
        overlay_seq = common_supersequence(overlay_seq, sequences_set[order[j]]) #calculamos a superseq das seqs
    return overlay_seq

def overlay(sequence_1, sequence_2):
    last_char_1 = len(sequence_1) - 1
    if len(sequence_2) >= len(sequence_1):
        last_char_2 = len(sequence_1) - 1 #se a seq2 for maior, "cortamos" os caracteres excedentes; se igual, tanto faz qual comprimento usar
    elif len(sequence_2) < len(sequence_1):
        last_char_2 = len(sequence_2) - 1 #se a seq2 for menor, utilizamos o próprio comprimento

    count = 0
    while count == 0 and last_char_2 > -1:
        aux1 = last_char_1 #para não perder o comprimento da seq1 e evitar o calculo de len()

        for i in range(last_char_2, -1, -1):
            if sequence_1[aux1] == sequence_2[i]: #char igual, incrementa o contador de sobreposição e decrementa o contador de char de seq1
                count += 1
                aux1 -= 1
            else: #a sobreposição não funcionou, contador é zerado para a próxima iteração
                count = 0
                break
        
        last_char_2 -= 1
        
    return count

def overlay_first_heuristic(sequences_set):
    heuristic_set_index = list(range(0, len(sequences_set)))

    while len(heuristic_set_index) > 1:
        max_overlay = -1
        max_overlay_set = []
        heuristic_set_value = []

        for i in heuristic_set_index: #verificamos a lista de índices de seq; ao final, teremos uma lista com as sequências e não seus indíces
            if(isinstance(i, list)): #se o índice for uma lista de índices de seq
                heuristic_set_value.append(common_supersequence_list(sequences_set, i))
            else:
                heuristic_set_value.append(sequences_set[i])

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

    overlay_seq = common_supersequence_list(sequences_set, heuristic_set_index[0])

    return overlay_seq, heuristic_set_index[0]

def random_heuristic(sequences_set):
    order = []
    
    while(len(order) < len(sequences_set)):
        new_seq = random.randint(0, len(sequences_set) - 1)
        if new_seq not in order:
            order.append(new_seq)
    
    return common_supersequence_list(sequences_set, order), order

def grasp_construction(sequences_set):
    grasp_sequences = [] + sequences_set
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
    
    while(len(constructed_solution) < len(sequences_set)):
        max_overlay = -1

        for j in range(0, len(grasp_sequences)): #buscamos as sequências com maior sobreposição
            if next_seq == j or j in constructed_solution:
                continue

            overlay_count = overlay(sequences_set[next_seq], grasp_sequences[j])

            if(max_overlay < overlay_count):
                max_overlay = overlay_count
                max_overlay_seq = [[j]]
            elif(max_overlay == overlay_count):
                max_overlay_seq.append([j])

        choosed = random.randint(0, len(max_overlay_seq) - 1)
        next_seq = max_overlay_seq[choosed][0]
        constructed_solution.append(next_seq)
        
    return common_supersequence_list(sequences_set, constructed_solution), constructed_solution


#def grasp_localsearch()

def find_random_neighboor_sequence(sequences_set, sequence_order):
    rand_sequence = random.randint(0, len(sequence_order) - 2) #vizinho será obtido alterando a posição de uma sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    new_order = [] + sequence_order
    new_order[rand_sequence] = sequence_order[rand_sequence + 1]
    new_order[rand_sequence + 1] = sequence_order[rand_sequence]

    return common_supersequence_list(sequences_set, new_order), new_order

def simulated_annealing(sequences_set, t_min, t_max):
    t = t_max
    #best_sequence, best_order = overlay_first_heuristic(sequences_set)
    best_sequence, best_order = random_heuristic(sequences_set)
    print("greedy_length: ", len(best_sequence))
    print(best_sequence)
    
    better = 1200
    count_equal = 0
    while(t > t_min):
        neighboor_sequence, neighboor_order = find_random_neighboor_sequence(sequences_set, best_order)
        fitness = len(neighboor_sequence) - len(best_sequence)
        probability_coeficient = random.uniform(0.0, 1.0)
        decision_coeficient = math.exp(-fitness/t)
        count_equal += 1

        if fitness <= 0 or (fitness > 0 and probability_coeficient <= decision_coeficient):
            best_sequence, best_order = neighboor_sequence, neighboor_order
            if(better > len(best_sequence)):
                print(count_equal)
                count_equal = 0
                better = len(best_sequence)

        t = t * 0.99
        #t = t * random.uniform(0.8, 0.99)
        #t = t * (math.exp((random.uniform(0.1, 0.9) * -t)/sigma)) 
    print("better_length: ", better)
    return best_sequence, best_order

if __name__ == "__main__":
    '''
    sigma = 0.09
    t_max = 100
    t_min = 0.0005
    '''
    t_min = 0.1
    t_max = 100000000000000000

    #sequences_set = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
    sequences_set = get_data("scs_problem_samples.txt")
    print(grasp_construction(sequences_set))
    msc, order = simulated_annealing(sequences_set, t_min, t_max)
    print("sa_length: ", len(msc))
    print(msc)